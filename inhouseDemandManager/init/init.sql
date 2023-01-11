CREATE TABLE families (
    id INTEGER PRIMARY KEY AUTO_INCREMENT NOT NULL, 
    name VARCHAR(20) NOT NULL,
    secret VARCHAR(50) NOT NULL,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

INSERT INTO families(name, secret) VALUES("unassigned", "PPPPLKJ@@@344(()))(((())<<>>");

CREATE TABLE users(
    id INTEGER PRIMARY KEY AUTO_INCREMENT NOT NULL, 
    username VARCHAR(20) NOT NULL, 
    password varchar(120) NOT NULL, 
    family_id INTEGER DEFAULT 1,

    FOREIGN KEY (family_id) REFERENCES families(id)
);

CREATE TABLE profiles(
    id INTEGER PRIMARY KEY AUTO_INCREMENT NOT NULL,
    user_id INTEGER NOT NULL,
    name VARCHAR(50) NOT NULL DEFAULT '' ,
    email VARCHAR(30) NOT NULL DEFAULT '',
    birthday TIMESTAMP NOT NULL DEFAULT UNIX_TIMESTAMP()
);

CREATE TABLE task_types(
    id INTEGER PRIMARY KEY AUTO_INCREMENT NOT NULL,
    type VARCHAR(20) NOT NULL
);

INSERT INTO task_types(type) VALUES('Bill');
INSERT INTO task_types(type) VALUES('Goods List');
INSERT INTO task_types(type) VALUES('Chores');

CREATE TABLE flags(
    id INTEGER PRIMARY KEY AUTO_INCREMENT NOT NULL,
    name VARCHAR(20) NOT NULL
);

INSERT INTO flags(name) VALUES('Overdue');
INSERT INTO flags(name) VALUES('Urgent');
INSERT INTO flags(name) VALUES('Postponed');
INSERT INTO flags(name) VALUES('Advanced');