-- MySQL dump 8.8
--
-- Host: localhost    Database: zike_plan
----------------------------------------------------------
-- Server version	3.23.23-beta


create table bug_area (
    ID int not null auto_increment primary key,
    area varchar(32)
);

create table bug_task (
    ID int not null auto_increment primary key,
    goalID int not null,
    task varchar(255),
    reason varchar(255),
    detail text,
    status enum ('urgent','active','open','closed')
);
