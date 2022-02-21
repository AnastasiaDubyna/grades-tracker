from tracker import app, db
from flask import render_template, request, redirect, url_for
from tracker.models import Subject, Rates, PassRequirements, Term, Schedule


@app.route("/schedule")
def schedule():
    term = Term.query.all()[-1]
    schedules = Schedule.query.all()
    return render_template("schedule.html", term=term, schedules=schedules, selected="schedule")


@app.route("/schedule/edit", methods=["GET", "POST"])
def edit_schedule():
    if request.method == "GET":
        term_number = request.args.get("term")
        subjects = Term.query.filter_by(number=term_number).first().subjects
        return render_template("schedule_form.html", subjects=subjects, selected="schedule")
    else:
        data = request.json
        print(data)
        subject_name = request.args.get("subjectName")
        for subject_type, schedule_data in data.items():
            if is_schedule_data_exist(schedule_data):
                if schedule_already_in_db(subject_type, subject_name):
                    update_schedule_data(subject_name, subject_type, schedule_data)
                new_schedule = Schedule(subject_name=subject_name, type=subject_type, day=schedule_data["day"],
                                        time=schedule_data["time"], duration=schedule_data["duration"])
                db.session.add(new_schedule)
                db.session.commit()
        return {"success": True, "message": "Schedule updated"}


def is_schedule_data_exist(data):
    return data and data["day"] and data["time"] and data["duration"]


def schedule_already_in_db(subject_type, subject_name):
    return Schedule.query.filter_by(subject_name=subject_name, type=subject_type).first()


def update_schedule_data(subject_name, subject_type, data):
    schedule_object = Schedule.query.filter_by(subject_name=subject_name, type=subject_type).first()
    schedule_object.day = data["day"]
    schedule_object.time = data["time"]
    schedule_object.duration = data["duration"]
    db.session.commit()
