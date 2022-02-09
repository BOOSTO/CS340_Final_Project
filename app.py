from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

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
        return render_template("projects.html") # if no POST, render project page


@app.route("/teams", methods=["POST", "GET"])
def teams():
    """Teams Page"""
    if request.method == "POST":
        data = request.form
        return redirect_from_submit(data)
    else:
        return render_template("teams.html")


@app.route("/members", methods=["POST", "GET"])
def members():
    """Members Page"""
    if request.method == "POST":
        data = request.form
        return redirect_from_submit(data)
    else:
        return render_template("members.html")


@app.route("/tasks", methods=["POST", "GET"])
def tasks():
    """Tasks Page"""
    if request.method == "POST":
        data = request.form
        return redirect_from_submit(data)
    else:
        return render_template("tasks.html")


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




# "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
# "navbar navbar-expand-lg navbar-light bg-light"