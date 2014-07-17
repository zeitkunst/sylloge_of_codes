insert into curator (username, password, given_name, surname, created, email) values ("admin", "$2a$12$swo2oGyA1KHSbhrMOlLCyuF.gwigiIsfg/aHyhSJU1mvms3YEl7sS", "Head", "Curator", datetime("now"), "curator@sylloge_of_codes.net");
insert into group_info (group_name, description) values ("admin", "Admin Group");
insert into groups (curator_id, group_info_id) values (1, 1);
