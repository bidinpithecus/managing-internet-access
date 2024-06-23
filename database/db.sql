BEGIN;

CREATE TABLE "admin" (
    "id" SERIAL PRIMARY KEY,
    "user" VARCHAR(255) UNIQUE NOT NULL,
    "password" VARCHAR(255) NOT NULL
);

CREATE TABLE "switch" (
    "id" SERIAL PRIMARY KEY,
    "mac" VARCHAR(255) UNIQUE NOT NULL,
    "ip" VARCHAR(255) UNIQUE NOT NULL,
    "read_community" VARCHAR(255) NOT NULL,
    "write_community" VARCHAR(255) NOT NULL,
    "snmp_version" INT NOT NULL,
    "num_of_ports" INT NOT NULL
);

CREATE TABLE "classroom" (
    "id" SERIAL PRIMARY KEY,
    "name" VARCHAR(255) UNIQUE NOT NULL,
    "size" INT NOT NULL
);

CREATE TABLE "port_type" (
    "id" SERIAL PRIMARY KEY,
    "description" VARCHAR(255) NOT NULL
);

CREATE TABLE "port" (
    "id" SERIAL PRIMARY KEY,
    "number" INT NOT NULL,
    "switch_id" INT,
    "room_id" INT,
    "type_id" INT,

    FOREIGN KEY ("type_id") REFERENCES "port_type"("id"),
    FOREIGN KEY ("switch_id") REFERENCES "switch"("id"),
    FOREIGN KEY ("room_id") REFERENCES "classroom"("id")
);

CREATE TABLE "scheduling" (
    "id" SERIAL PRIMARY KEY,
    "start_date" DATE NOT NULL,
    "finish_date" DATE NOT NULL,
    "port_id" INT,

    FOREIGN KEY ("port_id") REFERENCES "port"("id")
);

END;