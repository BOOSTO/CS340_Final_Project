var taskProjectInput = document.getElementById('taskProjectID');
var taskTeamInput = document.getElementById('taskTeamID');
var taskMemberInput = document.getElementById('taskMemberID');

// update the task's teams list when a new task project is selected
taskProjectInput.addEventListener('change', function (event) {
    taskTeamInput.disabled = false;
    taskMemberInput.disabled = true;

    // remove all children of taskTeamInput
    while(taskTeamInput.childElementCount > 1) {
        taskTeamInput.removeChild(taskTeamInput.lastChild)
    }
    // populate with result of a new query
    var selectedTaskProject = taskProjectInput.value
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
                taskTeamInput.appendChild(option)
            });
        } else console.log("ERROR: couldn't get teams list")
    };
    req.open("GET", "teams-by-proj?project_id="+selectedTaskProject, true);
    req.send();
});

console.log("up and running!");