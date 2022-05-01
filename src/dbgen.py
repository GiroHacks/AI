#!/usr/bin/python3

import psycopg2
conn = psycopg2.connect("host='192.168.1.69' port='5432' dbname='postgres' user='root' password='root' sslmode='disable' gssencmode='disable'")
cur = conn.cursor()
cur.execute("""
DROP TABLE if exists offers CASCADE;
DROP INDEX if exists offers_pk;

create table offers
(
    id               bigserial
        constraint offers_pk
            primary key,
    site_id          bigint not null,
    publication_date date,
    province         text,
    offer_type       text,
    industry         text,
    job_title        text,
    name             text,
    description      text,
    requirements     text,
    min_salary       decimal,
    max_salary       decimal,
    num_views        decimal,
    num_leads        decimal
);

alter table offers
    owner to root;

create unique index offers_site_id_uindex
    on offers (site_id);



DROP TABLE if exists skills CASCADE;
DROP INDEX if exists skills_nom_uindex;

create table skills
(
    id   bigserial
        constraint skills_pk
            primary key,
    name text not null
);

alter table skills
    owner to root;

create unique index skills_name_uindex
    on skills (name);



DROP TABLE if exists users_skills CASCADE;

CREATE TABLE users_skills
(
    user_id    int REFERENCES users (id),
    skill_id   int REFERENCES skills (id) ON UPDATE CASCADE,
    CONSTRAINT user_skills_pkey PRIMARY KEY (user_id, skill_id)
);



DROP TABLE if exists offers_skills CASCADE;

CREATE TABLE offers_skills
(
    offer_id   int REFERENCES offers (id),
    skill_id   int REFERENCES skills (id) ON UPDATE CASCADE,
    CONSTRAINT offers_skills_pk PRIMARY KEY (offer_id, skill_id)
);
""")
conn.commit()

print("Empalmant clean_ofertes")
with open('skiller/clean_ofertes.csv', 'r') as fin:
    # cur.copy_from(fin, 'offers', sep=';')
    sql = "COPY offers FROM STDIN DELIMITER ';' CSV HEADER"
    cur.copy_expert(sql, fin)

conn.commit()

print("Empalmant clean_skills")
with open('skiller/clean_skills.csv', 'r') as fin:
    # cur.copy_from(fin, 'offers', sep=';')
    sql = "COPY skills FROM STDIN DELIMITER ';' CSV HEADER"
    cur.copy_expert(sql, fin)

conn.commit()


print("Empalmant clean_relation_skills_ofertes")
with open('skiller/clean_relation_skills_ofertes.csv', 'r') as fin:
    # cur.copy_from(fin, 'offers', sep=';')
    sql = "COPY offers_skills FROM STDIN DELIMITER ';' CSV HEADER"
    cur.copy_expert(sql, fin)

conn.commit()

conn.close()
