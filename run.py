from tracker import db
from tracker import app
from tracker.models import Subject, Rates, PassRequirements, Term, TaskSheet


if __name__ == "__main__":
    # db.drop_all()
    # db.create_all()
    # term_1 = Term(number=1, start_year=2020, end_year=2021, season="winter")
    # term_2 = Term(number=2, start_year=2021, end_year=2021, season="summer")
    # term_3 = Term(number=3, start_year=2021, end_year=2022, season="winter")
    # db.session.add(term_3)
    # db.session.add(term_2)
    # db.session.add(term_1)
    # db.session.commit()
    app.run(debug=True)
