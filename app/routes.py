'''
Minerals: Nafiyu Murtaza, Ben Rudinski, Chloe Wong, Vedant Kothari
SoftDev
P00: Move Slowly and Fix Things
2024-10-31
Time Spent: 1.5
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
            flash("You have logged in successfully!", 'success')
            return redirect(url_for('home'))
        else:
            flash("Login unsuccessful. Check your username and password.", 'danger') # lol not actually dangerous but type of message
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
           flash("Username already exists. Please choose a different one!", 'warning')
           return redirect(url_for('register')) # take themm right back
       
       # hash pswd and add usr to db
       hashed_password = generate_password_hash(password, 'sha256') # special algorithm SHA
       new_user = User(username=username, password=hashed_password)
       db.session.add(new_user)
       db.session.commit() # create this session

       flash("Account created! You can log in now!", 'success')
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
    flash("You have been logged out. Hope to see you back soon!", 'info')
    return redirect(url_for('main'))

# route for creating new blog post
@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    if request.method == 'POST':
        category = request.form.get('category')
        article = request.form.get('article')
        
        # create new post with current user as author
        new_post = BlogPost(category=category, article=article, author_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()

        flask("Success! Your new blog post has been created!", 'success')
        return redirect(url_for('home'))
    return render_template('post.html') #some1 need to code this

# route for viewing blog posts by category
@app.route('/category/<category_name>')
def view_category():
    # query all posts w specific category
    posts = BlogPost.query.filter_by(category=category_name).all()
    
    return render_template('category.html', posts=posts, category=category_name)

# route for editing blog post
@app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = BlogPost.query.get_or_404(post_id) # or 404 holds error in case
    
    # makje sure current user is author of post
    if post_author_id != current_user.id:
        flash("Sorry but you do not have permission to edit this post!", 'danger')
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        post.category = request.form.get('category')
        post.article = request.form.get('article')

        db.session.commit()

        flash("Your blog post has been successfully edited! Nice work!", 'success')
        return redirect(url_for('view_category', category_name=post.category))

    return render_template('edit_post.html', post=post)

# route for deleting post
@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login.required
def delete_post(post_id):
    post = BlogPost.query.get_or_404(post_id)

    # makje sure current user is author of post
    if post_author_id != current_user.id:
        flash("Sorry but you do not have permission to edit this post!", 'danger')
        return redirect(url_for('home'))
    
    db.session.delete()
    db.session.commit() # commit and delete post :(

    flash("Your blog post has unfortunately been deleted.", 'info')
    return redirect(url_for('home'))














