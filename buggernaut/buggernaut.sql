# MySQL dump 5.10

# Table structure for table 'base_user'
#

CREATE TABLE base_user (
  ID int(11) NOT NULL auto_increment,
  uid varchar(32) DEFAULT '' NOT NULL,
  username varchar(32) DEFAULT '' NOT NULL,
  password varchar(32),
  PRIMARY KEY (ID),
  UNIQUE uid (uid)
);

CREATE TABLE base_contact (
  ID int(11) NOT NULL auto_increment,
  userID int(11) DEFAULT '0' NOT NULL,
  fname varchar(20),
  lname varchar(20),
  email varchar(50),
  address1 varchar(50),
  address2 varchar(50),
  address3 varchar(50),
  city varchar(30),
  stateCD char(2),
  postal varchar(12),
  countryCD char(2),
  phone varchar(15),
  PRIMARY KEY (ID)
);

CREATE TABLE plan_goal (
  ID int(11) NOT NULL auto_increment,
  parentID int(11) DEFAULT '0' NOT NULL,
  label varchar(50) DEFAULT '' NOT NULL,
  descript varchar(255),
  path varchar(255) DEFAULT '' NOT NULL,
  PRIMARY KEY (ID),
  KEY parentID (parentID),
  KEY path (path)
);


CREATE TABLE plan_status (
  ID int(11) DEFAULT '0' NOT NULL auto_increment,
  label varchar(32),
  PRIMARY KEY (ID)
);


CREATE TABLE plan_type (
  ID int(11) DEFAULT '0' NOT NULL auto_increment,
  label varchar(50),
  PRIMARY KEY (ID)
);


CREATE TABLE plan_task (
  ID int(11) DEFAULT '0' NOT NULL auto_increment,
  author_userID int not null default 0,
  owner_userID int not null default 0,
  summary varchar(255),
  detail varchar(255),
  typeID varchar(50),
  targetDate datetime,
  createDate datetime,
  risk   int not null default 5,
  reward int not null default 5,
  hrsOrig decimal(5,2),
  hrsCurr decimal(5,2),
  hrsElapsed decimal(5,2),
  status varchar(50),
  PRIMARY KEY (ID)
);

CREATE TABLE plan_goal_task (
  ID int(11) DEFAULT '0' NOT NULL auto_increment,
  goalID int not null default 0,
  taskID int not null default 0,
  primary key(ID)
);

CREATE TABLE plan_task_note (
  ID int(11) NOT NULL auto_increment,
  userID int(11) DEFAULT '0' NOT NULL,
  taskID int not null,
  content text,
  tsCreate datetime,
  tsUpdate datetime,
  PRIMARY KEY (ID),
  KEY userID (userID)
);
