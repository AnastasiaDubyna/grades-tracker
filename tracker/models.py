from tracker import db


class Subject(db.Model):
    name = db.Column(db.String(50), primary_key=True)
    max_points = db.Column(db.Integer, nullable=False)
    term_number = db.Column(db.Integer, db.ForeignKey("term.number"), nullable=False)
    grade_rates = db.relationship("Rates", backref="subject", lazy=True)
    pass_req = db.relationship("PassRequirements", backref="subject", lazy=True)
    tasksheets = db.relationship("TaskSheet", backref="subject", lazy=True)
    schedule = db.relationship("Schedule", backref="subject", lazy=True)

    def count_points(self):
        return sum([tasksheet.points for tasksheet in self.tasksheets])

    def get_points_percent(self):
        return self.count_points() * 100 / self.max_points

    def __repr__(self):
        return f"Subject('{self.name}')"


class Rates(db.Model):
    subject_name = db.Column(db.String(50), db.ForeignKey("subject.name"), primary_key=True, nullable=False)
    three_zero = db.Column(db.Integer, nullable=False)
    three_half = db.Column(db.Integer, nullable=False)
    four_zero = db.Column(db.Integer, nullable=False)
    four_half = db.Column(db.Integer, nullable=False)
    five_zero = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"{self.subject_name} : 3.0 - {self.three_zero}, 3.5 - {self.three_half}, 4.0 - {self.four_zero}, " \
               f"4.5 - {self.four_half}, 5.0 - {self.five_zero} "


class PassRequirements(db.Model):
    subject_name = db.Column(db.String(50), db.ForeignKey("subject.name"), primary_key=True, nullable=False)
    exam = db.Column(db.Boolean)
    tasksheets = db.Column(db.Boolean)
    project = db.Column(db.Boolean)

    def __repr__(self):
        return f"{self.subject_name}: Exam - {self.exam}, Tasksheets - {self.tasksheets}, Project - {self.project}"


class TaskSheet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String(50), db.ForeignKey("subject.name"), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Integer, nullable=False)
    max_points = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"{self.subject_name}|Task sheet {self.number}: {self.points}/{self.max_points}"


class Term(db.Model):
    number = db.Column(db.Integer, primary_key=True)
    start_year = db.Column(db.Integer, nullable=False)
    end_year = db.Column(db.Integer, nullable=False)
    season = db.Column(db.String(6), nullable=False)
    subjects = db.relationship("Subject", backref="term", lazy=True)

    def __repr__(self):
        return f"{self.season} term {self.start_year}|{self.end_year}"


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)
    day = db.Column(db.String(20), nullable=False)
    time = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    subject_name = db.Column(db.String(50), db.ForeignKey("subject.name"), nullable=False)

    def __repr__(self):
        return f"{self.subject_name}: {self.type} {self.day} {self.time}"

