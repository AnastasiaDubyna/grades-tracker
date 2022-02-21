from tracker import app, db
from flask import render_template, request, redirect, url_for
from tracker.models import Subject, Rates, PassRequirements, Term


@app.route("/get_terms", methods=["GET"])
def get_terms():
    response = {"terms": {}}
    for term in Term.query.all():
        response["terms"][term.number] = str(term)
        print(term.number)
        print(response)
    return response


@app.route("/get_subjects", methods=["GET"])
def get_subjects():
    term_number = request.args.get("term")
    subjects = Term.query.filter_by(number=term_number).first().subjects
    print({"subjects": [subject.name for subject in subjects]})
    return {"subjects": [subject.name for subject in subjects]}


@app.route("/get_schedule", methods=["GET"])
def get_schedule():
    subject_name = request.args.get("subjectName")
    response = {}
    schedule = Subject.query.filter_by(name=subject_name).first().schedule
    if schedule:
        for row in schedule:
            response[row.type] = {"day": row.day, "time": row.time, "duration": row.duration}
    return response


