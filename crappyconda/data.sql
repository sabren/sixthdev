-- MySQL dump 8.23
--
-- Host: db.sabren.com    Database: sabren_code
---------------------------------------------------------
-- Server version	3.23.58

--
-- Table structure for table `bug_area`
--

CREATE TABLE bug_area (
  ID int(11) NOT NULL auto_increment,
  area varchar(32) default NULL,
  PRIMARY KEY  (ID)
) TYPE=MyISAM;

--
-- Dumping data for table `bug_area`
--



--
-- Table structure for table `bug_module`
--

CREATE TABLE bug_module (
  ID int(11) NOT NULL auto_increment,
  module varchar(64) default NULL,
  PRIMARY KEY  (ID)
) TYPE=MyISAM;

--
-- Dumping data for table `bug_module`
--


INSERT INTO bug_module VALUES (1,'arlo');
INSERT INTO bug_module VALUES (2,'arlo.CallbackClerk');
INSERT INTO bug_module VALUES (3,'arlo.Clerk');
INSERT INTO bug_module VALUES (4,'arlo.ClerkError');
INSERT INTO bug_module VALUES (5,'arlo.IdxDict');
INSERT INTO bug_module VALUES (6,'arlo.LinkInjector');
INSERT INTO bug_module VALUES (7,'arlo.LinkSetInjector');
INSERT INTO bug_module VALUES (8,'arlo.MockClerk');
INSERT INTO bug_module VALUES (9,'handy');
INSERT INTO bug_module VALUES (10,'pytypes');
INSERT INTO bug_module VALUES (11,'pytypes.Date');
INSERT INTO bug_module VALUES (12,'pytypes.DateTime');
INSERT INTO bug_module VALUES (13,'pytypes.FixedPoint');
INSERT INTO bug_module VALUES (14,'pytypes.IdxDict');
INSERT INTO bug_module VALUES (15,'sixthday');
INSERT INTO bug_module VALUES (16,'sixthday.AdminApp');
INSERT INTO bug_module VALUES (17,'sixthday.App');
INSERT INTO bug_module VALUES (18,'sixthday.Auth');
INSERT INTO bug_module VALUES (19,'sixthday.Form');
INSERT INTO bug_module VALUES (20,'sixthday.Node');
INSERT INTO bug_module VALUES (21,'sixthday.SignupApp');
INSERT INTO bug_module VALUES (22,'sixthday.User');
INSERT INTO bug_module VALUES (23,'storage');
INSERT INTO bug_module VALUES (24,'storage.Date');
INSERT INTO bug_module VALUES (25,'storage.MockStorage');
INSERT INTO bug_module VALUES (26,'storage.MySQLStorage');
INSERT INTO bug_module VALUES (27,'storage.PySQLiteStorage');
INSERT INTO bug_module VALUES (28,'storage.Storage');
INSERT INTO bug_module VALUES (29,'strongbox');
INSERT INTO bug_module VALUES (30,'strongbox.Accessorize');
INSERT INTO bug_module VALUES (31,'strongbox.Attribute');
INSERT INTO bug_module VALUES (32,'strongbox.Attributize');
INSERT INTO bug_module VALUES (33,'strongbox.BoxView');
INSERT INTO bug_module VALUES (34,'strongbox.Link');
INSERT INTO bug_module VALUES (35,'strongbox.LinkSet');
INSERT INTO bug_module VALUES (36,'strongbox.Observable');
INSERT INTO bug_module VALUES (37,'strongbox.PrivateNamespace');
INSERT INTO bug_module VALUES (38,'strongbox.Stealthbox');
INSERT INTO bug_module VALUES (39,'strongbox.StealthboxMetaclass');
INSERT INTO bug_module VALUES (40,'strongbox.Strongbox');
INSERT INTO bug_module VALUES (41,'strongbox.StrongboxError');
INSERT INTO bug_module VALUES (42,'weblib');
INSERT INTO bug_module VALUES (43,'weblib.Engine');
INSERT INTO bug_module VALUES (44,'weblib.Finished');
INSERT INTO bug_module VALUES (45,'weblib.Redirect');
INSERT INTO bug_module VALUES (46,'weblib.Request');
INSERT INTO bug_module VALUES (47,'weblib.RequestBuilder');
INSERT INTO bug_module VALUES (48,'weblib.RequestData');
INSERT INTO bug_module VALUES (49,'weblib.Response');
INSERT INTO bug_module VALUES (50,'weblib.Sess');
INSERT INTO bug_module VALUES (51,'weblib.SessPool');
INSERT INTO bug_module VALUES (52,'zebra');
INSERT INTO bug_module VALUES (53,'zebra.Bootstrap');
INSERT INTO bug_module VALUES (54,'zebra.X2M');
INSERT INTO bug_module VALUES (55,'zebra.Z2X');

--
-- Table structure for table `bug_task`
--

CREATE TABLE bug_task (
  ID int(11) NOT NULL auto_increment,
  goalID int(11) NOT NULL default '0',
  task varchar(255) default NULL,
  reason varchar(255) default NULL,
  detail text,
  status varchar(32) default NULL,
  module varchar(64) default NULL,
  PRIMARY KEY  (ID)
) TYPE=MyISAM;

--
-- Dumping data for table `bug_task`
--


INSERT INTO bug_task VALUES (1,0,'testing',NULL,'test...','open','pytypes');

--
-- Table structure for table `plan_goal`
--

CREATE TABLE plan_goal (
  ID int(11) NOT NULL auto_increment,
  projectID int(11) NOT NULL default '0',
  name varchar(255) default NULL,
  data text,
  seq int(11) NOT NULL default '0',
  PRIMARY KEY  (ID)
) TYPE=MyISAM;

--
-- Dumping data for table `plan_goal`
--


INSERT INTO plan_goal VALUES (1,4,'goal 1','the first goal',0);

--
-- Table structure for table `plan_note`
--

CREATE TABLE plan_note (
  ID int(11) NOT NULL auto_increment,
  userID int(11) NOT NULL default '0',
  name varchar(255) default NULL,
  data text,
  PRIMARY KEY  (ID)
) TYPE=MyISAM;

--
-- Dumping data for table `plan_note`
--



--
-- Table structure for table `plan_project`
--

CREATE TABLE plan_project (
  ID int(11) NOT NULL auto_increment,
  name varchar(255) default NULL,
  data text,
  PRIMARY KEY  (ID)
) TYPE=MyISAM;

--
-- Dumping data for table `plan_project`
--


INSERT INTO plan_project VALUES (4,'take over the world','the same thing we do every weekend');
INSERT INTO plan_project VALUES (5,'aaaa','bbbb');

--
-- Table structure for table `plan_task`
--

CREATE TABLE plan_task (
  ID int(11) NOT NULL auto_increment,
  goalID int(11) NOT NULL default '0',
  name varchar(255) default NULL,
  data text,
  seq int(11) NOT NULL default '0',
  PRIMARY KEY  (ID)
) TYPE=MyISAM;

--
-- Dumping data for table `plan_task`
--


INSERT INTO plan_task VALUES (1,1,'task1','first task',0);

--
-- Table structure for table `plan_user`
--

CREATE TABLE plan_user (
  ID int(11) NOT NULL auto_increment,
  username varchar(32) default NULL,
  password varchar(32) default NULL,
  fname varchar(32) default NULL,
  lname varchar(32) default NULL,
  email varchar(64) default NULL,
  url varchar(64) default NULL,
  PRIMARY KEY  (ID)
) TYPE=MyISAM;

--
-- Dumping data for table `plan_user`
--



--
-- Table structure for table `work_action`
--

CREATE TABLE work_action (
  ID int(11) NOT NULL auto_increment,
  classID int(11) NOT NULL default '0',
  action enum('list','show','edit','delete','save') default NULL,
  view varchar(255) NOT NULL default '',
  next varchar(255) default NULL,
  PRIMARY KEY  (ID)
) TYPE=MyISAM;

--
-- Dumping data for table `work_action`
--


INSERT INTO work_action VALUES (1,1,'list','','');
INSERT INTO work_action VALUES (2,2,'list','','');
INSERT INTO work_action VALUES (3,3,'list','','');
INSERT INTO work_action VALUES (4,4,'list','','');
INSERT INTO work_action VALUES (5,5,'list','','');
INSERT INTO work_action VALUES (6,6,'list','','');
INSERT INTO work_action VALUES (7,7,'list','','');
INSERT INTO work_action VALUES (8,1,'delete','','?action=list&what=project');
INSERT INTO work_action VALUES (10,1,'save','','?action=list&what=project');
INSERT INTO work_action VALUES (9,1,'edit','','');
INSERT INTO work_action VALUES (11,2,'edit','','');
INSERT INTO work_action VALUES (12,2,'save','','?action=list&what=goal');
INSERT INTO work_action VALUES (13,3,'edit','',NULL);
INSERT INTO work_action VALUES (14,3,'save','','?action=list&what=task');

--
-- Table structure for table `work_attr`
--

CREATE TABLE work_attr (
  ID int(11) NOT NULL auto_increment,
  classID int(11) NOT NULL default '0',
  name varchar(32) default NULL,
  type varchar(32) default NULL,
  note text,
  okay varchar(255) default NULL,
  init varchar(255) default NULL,
  size int(11) default NULL,
  PRIMARY KEY  (ID)
) TYPE=MyISAM;

--
-- Dumping data for table `work_attr`
--


INSERT INTO work_attr VALUES (1,1,'name','str',NULL,NULL,NULL,NULL);
INSERT INTO work_attr VALUES (2,1,'data','str',NULL,NULL,NULL,NULL);
INSERT INTO work_attr VALUES (3,2,'name','str',NULL,NULL,NULL,NULL);
INSERT INTO work_attr VALUES (4,2,'data','str',NULL,NULL,NULL,NULL);
INSERT INTO work_attr VALUES (5,3,'name','str',NULL,NULL,NULL,NULL);
INSERT INTO work_attr VALUES (6,3,'data','str',NULL,NULL,NULL,NULL);
INSERT INTO work_attr VALUES (7,4,'name','str',NULL,NULL,NULL,NULL);
INSERT INTO work_attr VALUES (8,4,'note','str',NULL,NULL,NULL,NULL);
INSERT INTO work_attr VALUES (9,5,'name','str',NULL,NULL,NULL,NULL);
INSERT INTO work_attr VALUES (10,5,'note','str',NULL,NULL,NULL,NULL);
INSERT INTO work_attr VALUES (11,5,'type','str',NULL,NULL,NULL,NULL);
INSERT INTO work_attr VALUES (12,5,'okay','str',NULL,NULL,NULL,NULL);
INSERT INTO work_attr VALUES (13,5,'init','str',NULL,NULL,NULL,NULL);
INSERT INTO work_attr VALUES (14,5,'size','int',NULL,NULL,NULL,NULL);
INSERT INTO work_attr VALUES (15,6,'name','str',NULL,NULL,NULL,NULL);
INSERT INTO work_attr VALUES (16,6,'note','str',NULL,NULL,NULL,NULL);
INSERT INTO work_attr VALUES (17,6,'classID','int',NULL,NULL,NULL,NULL);
INSERT INTO work_attr VALUES (18,6,'otherID','long',NULL,NULL,NULL,NULL);
INSERT INTO work_attr VALUES (19,6,'joinID','long',NULL,NULL,NULL,NULL);
INSERT INTO work_attr VALUES (20,6,'field','str',NULL,NULL,NULL,NULL);
INSERT INTO work_attr VALUES (21,7,'name','str',NULL,NULL,NULL,NULL);
INSERT INTO work_attr VALUES (22,7,'note','str',NULL,NULL,NULL,NULL);
INSERT INTO work_attr VALUES (23,7,'classID','long',NULL,NULL,NULL,NULL);
INSERT INTO work_attr VALUES (24,7,'otherID','long',NULL,NULL,NULL,NULL);
INSERT INTO work_attr VALUES (25,7,'field','str',NULL,NULL,NULL,NULL);

--
-- Table structure for table `work_class`
--

CREATE TABLE work_class (
  ID int(11) NOT NULL auto_increment,
  name varchar(32) default NULL,
  note text,
  _table varchar(32) default NULL,
  PRIMARY KEY  (ID)
) TYPE=MyISAM;

--
-- Dumping data for table `work_class`
--


INSERT INTO work_class VALUES (1,'Project',NULL,'plan_project');
INSERT INTO work_class VALUES (2,'Goal',NULL,'plan_goal');
INSERT INTO work_class VALUES (3,'Task',NULL,'plan_task');
INSERT INTO work_class VALUES (4,'Class',NULL,'work_class');
INSERT INTO work_class VALUES (5,'Attr',NULL,'work_attr');
INSERT INTO work_class VALUES (6,'Link',NULL,'work_link');
INSERT INTO work_class VALUES (7,'Join',NULL,'work_join');

--
-- Table structure for table `work_join`
--

CREATE TABLE work_join (
  ID int(11) NOT NULL auto_increment,
  name varchar(32) default NULL,
  note text,
  classID int(11) NOT NULL default '0',
  otherID int(11) default NULL,
  linkID int(11) NOT NULL default '0',
  field varchar(32) default NULL,
  PRIMARY KEY  (ID)
) TYPE=MyISAM;

--
-- Dumping data for table `work_join`
--


INSERT INTO work_join VALUES (1,'goals',NULL,1,2,1,'projectID');
INSERT INTO work_join VALUES (2,'tasks',NULL,2,3,0,'goalID');

--
-- Table structure for table `work_link`
--

CREATE TABLE work_link (
  ID int(11) NOT NULL auto_increment,
  name varchar(32) default NULL,
  note text,
  classID int(11) NOT NULL default '0',
  otherID int(11) default NULL,
  field varchar(32) default NULL,
  PRIMARY KEY  (ID)
) TYPE=MyISAM;

--
-- Dumping data for table `work_link`
--


INSERT INTO work_link VALUES (1,'project',NULL,2,1,'projectID');
INSERT INTO work_link VALUES (2,'goal',NULL,3,2,'goalID');

