# MySQL dump 5.10
#
# Host: db6.pair.com    Database: zike_zike
#--------------------------------------------------------
# Server version	3.22.30-log

#
# Table structure for table 'base_content'
#
CREATE TABLE base_content (
  ID int(11) DEFAULT '0' NOT NULL auto_increment,
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
# Table structure for table 'base_node'
#
CREATE TABLE base_node (
  ID int(11) DEFAULT '0' NOT NULL auto_increment,
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
# Table structure for table 'base_picture'
#
CREATE TABLE base_picture (
  ID int(11) DEFAULT '0' NOT NULL auto_increment,
  siteID int(11),
  picture mediumblob,
  type varchar(32),
  PRIMARY KEY (ID)
);

#
# Table structure for table 'base_user'
#
CREATE TABLE base_user (
  ID int(11) DEFAULT '0' NOT NULL auto_increment,
  uid varchar(32) DEFAULT '' NOT NULL,
  email varchar(128) DEFAULT '' NOT NULL,
  username varchar(32) DEFAULT '' NOT NULL,
  cryptedpass varchar(32),
  siteID int(11),
  PRIMARY KEY (ID),
  UNIQUE uid (uid)
);

#
# Table structure for table 'hertel_quick'
#
CREATE TABLE hertel_quick (
  ID int(11) DEFAULT '0' NOT NULL auto_increment,
  name varchar(50),
  email varchar(50),
  phone varchar(20),
  address1 varchar(100),
  address2 varchar(100),
  city varchar(50),
  state char(2),
  postal varchar(10),
  country varchar(50),
  cardnum varchar(20),
  cardexp_month char(2),
  cardexp_year char(2),
  message text,
  time_stamp datetime,
  comments text,
  status varchar(50),
  PRIMARY KEY (ID)
);

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
# Table structure for table 'shop_address'
#
CREATE TABLE shop_address (
  ID int(11) DEFAULT '0' NOT NULL auto_increment,
  customerID int(11) DEFAULT '0' NOT NULL,
  fname varchar(20),
  lname varchar(20),
  address1 varchar(50),
  address2 varchar(50),
  address3 varchar(50),
  city varchar(30),
  stateCD char(2),
  postal varchar(12),
  countryCD char(2),
  phone varchar(15),
  isPrimary tinyint(1) DEFAULT '0' NOT NULL,
  PRIMARY KEY (ID)
);

#
# Table structure for table 'shop_card'
#
CREATE TABLE shop_card (
  ID int(11) DEFAULT '0' NOT NULL auto_increment,
  customerID int(11) DEFAULT '0' NOT NULL,
  name varchar(50),
  number varchar(32),
  expMonth tinyint(4),
  expYear mediumint(9),
  addressID int(11) DEFAULT '0' NOT NULL,
  PRIMARY KEY (ID)
);

#
# Table structure for table 'shop_inventory'
#
CREATE TABLE shop_inventory (
  ID int(11) DEFAULT '0' NOT NULL auto_increment,
  locationID int(11) DEFAULT '0' NOT NULL,
  styleID int(11),
  amount int(11),
  PRIMARY KEY (ID)
);

#
# Table structure for table 'shop_location'
#
CREATE TABLE shop_location (
  ID int(11) DEFAULT '0' NOT NULL auto_increment,
  name varchar(32),
  siteID int(11),
  PRIMARY KEY (ID)
);

#
# Table structure for table 'shop_product'
#
CREATE TABLE shop_product (
  ID int(11) DEFAULT '0' NOT NULL auto_increment,
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
  PRIMARY KEY (ID)
);

#
# Table structure for table 'shop_product_node'
#
CREATE TABLE shop_product_node (
  productID int(11) DEFAULT '0' NOT NULL,
  nodeID int(11) DEFAULT '0' NOT NULL
);

#
# Table structure for table 'shop_sale'
#
CREATE TABLE shop_sale (
  ID int(11) DEFAULT '0' NOT NULL auto_increment,
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
  statusID int(11) DEFAULT '0' NOT NULL,
  comments text,
  siteID int(11) DEFAULT '1' NOT NULL,
  PRIMARY KEY (ID)
);

#
# Table structure for table 'shop_sale_item'
#
CREATE TABLE shop_sale_item (
  ID int(11) DEFAULT '0' NOT NULL auto_increment,
  saleID int(11) DEFAULT '0' NOT NULL,
  styleID int(11) DEFAULT '0' NOT NULL,
  item varchar(75),
  quantity int(11) DEFAULT '0' NOT NULL,
  price decimal(8,2),
  PRIMARY KEY (ID)
);

#
# Table structure for table 'shop_state'
#
CREATE TABLE shop_state (
  ID int(11) DEFAULT '0' NOT NULL auto_increment,
  storeID int(11) DEFAULT '0' NOT NULL,
  stateCD char(2),
  rate decimal(8,2),
  PRIMARY KEY (ID)
);

#
# Table structure for table 'shop_status'
#
CREATE TABLE shop_status (
  ID int(11) DEFAULT '0' NOT NULL auto_increment,
  status varchar(50),
  PRIMARY KEY (ID)
);

#
# Table structure for table 'shop_store'
#
CREATE TABLE shop_store (
  ID int(11) DEFAULT '0' NOT NULL auto_increment,
  siteID int(11) DEFAULT '0' NOT NULL,
  name varchar(50),
  addressID int(11),
  homepage varchar(200),
  PRIMARY KEY (ID)
);

#
# Table structure for table 'shop_style'
#
CREATE TABLE shop_style (
  ID int(11) DEFAULT '0' NOT NULL auto_increment,
  productID int(11) DEFAULT '0' NOT NULL,
  style varchar(50),
  PRIMARY KEY (ID)
);

#
# Table structure for table 'web_sess'
#
CREATE TABLE web_sess (
  ID int(11) DEFAULT '0' NOT NULL auto_increment,
  sid varchar(32) DEFAULT '' NOT NULL,
  name varchar(32) DEFAULT '' NOT NULL,
  sess text,
  tsUpdate datetime,
  PRIMARY KEY (ID),
  KEY name (name)
);

#
# Table structure for table 'zike_site'
#
CREATE TABLE zike_site (
  ID int(11) DEFAULT '0' NOT NULL auto_increment,
  site varchar(30),
  PRIMARY KEY (ID)
);

#
# Table structure for table 'zike_zuser'
#
CREATE TABLE zike_zuser (
  ID int(11) DEFAULT '0' NOT NULL auto_increment,
  userID int(11) DEFAULT '0' NOT NULL,
  PRIMARY KEY (ID)
);

