CREATE TABLE families (
    id INTEGER PRIMARY KEY AUTO_INCREMENT NOT NULL, 
    name VARCHAR(20) NOT NULL
);

CREATE TABLE users(
    id INTEGER PRIMARY KEY 
    AUTO_INCREMENT NOT NULL, 
    username VARCHAR(20) NOT NULL, 
    password varchar(120) NOT NULL, 
    family_id INTEGER, 
    
    FOREIGN KEY (family_id) REFERENCES families(id)
);


