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

CREATE TABLE bill_types(
    id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(20) NOT NULL
);

INSERT INTO bill_types(name) VALUES('Transferência');
INSERT INTO bill_types(name) VALUES('Boleto');

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

CREATE TABLE tasks(
    id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
    name VARCHAR(80) NOT NULL,
    type INTEGER NOT NULL,
    description VARCHAR(380) NOT NULL,
    created_by INTEGER NOT NULL,
    assigned_to INTEGER DEFAULT NULL,
    date_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
    date_due TIMESTAMP NOT NULL,
    flag_id INTEGER NOT NULL,

    FOREIGN KEY (type) REFERENCES task_types(id),
    FOREIGN KEY (created_by) REFERENCES users(id),
    FOREIGN KEY (assigned_to) REFERENCES users(id),
    FOREIGN KEY (flag_id) REFERENCES flags(id)
);

CREATE TABLE bills(
    id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
    type_id INTEGER NOT NULL,
    task_id INTEGER NOT NULL,
    name VARCHAR(35) NOT NULL,
    value REAL NOT NULL,
    due TIMESTAMP NOT NULL,
    bol_code VARCHAR(58) DEFAULT NULL,
    bank_code VARCHAR(4) DEFAULT NULL,
    bank_agency VARCHAR(8) DEFAULT NULL,
    bank_account VARCHAR(16) DEFAULT NULL,
    bank_cpfcpnj VARCHAR(20) DEFAULT NULL,
    bank_pix VARCHAR(70) DEFAULT NULL,
    

    FOREIGN KEY (type_id) REFERENCES bill_types(id),
    FOREIGN KEY (task_id) REFERENCES tasks(id)
)