DROP TABLE IF EXISTS posts;
CREATE TABLE posts(
  post_id int NOT NULL PRIMARY KEY,
  post_name varchar(50) UNIQUE
);

DROP TABLE IF EXISTS department;
CREATE TABLE department(
  department_id int NOT NULL PRIMARY KEY,
  dept_name VARCHAR(50)
);

DROP TABLE IF EXISTS faculty;
CREATE TABLE faculty(
  faculty_id SERIAL PRIMARY KEY NOT NULL,
  name varchar(50) NOT NULL,
  email varchar(50) NOT NULL UNIQUE,
  department_id int NOT NULL,
  post varchar(50),
  join_date timestamp,
  leave_date timestamp,
  leaves_remaining int,
  leaves_can_be_borrowed int,
  FOREIGN KEY(department_id) REFERENCES department(department_id),
  FOREIGN KEY(post) REFERENCES posts(post_name)
);

DROP TABLE IF EXISTS hod;
CREATE TABLE hod(
  dept_id int NOT NULL PRIMARY KEY,
  faculty_id int NOT NULL,
  FOREIGN KEY(faculty_id) REFERENCES faculty(faculty_id),
  FOREIGN KEY(dept_id) REFERENCES department(department_id)
);

DROP TABLE IF EXISTS application;
CREATE TABLE application(
  application_id SERIAL PRIMARY KEY NOT NULL,
  faculty_id int NOT NULL,
  start_date timestamp,
  end_date timestamp,
  FOREIGN KEY(faculty_id) REFERENCES faculty(faculty_id)
);

DROP TABLE IF EXISTS current_status;
CREATE TABLE current_status(
  status_id int PRIMARY KEY NOT NULL,
  current_holder_post varchar(50),
  current_holder_id int,
  status varchar(50),
  borrowed_leaves int,
  FOREIGN KEY(status_id) REFERENCES application(application_id),
  FOREIGN KEY(current_holder_id) REFERENCES faculty(faculty_id)
);

DROP TABLE IF EXISTS application_log;
CREATE TABLE application_log(
  log_id SERIAL NOT NULL PRIMARY KEY,
  application_id int NOT NULL,
  comment varchar(100),
  post varchar(50),
  date_of_comment timestamp,
  action_taken varchar(50),
  FOREIGN KEY(application_id) REFERENCES application(application_id),
  FOREIGN KEY(post) REFERENCES posts(post_name)
);

DROP TABLE IF EXISTS hod_logs;
CREATE TABLE hod_logs(
  log_id SERIAL NOT NULL PRIMARY KEY,
  faculty_id int NOT NULL,
  dept_id int NOT NULL,
  start_date timestamp,
  end_date timestamp,
  FOREIGN KEY(faculty_id) REFERENCES faculty(faculty_id),
  FOREIGN KEY(dept_id) REFERENCES department(department_id)
);

DROP TABLE IF EXISTS special_logs;
CREATE TABLE special_logs(
  log_id SERIAL NOT NULL PRIMARY KEY,
  faculty_id int NOT NULL,
  start_date timestamp,
  end_time timestamp,
  post varchar(50),
  FOREIGN KEY(faculty_id) REFERENCES faculty(faculty_id),
  FOREIGN KEY(post) REFERENCES posts(post_name)
);

DROP TABLE IF EXISTS special_posts;
CREATE TABLE special_posts(
  faculty_id int NOT NULL,
  post varchar(50) PRIMARY KEY,
  FOREIGN KEY(faculty_id) REFERENCES faculty(faculty_id),
  FOREIGN KEY(post) REFERENCES posts(post_name)
);

DROP TABLE IF EXISTS application_route;
CREATE TABLE application_route(
  sender varchar(50) NOT NULL UNIQUE,
  receiver varchar(50) NOT NULL,
  FOREIGN KEY(sender) REFERENCES posts(post_name),
  FOREIGN KEY(receiver) REFERENCES posts(post_name)
);

INSERT INTO posts(post_id, post_name) VALUES(1,'Faculty');
INSERT INTO posts(post_id, post_name) VALUES(2,'DeanFA');
INSERT INTO posts(post_id, post_name) VALUES(3,'DeanAFA');
INSERT INTO posts(post_id, post_name) VALUES(4,'HOD');
INSERT INTO posts(post_id, post_name) VALUES(5,'Director');

INSERT INTO department(department_id, dept_name) VALUES(1,'CSE');
INSERT INTO department(department_id, dept_name) VALUES(2,'ME');
INSERT INTO department(department_id, dept_name) VALUES(3,'EE');

INSERT INTO application_route(sender, receiver) VALUES('Faculty','HOD');
INSERT INTO application_route(sender, receiver) VALUES('HOD','DeanFA');
INSERT INTO application_route(sender, receiver) VALUES('DeanFA','Director');_
