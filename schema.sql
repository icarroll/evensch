pragma foreign_keys = off;

drop table if exists persons;
create table persons (
    id integer primary key,
    legal_name text unique,
    guardian_id integer,
    contact_info text,
    foreign key(guardian_id) references persons(id)
);

drop table if exists badges;
create table badges (
    id integer primary key,
    owner_id integer,
    number integer,
    name text,
    valid_id integer,
    foreign key(owner_id) references persons(id),
    foreign key(valid_id) references validities(id)
);

drop table if exists validities;
create table validities (
    id integer primary key,
    name text unique,
    year text
);

drop table if exists days;
create table days (
    id integer primary key,
    day text unique
);

drop table if exists validities_days;
create table validities_days (
    validity_id integer,
    day text,
    primary key(validity_id, day),
    foreign key(validity_id) references validities(id),
    foreign key(day) references days(day)
);

drop table if exists roles;
create table roles (
    id integer primary key,
    name text,
    description text
);

drop table if exists places;
create table places (
    id integer primary key,
    name text,
    parent_id integer,
    foreign key(parent_id) references places(id)
);

drop table if exists timeslots;
create table timeslots (
    id integer primary key,
    start datetime,
    end datetime
);

drop table if exists events;
create table events (
    id integer primary key,
    name text,
    description text
);

drop table if exists loci;
create table loci (
    event_id integer unique,
    place_id integer,
    timeslot_id integer,
    primary key(event_id, place_id, timeslot_id),
    foreign key(event_id) references events(id),
    foreign key(place_id) references places(id),
    foreign key(timeslot_id) references timeslots(id)
);

drop table if exists persons_roles;
create table persons_roles (
    person_id integer,
    role_id integer,
    event_id integer,
    primary key(person_id, role_id, event_id),
    foreign key(person_id) references persons(id),
    foreign key(role_id) references roles(id)
    foreign key(event_id) references events(id)
);
