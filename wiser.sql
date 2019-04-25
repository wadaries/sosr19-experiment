DROP TABLE IF EXISTS aBGP CASCADE;
CREATE TABLE aBGP
(
    prefix VARCHAR,
    egress VARCHAR,
    AS_path INT []
);

DROP TABLE IF EXISTS IGP CASCADE;
CREATE TABLE IGP
(
    AS_number INT,
    ingress VARCHAR,
    egress VARCHAR,
    cost INT
);

DROP TABLE IF EXISTS normal_factor CASCADE;
CREATE TABLE normal_factor
(
    src_AS INT,
    dst_AS INT,
    n REAL
);

DROP TABLE IF EXISTS adv_cost CASCADE;
CREATE TABLE adv_cost
(
    src_AS INT,
    dst_AS INT,
    prefix VARCHAR,
    Rs VARCHAR,
    Rd VARCHAR,
    cost REAL
);

DROP VIEW IF EXISTS normalized_adv_cost CASCADE;
CREATE VIEW normalized_adv_cost AS SELECT normal_factor.src_AS, normal_factor.dst_AS, prefix, Rs, Rd, n*cost AS cost FROM normal_factor JOIN adv_cost ON normal_factor.src_AS = adv_cost.src_AS AND normal_factor.dst_AS = adv_cost.dst_AS;

CREATE OR REPLACE VIEW Wiser AS SELECT aBGP.AS_number, prefix, aBGP.egress, cost, AS_path FROM aBGP JOIN IGP ON aBGP.AS_number = IGP.AS_number AND aBGP.egress = IGP.egress;

/* Returns AS paths that has minimum Wiser costs. */
CREATE OR REPLACE FUNCTION wiser_policy(target_AS INT) RETURNS TABLE
(
    prefix VARCHAR,
    egress VARCHAR,
    AS_path INT []
) AS
    $$
        WITH Wiser_cost AS (SELECT Wiser.prefix, egress, AS_path, (normalized_adv_cost.cost+Wiser.cost) AS cost FROM normalized_adv_cost JOIN Wiser ON normalized_adv_cost.dst_AS = Wiser.AS_number AND normalized_adv_cost.prefix = Wiser.prefix AND normalized_adv_cost.Rd = Wiser.egress WHERE Wiser.AS_number = target_AS) SELECT prefix, egress, AS_path FROM Wiser_cost wcost WHERE cost = (SELECT MIN(cost) FROM Wiser_cost WHERE prefix = wcost.prefix );
    $$
LANGUAGE SQL;

DROP VIEW IF EXISTS min_AS_len CASCADE;
CREATE VIEW min_AS_len AS SELECT prefix, MIN(array_length(AS_path, 1)) AS AS_len FROM wiser_policy(4) GROUP BY prefix;

CREATE OR REPLACE VIEW shortest_AS_path_route AS SELECT aBGP.prefix, egress, AS_path FROM aBGP JOIN min_AS_len ON aBGP.prefix = min_AS_len.prefix WHERE array_length(AS_path, 1) = AS_len AND AS_number = 4;

CREATE OR REPLACE VIEW all_potato_routes AS SELECT ingress, IGP.egress, cost, prefix, as_path FROM IGP JOIN shortest_AS_path_route ON IGP.egress = shortest_AS_path_route.egress WHERE AS_number = 4;

DROP VIEW IF EXISTS min_cost CASCADE;
CREATE VIEW min_cost AS SELECT prefix, MIN(cost) AS cost FROM all_potato_routes GROUP BY prefix;

DROP VIEW IF EXISTS route;
CREATE VIEW route AS SELECT all_potato_routes.prefix, egress AS next_hop, AS_path FROM all_potato_routes JOIN min_cost ON all_potato_routes.prefix = min_cost.prefix AND all_potato_routes.cost = min_cost.cost;

CREATE OR REPLACE VIEW MIRO AS SELECT prefix, AS_path FROM route;

