/*/
 * MySQL code for Rantelope tables.
 * 
 * $Id$
/*/

CREATE TABLE rnt_story (
    ID int not null auto_increment primary key,
    channelID int not null,
    title varchar(255),
    link varchar(255),
    description text
);

CREATE TABLE rnt_channel (
    ID int not null auto_increment primary key,
    title varchar(255),
    link varchar(255),
    rssfile varchar(32),
    description text
);
