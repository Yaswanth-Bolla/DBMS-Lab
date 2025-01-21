from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'student', 'company', 'coordinator'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Student(db.Model):
    usn = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cgpa = db.Column(db.Float, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    branch = db.Column(db.String(50), nullable=False)
    no_of_backlogs = db.Column(db.Integer, default=0)
    counselor_email = db.Column(db.String(100), nullable=True)  # New attribute
    interests = db.relationship('Interest', secondary='student_interests', backref='students')

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    domain = db.Column(db.String(100), nullable=False)
    poc = db.Column(db.String(100), nullable=False)
    job_roles = db.relationship('Job', backref='company', lazy=True)

class Job(db.Model):
    job_id = db.Column(db.Integer, primary_key=True)
    role_details = db.Column(db.String(100), nullable=False)
    apply_by = db.Column(db.DateTime)
    cgpa_cutoff = db.Column(db.Float)
    accepted_branches = db.Column(db.String(100))  # Comma-separated branches
    ctc = db.Column(db.Float)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))

class Interest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

class StudentInterests(db.Model):
    student_usn = db.Column(db.String(20), db.ForeignKey('student.usn'), primary_key=True)
    interest_id = db.Column(db.Integer, db.ForeignKey('interest.id'), primary_key=True)

class PlacementStatus(db.Model):
    student_usn = db.Column(db.String(20), db.ForeignKey('student.usn'), primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), primary_key=True)
    status = db.Column(db.String(20))  # 'Eligible', 'Placed', 'Not Eligible'

class Interview(db.Model):
    interview_id = db.Column(db.Integer, primary_key=True)
    student_usn = db.Column(db.String(20), db.ForeignKey('student.usn'))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    status = db.Column(db.String(20))  # 'Scheduled', 'Completed', 'Cancelled'
    round = db.Column(db.String(20))
    time = db.Column(db.DateTime)
    venue = db.Column(db.String(100))

class Placement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)

class Offer(db.Model):
    offer_id = db.Column(db.Integer, primary_key=True)
    student_usn = db.Column(db.String(20), db.ForeignKey('student.usn'))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    status = db.Column(db.String(20))  # 'Accepted', 'Rejected'
    date_received = db.Column(db.DateTime)

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_usn = db.Column(db.String(20), db.ForeignKey('student.usn'))
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp()) 