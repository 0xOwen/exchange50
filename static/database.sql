CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE trades
(
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
CREATE TABLE ownerships
(
    userid SMALLINT,
    currency_id TINYINT, value int,
    FOREIGN KEY(userid) REFERENCES users(id),
    FOREIGN KEY(currency_id) REFERENCES currencies(id)
);
CREATE TABLE offers
(
    userid SMALLINT,
    currency TINYINT,
    currency_needed TINYINT,
    FOREIGN KEY(userid) REFERENCES users(id),
    FOREIGN KEY(currency) REFERENCES currencies(id),
    FOREIGN KEY(currency_needed) REFERENCES currencies(id)
);
CREATE TABLE users
(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username CHAR(20) NOT NULL,
email VARCHAR(25) NOT NULL,
password INT NOT NULL,
date DATE DEFAULT (DATETIME())
);
CREATE TABLE currencies
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name CHAR(10),
    description CHAR(20) 
);
CREATE TABLE conversions
(
    currency_from_id INT,
    currency_to_id INT,
    trend TEXT,
    FOREIGN KEY(currency_from_id) REFERENCES currencies(id),
    FOREIGN KEY(currency_to_id) REFERENCES currencies(id) 
);
CREATE TABLE monthly_trends
(
    currency_from_id INT,
    currency_to_id INT,
    trend TEXT,
    FOREIGN KEY(currency_from_id) REFERENCES currencies(id),
    FOREIGN KEY(currency_to_id) REFERENCES currencies(id) 
);
CREATE TABLE daily_trends
(
    currency_from_id INT,
    currency_to_id INT,
    trend TEXT,
    FOREIGN KEY(currency_from_id) REFERENCES currencies(id),
    FOREIGN KEY(currency_to_id) REFERENCES currencies(id) 
);
