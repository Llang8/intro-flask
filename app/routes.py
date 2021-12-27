from flask.helpers import url_for
from app import app, db
from flask import render_template, request, flash, redirect, url_for
from app.models import User, Post
from flask_login import login_user, logout_user, current_user

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = User.query.filter_by(email = request.form.get('email')).first()

        if u is not None and u.check_password(request.form.get('password')):
            login_user(u)
            flash('You have logged in successfully', 'success')
            return redirect(url_for('home'))
        else:
            flash('Either the user doesnt exist of the password was incorrect', 'danger')
            return redirect(request.referrer)

    return render_template('login.html')

@app.route("/logout")
def logout():
    logout_user()
    flash('User logged out successfully', 'info')
    return redirect(url_for('login'))

@app.route("/register", methods=["GET", 'POST'])
def register():
    if request.method == 'POST':
        if User.query.filter_by(email=request.form.get('email')).first() is not None:
            flash('That email alredy belongs to a user. Try again.', 'warning')
            return redirect(request.referrer)

        if request.form.get('password') != request.form.get('confirm_password'):
            flash('Your passwoords dont match, please try again.', 'warning')
            return redirect(request.referrer)


        u = User(
            first_name = request.form.get('first_name'),
            last_name = request.form.get('last_name'),
            email = request.form.get('email'),
            password = request.form.get('password')
        )
        u.generate_password(u.password)
        db.session.add(u)
        db.session.commit()
        flash('User created successfully', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route("/profile", methods=['GET', 'POST'])
def profile():
    u = User.query.get(current_user.get_id())

    context = {
        "posts": Post.query.filter_by(user_id=current_user.get_id()).all()
    }

    if request.method =='POST':
        f_name = request.form.get('f_name')
        l_name = request.form.get('l_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        u.first_name = f_name
        u.last_name = l_name
        u.email = email

        if not password and not confirm_password:

            db.session.commit()
            flash('User info udated successfully', 'success')
            return redirect(request.referrer)

        else:
            if password == confirm_password:

                u.generate_password(password)
                db.session.commit()
                flash('Password updated successfully', 'success')
                return redirect(request.referrer)
            else:
                flash('Your passwords dont match try again', 'warning')
                return redirect(request.referrer)

    return render_template('profile.html', **context)