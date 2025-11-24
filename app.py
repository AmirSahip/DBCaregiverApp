from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, time
import os

app = Flask(__name__)
# Use environment variable for database URL, fallback to local for development
database_url = os.environ.get('DATABASE_URL', 'postgresql://postgres:123456@localhost:5432/caregiver_platform')
# Render provides DATABASE_URL with postgres://, but SQLAlchemy needs postgresql://
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')

db = SQLAlchemy(app)

# ========================================
# MODELS (Database Tables)
# ========================================

class User(db.Model):
    __tablename__ = 'USER'
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    given_name = db.Column(db.String(40), nullable=False)
    surname = db.Column(db.String(40), nullable=False)
    city = db.Column(db.String(100))
    phone_number = db.Column(db.String(30))
    profile_description = db.Column(db.Text)
    password = db.Column(db.String(255), nullable=False)

class Caregiver(db.Model):
    __tablename__ = 'caregiver'
    caregiver_user_id = db.Column(db.Integer, db.ForeignKey('USER.user_id'), primary_key=True)
    photo = db.Column(db.String(300))
    gender = db.Column(db.String(10))
    caregiving_type = db.Column(db.String(30), nullable=False)
    hourly_rate = db.Column(db.Numeric(10, 2), nullable=False)
    user = db.relationship('User', backref='caregiver', foreign_keys=[caregiver_user_id])

class Member(db.Model):
    __tablename__ = 'member'
    member_user_id = db.Column(db.Integer, db.ForeignKey('USER.user_id'), primary_key=True)
    house_rules = db.Column(db.Text)
    dependent_description = db.Column(db.Text)
    user = db.relationship('User', backref='member', foreign_keys=[member_user_id])

class Address(db.Model):
    __tablename__ = 'address'
    member_user_id = db.Column(db.Integer, db.ForeignKey('member.member_user_id'), primary_key=True)
    house_number = db.Column(db.String(20))
    street = db.Column(db.String(200), nullable=False)
    town = db.Column(db.String(100))

class Job(db.Model):
    __tablename__ = 'job'
    job_id = db.Column(db.Integer, primary_key=True)
    member_user_id = db.Column(db.Integer, db.ForeignKey('member.member_user_id'), nullable=False)
    required_caregiving_type = db.Column(db.String(50), nullable=False)
    other_requirements = db.Column(db.Text)
    date_posted = db.Column(db.Date, nullable=False)

class JobApplication(db.Model):
    __tablename__ = 'job_application'
    caregiver_user_id = db.Column(db.Integer, db.ForeignKey('caregiver.caregiver_user_id'), primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.job_id'), primary_key=True)
    date_applied = db.Column(db.Date, nullable=False)

class Appointment(db.Model):
    __tablename__ = 'appointment'
    appointment_id = db.Column(db.Integer, primary_key=True)
    caregiver_user_id = db.Column(db.Integer, db.ForeignKey('caregiver.caregiver_user_id'), nullable=False)
    member_user_id = db.Column(db.Integer, db.ForeignKey('member.member_user_id'), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.Time, nullable=False)
    work_hours = db.Column(db.Numeric(5, 2), nullable=False)
    status = db.Column(db.String(20), nullable=False)

# ========================================
# ROUTES
# ========================================

@app.route('/')
def index():
    return render_template('index.html')

# ========================================
# USER ROUTES
# ========================================

@app.route('/users')
def users():
    all_users = User.query.all()
    return render_template('users.html', users=all_users)

@app.route('/users/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        new_user = User(
            email=request.form['email'],
            given_name=request.form['given_name'],
            surname=request.form['surname'],
            city=request.form['city'],
            phone_number=request.form['phone_number'],
            profile_description=request.form['profile_description'],
            password=request.form['password']
        )
        db.session.add(new_user)
        db.session.commit()
        flash('User added successfully!', 'success')
        return redirect(url_for('users'))
    return render_template('user_form.html', user=None)

@app.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        user.email = request.form['email']
        user.given_name = request.form['given_name']
        user.surname = request.form['surname']
        user.city = request.form['city']
        user.phone_number = request.form['phone_number']
        user.profile_description = request.form['profile_description']
        user.password = request.form['password']
        db.session.commit()
        flash('User updated successfully!', 'success')
        return redirect(url_for('users'))
    return render_template('user_form.html', user=user)

@app.route('/users/delete/<int:user_id>')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('users'))

# ========================================
# CAREGIVER ROUTES
# ========================================

@app.route('/caregivers')
def caregivers():
    all_caregivers = db.session.query(Caregiver, User).join(User).all()
    return render_template('caregivers.html', caregivers=all_caregivers)

@app.route('/caregivers/add', methods=['GET', 'POST'])
def add_caregiver():
    if request.method == 'POST':
        new_caregiver = Caregiver(
            caregiver_user_id=request.form['caregiver_user_id'],
            photo=request.form['photo'],
            gender=request.form['gender'],
            caregiving_type=request.form['caregiving_type'],
            hourly_rate=request.form['hourly_rate']
        )
        db.session.add(new_caregiver)
        db.session.commit()
        flash('Caregiver added successfully!', 'success')
        return redirect(url_for('caregivers'))
    users = User.query.all()
    return render_template('caregiver_form.html', caregiver=None, users=users)

@app.route('/caregivers/edit/<int:caregiver_user_id>', methods=['GET', 'POST'])
def edit_caregiver(caregiver_user_id):
    caregiver = Caregiver.query.get_or_404(caregiver_user_id)
    if request.method == 'POST':
        caregiver.photo = request.form['photo']
        caregiver.gender = request.form['gender']
        caregiver.caregiving_type = request.form['caregiving_type']
        caregiver.hourly_rate = request.form['hourly_rate']
        db.session.commit()
        flash('Caregiver updated successfully!', 'success')
        return redirect(url_for('caregivers'))
    users = User.query.all()
    return render_template('caregiver_form.html', caregiver=caregiver, users=users)

@app.route('/caregivers/delete/<int:caregiver_user_id>')
def delete_caregiver(caregiver_user_id):
    caregiver = Caregiver.query.get_or_404(caregiver_user_id)
    db.session.delete(caregiver)
    db.session.commit()
    flash('Caregiver deleted successfully!', 'success')
    return redirect(url_for('caregivers'))

# ========================================
# MEMBER ROUTES
# ========================================

@app.route('/members')
def members():
    all_members = db.session.query(Member, User).join(User).all()
    return render_template('members.html', members=all_members)

@app.route('/members/add', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        new_member = Member(
            member_user_id=request.form['member_user_id'],
            house_rules=request.form['house_rules'],
            dependent_description=request.form['dependent_description']
        )
        db.session.add(new_member)
        db.session.commit()
        flash('Member added successfully!', 'success')
        return redirect(url_for('members'))
    users = User.query.all()
    return render_template('member_form.html', member=None, users=users)

@app.route('/members/edit/<int:member_user_id>', methods=['GET', 'POST'])
def edit_member(member_user_id):
    member = Member.query.get_or_404(member_user_id)
    if request.method == 'POST':
        member.house_rules = request.form['house_rules']
        member.dependent_description = request.form['dependent_description']
        db.session.commit()
        flash('Member updated successfully!', 'success')
        return redirect(url_for('members'))
    users = User.query.all()
    return render_template('member_form.html', member=member, users=users)

@app.route('/members/delete/<int:member_user_id>')
def delete_member(member_user_id):
    member = Member.query.get_or_404(member_user_id)
    db.session.delete(member)
    db.session.commit()
    flash('Member deleted successfully!', 'success')
    return redirect(url_for('members'))

# ========================================
# ADDRESS ROUTES
# ========================================

@app.route('/addresses')
def addresses():
    all_addresses = db.session.query(Address, Member, User).join(
        Member, Address.member_user_id == Member.member_user_id
    ).join(
        User, Member.member_user_id == User.user_id
    ).all()
    return render_template('addresses.html', addresses=all_addresses)

@app.route('/addresses/add', methods=['GET', 'POST'])
def add_address():
    if request.method == 'POST':
        new_address = Address(
            member_user_id=request.form['member_user_id'],
            house_number=request.form['house_number'],
            street=request.form['street'],
            town=request.form['town']
        )
        db.session.add(new_address)
        db.session.commit()
        flash('Address added successfully!', 'success')
        return redirect(url_for('addresses'))
    members = Member.query.all()
    return render_template('address_form.html', address=None, members=members)

@app.route('/addresses/edit/<int:member_user_id>', methods=['GET', 'POST'])
def edit_address(member_user_id):
    address = Address.query.get_or_404(member_user_id)
    if request.method == 'POST':
        address.house_number = request.form['house_number']
        address.street = request.form['street']
        address.town = request.form['town']
        db.session.commit()
        flash('Address updated successfully!', 'success')
        return redirect(url_for('addresses'))
    members = Member.query.all()
    return render_template('address_form.html', address=address, members=members)

@app.route('/addresses/delete/<int:member_user_id>')
def delete_address(member_user_id):
    address = Address.query.get_or_404(member_user_id)
    db.session.delete(address)
    db.session.commit()
    flash('Address deleted successfully!', 'success')
    return redirect(url_for('addresses'))

# ========================================
# JOB ROUTES
# ========================================

@app.route('/jobs')
def jobs():
    all_jobs = db.session.query(Job, Member, User).join(
        Member, Job.member_user_id == Member.member_user_id
    ).join(
        User, Member.member_user_id == User.user_id
    ).all()
    return render_template('jobs.html', jobs=all_jobs)

@app.route('/jobs/add', methods=['GET', 'POST'])
def add_job():
    if request.method == 'POST':
        new_job = Job(
            member_user_id=request.form['member_user_id'],
            required_caregiving_type=request.form['required_caregiving_type'],
            other_requirements=request.form['other_requirements'],
            date_posted=datetime.strptime(request.form['date_posted'], '%Y-%m-%d').date()
        )
        db.session.add(new_job)
        db.session.commit()
        flash('Job added successfully!', 'success')
        return redirect(url_for('jobs'))
    members = Member.query.all()
    return render_template('job_form.html', job=None, members=members)

@app.route('/jobs/edit/<int:job_id>', methods=['GET', 'POST'])
def edit_job(job_id):
    job = Job.query.get_or_404(job_id)
    if request.method == 'POST':
        job.member_user_id = request.form['member_user_id']
        job.required_caregiving_type = request.form['required_caregiving_type']
        job.other_requirements = request.form['other_requirements']
        job.date_posted = datetime.strptime(request.form['date_posted'], '%Y-%m-%d').date()
        db.session.commit()
        flash('Job updated successfully!', 'success')
        return redirect(url_for('jobs'))
    members = Member.query.all()
    return render_template('job_form.html', job=job, members=members)

@app.route('/jobs/delete/<int:job_id>')
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    flash('Job deleted successfully!', 'success')
    return redirect(url_for('jobs'))

# ========================================
# JOB APPLICATION ROUTES
# ========================================

@app.route('/applications')
def applications():
    all_applications = db.session.query(JobApplication, Job, Caregiver, User).join(
        Job, JobApplication.job_id == Job.job_id
    ).join(
        Caregiver, JobApplication.caregiver_user_id == Caregiver.caregiver_user_id
    ).join(
        User, Caregiver.caregiver_user_id == User.user_id
    ).all()
    return render_template('applications.html', applications=all_applications)

@app.route('/applications/add', methods=['GET', 'POST'])
def add_application():
    if request.method == 'POST':
        new_application = JobApplication(
            caregiver_user_id=request.form['caregiver_user_id'],
            job_id=request.form['job_id'],
            date_applied=datetime.strptime(request.form['date_applied'], '%Y-%m-%d').date()
        )
        db.session.add(new_application)
        db.session.commit()
        flash('Application added successfully!', 'success')
        return redirect(url_for('applications'))
    caregivers = Caregiver.query.all()
    jobs = Job.query.all()
    return render_template('application_form.html', application=None, caregivers=caregivers, jobs=jobs)

@app.route('/applications/delete/<int:caregiver_user_id>/<int:job_id>')
def delete_application(caregiver_user_id, job_id):
    application = JobApplication.query.get_or_404((caregiver_user_id, job_id))
    db.session.delete(application)
    db.session.commit()
    flash('Application deleted successfully!', 'success')
    return redirect(url_for('applications'))

# ========================================
# APPOINTMENT ROUTES
# ========================================

@app.route('/appointments')
def appointments():
    all_appointments = db.session.query(Appointment, Caregiver, Member, User).join(
        Caregiver, Appointment.caregiver_user_id == Caregiver.caregiver_user_id
    ).join(
        Member, Appointment.member_user_id == Member.member_user_id
    ).join(
        User, Member.member_user_id == User.user_id
    ).all()
    return render_template('appointments.html', appointments=all_appointments)

@app.route('/appointments/add', methods=['GET', 'POST'])
def add_appointment():
    if request.method == 'POST':
        new_appointment = Appointment(
            caregiver_user_id=request.form['caregiver_user_id'],
            member_user_id=request.form['member_user_id'],
            appointment_date=datetime.strptime(request.form['appointment_date'], '%Y-%m-%d').date(),
            appointment_time=datetime.strptime(request.form['appointment_time'], '%H:%M').time(),
            work_hours=request.form['work_hours'],
            status=request.form['status']
        )
        db.session.add(new_appointment)
        db.session.commit()
        flash('Appointment added successfully!', 'success')
        return redirect(url_for('appointments'))
    caregivers = Caregiver.query.all()
    members = Member.query.all()
    return render_template('appointment_form.html', appointment=None, caregivers=caregivers, members=members)

@app.route('/appointments/edit/<int:appointment_id>', methods=['GET', 'POST'])
def edit_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    if request.method == 'POST':
        appointment.caregiver_user_id = request.form['caregiver_user_id']
        appointment.member_user_id = request.form['member_user_id']
        appointment.appointment_date = datetime.strptime(request.form['appointment_date'], '%Y-%m-%d').date()
        appointment.appointment_time = datetime.strptime(request.form['appointment_time'], '%H:%M').time()
        appointment.work_hours = request.form['work_hours']
        appointment.status = request.form['status']
        db.session.commit()
        flash('Appointment updated successfully!', 'success')
        return redirect(url_for('appointments'))
    caregivers = Caregiver.query.all()
    members = Member.query.all()
    return render_template('appointment_form.html', appointment=appointment, caregivers=caregivers, members=members)

@app.route('/appointments/delete/<int:appointment_id>')
def delete_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    db.session.delete(appointment)
    db.session.commit()
    flash('Appointment deleted successfully!', 'success')
    return redirect(url_for('appointments'))

# ========================================
# RUN APP
# ========================================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
