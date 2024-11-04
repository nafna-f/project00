'''
Minerals: Nafiyu Murtaza, Ben Rudinski, Chloe Wong, Vedant Kothari
SoftDev
P00: Move Slowly and Fix Things
2024-10-31
Time Spent: .9
'''

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
from app.models import User, BlogPost

from werkzeug.security import generate_password_hash, check_password_hash # password stuff :D

# main page route 
@app.route('/')
def main():
    return render_template('main.html') # someone still need to code this lol

# login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    #if form is submitted via post
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        # check is usr exists and password is correct
        if user and check_password_hash(user.password, password):
            login_user(user) # log user in
            flash('You have logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Check username and password.', 'danger') # lol not actually dangerous but type of message
    return render_template('login.html') # someone still need to code this lol

# registration page to create an account
@app.route('/register', methods=['GET', 'POST'])
def register():
    # if form submitted via post
    if request.method == 'POST':
       username = request.form.get('username')
       password = request.form.get('password')

       # check is username alr exists
       if User.query.filter_by(username=username).first():
           flash('Yo Username already exists. Please choose a different one!', 'warning')
           return redirect(url_for('register')) # take themm right back
       
       # hash pswd and add usr to db
       hashed_password = generate_password_hash(password, 'sha256') # special algorithm SHA
       new_user = User(username=username, password=hashed_password)
       db.session.add(new_user)
       db.session.commit() # create this session

       flash('Account created! You can log in now!', 'success')
       return redirect(url_for('login'))

    return render_template('register.html') #  someone still need to code this lol

# home page :D - requires login
@app.route('/home')
@login_required
def home():
    return render_template('home.html') #  someone still need to code this lol

# logout route - req login
@app.route('/logout')
@login_required
def logout():
    logout_user() # logs usr out
    flash('You have been logged out. Hope to see you back soon!', 'info')
    return redirect(url_for('main'))