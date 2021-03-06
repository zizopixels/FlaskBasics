CREATE DATABASE meetup;
USE meetup;
CREATE TABLE users (
id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
email VARCHAR(100) NOT NULL,
username VARCHAR(30) NOT NULL,
password VARCHAR(100) NOT NULL,
reg_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE rooms (
room_id INT NOT NULL PRIMARY KEY,
author_id INT NOT NULL,
FOREIGN KEY (author_id) REFERENCES users(id),
room_name VARCHAR(50),
text VARCHAR (54),
start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
run_time INT NOT NULL,
public BOOLEAN NOT NULL
);