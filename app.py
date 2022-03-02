from flask import Flask, render_template, request, redirect, url_for
import mysql.connector  # used to connect to MYSQL DB


mydb = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
)

app = Flask(__name__)


def CRUD_operations(data):
    """updates mysql db depending which button user clicked"""
    if data['action'] == 'Create':  # if button was Create
        if data["page"] == "projectPage":
            projectName = data["projectName"]
            projectDesc = data["projectDesc"]
            sql = "INSERT INTO projects (projectName, projectDesc) VALUES (%s,%s)"
            values = (projectName, projectDesc)
            sql_INSERT(sql, values)
            return
        elif data["page"] == "memberPage":
            memberFName = data["memberFName"]
            memberLName = data["memberLName"]
            memberEmail = data["memberEmail"]
            sql = "INSERT INTO members (memberFName, memberLName, memberEmail) VALUES (%s,%s,%s)"
            values = (memberFName, memberLName, memberEmail)
            sql_INSERT(sql, values)
            return
        elif data["page"] == "teamPage":
            teamName = data["teamName"]
            teamDesc = data["teamDesc"]
            teamProjectID = data["teamProjectID"]
            sql = "INSERT INTO teams (teamName, teamDesc, teamProjectID) VALUES (%s,%s,%s)"
            values = (teamName, teamDesc, teamProjectID)
            sql_INSERT(sql, values)
            return
        elif data["page"] == "taskPage":
            taskName = data["taskName"]
            taskDesc = data["taskDesc"]
            taskPriority = data["taskPriority"]
            taskDeadline = data["taskDeadline"]
            taskDifficulty = data["taskDifficulty"]
            taskProjectID = data["taskProjectID"]
            taskTeamID = data["taskTeamID"]
            taskMemberID = data["taskMemberID"]
            try:
                taskDone = data["taskDone"]
            except:
                taskDone = "0"
            sql = "INSERT INTO tasks ( taskName, taskDesc, taskPriority, taskDeadline, taskDifficulty, taskDone, taskProjectID, taskTeamID, taskMemberID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (taskName, taskDesc, taskPriority, taskDeadline, taskDifficulty, taskDone, taskProjectID, taskTeamID, taskMemberID)
            sql_INSERT(sql, values)
            return
        elif data["page"] == "membersTeamsPage":
            memberID = data["memberID"]
            teamID = data["teamID"]
            sql = "INSERT INTO membersteams (memberID, teamID) VALUES (%s, %s)"
            values = (memberID, teamID)
            sql_INSERT(sql, values)
            return
    elif data['action'] == 'Update': # if button was Update
        if data["page"] == "projectPage":
            projectName = data["projectName"]
            projectDesc = data["projectDesc"]
            projectID = data["projectID"]
            sql = "UPDATE projects " \
                  f"SET projectName = '{projectName}', projectDesc = '{projectDesc}' " \
                  f"WHERE projectID = '{projectID}'"
            sql_UPDATE(sql)
            return
        elif data["page"] == "memberPage":
            memberFName = data["memberFName"]
            memberLName = data["memberLName"]
            memberEmail = data["memberEmail"]
            memberID = data["memberID"]
            sql = "UPDATE members " \
                  f"SET memberFName='{memberFName}', memberLName='{memberLName}', memberEmail='{memberEmail}' " \
                  f"WHERE memberID='{memberID}';"
            sql_UPDATE(sql)
            return
        elif data["page"] == "teamPage":
            teamName = data["teamName"]
            teamDesc = data["teamDesc"]
            teamProjectID = data["teamProjectID"]
            teamID = data["teamID"]
            sql = "UPDATE teams " \
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
            taskProjectID = data["taskProjectID"]
            taskTeamID = data["taskTeamID"]
            taskMemberID = data["taskMemberID"]
            taskID = data["taskID"]
            sql = "UPDATE tasks " \
                  f"SET taskName='{taskName}', taskDesc='{taskDesc}', taskPriority='{taskPriority}', taskDeadline='{taskDeadline}', " \
                  f"taskDifficulty='{taskDifficulty}', taskDone='{taskDone}', taskProjectID='{taskProjectID}', taskTeamID='{taskTeamID}', taskMemberID='{taskMemberID}' " \
                  f"WHERE taskID='{taskID}';"
            sql_UPDATE(sql)
            return
        elif data["page"] == "membersTeamsPage":
            memberID = data["memberID"]
            teamID = data["teamID"]
            mapID = data["mapID"]
            sql = "UPDATE membersteams " \
                  f"SET memberID={memberID}, teamID={teamID} " \
                  f"WHERE mapID={mapID};"
            sql_UPDATE(sql)
            return
    elif data['action'] == 'Delete': # if button was Delete
        if data["page"] == "projectPage":
            projectID = data["projectID"]
            sql = f"DELETE FROM projects WHERE projectID={projectID};"
            sql_DELETE(sql)
            return
        elif data["page"] == "memberPage":
            memberID = data["memberID"]
            sql = f"DELETE FROM members WHERE memberID={memberID};"
            sql_DELETE(sql)
            return
        elif data["page"] == "teamPage":
            teamID = data["teamID"]
            sql = f"DELETE FROM teams WHERE teamID={teamID}"
            sql_DELETE(sql)
            return
        elif data["page"] == "taskPage":
            taskID = data["taskID"]
            sql = f"DELETE FROM tasks WHERE taskID={taskID}"
            sql_DELETE(sql)
            return
        elif data["page"] == "membersTeamsPage":
            mapID = data["mapID"]
            sql = f"DELETE FROM membersteams WHERE mapID={mapID};"
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
        sql = f"SELECT * FROM projects WHERE projectName = '{usr_search}';"
    else:
        sql = "SELECT * FROM projects"
    result = sql_SELECT(sql)
    return render_template("projects.html", data=result)


@app.route("/teams", methods=["POST", "GET"])
def teams():
    """Teams Page"""
    if request.method == "POST":
        data = request.form
        print(data)
        CRUD_operations(data)
    result = sql_SELECT("SELECT teams.teamID, teams.teamName, teams.teamDesc, projects.projectName, projects.projectID FROM teams LEFT JOIN projects ON teams.teamProjectID=projects.projectID")
    teams_projects = sql_SELECT("SELECT projectID, projectName FROM projects")  # dropdown for projectID=projectName
    return render_template("teams.html", data=result, projects=teams_projects)


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
        sql = f"SELECT * FROM members WHERE memberEmail = '{usr_search}';"
    else:
        sql = "SELECT * FROM members"
    result = sql_SELECT(sql)
    return render_template("members.html", data=result)


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
            CRUD_operations(data)
    if usr_search:
        sql = "SELECT tasks.taskID, tasks.taskName, tasks.taskDesc, tasks.taskPriority, tasks.taskDeadline, tasks.taskDifficulty, tasks.taskDone, projects.projectName, teams.teamName, concat(memberFName, ' ',memberLName) fullName " \
                "FROM tasks " \
                "LEFT JOIN projects ON tasks.taskProjectID=projects.projectID " \
                "LEFT JOIN teams on tasks.taskTeamID=teams.teamID " \
                "LEFT JOIN members on tasks.taskMemberID=members.memberID " \
                f"WHERE projectName = '{usr_search}';"
    else:
        sql = "SELECT tasks.taskID, tasks.taskName, tasks.taskDesc, tasks.taskPriority, tasks.taskDeadline, tasks.taskDifficulty, tasks.taskDone, projects.projectName, teams.teamName, concat(memberFName, ' ',memberLName) fullName " \
            "FROM tasks " \
            "LEFT JOIN projects ON tasks.taskProjectID=projects.projectID " \
            "LEFT JOIN teams on tasks.taskTeamID=teams.teamID " \
            "LEFT JOIN members on tasks.taskMemberID=members.memberID " \
            "GROUP BY tasks.taskID;"
    result = sql_SELECT(sql)
    task_projects = sql_SELECT("SELECT projectID, projectName FROM projects")  # dropdown for projectID=projectName
    task_teams = sql_SELECT("SELECT teamID, teamName FROM teams")  # dropdown for teamID=teamName
    task_members = sql_SELECT("SELECT memberID, concat(memberFName, ' ',memberLName) fullName FROM members")  # dropwodnw for memberID=fullName
    return render_template("tasks.html", data=result, projects=task_projects, teams=task_teams, members=task_members)


@app.route("/members_teams", methods=["POST", "GET"])
def members_teams():
    """Members_Teams Page"""
    if request.method == "POST":
        data = request.form
        print(data)
        CRUD_operations(data)
    sql = "SELECT mapID, concat(memberFName, ' ',memberLName) fullName, teams.teamName " \
          "FROM membersteams " \
          "LEFT JOIN members ON membersteams.memberID=members.memberID " \
          "LEFT JOIN teams on membersteams.teamID=teams.teamID " \
          "GROUP BY mapID;"
    result = sql_SELECT(sql)
    mm_members = sql_SELECT("SELECT memberID, concat(memberFName, ' ',memberLName) fullName FROM members")  # dropdown for memberID=fullName
    mm_teams = sql_SELECT("SELECT teamID, teamName FROM teams")  # dropdown for teamID=teamName
    return render_template("members_teams.html", data=result, members=mm_members, teams=mm_teams)


if __name__ == "__main__":
    app.run(debug=True)
