# MySQL dump 8.8
#
# Host: localhost    Database: zike_test
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

INSERT INTO base_contact VALUES (1,0,NULL,NULL,'username',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO base_contact VALUES (2,0,NULL,NULL,'michal@sabren.com',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO base_contact VALUES (3,0,NULL,NULL,'fred@tempy.com',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);

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

INSERT INTO base_content VALUES (1,0,'a simple test',NULL,NULL,NULL,NULL);

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
# Dumping data for table 'base_node'
#


#
# Table structure for table 'base_picture'
#

CREATE TABLE base_picture (
  ID int(11) NOT NULL auto_increment,
  siteID int(11),
  picture mediumblob,
  type varchar(32),
  PRIMARY KEY (ID)
);

#
# Dumping data for table 'base_picture'
#


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

#
# Dumping data for table 'base_user'
#

INSERT INTO base_user VALUES (1,'username','username','$1$pw$D/pJQB6/3vtfaOYajbG6l0',1);
INSERT INTO base_user VALUES (2,'michal@sabren.com','michal@sabren.com','$1$pw$WHVw3m116CdEewcolX2jo/',-1);
INSERT INTO base_user VALUES (3,'3312e5d8e392d159b7b00886e23feeb0','fred','ehshf',0);

#
# Table structure for table 'ref_state'
#

CREATE TABLE ref_state (
  CD char(2) DEFAULT '' NOT NULL,
  name varchar(30),
  salestax decimal(5,3),
  PRIMARY KEY (CD)
);

#
# Dumping data for table 'ref_state'
#

INSERT INTO ref_state VALUES ('CA','california',8.250);
INSERT INTO ref_state VALUES ('TX','texas',5.000);

#
# Table structure for table 'shop_card'
#

CREATE TABLE shop_card (
  ID int(11) NOT NULL auto_increment,
  customerID int(11) DEFAULT '0' NOT NULL,
  name varchar(50),
  number varchar(32),
  expMonth tinyint(4),
  expYear mediumint(9),
  PRIMARY KEY (ID)
);

#
# Dumping data for table 'shop_card'
#


#
# Table structure for table 'shop_detail'
#

CREATE TABLE shop_detail (
  ID int(11) NOT NULL auto_increment,
  saleID int(11) DEFAULT '0' NOT NULL,
  productID int(11) DEFAULT '0' NOT NULL,
  quantity int(11) DEFAULT '0' NOT NULL,
  subtotal decimal(8,3),
  PRIMARY KEY (ID),
  KEY saleID (saleID),
  KEY productID (productID)
);

#
# Dumping data for table 'shop_detail'
#

INSERT INTO shop_detail VALUES (1,1,1,1,NULL);
INSERT INTO shop_detail VALUES (2,2,2,0,NULL);

#
# Table structure for table 'shop_product'
#

CREATE TABLE shop_product (
  ID int(11) NOT NULL auto_increment,
  parentID int(11) DEFAULT '0' NOT NULL,
  code varchar(32) DEFAULT '' NOT NULL,
  name varchar(50),
  price decimal(8,2),
  cost decimal(8,2),
  retail decimal(8,2),
  descSize varchar(50),
  descript text,
  isHidden tinyint(1) DEFAULT '0',
  pictureID int(11),
  instock_warn int(11),
  siteID int(11),
  ts timestamp(14),
  weight decimal(5,2),
  inStock int(11) DEFAULT '0',
  onHold int(11) DEFAULT '0',
  class enum('product','style'),
  PRIMARY KEY (ID)
);

#
# Dumping data for table 'shop_product'
#

INSERT INTO shop_product VALUES (1,0,'some01','something',NULL,NULL,NULL,NULL,NULL,0,NULL,NULL,-1,20001123124344,NULL,0,0,NULL);
INSERT INTO shop_product VALUES (2,0,'XXX','X RAY GLASSES',0.00,NULL,0.00,NULL,NULL,NULL,NULL,NULL,NULL,20001123124344,0.00,0,0,'product');

#
# Table structure for table 'shop_product_node'
#

CREATE TABLE shop_product_node (
  ID int(11) NOT NULL auto_increment,
  productID int(11) DEFAULT '0' NOT NULL,
  nodeID int(11) DEFAULT '0' NOT NULL,
  PRIMARY KEY (ID)
);

#
# Dumping data for table 'shop_product_node'
#


#
# Table structure for table 'shop_sale'
#

CREATE TABLE shop_sale (
  ID int(11) NOT NULL auto_increment,
  customerID int(11) DEFAULT '0' NOT NULL,
  ship_addressID int(11) DEFAULT '0' NOT NULL,
  bill_addressID int(11) DEFAULT '0' NOT NULL,
  cardID int(11) DEFAULT '0' NOT NULL,
  subtotal decimal(8,2),
  salestax decimal(8,2),
  shipping decimal(8,2),
  adjustment decimal(8,2),
  total decimal(8,2),
  shiptypeID int(11),
  tsSold datetime,
  status enum('new','complete','cancelled','pending'),
  comments text,
  siteID int(11) DEFAULT '1' NOT NULL,
  PRIMARY KEY (ID)
);

#
# Dumping data for table 'shop_sale'
#

INSERT INTO shop_sale VALUES (1,0,0,0,0,0.00,NULL,NULL,NULL,NULL,0,'2000-11-23 12:43:44','new',NULL,0);
INSERT INTO shop_sale VALUES (2,0,0,0,0,0.00,NULL,NULL,NULL,NULL,0,'2000-11-23 12:43:44','new',NULL,0);

#
# Table structure for table 'shop_state'
#

CREATE TABLE shop_state (
  ID int(11) NOT NULL auto_increment,
  storeID int(11) DEFAULT '0' NOT NULL,
  stateCD char(2),
  rate decimal(8,2),
  PRIMARY KEY (ID)
);

#
# Dumping data for table 'shop_state'
#


#
# Table structure for table 'shop_store'
#

CREATE TABLE shop_store (
  ID int(11) NOT NULL auto_increment,
  siteID int(11) DEFAULT '0' NOT NULL,
  name varchar(50),
  addressID int(11),
  homepage varchar(200),
  PRIMARY KEY (ID)
);

#
# Dumping data for table 'shop_store'
#

INSERT INTO shop_store VALUES (1,1,'test store',1,NULL);

#
# Table structure for table 'test_enum'
#

CREATE TABLE test_enum (
  ID int(11) NOT NULL auto_increment,
  bubba enum('red','white','blue'),
  PRIMARY KEY (ID)
);

#
# Dumping data for table 'test_enum'
#


#
# Table structure for table 'test_fish'
#

CREATE TABLE test_fish (
  ID int(11) NOT NULL auto_increment,
  fish varchar(32),
  PRIMARY KEY (ID)
);

#
# Dumping data for table 'test_fish'
#

INSERT INTO test_fish VALUES (1,'squid');

#
# Table structure for table 'test_types'
#

CREATE TABLE test_types (
  ID int(11) NOT NULL auto_increment,
  f_int int(11),
  f_string varchar(255),
  f_blob blob,
  f_text text,
  sometime datetime,
  PRIMARY KEY (ID)
);

#
# Dumping data for table 'test_types'
#


#
# Table structure for table 'web_sess'
#

CREATE TABLE web_sess (
  ID int(11) NOT NULL auto_increment,
  sid varchar(32) DEFAULT '' NOT NULL,
  name varchar(32) DEFAULT '' NOT NULL,
  sess text,
  tsUpdate datetime,
  PRIMARY KEY (ID),
  KEY name (name)
);

#
# Dumping data for table 'web_sess'
#


#
# Table structure for table 'zike_site'
#

CREATE TABLE zike_site (
  ID int(11) NOT NULL auto_increment,
  site varchar(30),
  PRIMARY KEY (ID)
);

#
# Dumping data for table 'zike_site'
#


#
# Table structure for table 'zike_zuser'
#

CREATE TABLE zike_zuser (
  ID int(11) NOT NULL auto_increment,
  userID int(11) DEFAULT '0' NOT NULL,
  PRIMARY KEY (ID)
);

#
# Dumping data for table 'zike_zuser'
#

INSERT INTO zike_zuser VALUES (1,1);

