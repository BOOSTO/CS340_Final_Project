var taskProjectInput = document.getElementById('taskProjectID');
var taskTeamInput = document.getElementById('taskTeamID');
var taskMemberInput = document.getElementById('taskMemberID');

// update the task's teams list when a new task project is selected
taskProjectInput.addEventListener('change', function (event) {
    taskTeamInput.disabled = false;
    taskMemberInput.disabled = true;

    // remove all children of taskTeamInput
    while(taskTeamInput.childElementCount > 0) {
        taskTeamInput.removeChild(taskTeamInput.lastChild);
    }
    // add the default option again
    const option = document.createElement("option");
    option.value = "";
    option.innerText = "Select Team";
    option.selected = true;
    option.disabled = true;
    taskTeamInput.appendChild(option);

    // populate with result of a new query
    var selectedTaskProject = taskProjectInput.value;
    const req = new XMLHttpRequest();
    req.onload = function() {
        var res = req.response;
        if (req.status == 200) {
            // add each team to list
            teams = JSON.parse(req.responseText)
            teams.forEach(team => {
                const option = document.createElement("option");
                option.value = team.teamID;
                option.innerText = team.teamName;
                taskTeamInput.appendChild(option);
            });
        } else console.log("ERROR: couldn't get teams list");
    };
    req.open("GET", "teams-by-proj?project_id="+selectedTaskProject, true);
    req.send();
});

// update the task's members list when a new task team is selected
taskTeamInput.addEventListener('change', function (event) {
    taskMemberInput.disabled = false;

    // remove all children of taskMemberInput
    while(taskMemberInput.childElementCount > 0) {
        taskMemberInput.removeChild(taskMemberInput.lastChild);
    }
    // add the default option again
    const option = document.createElement("option");
    option.value = "";
    option.innerText = "Select Member";
    option.selected = true;
    option.disabled = true;
    taskMemberInput.appendChild(option);

    // populate with result of a new query
    var selectedTaskTeam = taskTeamInput.value;
    const req = new XMLHttpRequest();
    req.onload = function() {
        var res = req.response;
        if (req.status == 200) {
            // add each team to list
            members = JSON.parse(req.responseText);
            members.forEach(member => {
                const option = document.createElement("option");
                option.value = member.memberID;
                option.innerText = member.fullName;
                taskMemberInput.appendChild(option);
            });
        } else console.log("ERROR: couldn't get members list");
    };
    req.open("GET", "members-by-team?team_id="+selectedTaskTeam, true);
    req.send();
});

// load page data for tasks in table
id_inputs = document.getElementsByClassName("row-task-id");
project_selects = document.getElementsByClassName("select-project");
team_selects = document.getElementsByClassName("select-team");
member_selects = document.getElementsByClassName("select-member");
for (let i = 0; i < id_inputs.length; ++i) {
    // isolate a single row
    const task_id = id_inputs[i].value;
    const project_select = project_selects[i]
    const team_select = team_selects[i]
    const member_select = member_selects[i]

    //populate its teams options
    {
        const req = new XMLHttpRequest();
        req.onload = function() {
            var res = req.response;
            if (req.status == 200) {
                // add each team to list
                first_element = true;
                teams = JSON.parse(req.responseText);
                teams.forEach(team => {
                    const option = document.createElement("option");
                    option.value = team.teamID;
                    option.innerText = team.teamName;
                    team_select.appendChild(option);
                    if (first_element) {
                        team_select.value = option.value;
                        if (option.value == "") {
                            member_select.disabled = true;
                        }
                        first_element = false;
                    }
                });
            } else console.log("ERROR: couldn't get task teams list");
        };
        req.open("GET", "teams-by-task?task_id="+task_id, true);
        req.send();
    }

    //populate its members options
    {
        const req = new XMLHttpRequest();
        req.onload = function() {
            var res = req.response;
            if (req.status == 200) {
                // add each team to list
                first_element = true;
                members = JSON.parse(req.responseText);
                members.forEach(member => {
                    const option = document.createElement("option");
                    option.value = member.memberID;
                    option.innerText = member.fullName;
                    member_select.appendChild(option);
                    if (first_element) {
                        member_select.value = option.value;
                        first_element = false;
                    }
                });
            } else console.log("ERROR: couldn't get task members list");
        };
        req.open("GET", "members-by-task?task_id="+task_id, true);
        req.send();
    }

    // set up event listeners on options
    {
        // update the task's teams list when a new task project is selected
        project_select.addEventListener('change', function (event) {
            team_select.disabled = false;
            member_select.disabled = true;

            // remove all children of taskTeamInput
            while(team_select.childElementCount > 0) {
                team_select.removeChild(team_select.lastChild);
            }
            // add the default option again
            const option = document.createElement("option");
            option.value = "";
            option.innerText = "No Team";
            option.selected = true;
            team_select.appendChild(option);

            {
                 // remove all children of taskMemberInput
                while(member_select.childElementCount > 0) {
                    member_select.removeChild(member_select.lastChild);
                }
                // add the default option again
                const option = document.createElement("option");
                option.value = "";
                option.innerText = "No Assignee";
                option.selected = true;
                member_select.appendChild(option);
            }

            // populate with result of a new query
            var selectedTaskProject = project_select.value;
            const req = new XMLHttpRequest();
            req.onload = function() {
                var res = req.response;
                if (req.status == 200) {
                    // add each team to list
                    teams = JSON.parse(req.responseText)
                    teams.forEach(team => {
                        const option = document.createElement("option");
                        option.value = team.teamID;
                        option.innerText = team.teamName;
                        team_select.appendChild(option);
                    });
                } else console.log("ERROR: couldn't get teams list");
            };
            req.open("GET", "teams-by-proj?project_id="+selectedTaskProject, true);
            req.send();
        });

        // update the task's members list when a new task team is selected
        team_select.addEventListener('change', function (event) {
            member_select.disabled = false;

            // remove all children of taskMemberInput
            while(member_select.childElementCount > 0) {
                member_select.removeChild(member_select.lastChild);
            }
            // add the default option again
            const option = document.createElement("option");
            option.value = "";
            option.innerText = "No Assignee";
            option.selected = true;
            member_select.appendChild(option);

            // populate with result of a new query
            var selectedTaskTeam = team_select.value;
            const req = new XMLHttpRequest();
            req.onload = function() {
                var res = req.response;
                if (req.status == 200) {
                    // add each team to list
                    members = JSON.parse(req.responseText);
                    members.forEach(member => {
                        const option = document.createElement("option");
                        option.value = member.memberID;
                        option.innerText = member.fullName;
                        member_select.appendChild(option);
                    });
                } else console.log("ERROR: couldn't get members list");
            };
            req.open("GET", "members-by-team?team_id="+selectedTaskTeam, true);
            req.send();
        });
    }
}

console.log("up and running!");