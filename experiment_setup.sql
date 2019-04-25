CREATE EXTENSION IF NOT EXISTS intarray;

drop table if exists as_links cascade;
create unlogged table as_links
(
    as1 int,
    as2 int
);

drop table if exists abgp cascade;
create unlogged table abgp
(
    fid serial primary key,
    prefix varchar,
    aspath int[]
);

drop table if exists bgp cascade;
create unlogged table bgp
(
    prefix varchar,
    ingress int,
    egress int,
    aspath int[],
    cost numeric
);
create index on bgp(prefix);

drop table if exists alligp cascade;
create unlogged table alligp
(
    asnum int,
    ingress int,
    egress int,
    cost numeric
);
create index on alligp(asnum, ingress, egress);

drop table if exists ingress_egress cascade;
create unlogged table ingress_egress
(
    downstreamas int,
    upstreamas int,
    ingress int[],
    egress int[]
);

drop table if exists peering_links cascade;
create unlogged table peering_links
(
    src_as int,
    dst_as int,
    source int,
    target int
);

drop table if exists upstream_costs cascade;
create table upstream_costs 
(
    src int, /* an src from the upstream AS */
    egress int, /* egress from the perspective of the upstream AS */
    next_hop int, /* the peering nodes in the downstream. Traffic leaves the upstream at the egress and enters the dowstream at the next_hop. */
    cost numeric
);
