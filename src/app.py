from flask import Flask, render_template, redirect, url_for, flash, request, send_file
from forms import RegistrationForm, StudentProfileForm, CompanyRegistrationForm, JobPostForm, InterestForm, JobApplicationForm, ResumeUploadForm, ResumeGenerationForm, LoginForm
from models import db, User, Student, Company, Job, Interest, PlacementStatus, Interview, Resume
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from analytics import generate_placement_statistics, track_student_performance
from flask_mail import Mail, Message
from resume_analyzer import analyze_resume
from resume_generator import generate_resume
from pdf_generator import generate_pdf

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///placements.db'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@example.com'
app.config['MAIL_PASSWORD'] = 'your_password'
app.config['MAIL_DEFAULT_SENDER'] = 'your_email@example.com'

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

mail = Mail(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, role=form.role.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/student_profile', methods=['GET', 'POST'])
@login_required
def student_profile():
    form = StudentProfileForm()
    if form.validate_on_submit():
        student = Student(
            usn=form.usn.data,
            name=form.name.data,
            cgpa=form.cgpa.data,
            email=form.email.data,
            branch=form.branch.data,
            no_of_backlogs=form.no_of_backlogs.data
        )
        db.session.add(student)
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('student_profile'))
    return render_template('student_profile.html', form=form)

@app.route('/company_register', methods=['GET', 'POST'])
@login_required
def company_register():
    form = CompanyRegistrationForm()
    if form.validate_on_submit():
        new_company = Company(
            name=form.name.data,
            domain=form.domain.data,
            poc=form.poc.data
        )
        db.session.add(new_company)
        db.session.commit()
        flash('Company registered successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('company_register.html', form=form)

@app.route('/post_job', methods=['GET', 'POST'])
@login_required
def post_job():
    form = JobPostForm()
    if form.validate_on_submit():
        new_job = Job(
            role_details=form.role_details.data,
            apply_by=form.apply_by.data,
            cgpa_cutoff=form.cgpa_cutoff.data,
            accepted_branches=form.accepted_branches.data,
            ctc=form.ctc.data,
            company_id=current_user.id  # Assuming current_user is a company
        )
        db.session.add(new_job)
        db.session.commit()
        flash('Job posted successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('job_post.html', form=form)

@app.route('/analytics')
@login_required
def analytics():
    stats = generate_placement_statistics()
    return render_template('analytics.html', stats=stats)

@app.route('/track_student/<student_usn>')
@login_required
def track_student(student_usn):
    performance = track_student_performance(student_usn)
    return render_template('student_performance.html', performance=performance)

@app.route('/update_interests', methods=['GET', 'POST'])
@login_required
def update_interests():
    form = InterestForm()
    form.interests.choices = [(interest.id, interest.name) for interest in Interest.query.all()]
    if form.validate_on_submit():
        student = Student.query.get(current_user.usn)
        student.interests = [Interest.query.get(interest_id) for interest_id in form.interests.data]
        db.session.commit()
        flash('Interests updated successfully!', 'success')
        return redirect(url_for('student_profile'))
    return render_template('student_interests.html', form=form)

@app.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    form = StudentProfileForm()
    if form.validate_on_submit():
        student = Student.query.get(form.usn.data)
        student.name = form.name.data
        student.cgpa = form.cgpa.data
        student.email = form.email.data
        student.branch = form.branch.data
        student.no_of_backlogs = form.no_of_backlogs.data
        student.counselor_email = form.counselor_email.data
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('student_profile'))
    return render_template('student_profile.html', form=form)

@app.route('/apply_job/<int:job_id>', methods=['GET', 'POST'])
@login_required
def apply_job(job_id):
    form = JobApplicationForm()
    form.job_id.choices = [(job.job_id, job.role_details) for job in Job.query.all()]
    if form.validate_on_submit():
        placement_status = PlacementStatus(student_usn=current_user.usn, company_id=job_id, status='Applied')
        db.session.add(placement_status)
        db.session.commit()
        send_email_notification(current_user.email, "Job Application", f"You have applied for job ID {job_id}.")
        flash('Job application submitted!', 'success')
        return redirect(url_for('student_profile'))
    return render_template('job_application.html', form=form)

def send_email_notification(student_email, subject, body):
    msg = Message(subject, recipients=[student_email])
    msg.body = body
    mail.send(msg)

@app.route('/notify_students')
def notify_students():
    students = Student.query.all()
    for student in students:
        send_email_notification(student.email, "Placement Update", "Check your placement schedule.")
        # Here you can also implement SMS notifications if needed
    return "Notifications sent!"

@app.route('/update_interview/<int:interview_id>', methods=['POST'])
@login_required
def update_interview(interview_id):
    # Logic to update interview status
    # After updating, send notification
    student_email = "student@example.com"  # Fetch from student model
    send_email_notification(student_email, "Interview Update", "Your interview status has been updated.")
    return redirect(url_for('analytics'))

@app.route('/analyze_resume', methods=['GET', 'POST'])
@login_required
def analyze_resume_route():
    form = ResumeUploadForm()
    if form.validate_on_submit():
        resume_content = form.resume_file.data.read().decode('utf-8')
        job_description = request.form.get('job_description')  # Assume this is passed in
        analysis_results = analyze_resume(resume_content, job_description)
        return render_template('resume_analysis_results.html', results=analysis_results)
    return render_template('resume_analyzer.html', form=form)

@app.route('/generate_resume', methods=['GET', 'POST'])
@login_required
def generate_resume_route():
    form = ResumeGenerationForm()
    if form.validate_on_submit():
        data = {
            'name': form.name.data,
            'email': form.email.data,
            'phone': form.phone.data,
            'education': form.education.data.split(','),
            'experience': form.experience.data.split(','),
            'skills': form.skills.data.split(',')
        }
        resume_content = generate_resume(data)
        return render_template('resume_output.html', resume_content=resume_content)
    return render_template('resume_generator.html', form=form)

@app.route('/export_report', methods=['GET'])
@login_required
def export_report():
    # Example report data (this should be generated based on actual data)
    report_data = {
        'Total Students Placed': 50,
        'Total Companies Participating': 10,
        'Total Job Roles Offered': 20,
        'Placement Success Rate': '80%',
    }

    filename = "placement_report.pdf"
    generate_pdf(report_data, filename)

    return send_file(filename, as_attachment=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Logic for user authentication
        return redirect(url_for('index'))  # Redirect to the index page after login
    return render_template('login.html', form=form)

@app.route('/placements', methods=['GET'])
@login_required
def placements():
    # Logic to retrieve and display placements
    return render_template('placements.html', placements=placements_data)

if __name__ == '__main__':
    app.run(debug=True) 