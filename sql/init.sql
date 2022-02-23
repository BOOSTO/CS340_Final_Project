CREATE DATABASE:
CREATE DATABASE 340_project;

CREATE TABLES:
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
    taskMemberID int ,
    CONSTRAINT taskProjectIDFK
    FOREIGN KEY (taskProjectID) REFERENCES projects(projectID)
    ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT taskTeamIDFK
    FOREIGN KEY (taskTeamID) REFERENCES teams(teamID)
    ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT taskMemberIDFK
    FOREIGN KEY (taskMemberID) REFERENCES members(memberID)
    ON UPDATE CASCADE ON DELETE CASCADE
);


INSERT SAMPLE DATA:
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






















SELECT
-- get all projectID, projectName, and projectDesc to populate Project’s Page --
SELECT * FROM projects;

-- get all memberID, memberFName, memberLName, and memberEmail to populate Member’s page –
SELECT * FROM members;

-- get all teamID, teamName, teamDesc, and projectName to populate team’s page  --
SELECT teams.teamID, teams.teamName, teams.teamDesc, projects.projectName
FROM teams
INNER JOIN projects ON teams.teamID=projects.projectID;

--  get all projectName to populate team’s column “Project” dropdown with all project names where teamProjectID=projectID –
SELECT projectName FROM projects;

-- get all mapID, memberID, teamID to populate membersteam’s page  --
SELECT *  from membersteams;
OR
--  get all mapID, memberEmail, teamName to populate membersteam’s page --
SELECT mapID, members.memberEmail, teams.teamName
FROM membersteams
INNER JOIN members ON membersteams.memberID=members.memberID
INNER JOIN teams on membersteams.teamID=teams.teamID;

--  get all taskID, taskName, taskDesc, taskPriority, taskDeadline, taskDifficulty, taskDone, taskProjectID, taskTeamID, taskMemberID to populate task’s page –
SELECT * FROM tasks;
OR
--  get all taskID, taskName, taskDesc, taskPriority, taskDeadline, taskDifficulty, taskDone, projectName, teamName, memberEmail to populate task’s page --
SELECT tasks.taskID, tasks.taskName, tasks.taskDesc, tasks.taskPriority, tasks.taskDeadline, tasks.taskDifficulty, tasks.taskDone, projects.projectName, teams.teamName, members.memberEmail
FROM tasks
INNER JOIN projects ON tasks.taskProjectID=projects.projectID
INNER JOIN teams on tasks.taskTeamID=teams.teamID
INNER JOIN members on tasks.taskMemberID=members.memberID;

-- get single task for the search form –
SELECT * FROM tasks WHERE taskName = {{taskName}};

-- get single project for the search form –
SELECT * FROM projects WHERE projectName = {{projectName}};

-- get single member for the search form –
SELECT * FROM members WHERE memberEmail = {{memberEmail}};


CREATE
-- add new project –
INSERT INTO projects (projectName, projectDesc) VALUES 
({{projectName}}, {{projectDesc}});

-- add new member –
INSERT INTO members (memberFName, memberLName, memberEmail) VALUES 
({{memberFName}}, {{memberLName}}, {{memberEmail}});



-- add new team –
INSERT INTO teams (teamName, teamDesc, teamProjectID)
VALUES 
    ({{teamName}}, {{teamDesc}}, {{teamProjectID}});

-- add new members_teams –
INSERT INTO membersteams (memberID, teamID)
VALUES 
    ({{memberID}}, {{teamID}});

-- add new task –
INSERT INTO tasks (taskName, taskDesc, taskPriority, taskDeadline, taskDifficulty, taskDone, taskProjectID, taskTeamID, taskMemberID)
VALUES 
({{taskName}}, {{taskDesc}}, {{taskPriority}}, {{taskDeadline}}, {{taskDifficulty}}, {{taskDone}}, {{taskProjectID}}, {{taskTeamID}}, {{teaskMemberID}})

UPDATE
-- update project data based on user submission of form --
UPDATE projects SET projectName={{projectName}}, projectDesc={{projectDesc}} WHERE projectID={{projectID}};

-- update member data based on user submission of form -- 
UPDATE members SET memberFName={{memberFName}}, memberLName={{memberLName}}, memberEmail={{memberEmail}} WHERE memberID={{memberID}};

-- update team data based on user submission of form --
UPDATE teams SET teamName={{teamName}}, teamDesc={{teamDesc}}, teamProjectID={{teamProjectID}} WHERE teamID={{teamID}};
- update membersteams based on user submission of form --
UPDATE membersteams SET memberID={{memberID}}, teamID={{teamID}} WHERE mapID={{mapID}};

-- update task based on user submission of form –
UPDATE tasks SET taskName={{taskName}}, taskDesc={{taskDesc}}, taskPriority={{taskPriority}}, taskDeadline={{taskDeadline}}, taskDifficulty={{taskDifficulty}}, taskDone={{taskDone}}, taskProjectID={{taskProjectID}}, taskTeamID={{taskTeamID}}, taskMemberID={{taskMemberID}} WHERE taskID={{taskID}};

DELETE
-- delete project data based on user submission of form –
DELETE FROM projects WHERE projectID={{projectID}};

-- delete member data based on user submission of form –
DELETE FROM members WHERE memberID={{memberID}};

-- delete team data based on user submission of form –
DELETE FROM teams WHERE teamID={{teamID}}

-- delete membersteams data based on user submission of form –
DELETE FROM membersteams WHERE mapID={{mapID}};

-- delete task data based on user submission of form –
DELETE FROM tasks WHERE taskID={{taskID}}