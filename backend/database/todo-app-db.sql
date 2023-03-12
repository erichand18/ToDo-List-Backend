CREATE DATABASE IF NOT EXISTS todo_app_db;

USE todo_app_db;

CREATE TABLE IF NOT EXISTS user (
  id INT(11) NOT NULL,
  username VARCHAR(255),
  hashed_pw VARCHAR(255),
  first_name VARCHAR(255),
  last_name VARCHAR(255),
  date_created DATETIME,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS task (
  id INT(11) NOT NULL,
  user_id INT(11) NOT NULL,
  task_name VARCHAR(255),
  task_description VARCHAR(4095),
  color VARCHAR(255),
  date_created DATETIME,
  start_date DATETIME,
  end_date DATETIME,
  PRIMARY KEY (id),
  FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS task_share (
  id INT(11) NOT NULL,
  task_id INT(11) NOT NULL,
  sender_user_id INT(11) NOT NULL,
  recipient_user_id INT(11) NOT NULL,
  date_shared DATETIME,
  viewed TINYINT(1),
  PRIMARY KEY (id),
  FOREIGN KEY (task_id) REFERENCES task(id),
  FOREIGN KEY (sender_user_id) REFERENCES user(id),
  FOREIGN KEY (recipient_user_id) REFERENCES user(id)
);