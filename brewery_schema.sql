CREATE TABLE "brewery" (
    "id" int   NOT NULL,
    "name" sting   NOT NULL,
    "brewer_type" string   NOT NULL,
    "street" string   NOT NULL,
    "address_2" string   NOT NULL,
    "address_3" string   NOT NULL,
    "city" string   NOT NULL,
    "state" string   NOT NULL,
    "county_province" string   NOT NULL,
    "postal_code" int   NOT NULL,
    "country" string   NOT NULL,
    "long" float   NOT NULL,
    "lat" float   NOT NULL,
    "phone_num" int   NOT NULL,
    "website" url   NOT NULL,
    CONSTRAINT "pk_brewery" PRIMARY KEY (
        "id"
     )
);

CREATE TABLE "user" (
    "id" int   NOT NULL,
    "first_name" string   NOT NULL,
    "last_name" string   NOT NULL,
    "username" string   NOT NULL,
    "city" string   NOT NULL,
    "state" string   NOT NULL,
    "favorite_brewery" string   NOT NULL,
    "password" string   NOT NULL,
    CONSTRAINT "pk_user" PRIMARY KEY (
        "id"
     )
);

CREATE TABLE "likes" (
    "user_id" int   NOT NULL,
    "brewery_id" int   NOT NULL,
    "brewery_name" string   NOT NULL
);

ALTER TABLE "likes" ADD CONSTRAINT "fk_likes_user_id" FOREIGN KEY("user_id")
REFERENCES "user" ("id");

ALTER TABLE "likes" ADD CONSTRAINT "fk_likes_brewery_id_brewery_name" FOREIGN KEY("brewery_id", "brewery_name")
REFERENCES "brewery" ("id", "name");

