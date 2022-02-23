-- SELECT, UPDATE, DELETE Queries. Variables are denoted by {{var}} syntax.

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

--  get all mapID, memberEmail, teamName to populate membersteam’s page --
SELECT mapID, members.memberEmail, teams.teamName
FROM membersteams
INNER JOIN members ON membersteams.memberID=members.memberID
INNER JOIN teams on membersteams.teamID=teams.teamID;

--  get all taskID, taskName, taskDesc, taskPriority, taskDeadline, taskDifficulty, taskDone, taskProjectID, taskTeamID, taskMemberID to populate task’s page –
SELECT * FROM tasks;

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