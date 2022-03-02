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
    FOREIGN KEY (teamProjectID) REFERENCES Projects(projectID)
    ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE MembersTeams (
    mapID int AUTO_INCREMENT PRIMARY KEY NOT NULL,
    memberID int NOT NULL,
    teamID int NOT NULL,
    CONSTRAINT memberIDFK
    FOREIGN KEY (memberID) REFERENCES Members(memberID)
    ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT teamIDFK
    FOREIGN KEY (teamID) REFERENCES Teams(teamID)
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
    FOREIGN KEY (taskProjectID) REFERENCES Projects(projectID)
    ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT taskTeamIDFK
    FOREIGN KEY (taskTeamID) REFERENCES Teams(teamID)
    ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT taskMemberIDFK
    FOREIGN KEY (taskMemberID) REFERENCES Members(memberID)
    ON UPDATE CASCADE ON DELETE SET NULL
);

-- Insert values into tables -
INSERT INTO Projects (projectName, projectDesc)
VALUES 
    ('Among Us', 'The revolutionary game that brought people together during the pandemic'),
    ('Halo', 'Emotionally stunted green man rescues blue girl.'),
    ('Modern warfare 2', 'Shooty gun gun');

INSERT INTO Members (memberFName, memberLName, memberEmail)
VALUES 
    ('Purple', 'Guy', 'PurpleAmongUs@mail.com'),
    ('Cortona', 'AI', 'Cortona@mail.com'),
    ('Morty', 'Smith', 'Mort@mail.com');

INSERT INTO Teams (teamName, teamDesc, teamProjectID)
VALUES 
    ('Concept Artist', 'Responsible for all conceptual art and designs.', 1),
    ('Playtesters', 'Evaluate user experience and game reliability.', 2),
    ('Elite gamers', 'Pwn n00bs and drink mtn dew! XD', 2);

INSERT INTO MembersTeams (memberID, teamID)
VALUES 
    (1, 2),
    (3, 1),
    (2, 3);

INSERT INTO Tasks ( taskName, taskDesc, taskPriority, taskDeadline, taskDifficulty, taskDone, taskProjectID, taskTeamID, taskMemberID)
VALUES 
    ('Survive bad guy Among Us', 'Avoid bad guy Among Us at all times or they will get you', 100, '2013-04-02', 2, False, 1, 2, 1),
    ('Save Sgt. Jognson from flood', 'Sgt. Johnson has been ambushed and needs our help', 10, '2022-12-08', 4, False, 2, 3, 2),
    ('Study Chicken', 'Try to understand why chicken crossed the road', 2, '2013-01-08', 4, True, 3, 1, 3);

-- get all projectID, projectName, and projectDesc to populate Project’s Page --
SELECT * FROM Projects;

-- get all memberID, memberFName, memberLName, and memberEmail to populate Member’s page –
SELECT * FROM Members;

-- get all teamID, teamName, teamDesc, and projectName to populate team’s page  --
SELECT Teams.teamID, Teams.teamName, Teams.teamDesc, Projects.projectName
FROM Teams
INNER JOIN Projects ON Teams.teamID=Projects.projectID;

--  get all projectName to populate team’s column “Project” dropdown with all project names where teamProjectID=projectID –
SELECT projectName FROM Projects;

-- get all mapID, memberID, teamID to populate membersteam’s page  --
SELECT *  from MembersTeams;
OR
--  get all mapID, memberEmail, teamName to populate membersteam’s page --
SELECT mapID, Members.memberEmail, Teams.teamName
FROM MembersTeams
INNER JOIN Members ON MembersTeams.memberID=Members.memberID
INNER JOIN Teams on MembersTeams.teamID=Teams.teamID;

--  get all taskID, taskName, taskDesc, taskPriority, taskDeadline, taskDifficulty, taskDone, taskProjectID, taskTeamID, taskMemberID to populate task’s page –
SELECT * FROM Tasks;
OR
--  get all taskID, taskName, taskDesc, taskPriority, taskDeadline, taskDifficulty, taskDone, projectName, teamName, memberEmail to populate task’s page --
SELECT Tasks.taskID, Tasks.taskName, Tasks.taskDesc, Tasks.taskPriority, Tasks.taskDeadline, Tasks.taskDifficulty, Tasks.taskDone, Projects.projectName, Teams.teamName, Members.memberEmail
FROM Tasks
INNER JOIN Projects ON Tasks.taskProjectID=Projects.projectID
INNER JOIN Teams on Tasks.taskTeamID=Teams.teamID
INNER JOIN Members on Tasks.taskMemberID=Members.memberID;

-- get single task for the search form –
SELECT * FROM Tasks WHERE taskName = {{taskName}};

-- get single project for the search form –
SELECT * FROM Projects WHERE projectName = {{projectName}};

-- get single member for the search form –
SELECT * FROM Members WHERE memberEmail = {{memberEmail}};

-- add new project –
INSERT INTO Projects (projectName, projectDesc) VALUES 
({{projectName}}, {{projectDesc}});

-- add new member –
INSERT INTO Members (memberFName, memberLName, memberEmail) VALUES 
({{memberFName}}, {{memberLName}}, {{memberEmail}});

-- add new team –
INSERT INTO Teams (teamName, teamDesc, teamProjectID)
VALUES 
    ({{teamName}}, {{teamDesc}}, {{teamProjectID}});

-- add new members_teams –
INSERT INTO MembersTeams (memberID, teamID)
VALUES 
    ({{memberID}}, {{teamID}});

-- add new task –
INSERT INTO Tasks (taskName, taskDesc, taskPriority, taskDeadline, taskDifficulty, taskDone, taskProjectID, taskTeamID, taskMemberID)
VALUES 
({{taskName}}, {{taskDesc}}, {{taskPriority}}, {{taskDeadline}}, {{taskDifficulty}}, {{taskDone}}, {{taskProjectID}}, {{taskTeamID}}, {{taskMemberID}})

-- update project data based on user submission of form --
UPDATE Projects SET projectName={{projectName}}, projectDesc={{projectDesc}} WHERE projectID={{projectID}};

-- update member data based on user submission of form -- 
UPDATE Members SET memberFName={{memberFName}}, memberLName={{memberLName}}, memberEmail={{memberEmail}} WHERE memberID={{memberID}};

-- update team data based on user submission of form --
UPDATE Teams SET teamName={{teamName}}, teamDesc={{teamDesc}}, teamProjectID={{teamProjectID}} WHERE teamID={{teamID}};
-- update membersteams based on user submission of form --
UPDATE MembersTeams SET memberID={{memberID}}, teamID={{teamID}} WHERE mapID={{mapID}};

-- update task based on user submission of form –
UPDATE Tasks SET taskName={{taskName}}, taskDesc={{taskDesc}}, taskPriority={{taskPriority}}, taskDeadline={{taskDeadline}}, taskDifficulty={{taskDifficulty}}, taskDone={{taskDone}}, taskProjectID={{taskProjectID}}, taskTeamID={{taskTeamID}}, taskMemberID={{taskMemberID}} WHERE taskID={{taskID}};

-- delete project data based on user submission of form –
DELETE FROM Projects WHERE projectID={{projectID}};

-- delete member data based on user submission of form –
DELETE FROM Members WHERE memberID={{memberID}};

-- delete team data based on user submission of form –
DELETE FROM Teams WHERE teamID={{teamID}}

-- delete membersteams data based on user submission of form –
DELETE FROM MembersTeams WHERE mapID={{mapID}};

-- delete task data based on user submission of form –
DELETE FROM Tasks WHERE taskID={{taskID}}