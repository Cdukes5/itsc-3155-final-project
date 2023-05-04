# Add these to the database in order due to constraints!
# After they are in your database don't forget to connect to the database with your mysql password in app.py
# Change password and schema name to your own in app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:PASSWORD@localhost/'SCHEMA NAME'

CREATE TABLE User (
    id INT NOT NULL AUTO_INCREMENT,
    email VARCHAR(120) NOT NULL,
    password VARCHAR(255) NOT NULL,
    username VARCHAR(50) NOT NULL,
    is_active BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (id),
    UNIQUE (email),
    UNIQUE (username)
);

CREATE TABLE `Session` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `session_key` varchar(32) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `session_key` (`session_key`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `Session_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `User` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE forum (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50) NOT NULL
);

INSERT INTO forum (name) VALUES ('General Chat');
INSERT INTO forum (name) VALUES ('Animals and Pets');
INSERT INTO forum (name) VALUES ('Everyday Advice');
INSERT INTO forum (name) VALUES ('Relationships');
INSERT INTO forum (name) VALUES ('Fitness and Health');
INSERT INTO forum (name) VALUES ('Fashion');
INSERT INTO forum (name) VALUES ('Travel');
INSERT INTO forum (name) VALUES ('Study Help');
INSERT INTO forum (name) VALUES ('Job Application Advice');
INSERT INTO forum (name) VALUES ('Armed Forces');
INSERT INTO forum (name) VALUES ('Education Jobs');
INSERT INTO forum (name) VALUES ('Finance Jobs');
INSERT INTO forum (name) VALUES ('Law Career Work');
INSERT INTO forum (name) VALUES ('Science and Tech Jobs');

CREATE TABLE Thread (
  id INT(11) NOT NULL AUTO_INCREMENT,
  title VARCHAR(255) NOT NULL,
  content TEXT NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  forum_id INT(11) NOT NULL,
  username VARCHAR(50) NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (forum_id) REFERENCES Forum (id),
  FOREIGN KEY (username) REFERENCES User (username)
);

CREATE TABLE post (
  id INT AUTO_INCREMENT PRIMARY KEY,
  content VARCHAR(500) NOT NULL,
  date_created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  username VARCHAR(50) NOT NULL,
  thread_id INT NOT NULL,
  FOREIGN KEY (username) REFERENCES user(username),
  FOREIGN KEY (thread_id) REFERENCES thread(id)
);