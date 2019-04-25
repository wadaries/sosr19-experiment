DROP TABLE IF EXISTS Wiser_BGP CASCADE;
CREATE UNLOGGED TABLE Wiser_BGP
(
    prefix varchar,
    ingress int,
    egress int,
    aspath int[],
    wisercost real,
    PRIMARY KEY(prefix)
);
CREATE INDEX ON Wiser_BGP(prefix, aspath);

/* This function can not handle the case where multiple pairs of (prefix, AS path) are inserted into BGP table in a single statement. */
CREATE OR REPLACE FUNCTION wiser_ins_check() RETURNS
TRIGGER AS
$$
    DECLARE
        candidate Wiser_BGP%ROWTYPE;
        currentCost REAL;
    BEGIN
        WITH BGP_update AS (SELECT prefix, ingress, BGP_announcement.egress, ASpath, (BGP_announcement.cost+upstream_costs.cost) AS wisercost FROM upstream_costs JOIN BGP_announcement ON upstream_costs.next_hop = BGP_announcement.ingress) SELECT * INTO candidate FROM BGP_update WHERE wisercost = (SELECT min(wisercost) FROM BGP_update) LIMIT 1;
        SELECT wisercost INTO currentCost FROM Wiser_BGP WHERE prefix = candidate.prefix;
        IF currentCost IS NULL THEN
            INSERT INTO Wiser_BGP VALUES (candidate.*);
        END IF;
        IF currentCost < candidate.wisercost THEN
            UPDATE Wiser_BGP SET aspath = candidate.aspath, wisercost = candidate.wisercost WHERE prefix = candidate.prefix;
        END IF;
        RETURN NULL;
    END;
$$
LANGUAGE PLPGSQL;

/* This function can not handle the case where multiple pairs of (prefix, AS path) are deleted from BGP table in a single statement. */
CREATE OR REPLACE FUNCTION wiser_del_check() RETURNS
TRIGGER AS
$$
    DECLARE
        candidate Wiser_BGP%ROWTYPE;
        currentPath INT[];
        currentCost REAL;
    BEGIN
        SELECT * INTO candidate FROM Wiser_BGP WHERE (prefix, aspath) IN (SELECT DISTINCT prefix, aspath FROM BGP_withdrawal); 
        IF candidate IS NOT NULL THEN
            DELETE FROM Wiser_BGP WHERE prefix = candidate.prefix;
            WITH involved_BGP AS (SELECT * FROM BGP WHERE prefix = candidate.prefix), BGP_update AS (SELECT prefix, ingress, involved_BGP.egress, ASpath, (involved_BGP.cost+upstream_costs.cost) AS wisercost FROM upstream_costs JOIN involved_BGP ON upstream_costs.next_hop = involved_BGP.ingress) SELECT * INTO candidate FROM BGP_update WHERE wisercost = (SELECT min(wisercost) FROM BGP_update) LIMIT 1;
            IF candidate IS NOT NULL THEN
                INSERT INTO Wiser_BGP VALUES (candidate.*);
            END IF;
        END IF;
        RETURN NULL;
    END;
$$
LANGUAGE PLPGSQL;

CREATE OR REPLACE FUNCTION load_wiser() RETURNS VOID AS
$$
    TRUNCATE Wiser_BGP;
    DROP TRIGGER IF EXISTS BGP_insert ON BGP;
    CREATE TRIGGER BGP_insert AFTER INSERT
        ON BGP
        REFERENCING NEW TABLE AS BGP_announcement
        FOR EACH STATEMENT
        EXECUTE PROCEDURE wiser_ins_check();

    DROP TRIGGER IF EXISTS BGP_delete ON BGP;
    CREATE TRIGGER BGP_delete AFTER DELETE
        ON BGP
        REFERENCING OLD TABLE AS BGP_withdrawal
        FOR EACH STATEMENT
        EXECUTE PROCEDURE wiser_del_check();
$$
LANGUAGE SQL;

CREATE OR REPLACE FUNCTION unload_wiser() RETURNS VOID AS
$$
    DROP TRIGGER IF EXISTS BGP_insert ON BGP;
    DROP TRIGGER IF EXISTS BGP_delete ON BGP;
$$
LANGUAGE SQL;