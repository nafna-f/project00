from flask import render_template, redirect, url_for, flask, request
from app import app, db
from app.models import User, BlogPost

# main page route 
@app.route('/')
def main():
    return render_template('main.html') # someone still need to code this lol

# login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    #if form is submitted via post
    if request.method == 'POST':
        pass # check login credentials would go here
    return render_template('login.html') # someone still need to code this lol

# registration page to create an account
@app.route('/register', methods=['GET', 'POST'])
def register():
    # if form submitted via post
    if request.method == 'POST':
        pass  # check login credentials would go here
    return render_template('register.html') #  someone still need to code this lol

# home page :D
@app.route('/home')
def home():
    return render_template('home.html') #  someone still need to code this lol