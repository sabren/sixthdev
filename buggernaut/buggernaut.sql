# MySQL dump 8.8
#
# Host: localhost    Database: zike_plan
#--------------------------------------------------------
# Server version	3.23.23-beta

#
# Table structure for table 'base_contact'
#

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

#
# Dumping data for table 'base_contact'
#

INSERT INTO base_contact VALUES (1,0,'m','m','m@sabren.com','','','','','','',NULL,'m');

#
# Table structure for table 'base_content'
#

CREATE TABLE base_content (
  ID int(11) NOT NULL auto_increment,
  name varchar(50),
  PRIMARY KEY (ID)
);

#
# Dumping data for table 'base_content'
#


#
# Table structure for table 'base_node'
#

CREATE TABLE base_node (
  ID int(11) NOT NULL auto_increment,
  name varchar(50),
  PRIMARY KEY (ID)
);

#
# Dumping data for table 'base_node'
#


#
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

#
# Dumping data for table 'base_user'
#

INSERT INTO base_user VALUES (1,'4b50c5420ba5c16395131077244c38a4','m','$1$pw$XErMV677dMa.o.clwoDfN.');

#
# Table structure for table 'plan_goal'
#

CREATE TABLE plan_goal (
  ID int(11) NOT NULL auto_increment,
  parentID int(11) DEFAULT '0' NOT NULL,
  name varchar(50) DEFAULT '' NOT NULL,
  descript varchar(255),
  path varchar(255) DEFAULT '' NOT NULL,
  PRIMARY KEY (ID),
  KEY parentID (parentID),
  KEY path (path)
);

#
# Dumping data for table 'plan_goal'
#

INSERT INTO plan_goal VALUES (1,0,'first goal','','first goal');

#
# Table structure for table 'plan_goal_task'
#

CREATE TABLE plan_goal_task (
  ID int(11) NOT NULL auto_increment,
  goalID int(11) DEFAULT '0' NOT NULL,
  taskID int(11) DEFAULT '0' NOT NULL,
  PRIMARY KEY (ID)
);

#
# Dumping data for table 'plan_goal_task'
#


#
# Table structure for table 'plan_task'
#

CREATE TABLE plan_task (
  ID int(11) NOT NULL auto_increment,
  author_userID int(11) DEFAULT '0' NOT NULL,
  owner_userID int(11) DEFAULT '0' NOT NULL,
  summary varchar(255),
  detail varchar(255),
  typeID int(11),
  status enum('open','closed','ignore'),
  targetDate datetime,
  createDate datetime,
  risk enum('low','medium','high','unknown'),
  priority enum('low','medium','high','critical'),
  hrsOrig decimal(5,2),
  hrsCurr decimal(5,2),
  hrsElap decimal(5,2),
  owner enum('zach','michal','nobody') DEFAULT 'michal',
  project varchar(50),
  PRIMARY KEY (ID)
);

#
# Dumping data for table 'plan_task'
#

INSERT INTO plan_task VALUES (1,0,0,'grey if status=closed','',0,'closed',NULL,'2001-02-16 23:27:39','low','medium',0.00,0.01,0.01,'michal','buggernaut');
INSERT INTO plan_task VALUES (7,0,0,'color code by priority','just a box on left hand side...',0,'closed',NULL,'2001-02-26 20:18:54','medium','medium',0.25,0.25,0.25,'michal','buggernaut');
INSERT INTO plan_task VALUES (3,0,0,'assign to user','(allow assigning to nobody)',0,'closed',NULL,'2001-02-26 19:44:22','low','critical',0.00,0.50,0.50,'michal','buggernaut');
INSERT INTO plan_task VALUES (4,0,0,'sort list by priority, risk','',0,'closed',NULL,'2001-02-26 19:46:02','low','medium',2.00,0.25,0.25,'michal','buggernaut');
INSERT INTO plan_task VALUES (5,0,0,'priority and risk should be dropdowns','',0,'closed',NULL,'2001-02-26 20:12:31','low','low',0.00,NULL,NULL,'michal','buggernaut');
INSERT INTO plan_task VALUES (6,0,0,'add tasks to goals','',0,'closed',NULL,'2001-02-26 20:14:44','low','high',0.50,0.25,0.25,'michal','buggernaut');
INSERT INTO plan_task VALUES (8,0,0,'opt_XXX for validation / dropdowns','',0,'closed',NULL,'2001-02-26 20:20:16','low','medium',0.50,0.50,0.50,'michal','buggernaut');
INSERT INTO plan_task VALUES (9,0,0,'filter by project','',0,'closed',NULL,'2001-02-26 21:48:33','medium','critical',0.50,0.25,0.25,'michal','buggernaut');

#
# Table structure for table 'plan_task_note'
#

CREATE TABLE plan_task_note (
  ID int(11) NOT NULL auto_increment,
  userID int(11) DEFAULT '0' NOT NULL,
  taskID int(11) DEFAULT '0' NOT NULL,
  content text,
  tsCreate datetime,
  tsUpdate datetime,
  PRIMARY KEY (ID),
  KEY userID (userID)
);

#
# Dumping data for table 'plan_task_note'
#


#
# Table structure for table 'plan_type'
#

CREATE TABLE plan_type (
  ID int(11) NOT NULL auto_increment,
  label varchar(50),
  PRIMARY KEY (ID)
);

#
# Dumping data for table 'plan_type'
#


