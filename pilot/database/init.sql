-- Adminer 4.8.1 PostgreSQL 16.2 dump

\connect "aeroflot";

DROP TABLE IF EXISTS "Inventory";
DROP SEQUENCE IF EXISTS "Inventory_id_seq";
CREATE SEQUENCE "Inventory_id_seq" INCREMENT  MINVALUE  MAXVALUE  CACHE ;

CREATE TABLE "public"."Inventory" (
    "id" integer DEFAULT nextval('"Inventory_id_seq"') NOT NULL,
    "time" timestamptz NOT NULL,
    "flight" character varying(256) NOT NULL,
    "departure" timestamptz NOT NULL,
    "flight booking class" text NOT NULL,
    "idle seats count" integer NOT NULL,
    CONSTRAINT "Inventory_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


-- 2024-05-09 11:11:50.033333+00