DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Quest;
DROP TABLE IF EXISTS TimeRecord CASCADE;
DROP TABLE IF EXISTS ArmorSet;
DROP TABLE IF EXISTS Skill CASCADE;
DROP TABLE IF EXISTS TimeRecord CASCADE;
-- Table for user
CREATE TABLE Users(
    username varchar(15) not null,
    pass varchar(15) not null,
    userrole varchar(15) not null,
    primary key(username)
);
CREATE TABLE Quest(
    questname varchar(100) not null,
    monster varchar(30) not null,
    questrank int(2) not null,
    primary key(questname)
);

CREATE TABLE ArmorSet(
    id int not null AUTO_INCREMENT,
    weapon varchar(30),
    weaponname varchar(30),
    helm varchar(30),
    chest varchar(30),
    arm varchar(30),
    waist varchar(30),
    leg varchar(30),
    deco varchar(30),  
    primary key(id)
);
CREATE TABLE Skill(
    skillid int AUTO_INCREMENT,
    armorid int not null,
    skillname varchar(30),
    skilllevel int(1),
    primary key(skillid)
);
CREATE TABLE TimeRecord(
    questname varchar(100) not null,
    weapon varchar(20) not null,
    minute int(2) not null,
    seconds int(2) not null,
    uploaddate date not null,
    username varchar(15),
    armorid int not null,
    primary key(questname,weapon,username,armorid)
);
INSERT INTO users VALUES('me','s','a');
INSERT INTO Quest VALUES('プケプケ','asa','1');
INSERT INTO Quest VALUES('プケプ','asa','2');
INSERT INTO ArmorSet VALUES('1','太刀','月刀　夜影','カイザー','ヴァイク','レウス','ジャナフ','ハンター','見切り４スロ３');
INSERT INTO TimeRecord VALUES('プケプケ','太刀','5','20','2020-03-01','me','1');
