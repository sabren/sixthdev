# MySQL dump 8.8
#
# Host: localhost    Database: timesheet
#--------------------------------------------------------
# Server version	3.23.23-beta

#
# Table structure for table 'times'
#

CREATE TABLE times (
  ID int(11) NOT NULL auto_increment,
  day date,
  hours decimal(4,2),
  note text,
  user enum('michal','mario'),
  project varchar(30),
  PRIMARY KEY (ID)
);

CREATE TABLE web_sess (
  ID int(11) NOT NULL auto_increment,
  sid varchar(32) NOT NULL default '',
  name varchar(32) NOT NULL default '',
  sess text,
  tsUpdate datetime default NULL,
  PRIMARY KEY  (ID),
  KEY name (name)
);


