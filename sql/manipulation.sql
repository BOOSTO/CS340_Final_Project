-- Basic C[RUD]
INSERT INTO Projects (projectName, projectDesc) VALUES (%s,%s);
UPDATE Projects SET projectName=%s, projectDesc =%s WHERE projectID =%s;
DELETE FROM Projects WHERE projectID={projectID};

INSERT INTO Members (memberFName, memberLName, memberEmail) VALUES (%s,%s,%s);
UPDATE Members SET memberFName=%s, memberLName=%s, memberEmail=%s WHERE memberID=%s;
DELETE FROM Members WHERE memberID={memberID};

INSERT INTO Teams (teamName, teamDesc, teamProjectID) VALUES (%s,%s,%s);
UPDATE Teams SET teamName=%s, teamDesc=%s, teamProjectID=%s WHERE teamID=%s;
DELETE FROM Teams WHERE teamID={teamID};

INSERT INTO Tasks ( taskName, taskDesc, taskPriority, taskDeadline, taskDifficulty, taskDone, taskProjectID, taskTeamID, taskMemberID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
UPDATE Tasks SET taskName=%s, taskDesc=%s, taskPriority=%s, taskDeadline=%s, taskDifficulty=%s, taskDone=%s, taskProjectID=%s, taskTeamID=%s, taskMemberID=%s WHERE taskID=%s;
DELETE FROM Tasks WHERE taskID={taskID};

INSERT INTO MembersTeams (memberID, teamID) VALUES (%s, %s)
UPDATE MembersTeams SET memberID=%s, teamID=%s WHERE mapID=%s;
DELETE FROM MembersTeams WHERE mapID={mapID};

SELECT * FROM {table} WHERE {tableID}={inputID};
SELECT teamID, teamProjectID FROM Teams WHERE teamProjectID={compareID};
SELECT memberID, teamID FROM MembersTeams WHERE teamID={compareID};


-- Search Queries

-- Search projects by name or desc
SELECT * FROM Projects WHERE projectName LIKE '%{usr_search}%' UNION 
    SELECT * FROM Projects WHERE projectDesc LIKE '%{usr_search}%';

-- Search teams by name, desc, or associated project name
SELECT Teams.teamID, Teams.teamName, Teams.teamDesc, Projects.projectName, Projects.projectID
    FROM Teams LEFT JOIN Projects ON Teams.teamProjectID=Projects.projectID WHERE teamName LIKE '%{usr_search}%' UNION
    SELECT Teams.teamID, Teams.teamName, Teams.teamDesc, Projects.projectName, Projects.projectID
    FROM Teams LEFT JOIN Projects ON Teams.teamProjectID=Projects.projectID WHERE teamDesc LIKE '%{usr_search}%' UNION
    SELECT Teams.teamID, Teams.teamName, Teams.teamDesc, Projects.projectName, Projects.projectID
    FROM Teams LEFT JOIN Projects ON Teams.teamProjectID=Projects.projectID WHERE projectName LIKE '%{usr_search}%';

--  Search members by name or email
SELECT * FROM Members WHERE memberFName LIKE '%{usr_search}%' UNION
    SELECT * FROM Members WHERE memberLName LIKE '%{usr_search}%' UNION
    SELECT * FROM Members WHERE memberEmail LIKE '%{usr_search}%';

-- Search tasks by name, description, projectName, teamName, or memberName
SELECT Tasks.taskID, Tasks.taskName, Tasks.taskDesc, Tasks.taskPriority, Tasks.taskDeadline, Tasks.taskDifficulty, Tasks.taskDone, Projects.projectName, Projects.projectID, Teams.teamName, Teams.teamID, concat(memberFName, ' ',memberLName) fullName, Members.memberID FROM Tasks
    LEFT JOIN Projects ON Tasks.taskProjectID=Projects.projectID 
    LEFT JOIN Teams on Tasks.taskTeamID=Teams.teamID
    LEFT JOIN Members on Tasks.taskMemberID=Members.memberID
    WHERE taskName LIKE '%{usr_search}%' UNION
    SELECT Tasks.taskID, Tasks.taskName, Tasks.taskDesc, Tasks.taskPriority, Tasks.taskDeadline, Tasks.taskDifficulty, Tasks.taskDone, Projects.projectName, Projects.projectID, Teams.teamName, Teams.teamID, concat(memberFName, ' ',memberLName) fullName, Members.memberID FROM Tasks
    LEFT JOIN Projects ON Tasks.taskProjectID=Projects.projectID
    LEFT JOIN Teams on Tasks.taskTeamID=Teams.teamID
    LEFT JOIN Members on Tasks.taskMemberID=Members.memberID
    WHERE taskDesc LIKE '%{usr_search}%' UNION
    SELECT Tasks.taskID, Tasks.taskName, Tasks.taskDesc, Tasks.taskPriority, Tasks.taskDeadline, Tasks.taskDifficulty, Tasks.taskDone, Projects.projectName, Projects.projectID, Teams.teamName, Teams.teamID, concat(memberFName, ' ',memberLName) fullName, Members.memberID
    FROM Tasks
    LEFT JOIN Projects ON Tasks.taskProjectID=Projects.projectID
    LEFT JOIN Teams on Tasks.taskTeamID=Teams.teamID
    LEFT JOIN Members on Tasks.taskMemberID=Members.memberID
    WHERE projectName LIKE '%{usr_search}%' UNION
    SELECT Tasks.taskID, Tasks.taskName, Tasks.taskDesc, Tasks.taskPriority, Tasks.taskDeadline, Tasks.taskDifficulty, Tasks.taskDone, Projects.projectName, Projects.projectID, Teams.teamName, Teams.teamID, concat(memberFName, ' ',memberLName) fullName, Members.memberID
    FROM Tasks
    LEFT JOIN Projects ON Tasks.taskProjectID=Projects.projectID
    LEFT JOIN Teams on Tasks.taskTeamID=Teams.teamID
    LEFT JOIN Members on Tasks.taskMemberID=Members.memberID
    WHERE teamName LIKE '%{usr_search}%' UNION
    SELECT Tasks.taskID, Tasks.taskName, Tasks.taskDesc, Tasks.taskPriority, Tasks.taskDeadline, Tasks.taskDifficulty, Tasks.taskDone, Projects.projectName, Projects.projectID, Teams.teamName, Teams.teamID, concat(memberFName, ' ',memberLName) fullName, Members.memberID
    FROM Tasks
    LEFT JOIN Projects ON Tasks.taskProjectID=Projects.projectID
    LEFT JOIN Teams on Tasks.taskTeamID=Teams.teamID
    LEFT JOIN Members on Tasks.taskMemberID=Members.memberID
    WHERE memberFName LIKE '%{usr_search}%' UNION
    SELECT Tasks.taskID, Tasks.taskName, Tasks.taskDesc, Tasks.taskPriority, Tasks.taskDeadline, Tasks.taskDifficulty, Tasks.taskDone, Projects.projectName, Projects.projectID, Teams.teamName, Teams.teamID, concat(memberFName, ' ',memberLName) fullName, Members.memberID
    FROM Tasks  
    LEFT JOIN Projects ON Tasks.taskProjectID=Projects.projectID 
    LEFT JOIN Teams on Tasks.taskTeamID=Teams.teamID  
    LEFT JOIN Members on Tasks.taskMemberID=Members.memberID 
    WHERE memberLName LIKE '%{usr_search}%';

-- Select all columns and group by ID
SELECT Tasks.taskID, Tasks.taskName, Tasks.taskDesc, Tasks.taskPriority, Tasks.taskDeadline, Tasks.taskDifficulty, Tasks.taskDone, Projects.projectName, Projects.projectID, Teams.teamName, Teams.teamID, concat(memberFName, ' ',memberLName) fullName, Members.memberID FROM Tasks 
    LEFT JOIN Projects ON Tasks.taskProjectID=Projects.projectID 
    LEFT JOIN Teams on Tasks.taaskTeamID=Teams.teamID 
    LEFT JOIN Members on Tasks.taskMemberID=Members.memberID 
    GROUP BY Tasks.taskID;


-- Select Box Queries

-- get teams associated with a specific project
SELECT teamID, teamName FROM Teams WHERE teamProjectID = '{project_id}'

--  get teams associated with a specific task's project
SELECT teamID, teamName FROM Teams WHERE teamID = (SELECT taskTeamID FROM Tasks WHERE taskID = '{task_id}') UNION 
    SELECT teamID, teamName FROM Teams WHERE teamProjectID = (SELECT taskProjectID FROM Tasks WHERE taskID = '{task_id}';

-- get members associated with a specific task's team
SELECT memberID, concat(memberFName, ' ', memberLName) fullName FROM Members WHERE memberID = (SELECT taskMemberID FROM Tasks WHERE taskID = '{task_id}') UNION
    SELECT Members.memberID, concat(Members.memberFName, ' ', Members.memberLName) fullName FROM MembersTeams LEFT JOIN Members ON MembersTeams.memberID = Members.memberID
    WHERE MembersTeams.teamID = (SELECT taskTeamID FROM Tasks WHERE taskID = '{task_id}');

-- get members associated with a specific team
SELECT Members.memberID, concat(Members.memberFName, ' ', Members.memberLName) fullName FROM MembersTeams LEFT JOIN Members ON MembersTeams.memberID = Members.memberID WHERE teamID = '{team_id}';