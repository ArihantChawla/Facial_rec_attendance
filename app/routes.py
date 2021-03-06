from app import APP,db
from flask import render_template,flash,Flask, jsonify, request, redirect,url_for
from app.forms import LoginForm,RegistrationForm,ResetPasswordRequestForm,ResetPasswordForm,EditProfileForm,ChangePWDForm,CheckAttendanceForm
import face_recognition
import os
from werkzeug.urls import url_parse
from flask_login import current_user, login_user,logout_user,login_required
from app.models import User,Student,Course,TA,Prof
from app.email import send_password_reset_email

@APP.route('/Home_TA')
@login_required
def TAhome(username):
	if current_user.is_authenticated is False:
		flash("Error login first")
		return redirect(url_for('loginTA'))

	return render_template('Home_TA.html')

@APP.route('/Home_stud')
@login_required
def studhome(username):
	if current_user.is_authenticated is False:
		flash("Error login first")
		return redirect(url_for('loginstud'))

	return render_template('Home_stud.html')

@APP.route('/Home_prof')
@login_required
def profhome(username):
	if current_user.is_authenticated is False:
		flash("Error login first")
		return redirect(url_for('loginprof'))
	return render_template('Home_prof.html')

@APP.route('/login_TA',methods={'GET','POST'})
def loginTA():
	if current_user.is_authenticated:
		return redirect(url_for('TAhome'))
	form = LoginForm()
	if form.validate_on_submit():
		user = TA.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('loginTA'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		
		return redirect(next_page)
		
	return render_template('login.html', title='Sign In', form=form)

@APP.route('/login_faculty',methods={'GET','POST'})
def loginprof():
	if current_user.is_authenticated:
		return redirect(url_for('profhome'))
	form = LoginForm()
	if form.validate_on_submit():
		user = Prof.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('loginprof'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		
		return redirect(next_page)
		
	return render_template('login.html', title='Sign In', form=form)

@APP.route('/login_stud',methods={'GET','POST'})
def loginstud():
	if current_user.is_authenticated:
		return redirect(url_for('studhome'))
	form = LoginForm()
	if form.validate_on_submit():
		user = Student.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('loginstud'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		
		return redirect(next_page)
		
	return render_template('login.html', title='Sign In', form=form)

@APP.route('/login',methods={'GET','POST'})
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		
		return redirect(next_page)
		
	return render_template('login.html', title='Sign In', form=form)

@APP.route('/user/<username>')
@login_required
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	return render_template('user.html', user=user)

@APP.route('/index')
@APP.route('/')
@login_required
def index():
	return render_template('index.html', title='Home')

@APP.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm(current_user)
	if form.validate_on_submit():
		current_user.email = form.email.data
		current_user.fname = form.fname.data
		current_user.lname = form.lname.data
		db.session.commit()
		flash('Your changes have been saved.')
		return redirect(url_for('edit_profile'))

	elif request.method == 'GET':
		form.email.data = current_user.email
		form.fname.data = current_user.fname
		form.lname.data = current_user.lname
	return render_template('edit_profile.html', title='Edit Profile',form=form)	


@APP.route('/change_password', methods=['GET','POST'])
@login_required
def change_password():
	form = ChangePWDForm()
	if request.method == 'POST':
		if form.validate_on_submit(): 
			if current_user.check_password(form.currentpassword.data):
				current_user.set_password(form.newpassword.data)
				db.session.commit()
				flash('Your changes have been saved.')
				return redirect(url_for('index'))
			else :
				flash('Old password incorrect')
			return redirect(url_for('change_password'))
	return render_template('change_password.html', title='Change Password',form=form)	

@APP.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@APP.route('/register',methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data, fname=form.fname.data, lname=form.lname.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Congratulations, you are now a registered user!')
		return redirect(url_for('loginprof'))
	return render_template('register.html', title='Register', form=form)

@APP.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = ResetPasswordRequestForm()
	if form.validate_on_submit():
		#method = form.choice.data
		#if(method == "username"):
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			send_password_reset_email(user,user.email)
			flash('Check your email for the instructions to reset your password')
			return redirect(url_for('loginprof'))
		else:
			flash('Error couldnot send email as User not registered or no email entered for this user')
			return redirect(url_for('reset_password_request'))

	return render_template('reset_password_request.html',title='Reset Password', form=form)

@APP.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	user = User.verify_reset_password_token(token)
	if not user:
		return redirect(url_for('index'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		user.set_password(form.password.data)
		db.session.commit()
		flash('Your password has been reset.')
		return redirect(url_for('loginprof'))
	return render_template('reset_password.html', form=form)


@APP.route('/check_attendance',methods=['GET','POST'])
@login_required
def checkattd():
	form =CheckAttendanceForm()
	if form.validate_on_submit():
		course = form.courseID.data
		attd = db.session.query(Attendance).join(Course).join(Student).join(Prof).join(TA).filter(Course.c.Course_ID == course)
		if attd is False:
			flash('Incorrect course code')
			return redirect(url_for('checkattd'))

	return render_template('check_attendance.html',form=form)


def allowed_file(filename):
	ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@APP.route('/faces', methods=['GET', 'POST'])
@login_required
def upload_image():

	if request.method == 'POST':
		if 'file' not in request.files:
			flash("not got file ")
			return redirect(request.url)

		file = request.files['file']

		if file.filename == '':
			flash("no file selected")
			return redirect(request.url)

		if file and allowed_file(file.filename):
			return detect_faces_in_image(file)

	return render_template("face_rec.html",title="Hello")


def detect_faces_in_image(file_stream):
	known_dir = "/home/agrim/known"

	known_encodings = []
	for img in os.listdir(known_dir):
		img_dat = face_recognition.load_image_file(known_dir+'/'+img)
		known_encodings.append(face_recognition.face_encodings(img_dat)[0])

	un_img = face_recognition.load_image_file(file_stream)
	unknown_face_encodings = face_recognition.face_encodings(un_img)

	face_found = False
	is_obama = False

	if len(unknown_face_encodings) > 0:
		face_found = True
		for encodings in known_encodings:

			match_results = face_recognition.compare_faces([encodings], unknown_face_encodings[0])
			if match_results[0]:
				is_obama = True

				result = {
					"face_found_in_image": face_found,
					"is_picture_of_obama": is_obama
					}
				return jsonify(result)
				break
	result = {
			"face_found_in_image": face_found,
			"is_picture_of_obama": is_obama
		}

	return jsonify(result)