from flask import Flask, render_template, request, redirect, url_for
import mysql.connector  # used to connect to MYSQL DB


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Rtruong3990",
    database="340_project"
)

app = Flask(__name__)


def redirect_from_submit(data):
    """Redirect User to appropriate page based on what submit button they clicked"""
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
        return redirect(url_for("update", data=data))
    elif data['action'] == 'Delete': # if button was Delete
        return redirect(url_for("delete", data=data))


def sql_INSERT(sql, values):
    mycursor = mydb.cursor()
    mycursor.execute(sql, values)
    print(mycursor.rowcount, "was inserted.")
    mydb.commit()
    mycursor.close()
    return


@app.route("/", methods=["POST", "GET"])
def home():
    """Home Page"""
    return render_template("index.html")


@app.route("/projects", methods=["POST", "GET"])
def projects():
    """Project Page"""
    usr_search = False
    if request.method == "POST": # if page gets a POST request
        data = request.form
        print(data)
        if data["search"] == "Go":
            usr_search = data["search-input"]
        else:
            redirect_from_submit(data)
    if usr_search:
        query = f"SELECT * FROM projects WHERE projectName = '{usr_search}';"
    else:
        query = "SELECT * FROM projects"
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute(query)
    result = mycursor.fetchall()
    mycursor.close()
    return render_template("projects.html", data=result)


@app.route("/teams", methods=["POST", "GET"])
def teams():
    """Teams Page"""
    if request.method == "POST":
        data = request.form
        print(data)
        redirect_from_submit(data)
    mycursor = mydb.cursor(dictionary=True)
    query = "SELECT teams.teamID, teams.teamName, teams.teamDesc, projects.projectName " \
            "FROM teams " \
            "INNER JOIN projects ON teams.teamID=projects.projectID"
    mycursor.execute(query)
    result = mycursor.fetchall()
    query = "SELECT projectID, projectName FROM projects"
    mycursor.execute(query)
    teams_projects = mycursor.fetchall()
    mycursor.close()
    return render_template("teams.html", data=result, projects=teams_projects)


@app.route("/members", methods=["POST", "GET"])
def members():
    """Members Page"""
    usr_search = False
    if request.method == "POST":
        data = request.form
        if data["search"] == "Go":
            usr_search = data["search-input"]
        else:
            redirect_from_submit(data)
    if usr_search:
        query = f"SELECT * FROM members WHERE memberEmail = '{usr_search}';"
    else:
        query = "SELECT * FROM members"
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute(query)
    result = mycursor.fetchall()
    mycursor.close()
    return render_template("members.html", data=result)


@app.route("/tasks", methods=["POST", "GET"])
def tasks():
    """Tasks Page"""
    usr_search = False
    if request.method == "POST":
        data = request.form
        print(data)
        if data["search"] == "Go":
            usr_search = data["search-input"]
        else:
            redirect_from_submit(data)
    if usr_search:
        query = "SELECT tasks.taskID, tasks.taskName, tasks.taskDesc, tasks.taskPriority, tasks.taskDeadline, tasks.taskDifficulty, tasks.taskDone, projects.projectName, teams.teamName, concat(memberFName, ' ',memberLName) fullName " \
                "FROM tasks " \
                "LEFT JOIN projects ON tasks.taskProjectID=projects.projectID " \
                "LEFT JOIN teams on tasks.taskTeamID=teams.teamID " \
                "LEFT JOIN members on tasks.taskMemberID=members.memberID " \
                f"WHERE projectName = '{usr_search}';"
    else:
        query = "SELECT tasks.taskID, tasks.taskName, tasks.taskDesc, tasks.taskPriority, tasks.taskDeadline, tasks.taskDifficulty, tasks.taskDone, projects.projectName, teams.teamName, concat(memberFName, ' ',memberLName) fullName " \
            "FROM tasks " \
            "LEFT JOIN projects ON tasks.taskProjectID=projects.projectID " \
            "LEFT JOIN teams on tasks.taskTeamID=teams.teamID " \
            "LEFT JOIN members on tasks.taskMemberID=members.memberID " \
            "GROUP BY tasks.taskID;"
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute(query)
    result = mycursor.fetchall()
    query = "SELECT projectID, projectName FROM projects"
    mycursor.execute(query)
    task_projects = mycursor.fetchall()
    query = "SELECT teamID, teamName FROM teams"
    mycursor.execute(query)
    task_teams = mycursor.fetchall()
    query = "SELECT memberID, concat(memberFName, ' ',memberLName) fullName FROM members"
    mycursor.execute(query)
    task_members = mycursor.fetchall()
    mycursor.close()
    return render_template("tasks.html", data=result, projects=task_projects, teams=task_teams, members=task_members)


@app.route("/members_teams", methods=["POST", "GET"])
def members_teams():
    """Members_Teams Page"""
    if request.method == "POST":
        data = request.form
        print(data)
        redirect_from_submit(data)
    mycursor = mydb.cursor(dictionary=True)
    query = "SELECT mapID, concat(memberFName, ' ',memberLName) fullName, teams.teamName " \
            "FROM membersteams " \
            "LEFT JOIN members ON membersteams.memberID=members.memberID " \
            "LEFT JOIN teams on membersteams.teamID=teams.teamID " \
            "GROUP BY mapID;"
    mycursor.execute(query)
    result = mycursor.fetchall()
    query = "SELECT memberID, concat(memberFName, ' ',memberLName) fullName FROM members"
    mycursor.execute(query)
    mm_members = mycursor.fetchall()
    query = "SELECT teamID, teamName FROM teams"
    mycursor.execute(query)
    mm_teams = mycursor.fetchall()
    mycursor.close()
    return render_template("members_teams.html", data=result, members=mm_members, teams=mm_teams)


@app.route("/create/<data>", methods=["POST", "GET"])
def create(data):
    """Clicking button takes your to this Create Page"""
    return render_template("create.html", data=data)


@app.route("/update/<data>", methods=["POST", "GET"])
def update(data):
    """Clicking button takes your to this Update Page"""
    return render_template("update.html", data=data)


@app.route("/delete/<data>", methods=["POST", "GET"])
def delete(data):
    """Clicking button takes your to this Delete Page"""
    return render_template("delete.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)
