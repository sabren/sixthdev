### test tables for ZDC ###############

#
# Table structure for table 'test_enum'
#

CREATE TABLE test_enum (
  ID int(11) NOT NULL auto_increment,
  bubba enum('red','white','blue'),
  PRIMARY KEY (ID)
);

#
# Table structure for table 'test_fish'
#

CREATE TABLE test_fish (
  ID int(11) NOT NULL auto_increment,
  fish varchar(32),
  PRIMARY KEY (ID)
);

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
