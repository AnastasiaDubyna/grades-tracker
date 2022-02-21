from tracker import app, db
from flask import render_template, request, redirect, url_for
from tracker.models import Subject, Rates, PassRequirements, Term
from sqlalchemy import exc


@app.route("/test")
def test():
    term = Term.query.all()[-1]

    return render_template("base_with_subject_selector.html", term=term, add_new="subject", subject_name="Analiza numeryczna")

@app.route("/subjects")
@app.route("/")
def home():
    last_term = Term.query.all()[-1].number
    return redirect(url_for("subjects", term=last_term))


@app.route("/subjects/<term>", methods=["GET"])
def subjects(term):
    curr_term = Term.query.filter_by(number=term).first()
    subjects_list = curr_term.subjects
    return render_template("subjects.html", subjects=subjects_list, term=curr_term, selected="subjects", add_new="subject")




@app.route("/subjects/add_new_subject", methods=["GET", "POST"])
def add_new_subject():
    if request.method == "POST":
        data = request.json
        if is_data_exist(data):
            if not are_rates_valid(data["rates"]):
                return {"success": False, "message": "Rates are invalid"}
            if does_subject_exist(data["name"]):
                return {"success": False, "message": "Subject already exists"}
            create_new_subject(data)
            return {"success": True}
        else:
            return {"success": False, "message": "Please fill all inputs"}
    else:
        return render_template("subject_form.html", subject_data=None, term=request.args.get("term"), selected="subjects")


@app.route("/subjects/edit/<subject_name>", methods=["GET", "POST"])
def edit(subject_name):
    if request.method == "GET":
        return render_template("subject_form.html", subject_data=Subject.query.filter_by(name=subject_name).first(), selected="subjects")
    else:
        new_data = request.json
        print(type(new_data["maxPoints"]))
        if is_data_exist(new_data):
            if not are_rates_valid(new_data["rates"]):
                return {"success": False, "message": "Rates are invalid"}
            update_subject_data(new_data, subject_name)
            return {"success": True}
        else:
            return {"success": False, "message": "Please fill all inputs"}


def is_data_exist(data):
    subject_keys = ["name", "rates", "passRequirements", "termNumber", "maxPoints"]
    rates_keys = ["threeZero", "threeHalf", "fourZero", "fourHalf", "fiveZero"]
    return all([data[key] for key in subject_keys]) \
           and all([data["rates"][key] for key in rates_keys])


def does_subject_exist_in_term(name, term_number):
    term_subjects = Term.query.filter_by(number=term_number).first().subjects
    for subject in term_subjects:
        if subject.name == name:
            return True
    return False


def does_subject_exist(name):
    print(Subject.query.filter_by(name=name).first())
    return Subject.query.filter_by(name=name).first()


def are_rates_valid(rates_dict):
    keys = list(rates_dict.keys())
    for i in range(len(keys) - 1):
        if rates_dict[keys[i]] > rates_dict[keys[i + 1]]:
            return False
    return True


def create_new_subject(data):
    rates = data["rates"]
    pass_reqs = data["passRequirements"]
    new_subject = Subject(name=data["name"], max_points=data["maxPoints"], term_number=data["termNumber"])
    new_rates = Rates(subject_name=data["name"], three_zero=rates["threeZero"], three_half=rates["threeHalf"],
                      four_zero=rates["fourZero"], four_half=rates["fourHalf"], five_zero=rates["fiveZero"])
    new_requirements = PassRequirements(subject_name=data["name"], exam=pass_reqs["exam"],
                                        tasksheets=pass_reqs["tasksheets"], project=pass_reqs["project"])
    db.session.add(new_subject)
    db.session.add(new_rates)
    db.session.add(new_requirements)
    db.session.commit()


def update_subject_data(new_data, subject_name):
    subject = Subject.query.filter_by(name=subject_name).first()
    grade_rates = subject.grade_rates[0]
    pass_requirements = subject.pass_req[0]
    new_rates = new_data["rates"]
    new_requirements = new_data["passRequirements"]

    subject.name = new_data["name"]
    subject.max_points = new_data["maxPoints"]
    subject.term_number = new_data["termNumber"]
    grade_rates.three_zero = new_rates["threeZero"]
    grade_rates.three_half = new_rates["threeHalf"]
    grade_rates.four_zero = new_rates["fourZero"]
    grade_rates.four_half = new_rates["fourHalf"]
    grade_rates.five_zero = new_rates["fiveZero"]
    pass_requirements.exam = new_requirements["exam"]
    pass_requirements.tasksheets = new_requirements["tasksheets"]
    pass_requirements.project = new_requirements["project"]
    db.session.commit()
