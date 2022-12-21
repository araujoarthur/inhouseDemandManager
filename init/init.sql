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

