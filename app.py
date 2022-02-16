from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

fake_data_project = [
    {
        "projectID": "0",
        "projectName": "Among Us",
        "projectDesc": "The revolutionary game that brought people together during the pandemic!"
    },
    {
        "projectID": "1",
        "projectName": "Halo",
        "projectDesc": "Emotionally stunted green man rescues blue girl."
    },
    {
        "projectID": "2",
        "projectName": "Modern Warefare 2",
        "projectDesc": "Shooty gun gun"
    }
]
fake_teams_data = [
    {
        "teamID": "0",
        "teamName": "Concept Artist",
        "teamDesc": "Responsible for all conceptual art and designs.",
        "teamProjectID": "0"
    },
    {
        "teamID": "1",
        "teamName": "Playtesters",
        "teamDesc": "Evaluate user experience and game reliability.",
        "teamProjectID": "1"
    },
    {
        "teamID": "2",
        "teamName": "Elite Gamers",
        "teamDesc": "Pwn n00bs and drink mtn dew! XD",
        "teamProjectID": "1"
    }
]
fake_members_data = [
    {
        "memberID": "0",
        "memberFname": "Purple",
        "memberLname": "Guy",
        "memberEmail": "PurpleAmongUs@mail.com"
    },
    {
        "memberID": "1",
        "memberFname": "Cortona",
        "memberLname": "AI",
        "memberEmail": "Cortona@mail.com"
    },
    {
        "memberID": "2",
        "memberFname": "Morty",
        "memberLname": "Smith",
        "memberEmail": "Morty@mail.com"
    }
]
fake_tasks_data = [
    {
        "taskID": "0",
        "taskName": "Survive bad guy Among Us",
        "taskDesc": "Avoid bad guy Among Us at all times or they will get you",
        "taskPriority": "100",
        "taskDeadline": "02-10-2020",
        "taskDifficulty": "2",
        "taskDone": "No",
        "taskProjectID": "1",
        "taskTeamID": "2",
        "taskMemberID": "1"
    },
    {
        "taskID": "1",
        "taskName": "Save Sgt. Johnson from flood",
        "taskDesc": "Sgt. Johnson has been ambushed and needs our help",
        "taskPriority": "10",
        "taskDeadline": "01-10-2008",
        "taskDifficulty": "4",
        "taskDone": "No",
        "taskProjectID": "2",
        "taskTeamID": "5",
        "taskMemberID": "2"
    },
    {
        "taskID": "2",
        "taskName": "Study Chicken",
        "taskDesc": "Try to understand why chicken crossed the road",
        "taskPriority": "2",
        "taskDeadline": "05-25-2015",
        "taskDifficulty": "4",
        "taskDone": "Yes",
        "taskProjectID": "3",
        "taskTeamID": "1",
        "taskMemberID": "4"
    }
]


def redirect_from_submit(data):
    """Redirect User to appropriate page based on what submit button they clicked"""
    if data['action'] == 'Create': # if button was Create
        return redirect(url_for("create", data=data))
    elif data['action'] == 'Update': # if button was Update
        return redirect(url_for("update", data=data))
    elif data['action'] == 'Delete': # if button was Delete
        return redirect(url_for("delete", data=data))

example_data_from_create = [
    ('projectID', ''), 
    ('projectName', 'Stonks Trader'), 
    ('projectDesc', 'Trades Stonks'), 
    ('action', 'Create')
    ]


@app.route("/", methods=["POST", "GET"])
def home():
    """Home Page"""
    return render_template("index.html")


@app.route("/projects", methods=["POST", "GET"])
def projects():
    """Project Page"""
    if request.method == "POST": # if page gets a POST request
        data = request.form
        return redirect_from_submit(data) # redirect the input data to new page
    else:
        return render_template("projects.html", data=fake_data_project) # if no POST, render project page


@app.route("/teams", methods=["POST", "GET"])
def teams():
    """Teams Page"""
    if request.method == "POST":
        data = request.form
        return redirect_from_submit(data)
    else:
        return render_template("teams.html", data=fake_teams_data)


@app.route("/members", methods=["POST", "GET"])
def members():
    """Members Page"""
    if request.method == "POST":
        data = request.form
        return redirect_from_submit(data)
    else:
        return render_template("members.html", data=fake_members_data)


@app.route("/tasks", methods=["POST", "GET"])
def tasks():
    """Tasks Page"""
    if request.method == "POST":
        data = request.form
        return redirect_from_submit(data)
    else:
        return render_template("tasks.html", data=fake_tasks_data)


@app.route("/members_teams", methods=["POST", "GET"])
def members_teams():
    """Members_Teams Page"""
    return render_template("members_teams.html")


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




"""
{% for item in data %}
        <tr>
            <form action="#" method="post">
                <td><input type="text" name="teamID" value="{{item['teamID']}}" readonly /></td>
                <td><input type="text" name="teamName" value="{{item['teamName']}}" /></td>
                <td><input type="text" name="teamDesc" value="{{item['teamDesc']}}" /></td>
                <td><input type="text" name="teamProjectID" value="{{item['teamProjectID']}}" /></td>
                <td class="col-act">
                    <button type="submit" name="action" value="Update"><i class="fa-solid fa-pen-to-square"></i></button>
                    <button type="submit" name="action" value="Delete"><i class="fa-solid fa-trash"></i></button>
                </td>
            </form>
        </tr>
    {% endfor %}
</table>
{% endblock %}"""