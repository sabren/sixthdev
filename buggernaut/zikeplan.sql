# MySQL dump 5.10

#
# Table structure for table 'plan_area'
#
CREATE TABLE plan_area (
  ID int(11) DEFAULT '0' NOT NULL auto_increment,
  area varchar(32),
  PRIMARY KEY (ID)
);

#
# Table structure for table 'plan_status'
#
CREATE TABLE plan_status (
  status varchar(50)
);

#
# Table structure for table 'plan_story'
#
CREATE TABLE plan_story (
  ID int(11) DEFAULT '0' NOT NULL auto_increment,
  projectID int(11),
  area varchar(50),
  summary varchar(255),
  detail varchar(255),
  type varchar(50),
  hrsOrig decimal(5,2),
  hrsCurr decimal(5,2),
  hrsElapsed decimal(5,2),
  target varchar(50),
  isComplete tinyint(1) DEFAULT '0',
  status varchar(50),
  PRIMARY KEY (ID)
);

#
# Table structure for table 'plan_target'
#
CREATE TABLE plan_target (
  ID int(11) DEFAULT '0' NOT NULL auto_increment,
  target varchar(50),
  PRIMARY KEY (ID)
);

#
# Table structure for table 'plan_type'
#
CREATE TABLE plan_type (
  ID int(11) DEFAULT '0' NOT NULL auto_increment,
  type varchar(50),
  PRIMARY KEY (ID)
);

