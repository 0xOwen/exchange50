CREATE DATABASE db50;
CREATE TABLE users(
    id SMALLINT PRIMARY KEY AUTO_INCREMENT,
    username CHAR(20) NOT NULL UNIQUE, 
    password INT NOT NULL,
    email CHAR(25) NOT NULL,
    date DATE DEFAULT GETDATE()
);
CREATE TABLE currencies(
    id TINYINT PRIMARY KEY AUTO_INCREMENT,
    name CHAR(10),
    description CHAR(30)
);
CREATE TABLE trades(
    user1 SMALLINT,
    currency_user1 TINYINT,
    value_user1 INT,
    user2 SMALLINT,
    value_user2 INT, 
    currency_user2 TINYINT,
    FOREIGN KEY(user1) REFERENCES users(id),
    FOREIGN KEY(user2) REFERENCES users(id),
    FOREIGN KEY(currency_user1) REFERENCES currencies(id),
    FOREIGN KEY(currency_user1) REFERENCES currencies(id)
);
CREATE TABLE ownerships(
    userid SMALLINT,
    currency_id TINYINT,
    FOREIGN KEY(userid) REFERENCES users(id),
    FOREIGN KEY(currency_id) REFERENCES currencies(id)
);
CREATE TABLE offers(
    userid SMALLINT,
    currency TINYINT,
    currency_needed TINYINT,
    FOREIGN KEY(userid) REFERENCES users(id),
    FOREIGN KEY(currency) REFERENCES currencies(id),
    FOREIGN KEY(currency_needed) REFERENCES currencies(id)
)

