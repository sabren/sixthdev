/*/
 * MySQL code for Rantelope tables.
 * @TODO: generate this from schema.py
 * 
 * $Id$
/*/

CREATE TABLE rnt_author (
    ID integer not null auto_increment primary key,
    username varchar(32),
    cryptpwd varchar(32),
    fname varchar(32),
    lname varchar(32),
    email varchar(32),
    homepage varchar(64)
);

/* initial admin/admin user */
INSERT INTO rnt_author (fname, lname, username, cryptpwd)
    VALUES ('admin', 'user', 'admin', 'xxiz1FI3TBLPs');


CREATE TABLE rnt_story (
    ID integer not null auto_increment primary key,
    authorID integer not null,
    channelID integer not null,
    categoryID integer,
    title varchar(255),
    url varchar(255),
    description text
);

CREATE TABLE rnt_channel (
    ID integer not null auto_increment primary key,
    title varchar(255),
    url varchar(255),
    rssfile varchar(32),
    htmlfile varchar(32),
    description text,
    template text,
    path varchar(255)
);

CREATE TABLE rnt_category (
    ID integer not null auto_increment primary key,
    channelID integer not null,
    name varchar(50)
);

CREATE TABLE rnt_comment (
    ID integer not null auto_increment primary key,
    storyID integer not null,
    name varchar(50),
    mail varchar(50),
    url varchar(255),
    note text
);

CREATE TABLE web_sess (
    name varchar(32) not null,
    sid varchar(64) not null,
    sess blob,
    tsUpdate timestamp,
    primary key (name, sid)
);

/**
 *  This table was for testing purposes only. You
 *  can use it if you want to play around with the
 *  code in Node.py
**/
-- CREATE TABLE rnt_node (
--     ID integer not null auto_increment primary key,
--     parentID integer not null,
--     name varchar(64),
--     note varchar(255),
-- );
