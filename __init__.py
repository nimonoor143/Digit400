from flask import Flask, render_template, flash, url_for, redirect, request, session
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
import gc
import os
from functools import wraps
from content_management import Content
from db_connect import connection

app = Flask(__name__)

# CMS Structure: Title, Path, Message 
APP_CONTENT = {
    "Home":[["Welcome", "/welcome/", "Welcome to my app you can do many things here!"],
           ["Background", "/background/", "We had alot of fun building this app. Learn more abour our story."]
           ["Messages", "/messages/","Get your messages from the community!"],],
    "Profile":[["User Profile", "/profile/", "Edit your profile here."],
               ["Terms of Service","/tos/", "The Legal stuff"],
              ["Photo Upload","/photo/","Upload your photo"]],
    "Contact":[["Contact Us", "/contact/","Get in touch! We'd love to hear from you!"],],
}

# Login Required Decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("Please login.")
            return redirect(url_for('login_page'))

    return wrap

# MAIN

@app.route("/")
def main():
    try:
        return render_template("main.html")
    except Exception as e:
        return render_template("500.htnl", error = e)
    
# Dashboard

@app.route("/dashboard/")
def dashboard():
    try:
        return render_template("dashboard.html", APP_CONTENT = APP_CONTENT)
    except Exception as e:
        return render_template("500.htnl", error = e)

# login

@app.route("/login/", methods = ["GET", "POST"])
def login():
    error = ""
    try:
        c, conn = connection()
    
        if request.method == "POST":
            entered_username = request.form['username']
            entered_password = request.form['password']
            
            if entered_username == "demo" and entered_password == "demo":
                flash("Howdy, " + entered_username)
                return redirect(url_for("dashboard"))     
            
            else: 
                data = c.execute("SELECT * FROM users WHERE username = ('{0}')" .format(thwart(request.form['username'])))

                data = c.fetchone()[2]

                if sha256_crypt.verify(request.form['password'], data):
                    session['logged_in'] = True
                    session['username'] = request.form['username']

                    flash("You are now logged in" + session['username'])
                    return redirect(url_for("dashboard"))
                else:
                    error = "Invalid Credentials. Please Try Again."
        else:
            return render_template("login.html", error = error)

    except Exception as e:
        flash(e)
        return render_template("login.html", error = error)
    
# Class Registration Form

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice', [validators.Required()])

# Register Page
@app.route('/register/', methods=["GET","POST"])
def register_page():
    try:
        form = RegistrationForm(request.form)

        if request.method == "POST" and form.validate():
            username  = form.username.data
            email = form.email.data
            password = sha256_crypt.encrypt((str(form.password.data)))
            c, conn = connection()

            x = c.execute("SELECT * FROM users WHERE username = ('{0}')".format(thwart(username)))

            if int(x) > 0:
                flash("That username is already taken, please choose another.")
                return render_template('register.html', form = form)

            else:
                c.execute("INSERT INTO users (username, password, email, tracking) VALUES ('{0}','{1}','{2}','{3}')".format(thwart(username), thwart(password), thwart(email), thwart("/dashboard/")))

                conn.commit()
                flash("Thanks for registering!")
                c.close()
                conn.close()
                gc.collect()

                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for('dashboard'))

        return render_template("register.html", form = form)

    except Exception as e:
        return(str(e))

# Logout 
@app.route("/logout/")
@login_required
def logout ():
    seesion.clear()
    flash("You have been logged out")
    gc.colloect()
    return redirect(url_for("main"))



@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.errorhandler(405)
def page_not_found(e):
    return render_template("405.html")

@app.errorhandler(500)
def int_server_error(e):
    return render_template("500.html", error = e)

if __name__ == "__main__":
	app.run()

