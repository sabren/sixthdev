# MySQL tables for zikebase users
# $Id$

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
# Table structure for table 'base_content'
#

CREATE TABLE base_content (
  ID int(11) NOT NULL auto_increment,
  userID int(11) DEFAULT '0' NOT NULL,
  title varchar(255),
  keywords varchar(255),
  content text,
  tsCreate datetime,
  tsUpdate datetime,
  PRIMARY KEY (ID),
  KEY userID (userID)
);

#
# Dumping data for table 'base_content'
#


#
# Table structure for table 'base_node'
#

CREATE TABLE base_node (
  ID int(11) NOT NULL auto_increment,
  parentID int(11) DEFAULT '0' NOT NULL,
  name varchar(50) DEFAULT '' NOT NULL,
  descript varchar(255),
  path varchar(255) DEFAULT '' NOT NULL,
  importance int(11) DEFAULT '5',
  siteID int(11),
  PRIMARY KEY (ID),
  KEY parentID (parentID),
  KEY path (path)
);

#
# Table structure for table 'base_user'
#

CREATE TABLE base_user (
  ID int(11) NOT NULL auto_increment,
  uid varchar(32) DEFAULT '' NOT NULL,
  username varchar(32) DEFAULT '' NOT NULL,
  password varchar(32),
  siteID int(11),
  PRIMARY KEY (ID),
  UNIQUE uid (uid)
);
