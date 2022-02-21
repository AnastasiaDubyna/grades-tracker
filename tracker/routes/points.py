from tracker import app, db
from flask import render_template, request, redirect, url_for
from tracker.models import Subject, Rates, PassRequirements, Term, TaskSheet


@app.route("/points")
def points():
    print("HERE")
    term_number = request.args.get("term")
    print(term_number)
    term = Term.query.filter_by(number=term_number).first() if term_number else Term.query.all()[-1]
    if term.subjects:
        subject = term.subjects[0]
        return redirect(url_for("points_for_subject", subject_name=subject.name))
    else:
        return render_template("points.html", term=term)


@app.route("/points/<subject_name>")
def points_for_subject(subject_name):
    print(subject_name)
    subject = Subject.query.filter_by(name=subject_name).first()
    tasksheets = TaskSheet.query.order_by(TaskSheet.number).filter_by(subject_name=subject_name).all()
    print(tasksheets)
    term = Term.query.filter_by(number=subject.term_number).first()
    return render_template("points.html", subject_name=subject.name, tasksheets=tasksheets, term=term, selected="points", add_new="tasksheet")


@app.route("/points/add_new_tasksheet", methods=["POST", "GET"])
def add_new_tasksheet():
    if request.method == "GET":
        print(request.args.get("subjectName"))
        return render_template("tasksheet_form.html", subject_name=request.args.get("subjectName"), selected="points")
    else:
        data = request.json
        if is_data_exist(data):
            if does_tasksheet_exist(data["subjectName"], data["number"]):
                return {"success": False, "message": "Task sheet already exists"}
            new_tasksheet = TaskSheet(subject_name=data["subjectName"], number=data["number"], points=data["points"],
                                      max_points=data["maxPoints"])
            db.session.add(new_tasksheet)
            db.session.commit()
            return {"success": True}
        else:
            return {"success": False, "message": "Please fill all inputs"}


@app.route("/points/<subject>/edit/<tasksheet_number>", methods=["GET", "POST"])
def edit_tasksheet(subject, tasksheet_number):
    tasksheet = TaskSheet.query.filter_by(subject_name=subject, number=tasksheet_number).first()
    if request.method == "GET":
        return render_template("tasksheet_form.html", subject_name=subject, tasksheet_data=tasksheet, selected="points")
    else:
        new_data = request.json
        if is_data_exist(new_data):
            if not is_data_valid(new_data):
                return {"success": False, "message": "You can't get more points than maximum"}
            update_tasksheet_data(new_data, tasksheet)
            return {"success": True}
        else:
            return {"success": False, "message": "Please fill all inputs"}


def is_data_exist(data):
    keys = ["subjectName", "number", "points", "maxPoints"]
    return all([data[key] for key in keys])


def does_tasksheet_exist(subject_name, tasksheet_number):
    return TaskSheet.query.filter_by(subject_name=subject_name, number=tasksheet_number).first()


def is_data_valid(data):
    return int(data["points"]) <= int(data["maxPoints"])


def update_tasksheet_data(new_data, tasksheet):
    tasksheet.number = new_data["number"]
    tasksheet.points = new_data["points"]
    tasksheet.max_points = new_data["maxPoints"]
    db.session.commit()
