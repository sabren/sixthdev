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
  PRIMARY KEY (ID)
);

