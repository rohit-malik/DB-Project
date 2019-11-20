CREATE TABLE Posts(
  post_id int NOT NULL PRIMARY KEY,
  post_name varchar(50) UNIQUE
);

CREATE TABLE Department(
  department_id int NOT NULL PRIMARY KEY,
  dept_name VARCHAR(50)
);


CREATE TABLE Faculty(
  faculty_id int PRIMARY KEY NOT NULL,
  department_id int NOT NULL,
  post varchar(50),
  join_date timestamp,
  leave_date timestamp,
  leaves_remaining int,
  leaves_can_be_borrowed int,
  FOREIGN KEY(department_id) REFERENCES Department(department_id),
  FOREIGN KEY(post) REFERENCES Posts(post_name)
);

CREATE TABLE HOD(
  dept_id int NOT NULL PRIMARY KEY,
  faculty_id int NOT NULL,
  FOREIGN KEY(faculty_id) REFERENCES Faculty(faculty_id),
  FOREIGN KEY(dept_id) REFERENCES Department(department_id)
);


CREATE TABLE Application(
  application_id int PRIMARY KEY NOT NULL,
  faculty_id int NOT NULL,
  start_date timestamp,
  end_date timestamp,
  FOREIGN KEY(faculty_id) REFERENCES Faculty(faculty_id)
);

CREATE TABLE Current_Status(
  status_id int PRIMARY KEY NOT NULL,
  current_holder_post varchar(50),
  current_holder_id int,
  status varchar(50),
  borrowed_leaves int,
  FOREIGN KEY(status_id) REFERENCES Application(application_id),
  FOREIGN KEY(current_holder_id) REFERENCES Faculty(faculty_id)
);

CREATE TABLE Application_log(
  log_id int NOT NULL PRIMARY KEY,
  application_id int NOT NULL,
  comment varchar(100),
  post varchar(50),
  date_of_comment timestamp,
  action_taken varchar(50),
  FOREIGN KEY(application_id) REFERENCES Application(application_id),
  FOREIGN KEY(post) REFERENCES Posts(post_name)
);


CREATE TABLE HOD_logs(
  log_id int NOT NULL PRIMARY KEY,
  faculty_id int NOT NULL,
  dept_id int NOT NULL,
  start_date timestamp,
  end_date timestamp,
  FOREIGN KEY(faculty_id) REFERENCES Faculty(faculty_id),
  FOREIGN KEY(dept_id) REFERENCES Department(department_id)
);


CREATE TABLE Special_logs(
  faculty_id int NOT NULL,
  start_date timestamp,
  end_time timestamp,
  post varchar(50),
  FOREIGN KEY(faculty_id) REFERENCES Faculty(faculty_id),
  FOREIGN KEY(post) REFERENCES Posts(post_name)
);

CREATE TABLE Special_posts(
  faculty_id int NOT NULL,
  post varchar(50) PRIMARY KEY,
  FOREIGN KEY(faculty_id) REFERENCES Faculty(faculty_id),
  FOREIGN KEY(post) REFERENCES Posts(post_name)
);
