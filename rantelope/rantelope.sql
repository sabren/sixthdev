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
    htmlfile varchar(32),
    description text,
    template text,
    path varchar(255)
);

CREATE TABLE rnt_comment (
    ID int not null auto_increment primary key,
    storyID int not null,
    name varchar(50),
    mail varchar(50),
    link varchar(255),
    note text
);

/**
 *  This table was for testing purposes only. You
 *  can use it if you want to play around with the
 *  code in Node.py
**/
-- CREATE TABLE rnt_node (
--     ID int not null auto_increment primary key,
--     parentID int not null,
--     name varchar(64),
--     note varchar(255),
-- );
