pragma foreign_keys = on;

begin;
delete from persons;
insert into persons (id, legal_name, contact_info)
    values (1, "Isaac Carroll", "icarroll@pobox.com"),
           (2, "Beverly Block", "beverly.block@comcast.net"),
           (3, "Matt Buckley", "wagoncon@gmail.com");
commit;

begin;
delete from badges;
commit;

begin;
delete from validities;
insert into validities (id, name, year)
    values (1, "GS22 All", "2020"),
           (2, "GS22 Thursday", "2020"),
           (3, "GS22 Friday", "2020"),
           (4, "GS22 Saturday", "2020"),
           (5, "GS22 Sunday", "2020");
commit;

begin;
delete from days;
insert into days (day)
    values ("Thursday"),
           ("Friday"),
           ("Saturday"),
           ("Sunday");
commit;

begin;
delete from validities_days;
insert into validities_days (validity_id, day)
    values (1, "Thursday"),
           (1, "Friday"),
           (1, "Saturday"),
           (1, "Sunday"),
           (2, "Thursday"),
           (3, "Friday"),
           (4, "Saturday"),
           (5, "Sunday");
commit;

begin;
delete from roles;
insert into roles (id, name, description)
    values (1, "staff", "convention staff member"),
           (2, "game master", "runs a game event"),
           (3, "speaker", "speaks alone or on a panel"),
           (4, "player", "plays a game");
commit;

begin;
delete from places;
insert into places (id, name, parent_id)
    values (1, "The Hotel", NULL),
           (2, "Big Room", 1),
           (3, "Small Room", 1),
           (4, "Table 1", 2),
           (5, "Table 2", 2);
commit;

begin;
delete from timeslots;
insert into timeslots (id, start, end)
    values (1, "2020-03-26 12:00:00", "2020-03-29 19:00:00"),
           (2, "2020-03-26 14:00:00", "2020-03-26 18:00:00"),
           (3, "2020-03-26 14:00:00", "2020-03-26 15:30:00");
commit;

begin;
delete from events;
insert into events (id, name, description)
    values (1, "The Convention", "The whole ball of wax"),
           (2, "game", "probably a game of some sort"),
           (3, "blab", "some people yapping I think");
commit;

begin;
delete from loci;
insert into loci (event_id, place_id, timeslot_id)
    values (1, 1, 1),
           (2, 4, 2),
           (3, 3, 3);
commit;

begin;
delete from persons_roles;
insert into persons_roles (person_id, role_id, event_id)
    values (2, 1, 1),
           (3, 2, 2),
           (1, 4, 2);
commit;
