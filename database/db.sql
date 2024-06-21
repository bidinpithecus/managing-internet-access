BEGIN;

CREATE TABLE "admin" (
    "id" INT PRIMARY KEY,
    "user" VARCHAR(255) NOT NULL,
    "password" VARCHAR(255) NOT NULL
);

CREATE TABLE "switch" (
    "id" INT PRIMARY KEY,
    "mac" VARCHAR(255) NOT NULL,
    "ip" VARCHAR(255) NOT NULL,
    "version" INT NOT NULL,
    "size" INT NOT NULL
);

CREATE TABLE "classroom" (
    "id" INT PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "size" INT NOT NULL
);

CREATE TABLE "port_type" (
    "id" INT PRIMARY KEY,
    "description" VARCHAR(255) NOT NULL
);

CREATE TABLE "port" (
    "id" INT PRIMARY KEY,
    "number" INT NOT NULL,
    "switch_id" INT,
    "room_id" INT,
    "type_id" INT,

    FOREIGN KEY ("type_id") REFERENCES "port_type"("id"),
    FOREIGN KEY ("switch_id") REFERENCES "switch"("id"),
    FOREIGN KEY ("room_id") REFERENCES "classroom"("id")
);

CREATE TABLE "scheduling" (
    "id" INT PRIMARY KEY,
    "start_date" DATE NOT NULL,
    "finish_date" DATE NOT NULL,
    "port_id" INT,

    FOREIGN KEY ("port_id") REFERENCES "port"("id")
);

END;