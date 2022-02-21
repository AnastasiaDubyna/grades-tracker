from tracker import app, db
from flask import render_template, request, redirect, url_for
from tracker.models import Subject, Rates, PassRequirements, Term, TaskSheet


@app.route("/remove/subject/<name>", methods=["POST"])
def remove_subject(name):
    Subject.query.filter_by(name=name).delete()
    TaskSheet.query.filter_by(subject_name=name).delete()
    PassRequirements.query.filter_by(subject_name=name).delete()
    Rates.query.filter_by(subject_name=name).delete()
    db.session.commit()
    return {"success": True}


@app.route("/remove/<subject_name>/<tasksheet_number>", methods=["POST"])
def remove_tasksheet(subject_name, tasksheet_number):
    TaskSheet.query.filter_by(subject_name=subject_name, number=tasksheet_number).delete()
    db.session.commit()
    return {"success": True}
