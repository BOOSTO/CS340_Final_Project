-- Create database -
CREATE DATABASE 340_project;

-- Create tables -
CREATE TABLE Projects (
    projectID INT AUTO_INCREMENT PRIMARY KEY NOT NULL, 
    projectName VARCHAR(255) NOT NULL, 
    projectDesc VARCHAR(255)
);
CREATE TABLE Members (
    memberID INT AUTO_INCREMENT PRIMARY KEY NOT NULL, 
    memberFName VARCHAR(255) NOT NULL, 
    memberLName VARCHAR(255) NOT NULL,
    memberEmail VARCHAR(255) NOT NULL
);
CREATE TABLE Teams (
    teamID int AUTO_INCREMENT PRIMARY KEY NOT NULL,
    teamName VARCHAR(255) NOT NULL,
    teamDesc VARCHAR(255),
    teamProjectID int NOT NULL,
    CONSTRAINT teamProjectIDFK
    FOREIGN KEY (teamProjectID) REFERENCES projects(projectID)
    ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE MembersTeams (
    mapID int AUTO_INCREMENT PRIMARY KEY NOT NULL,
    memberID int NOT NULL,
    teamID int NOT NULL,
    CONSTRAINT memberIDFK
    FOREIGN KEY (memberID) REFERENCES members(memberID)
    ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT teamIDFK
    FOREIGN KEY (teamID) REFERENCES teams(teamID)
    ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE Tasks (
    taskID int AUTO_INCREMENT PRIMARY KEY NOT NULL,
    taskName VARCHAR(255) NOT NULL,
    taskDesc VARCHAR(1024),
    taskPriority int NOT NULL,
    taskDeadline DATETIME,
    taskDifficulty int NOT NULL,
    taskDone BOOLEAN NOT NULL,
    taskProjectID int NOT NULL,
    taskTeamID int,
    taskMemberID int,
    CONSTRAINT taskProjectIDFK
    FOREIGN KEY (taskProjectID) REFERENCES projects(projectID)
    ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT taskTeamIDFK
    FOREIGN KEY (taskTeamID) REFERENCES teams(teamID)
    ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT taskMemberIDFK
    FOREIGN KEY (taskMemberID) REFERENCES members(memberID)
    ON UPDATE CASCADE ON DELETE SET NULL
);

-- Insert values into tables -
INSERT INTO projects (projectName, projectDesc)
VALUES 
    ('Among Us', 'The revolutionary game that brought people together during the pandemic'),
    ('Halo', 'Emotionally stunted green man rescues blue girl.'),
    ('Modern warfare 2', 'Shooty gun gun');

INSERT INTO members (memberFName, memberLName, memberEmail)
VALUES 
    ('Purple', 'Guy', 'PurpleAmongUs@mail.com'),
    ('Cortona', 'AI', 'Cortona@mail.com'),
    ('Morty', 'Smith', 'Mort@mail.com');

INSERT INTO teams (teamName, teamDesc, teamProjectID)
VALUES 
    ('Concept Artist', 'Responsible for all conceptual art and designs.', 1),
    ('Playtesters', 'Evaluate user experience and game reliability.', 2),
    ('Elite gamers', 'Pwn n00bs and drink mtn dew! XD', 2);

INSERT INTO membersteams (memberID, teamID)
VALUES 
    (1, 2),
    (3, 1),
    (2, 3);

INSERT INTO tasks ( taskName, taskDesc, taskPriority, taskDeadline, taskDifficulty, taskDone, taskProjectID, taskTeamID, taskMemberID)
VALUES 
    ('Survive bad guy Among Us', 'Avoid bad guy Among Us at all times or they will get you', 100, '2013-04-02', 2, False, 1, 2, 1),
    ('Save Sgt. Jognson from flood', 'Sgt. Johnson has been ambushed and needs our help', 10, '2022-12-08', 4, False, 2, 3, 2),
    ('Study Chicken', 'Try to understand why chicken crossed the road', 2, '2013-01-08', 4, True, 3, 1, 3);