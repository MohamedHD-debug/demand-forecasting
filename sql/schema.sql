create table dim_date(
    id serial primary key,
    date_id TEXT UNIQUE NOT NULL,
    la_date date not null,
    jour_de_semaine text not null,
    is_weekend boolean,
    is_holiday boolean
);

create table item (
    id serial primary key,
    item_id TEXT UNIQUE NOT NULL,
    categorie text not null,
    departement text
);

create table store (
    id serial primary key,
    store_id TEXT UNIQUE NOT NULL,
    etat text not null
);

create table price(
    id serial primary key,
    price decimal not null,
    valid_from date not null,
    valid_to date,
    item_id int references item(id),
    store_id int references store(id)
);

create table fact_sales (
    id serial primary key,
    quantite int not null,
    item_id int references item(id),
    store_id int references store(id),
    date_id int references dim_date(id)
);