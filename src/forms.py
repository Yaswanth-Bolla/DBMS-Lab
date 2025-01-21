from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, SubmitField, DateTimeField, SelectField, SelectMultipleField, FileField
from wtforms.validators import DataRequired, Email

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Role', choices=[('student', 'Student'), ('company', 'Company')], validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class StudentProfileForm(FlaskForm):
    usn = StringField('USN', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    cgpa = FloatField('CGPA', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    branch = StringField('Branch', validators=[DataRequired()])
    no_of_backlogs = FloatField('No of Backlogs', default=0)
    counselor_email = StringField('Counselor Email')
    submit = SubmitField('Update Profile')

class CompanyRegistrationForm(FlaskForm):
    name = StringField('Company Name', validators=[DataRequired()])
    domain = StringField('Domain', validators=[DataRequired()])
    poc = StringField('Point of Contact', validators=[DataRequired()])
    submit = SubmitField('Register Company')

class JobPostForm(FlaskForm):
    role_details = StringField('Job Role Details', validators=[DataRequired()])
    apply_by = DateTimeField('Apply By', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    cgpa_cutoff = FloatField('CGPA Cutoff', validators=[DataRequired()])
    accepted_branches = StringField('Accepted Branches (comma-separated)', validators=[DataRequired()])
    ctc = FloatField('CTC', validators=[DataRequired()])
    submit = SubmitField('Post Job')

class PlacementForm(FlaskForm):
    student_name = StringField('Student Name', validators=[DataRequired()])
    company = StringField('Company', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    submit = SubmitField('Add Placement')

class InterestForm(FlaskForm):
    interests = SelectMultipleField('Interests', choices=[], validators=[DataRequired()])
    submit = SubmitField('Update Interests')

class JobApplicationForm(FlaskForm):
    job_id = SelectField('Job Role', choices=[], validators=[DataRequired()])
    submit = SubmitField('Apply')

class ResumeUploadForm(FlaskForm):
    resume_file = FileField('Upload Resume', validators=[DataRequired()])
    submit = SubmitField('Analyze Resume')

class ResumeGenerationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    education = StringField('Education (comma-separated)', validators=[DataRequired()])
    experience = StringField('Experience (comma-separated)', validators=[DataRequired()])
    skills = StringField('Skills (comma-separated)', validators=[DataRequired()])
    submit = SubmitField('Generate Resume') 