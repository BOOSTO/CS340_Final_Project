import sys
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import mysql.connector  # used to connect to MYSQL DB


if len(sys.argv) != 6:
    print("ERROR usage: 'python3 app.py <sv_port> <db_hostname> <db_database_name> <db_username> <db_passwd>'")
    exit()


app = Flask(__name__)
app.config['SECRET_KEY'] = "megasecretkey"


def CRUD_projects(data):
    """Checks user input. If attribute was empty string, set to Null, then send to sql DB"""
    usr_input = {k: None if not v else v for k, v in data.to_dict().items()}
    projectID = usr_input["projectID"]
    projectName = usr_input["projectName"]
    projectDesc = usr_input["projectDesc"]
    if usr_input["action"] == "Create":
        sql = "INSERT INTO Projects (projectName, projectDesc) VALUES (%s,%s)"
        values = (projectName, projectDesc)
        sql_INSERT(sql, values)
    elif usr_input["action"] == "Update":
        sql = "UPDATE Projects " \
              "SET projectName=%s, projectDesc =%s " \
              "WHERE projectID =%s;"
        values = (projectName, projectDesc, projectID)
        sql_UPDATE(sql, values)
    elif usr_input["action"] == "Delete":
        sql = f"DELETE FROM Projects WHERE projectID={projectID};"
        sql_DELETE(sql)
    return


def CRUD_members(data):
    """Checks user input. If attribute was empty string, set to Null, then send to sql DB"""
    usr_input = {k: None if not v else v for k, v in data.to_dict().items()}
    memberID = usr_input["memberID"]
    memberFName = usr_input["memberFName"]
    memberLName = usr_input["memberLName"]
    memberEmail = usr_input["memberEmail"]
    if usr_input["action"] == "Create":
        sql = "INSERT INTO Members (memberFName, memberLName, memberEmail) VALUES (%s,%s,%s)"
        values = (memberFName, memberLName, memberEmail)
        sql_INSERT(sql, values)
    elif usr_input["action"] == "Update":
        sql = "UPDATE Members " \
              "SET memberFName=%s, memberLName=%s, memberEmail=%s " \
              "WHERE memberID=%s;"
        values = (memberFName, memberLName, memberEmail, memberID)
        sql_UPDATE(sql, values)
    elif usr_input["action"] == "Delete":
        sql = f"DELETE FROM Members WHERE memberID={memberID};"
        sql_DELETE(sql)
    return


def CRUD_teams(data):
    """Checks user input. If attribute was empty string, set to Null, then send to sql DB"""
    usr_input = {k: None if not v else v for k, v in data.to_dict().items()}
    teamID = usr_input["teamID"]
    teamName = usr_input["teamName"]
    teamDesc = usr_input["teamDesc"]
    teamProjectID = usr_input["teamProjectID"] if "teamProjectID" in usr_input else None
    action = usr_input["action"]

    if validate_ID(teamProjectID, "Projects", action) is False:
        return

    if usr_input["action"] == "Create":
        sql = "INSERT INTO Teams (teamName, teamDesc, teamProjectID) VALUES (%s,%s,%s)"
        values = (teamName, teamDesc, teamProjectID)
        sql_INSERT(sql, values)
    elif usr_input["action"] == "Update":
        sql = "UPDATE Teams " \
              "SET teamName=%s, teamDesc=%s, teamProjectID=%s " \
              "WHERE teamID=%s;"
        values = (teamName, teamDesc, teamProjectID, teamID)
        sql_UPDATE(sql, values)
    elif usr_input["action"] == "Delete":
        sql = f"DELETE FROM Teams WHERE teamID={teamID}"
        sql_DELETE(sql)
    return


def CRUD_tasks(data):
    """Checks user input. If attribute was empty string, set to Null, then send to sql DB"""
    usr_input = {k: None if not v else v for k, v in data.to_dict().items()}
    taskID = usr_input["taskID"]
    taskName = usr_input["taskName"]
    taskDesc = usr_input["taskDesc"]
    taskPriority = usr_input["taskPriority"]
    taskDeadline = usr_input["taskDeadline"]
    taskDifficulty = usr_input["taskDifficulty"]
    taskProjectID = usr_input["taskProjectID"] if "taskProjectID" in usr_input else None
    taskTeamID = usr_input["taskTeamID"] if "taskTeamID" in usr_input else None
    taskMemberID = usr_input["taskMemberID"] if "taskMemberID" in usr_input else None
    taskDone = usr_input["taskDone"] if "taskDone" in usr_input else "0"
    action = usr_input["action"]

    if False in (validate_ID(taskProjectID, "projectID", action),
                 validate_ID(taskTeamID, "teamID", action) if not taskTeamID == None else True,
                 validate_ID(taskMemberID, "memberID", action) if not taskMemberID == None else True,
                 validate_relationship(taskTeamID, taskProjectID, "teamID", action) if not taskTeamID == None else True,
                 validate_relationship(taskMemberID, taskTeamID, "memberID", action) if not taskMemberID == None else True):
        return

    if usr_input["action"] == "Create":
        sql = "INSERT INTO Tasks ( taskName, taskDesc, taskPriority, taskDeadline, taskDifficulty, taskDone, taskProjectID, taskTeamID, taskMemberID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (taskName, taskDesc, taskPriority, taskDeadline, taskDifficulty, taskDone, taskProjectID, taskTeamID, taskMemberID)
        sql_INSERT(sql, values)
    elif usr_input["action"] == "Update":
        sql = "UPDATE Tasks " \
              "SET taskName=%s, taskDesc=%s, taskPriority=%s, taskDeadline=%s, " \
              "taskDifficulty=%s, taskDone=%s, taskProjectID=%s, taskTeamID=%s, taskMemberID=%s " \
              "WHERE taskID=%s;"
        values = (taskName, taskDesc, taskPriority, taskDeadline, taskDifficulty, taskDone, taskProjectID, taskTeamID, taskMemberID, taskID)
        sql_UPDATE(sql, values)
    elif usr_input["action"] == "Delete":
        sql = f"DELETE FROM Tasks WHERE taskID={taskID}"
        sql_DELETE(sql)
    return


def CRUD_membersteams(usr_input):
    """Checks user input. If attribute was empty string, set to Null, then send to sql DB"""
    mapID = usr_input["mapID"]
    teamID = usr_input["teamID"] if "teamID" in usr_input else None
    memberID = usr_input["memberID"] if "memberID" in usr_input else None
    action = usr_input["action"]

    if False in (validate_ID(teamID, "Teams", action),
                 validate_ID(memberID, "Members", action)):
        return

    if usr_input["action"] == "Create":
        sql = "INSERT INTO MembersTeams (memberID, teamID) VALUES (%s, %s)"
        values = (memberID, teamID)
        sql_INSERT(sql, values)
    elif usr_input["action"] == "Update":
        sql = "UPDATE MembersTeams " \
              "SET memberID=%s, teamID=%s " \
              "WHERE mapID=%s;"
        values = (memberID, teamID, mapID)
        sql_UPDATE(sql, values)
    elif usr_input["action"] == "Delete":
        sql = f"DELETE FROM MembersTeams WHERE mapID={mapID};"
        sql_DELETE(sql)
    return


def validate_ID(inputID, tableID, action):
    """Validates if the given ID exist in DB."""
    table = "Projects" if tableID == "projectID" else "Teams" if tableID == "teamID" else "Members"
    if not sql_SELECT(f"SELECT * FROM {table} WHERE {tableID}={inputID}"):
        flash(f"{action} Failed: Could not find {tableID} = {inputID}")
        return False
    return True


def validate_relationship(inputID, compareID, table_key, action):
    """Validates if ID has a relationship with compareID. Grab all rows related to compareID and check if inputID is in it"""
    if table_key == "teamID":
        sql = f"SELECT teamID, teamProjectID FROM Teams WHERE teamProjectID={compareID}"
        err = f"{action} Failed: taskTeamID:{inputID} not related to projectID:{compareID}"
    else:
        sql = f"SELECT memberID, teamID FROM MembersTeams WHERE teamID={compareID}"
        err = f"{action} Failed: taskMemberID:{inputID} not related to teamID:{compareID}"
    if int(inputID) not in [row[table_key] for row in sql_SELECT(sql)]:
        flash(err)
        return False
    return True


def connect_to_db():
    mydb = mysql.connector.connect(
        host=sys.argv[2],
        user=sys.argv[4],
        password=sys.argv[5],
        database=sys.argv[3])
    return mydb


def sql_SELECT(sql):
    """SELECT MySQL using query"""
    mydb = connect_to_db()
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute(sql)
    result = mycursor.fetchall()
    mycursor.close()
    mydb.close()
    return result


def sql_INSERT(sql, values):
    """INSERT into MySQL using query and values"""
    mydb = connect_to_db()
    mycursor = mydb.cursor()
    mycursor.execute(sql, values)
    print(mycursor.rowcount, "record inserted.")
    mydb.commit()
    mycursor.close()
    mydb.close()


def sql_UPDATE(sql, values):
    """UPDATE MySQL using query that has Null values"""
    mydb = connect_to_db()
    mycursor = mydb.cursor()
    mycursor.execute(sql, values)
    print(mycursor.rowcount, "record updated")
    mydb.commit()
    mycursor.close()
    mydb.close()


def sql_DELETE(sql):
    """DELETE MySQL row using ID"""
    mydb = connect_to_db()
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    print(mycursor.rowcount, "record deleted")
    mydb.commit()
    mycursor.close()
    mydb.close()


def user_input_validation(CRUD_page, data):
    """Tries to do CRUD operation. If invalid input, show error for user to see"""
    try:
        CRUD_page(data)
    except Exception as err:
        err = str(err)[str(err).find(':') + 2:]
        action = data["action"]
        flash(f"{action} Failed: {err}")


def replace_None_with_emp_str(elements):
    newelements = []
    for item in elements:
        item = {k: "" if v is None else v for k, v in item.items()}
        newelements.append(item)
    return newelements


@app.route("/", methods=["POST", "GET"])
def home():
    """Home Page"""
    return render_template("index.html")


@app.route("/projects", methods=["POST", "GET"])
def projects():
    """Project Page"""
    usr_search = False
    if request.method == "POST":
        data = request.form
        print(data)
        if data["search"] == "Go":  # If user pressed search button
            usr_search = data["search-input"]
        else:
            user_input_validation(CRUD_projects, data)
    if usr_search:
        sql = f"SELECT * FROM Projects WHERE projectName LIKE '%{usr_search}%' UNION "\
              f"SELECT * FROM Projects WHERE projectDesc LIKE '%{usr_search}%';"
    else:
        sql = "SELECT * FROM Projects"
    result = replace_None_with_emp_str(sql_SELECT(sql))
    return render_template("projects.html", data=result)


@app.route("/teams", methods=["POST", "GET"])
def teams():
    """Teams Page"""
    usr_search = False
    if request.method == "POST":
        data = request.form
        print(data)
        if data["search"] == "Go":  # If user pressed search button
            usr_search = data["search-input"]
        else:
            user_input_validation(CRUD_teams, data)
    # TODO: FINISH
    if usr_search:
        sql ="SELECT Teams.teamID, Teams.teamName, Teams.teamDesc, Projects.projectName, Projects.projectID "\
            f"FROM Teams LEFT JOIN Projects ON Teams.teamProjectID=Projects.projectID WHERE teamName LIKE '%{usr_search}%' UNION "\
             "SELECT Teams.teamID, Teams.teamName, Teams.teamDesc, Projects.projectName, Projects.projectID "\
            f"FROM Teams LEFT JOIN Projects ON Teams.teamProjectID=Projects.projectID WHERE teamDesc LIKE '%{usr_search}%' UNION "\
             "SELECT Teams.teamID, Teams.teamName, Teams.teamDesc, Projects.projectName, Projects.projectID "\
            f"FROM Teams LEFT JOIN Projects ON Teams.teamProjectID=Projects.projectID WHERE projectName LIKE '%{usr_search}%';"      
    else:
        sql = "SELECT Teams.teamID, Teams.teamName, Teams.teamDesc, Projects.projectName, Projects.projectID "\
              "FROM Teams LEFT JOIN Projects ON Teams.teamProjectID=Projects.projectID;"
    result = replace_None_with_emp_str(sql_SELECT(sql))
    teams_projects = sql_SELECT("SELECT projectID, projectName FROM Projects")  # dropdown for projectID=projectName
    return render_template("teams.html", data=result, projects=teams_projects)

@app.route("/teams-by-proj", methods=["GET"])
def teams_by_proj():
    project_id = request.args.get('project_id')
    sql = f"SELECT teamID, teamName FROM Teams WHERE teamProjectID = '{project_id}'"
    result = sql_SELECT(sql)
    return jsonify(result)

@app.route("/teams-by-task", methods=["GET"])
def teams_by_task():
    task_id = request.args.get('task_id')
    sql = f"SELECT teamID, teamName FROM Teams WHERE teamID = (SELECT taskTeamID FROM Tasks WHERE taskID = '{task_id}') " \
        "UNION " \
        f"SELECT teamID, teamName FROM Teams WHERE teamProjectID = (SELECT taskProjectID FROM Tasks WHERE taskID = '{task_id}')"
    null_check = f"(SELECT taskTeamID FROM Tasks WHERE taskID = '{task_id}') "
    result = sql_SELECT(sql)
    null_check = sql_SELECT(null_check)[0]['taskTeamID']
    # create the none option
    opt_none = {}
    opt_none['teamID'] = ""
    opt_none['teamName'] = "No Team"
    # if null check fails (we have a selected team)
    if (null_check):
        result.append(opt_none)
    # otherwise we don't (make none option first item)
    else:
        result.insert(0, opt_none)
    return jsonify(result)

@app.route("/members", methods=["POST", "GET"])
def members():
    """Members Page"""
    usr_search = False
    if request.method == "POST":
        data = request.form
        print(data)
        if data["search"] == "Go":  # If user pressed search button
            usr_search = data["search-input"]
        else:
            user_input_validation(CRUD_members, data)
    if usr_search:
        sql = f"SELECT * FROM Members WHERE memberFName LIKE '%{usr_search}%' UNION "\
              f"SELECT * FROM Members WHERE memberLName LIKE '%{usr_search}%' UNION "\
              f"SELECT * FROM Members WHERE memberEmail LIKE '%{usr_search}%';"

    else:
        sql = "SELECT * FROM Members"
    result = replace_None_with_emp_str(sql_SELECT(sql))
    return render_template("members.html", data=result)

@app.route("/members-by-team", methods=["GET"])
def members_by_team():
    team_id = request.args.get('team_id')
    sql = "SELECT Members.memberID, concat(Members.memberFName, ' ', Members.memberLName) fullName FROM MembersTeams " \
          "LEFT JOIN Members ON MembersTeams.memberID = Members.memberID " \
          f"WHERE teamID = '{team_id}'"
    result = sql_SELECT(sql)
    return jsonify(result)

@app.route("/members-by-task", methods=["GET"])
def members_by_task():
    task_id = request.args.get('task_id')
    sql = f"SELECT memberID, concat(memberFName, ' ', memberLName) fullName FROM Members WHERE memberID = (SELECT taskMemberID FROM Tasks WHERE taskID = '{task_id}') " \
        "UNION " \
        f"SELECT Members.memberID, concat(Members.memberFName, ' ', Members.memberLName) fullName FROM MembersTeams " \
        "LEFT JOIN Members ON MembersTeams.memberID = Members.memberID " \
        f"WHERE MembersTeams.teamID = (SELECT taskTeamID FROM Tasks WHERE taskID = '{task_id}')"
    null_check = f"(SELECT taskMemberID FROM Tasks WHERE taskID = '{task_id}') "
    result = sql_SELECT(sql)
    null_check = sql_SELECT(null_check)[0]['taskMemberID']
    # create the none option
    opt_none = {}
    opt_none['memberID'] = ""
    opt_none['fullName'] = "No Assignee"
    # if null check fails (we have a selected team)
    if (null_check):
        result.append(opt_none)
    # otherwise we don't (make none option first item)
    else:
        result.insert(0, opt_none)
    return jsonify(result)

@app.route("/tasks", methods=["POST", "GET"])
def tasks():
    """Tasks Page"""
    usr_search = False
    if request.method == "POST":
        data = request.form
        print(data)
        if data["search"] == "Go":  # If user pressed search button
            usr_search = data["search-input"]
        else:
            user_input_validation(CRUD_tasks, data)
    if usr_search:
        #sql = "SELECT Tasks.taskID, Tasks.taskName, Tasks.taskDesc, Tasks.taskPriority, Tasks.taskDeadline, Tasks.taskDifficulty, Tasks.taskDone, Projects.projectName, Projects.projectID, Teams.teamName, Teams.teamID, concat(memberFName, ' ',memberLName) fullName, Members.memberID " \
        #      "FROM Tasks " \
        #      "LEFT JOIN Projects ON Tasks.taskProjectID=Projects.projectID " \
         #     "LEFT JOIN Teams on Tasks.taskTeamID=Teams.teamID " \
        #      "LEFT JOIN Members on Tasks.taskMemberID=Members.memberID " \
        #      f"WHERE projectName = '{usr_search}';

        sql = "SELECT Tasks.taskID, Tasks.taskName, Tasks.taskDesc, Tasks.taskPriority, Tasks.taskDeadline, Tasks.taskDifficulty, Tasks.taskDone, Projects.projectName, Projects.projectID, Teams.teamName, Teams.teamID, concat(memberFName, ' ',memberLName) fullName, Members.memberID " \
               "FROM Tasks " \
               "LEFT JOIN Projects ON Tasks.taskProjectID=Projects.projectID " \
               "LEFT JOIN Teams on Tasks.taskTeamID=Teams.teamID " \
               "LEFT JOIN Members on Tasks.taskMemberID=Members.memberID " \
               f"WHERE taskName LIKE '%{usr_search}%' UNION " \
               "SELECT Tasks.taskID, Tasks.taskName, Tasks.taskDesc, Tasks.taskPriority, Tasks.taskDeadline, Tasks.taskDifficulty, Tasks.taskDone, Projects.projectName, Projects.projectID, Teams.teamName, Teams.teamID, concat(memberFName, ' ',memberLName) fullName, Members.memberID " \
               "FROM Tasks " \
               "LEFT JOIN Projects ON Tasks.taskProjectID=Projects.projectID " \
               "LEFT JOIN Teams on Tasks.taskTeamID=Teams.teamID " \
               "LEFT JOIN Members on Tasks.taskMemberID=Members.memberID " \
               f"WHERE taskDesc LIKE '%{usr_search}%' UNION " \
               "SELECT Tasks.taskID, Tasks.taskName, Tasks.taskDesc, Tasks.taskPriority, Tasks.taskDeadline, Tasks.taskDifficulty, Tasks.taskDone, Projects.projectName, Projects.projectID, Teams.teamName, Teams.teamID, concat(memberFName, ' ',memberLName) fullName, Members.memberID " \
               "FROM Tasks " \
               "LEFT JOIN Projects ON Tasks.taskProjectID=Projects.projectID " \
               "LEFT JOIN Teams on Tasks.taskTeamID=Teams.teamID " \
               "LEFT JOIN Members on Tasks.taskMemberID=Members.memberID " \
               f"WHERE projectName LIKE '%{usr_search}%' UNION " \
               "SELECT Tasks.taskID, Tasks.taskName, Tasks.taskDesc, Tasks.taskPriority, Tasks.taskDeadline, Tasks.taskDifficulty, Tasks.taskDone, Projects.projectName, Projects.projectID, Teams.teamName, Teams.teamID, concat(memberFName, ' ',memberLName) fullName, Members.memberID " \
               "FROM Tasks " \
               "LEFT JOIN Projects ON Tasks.taskProjectID=Projects.projectID " \
               "LEFT JOIN Teams on Tasks.taskTeamID=Teams.teamID " \
               "LEFT JOIN Members on Tasks.taskMemberID=Members.memberID " \
               f"WHERE teamName LIKE '%{usr_search}%' UNION " \
               "SELECT Tasks.taskID, Tasks.taskName, Tasks.taskDesc, Tasks.taskPriority, Tasks.taskDeadline, Tasks.taskDifficulty, Tasks.taskDone, Projects.projectName, Projects.projectID, Teams.teamName, Teams.teamID, concat(memberFName, ' ',memberLName) fullName, Members.memberID " \
               "FROM Tasks " \
               "LEFT JOIN Projects ON Tasks.taskProjectID=Projects.projectID " \
               "LEFT JOIN Teams on Tasks.taskTeamID=Teams.teamID " \
               "LEFT JOIN Members on Tasks.taskMemberID=Members.memberID " \
               f"WHERE memberFName LIKE '%{usr_search}%' UNION " \
               "SELECT Tasks.taskID, Tasks.taskName, Tasks.taskDesc, Tasks.taskPriority, Tasks.taskDeadline, Tasks.taskDifficulty, Tasks.taskDone, Projects.projectName, Projects.projectID, Teams.teamName, Teams.teamID, concat(memberFName, ' ',memberLName) fullName, Members.memberID " \
               "FROM Tasks " \
               "LEFT JOIN Projects ON Tasks.taskProjectID=Projects.projectID " \
               "LEFT JOIN Teams on Tasks.taskTeamID=Teams.teamID " \
               "LEFT JOIN Members on Tasks.taskMemberID=Members.memberID " \
               f"WHERE memberLName LIKE '%{usr_search}%';" \
               

    else:
        sql = "SELECT Tasks.taskID, Tasks.taskName, Tasks.taskDesc, Tasks.taskPriority, Tasks.taskDeadline, Tasks.taskDifficulty, Tasks.taskDone, Projects.projectName, Projects.projectID, Teams.teamName, Teams.teamID, concat(memberFName, ' ',memberLName) fullName, Members.memberID " \
              "FROM Tasks " \
              "LEFT JOIN Projects ON Tasks.taskProjectID=Projects.projectID " \
              "LEFT JOIN Teams on Tasks.taskTeamID=Teams.teamID " \
              "LEFT JOIN Members on Tasks.taskMemberID=Members.memberID " \
              "GROUP BY Tasks.taskID;"
              
    result = replace_None_with_emp_str(sql_SELECT(sql))
    task_projects = sql_SELECT("SELECT projectID, projectName FROM Projects")  # dropdown for projectID=projectName
    return render_template("tasks.html", data=result, projects=task_projects)


@app.route("/members_teams", methods=["POST", "GET"])
def members_teams():
    """Members_Teams Page"""
    if request.method == "POST":
        data = request.form
        print(data)
        user_input_validation(CRUD_membersteams, data)
    sql = "SELECT mapID, concat(memberFName, ' ',memberLName) fullName, Members.memberID, Teams.teamName, Teams.teamID " \
          "FROM MembersTeams " \
          "LEFT JOIN Members ON MembersTeams.memberID=Members.memberID " \
          "LEFT JOIN Teams on MembersTeams.teamID=Teams.teamID " \
          "GROUP BY mapID;"
    result = replace_None_with_emp_str(sql_SELECT(sql))
    mm_members = sql_SELECT("SELECT memberID, concat(memberFName, ' ',memberLName) fullName FROM Members")  # dropdown for memberID=fullName
    mm_teams = sql_SELECT("SELECT teamID, teamName FROM Teams")  # dropdown for teamID=teamName
    return render_template("members_teams.html", data=result, members=mm_members, teams=mm_teams)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=sys.argv[1], debug=True)
    #app.run(debug=True)
