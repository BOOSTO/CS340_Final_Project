import sys
from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector  # used to connect to MYSQL DB

if len(sys.argv) != 6:
    print("ERROR usage: 'python3 app.py <sv_port> <db_hostname> <db_database_name> <db_username> <db_passwd>'")
    exit()

mydb = mysql.connector.connect(
    host=sys.argv[2],
    user=sys.argv[4],
    password=sys.argv[5],
    database=sys.argv[3]
)


app = Flask(__name__)

def CRUD_tasks(task):
    try:
        taskID = "'" + task["taskID"] + "'"
    except:
        taskID = None
    taskName = "'" + task["taskName"] + "'" if task["taskName"] != "" else None
    taskDesc = "'" + task["taskDesc"] + "'" if task["taskDesc"] != "" else None
    taskPriority = "'" + task["taskPriority"] + "'" if task["taskPriority"] != "" else None
    taskDeadline = "'" + task["taskDeadline"] + "'" if task["taskDeadline"] != "" else None
    taskDifficulty = "'" + task["taskDifficulty"] + "'" if task["taskDifficulty"] != "" else None
    try:
        taskProjectID = "'" + task["taskProjectID"] + "'" if task["taskProjectID"] != "None" else None
    except:
        taskProjectID = None
    try:
        taskTeamID = "'" + task["taskTeamID"] + "'" if task["taskTeamID"] != "None" else None
    except:
        taskTeamID = None
    try:
        taskMemberID = "'" + task["taskMemberID"] + "'" if task["taskMemberID"] != "None" else None
    except:
        taskMemberID = None
    try:
        taskDone = "'" + task["taskDone"] + "'"
    except:
        taskDone = "0"

    if task["action"] == "Create":
        sql = "INSERT INTO Tasks ( taskName, taskDesc, taskPriority, taskDeadline, taskDifficulty, taskDone, taskProjectID, taskTeamID, taskMemberID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (taskName, taskDesc, taskPriority, taskDeadline, taskDifficulty, taskDone, taskProjectID, taskTeamID, taskMemberID)
        sql_INSERT(sql, values)
    elif task["action"] == "Update":
        sql = "UPDATE Tasks " \
            f"SET taskName={taskName}, taskDesc={taskDesc}, taskPriority={taskPriority}, taskDeadline={taskDeadline}, " \
            f"taskDifficulty={taskDifficulty}, taskDone={taskDone}, taskProjectID={taskProjectID}, taskTeamID={taskTeamID}, taskMemberID={taskMemberID} " \
            f"WHERE taskID={taskID};"
        print("SQL FUCK:")
        print(sql)
        sql_UPDATE(sql)
    elif task["action"] == "Delete":
        sql = f"DELETE FROM Tasks WHERE taskID={taskID}"
        sql_DELETE(sql)
    else:
        print("this shouldn't happen.")
    print(sql)
    return

def CRUD_operations(data):
    """updates mysql db depending which button user clicked"""
    if data['action'] == 'Create':  # if button was Create
        if data["page"] == "projectPage":
            projectName = data["projectName"]
            projectDesc = data["projectDesc"]
            sql = "INSERT INTO Projects (projectName, projectDesc) VALUES (%s,%s)"
            values = (projectName, projectDesc)
            sql_INSERT(sql, values)
            return
        elif data["page"] == "memberPage":
            memberFName = data["memberFName"]
            memberLName = data["memberLName"]
            memberEmail = data["memberEmail"]
            sql = "INSERT INTO Members (memberFName, memberLName, memberEmail) VALUES (%s,%s,%s)"
            values = (memberFName, memberLName, memberEmail)
            sql_INSERT(sql, values)
            return
        elif data["page"] == "teamPage":
            teamName = data["teamName"]
            teamDesc = data["teamDesc"]
            teamProjectID = data["teamProjectID"]
            sql = "INSERT INTO Teams (teamName, teamDesc, teamProjectID) VALUES (%s,%s,%s)"
            values = (teamName, teamDesc, teamProjectID)
            sql_INSERT(sql, values)
            return
        elif data["page"] == "taskPage":
            taskName = data["taskName"]
            taskDesc = data["taskDesc"]
            taskPriority = data["taskPriority"]
            taskDeadline = data["taskDeadline"]
            taskDifficulty = data["taskDifficulty"]
            try:
                taskProjectID = data["taskProjectID"]
            except:
                taskProjectID = None
            try:
                taskTeamID = data["taskTeamID"]
            except:
                taskTeamID = None
            try:
                taskMemberID = data["taskMemberID"]
            except:
                taskMemberID = None
            try:
                taskDone = data["taskDone"]
            except:
                taskDone = "0"
            sql = "INSERT INTO Tasks ( taskName, taskDesc, taskPriority, taskDeadline, taskDifficulty, taskDone, taskProjectID, taskTeamID, taskMemberID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (taskName, taskDesc, taskPriority, taskDeadline, taskDifficulty, taskDone, taskProjectID, taskTeamID, taskMemberID)
            sql_INSERT(sql, values)
            return
        elif data["page"] == "membersTeamsPage":
            memberID = data["memberID"]
            teamID = data["teamID"]
            sql = "INSERT INTO MembersTeams (memberID, teamID) VALUES (%s, %s)"
            values = (memberID, teamID)
            sql_INSERT(sql, values)
            return
    elif data['action'] == 'Update': # if button was Update
        if data["page"] == "projectPage":
            projectName = data["projectName"]
            projectDesc = data["projectDesc"]
            projectID = data["projectID"]
            sql = "UPDATE Projects " \
                  f"SET projectName = '{projectName}', projectDesc = '{projectDesc}' " \
                  f"WHERE projectID = '{projectID}'"
            sql_UPDATE(sql)
            return
        elif data["page"] == "memberPage":
            memberFName = data["memberFName"]
            memberLName = data["memberLName"]
            memberEmail = data["memberEmail"]
            memberID = data["memberID"]
            sql = "UPDATE Members " \
                  f"SET memberFName='{memberFName}', memberLName='{memberLName}', memberEmail='{memberEmail}' " \
                  f"WHERE memberID='{memberID}';"
            sql_UPDATE(sql)
            return
        elif data["page"] == "teamPage":
            teamName = data["teamName"]
            teamDesc = data["teamDesc"]
            teamProjectID = data["teamProjectID"]
            teamID = data["teamID"]
            sql = "UPDATE Teams " \
                  f"SET teamName='{teamName}', teamDesc='{teamDesc}', teamProjectID='{teamProjectID}' " \
                  f"WHERE teamID='{teamID}';"
            sql_UPDATE(sql)
            return
        elif data["page"] == "taskPage":
            taskName = data["taskName"]
            taskDesc = data["taskDesc"]
            taskPriority = data["taskPriority"]
            taskDeadline = data["taskDeadline"]
            taskDifficulty = data["taskDifficulty"]
            try:
                taskDone = data["taskDone"]
            except:
                taskDone = "0"
            taskProjectID = "NULL"
            if data["taskProjectID"] != "None":
                taskProjectID = data["taskProjectID"]
            taskTeamID = "NULL"
            if data["taskTeamID"] != "None":
                taskTeamID = data["taskTeamID"]
            taskMemberID = "NULL"
            if data["taskMemberID"] != "None":
                taskMemberID = data["taskMemberID"]
            taskID = data["taskID"]
            sql = "UPDATE Tasks " \
                  f"SET taskName='{taskName}', taskDesc='{taskDesc}', taskPriority='{taskPriority}', taskDeadline='{taskDeadline}', " \
                  f"taskDifficulty='{taskDifficulty}', taskDone='{taskDone}', taskProjectID={taskProjectID}, taskTeamID={taskTeamID}, taskMemberID={taskMemberID} " \
                  f"WHERE taskID='{taskID}';"
            sql_UPDATE(sql)
            return
        elif data["page"] == "membersTeamsPage":
            memberID = data["memberID"]
            teamID = data["teamID"]
            mapID = data["mapID"]
            sql = "UPDATE MembersTeams " \
                  f"SET memberID={memberID}, teamID={teamID} " \
                  f"WHERE mapID={mapID};"
            sql_UPDATE(sql)
            return
    elif data['action'] == 'Delete': # if button was Delete
        if data["page"] == "projectPage":
            projectID = data["projectID"]
            sql = f"DELETE FROM Projects WHERE projectID={projectID};"
            sql_DELETE(sql)
            return
        elif data["page"] == "memberPage":
            memberID = data["memberID"]
            sql = f"DELETE FROM Members WHERE memberID={memberID};"
            sql_DELETE(sql)
            return
        elif data["page"] == "teamPage":
            teamID = data["teamID"]
            sql = f"DELETE FROM Teams WHERE teamID={teamID}"
            sql_DELETE(sql)
            return
        elif data["page"] == "taskPage":
            taskID = data["taskID"]
            sql = f"DELETE FROM Tasks WHERE taskID={taskID}"
            sql_DELETE(sql)
            return
        elif data["page"] == "membersTeamsPage":
            mapID = data["mapID"]
            sql = f"DELETE FROM MembersTeams WHERE mapID={mapID};"
            sql_DELETE(sql)
            return


def sql_SELECT(sql):
    """SELECT MySQL using query"""
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute(sql)
    result = mycursor.fetchall()
    mycursor.close()
    return result


def sql_INSERT(sql, values):
    """INSERT into MySQL using query and values"""
    mycursor = mydb.cursor()
    mycursor.execute(sql, values)
    print(mycursor.rowcount, "record inserted.")
    mydb.commit()
    mycursor.close()

def sql_UPDATE(sql, values):
    """UPDATE MySQL using query"""
    mycursor = mydb.cursor()
    mycursor.execute(sql, values)
    print(mycursor.rowcount, "record updated")
    mydb.commit()
    mycursor.close()

def sql_UPDATE(sql):
    """UPDATE MySQL using query"""
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    print(mycursor.rowcount, "record updated")
    mydb.commit()
    mycursor.close()


def sql_DELETE(sql):
    """DELETE MySQL row using ID"""
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    print(mycursor.rowcount, "record deleted")
    mydb.commit()
    mycursor.close()


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
        if data["search"] == "Go":
            """If user pressed search button"""
            usr_search = data["search-input"]
        else:
            CRUD_operations(data)
    if usr_search:
        sql = f"SELECT * FROM Projects WHERE projectName = '{usr_search}';"
    else:
        sql = "SELECT * FROM Projects"
    result = sql_SELECT(sql)
    return render_template("projects.html", data=result)


@app.route("/teams", methods=["POST", "GET"])
def teams():
    """Teams Page"""
    if request.method == "POST":
        data = request.form
        print(data)
        CRUD_operations(data)
    result = sql_SELECT("SELECT Teams.teamID, Teams.teamName, Teams.teamDesc, Projects.projectName, Projects.projectID FROM Teams LEFT JOIN Projects ON Teams.teamProjectID=Projects.projectID")
    teams_projects = sql_SELECT("SELECT projectID, projectName FROM Projects")  # dropdown for projectID=projectName
    return render_template("teams.html", data=result, projects=teams_projects)

@app.route("/teams-by-proj", methods=["GET"])
def teams_by_proj():
    project_id = request.args.get('project_id')
    sql = f"SELECT teamID, teamName FROM Teams WHERE teamProjectID = '{project_id}'"
    result = sql_SELECT(sql)
    return jsonify(result)

@app.route("/members", methods=["POST", "GET"])
def members():
    """Members Page"""
    usr_search = False
    if request.method == "POST":
        data = request.form
        print(data)
        if data["search"] == "Go":
            """If user pressed search button"""
            usr_search = data["search-input"]
        else:
            CRUD_operations(data)
    if usr_search:
        sql = f"SELECT * FROM Members WHERE memberEmail = '{usr_search}';"
    else:
        sql = "SELECT * FROM Members"
    result = sql_SELECT(sql)
    return render_template("members.html", data=result)

@app.route("/members-by-team", methods=["GET"])
def members_by_team():
    team_id = request.args.get('team_id')
    sql = "SELECT Members.memberID, concat(Members.memberFName, ' ', Members.memberLName) fullName FROM MembersTeams " \
           "LEFT JOIN Members ON MembersTeams.memberID = Members.memberID " \
           f"WHERE teamID = '{team_id}'"
    result = sql_SELECT(sql)
    return jsonify(result)

@app.route("/tasks", methods=["POST", "GET"])
def tasks():
    """Tasks Page"""
    usr_search = False
    if request.method == "POST":
        data = request.form
        print(data)
        if data["search"] == "Go":
            """If user pressed search button"""
            usr_search = data["search-input"]
        else:
            # CRUD_operations(data)
            CRUD_tasks(data)
    if usr_search:
        sql = "SELECT Tasks.taskID, Tasks.taskName, Tasks.taskDesc, Tasks.taskPriority, Tasks.taskDeadline, Tasks.taskDifficulty, Tasks.taskDone, Projects.projectName, Projects.projectID, Teams.teamName, Teams.teamID, concat(memberFName, ' ',memberLName) fullName, Members.memberID " \
                "FROM Tasks " \
                "LEFT JOIN Projects ON Tasks.taskProjectID=Projects.projectID " \
                "LEFT JOIN Teams on Tasks.taskTeamID=Teams.teamID " \
                "LEFT JOIN Members on Tasks.taskMemberID=Members.memberID " \
                f"WHERE projectName = '{usr_search}';"
    else:
        sql = "SELECT Tasks.taskID, Tasks.taskName, Tasks.taskDesc, Tasks.taskPriority, Tasks.taskDeadline, Tasks.taskDifficulty, Tasks.taskDone, Projects.projectName, Projects.projectID, Teams.teamName, Teams.teamID, concat(memberFName, ' ',memberLName) fullName, Members.memberID " \
            "FROM Tasks " \
            "LEFT JOIN Projects ON Tasks.taskProjectID=Projects.projectID " \
            "LEFT JOIN Teams on Tasks.taskTeamID=Teams.teamID " \
            "LEFT JOIN Members on Tasks.taskMemberID=Members.memberID " \
            "GROUP BY Tasks.taskID;"
    result = sql_SELECT(sql)
    task_projects = sql_SELECT("SELECT projectID, projectName FROM Projects")  # dropdown for projectID=projectName
    task_teams = sql_SELECT("SELECT teamID, teamName FROM Teams")  # dropdown for teamID=teamName
    task_members = sql_SELECT("SELECT memberID, concat(memberFName, ' ',memberLName) fullName FROM Members")  # dropwodnw for memberID=fullName
    return render_template("tasks.html", data=result, projects=task_projects, teams=task_teams, members=task_members)


@app.route("/members_teams", methods=["POST", "GET"])
def members_teams():
    """Members_Teams Page"""
    if request.method == "POST":
        data = request.form
        print(data)
        CRUD_operations(data)
    sql = "SELECT mapID, concat(memberFName, ' ',memberLName) fullName, Teams.teamName " \
          "FROM MembersTeams " \
          "LEFT JOIN Members ON MembersTeams.memberID=Members.memberID " \
          "LEFT JOIN Teams on MembersTeams.teamID=Teams.teamID " \
          "GROUP BY mapID;"
    result = sql_SELECT(sql)
    mm_members = sql_SELECT("SELECT memberID, concat(memberFName, ' ',memberLName) fullName FROM Members")  # dropdown for memberID=fullName
    mm_teams = sql_SELECT("SELECT teamID, teamName FROM Teams")  # dropdown for teamID=teamName
    return render_template("members_teams.html", data=result, members=mm_members, teams=mm_teams)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=sys.argv[1], debug=True)
