'''
Minerals: Nafiyu Murtaza, Ben Rudinski, Chloe Wong, Vedant Kothari
SoftDev
P00: Move Slowly and Fix Things
2024-10-31
Time Spent: 1.9
'''

from flask import render_template, redirect, url_for, flash, request, session
from flask_simplelogin import SimpleLogin, login_required as simple_login_required
from app import app
from app.models import User, BlogPost

# initialize db
with app.app_context():
    from app.models import init_db
    init_db()

# main page route
@app.route('/')
def main():
    return render_template('main.html') # someone still need to code this lol

# login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    print("Login route accessed.")  # Debug message

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Debugging messages to check form data
        print(f"Username submitted: {username}")
        print(f"Password submitted: {'*' * len(password) if password else 'No password provided'}")

        # Check if the user exists and validate password
        user = User.get_by_username(username)
        if user and user.verify_password(user.password, password):
            print("User found and password is correct.")  # Debug message
            session['user_id'] = user.id  # cookieee
            flash("Login successful!", "success")
            return redirect(url_for('home'))
        else:
            print("Invalid login attempt.")  # Debug message
            flash("Invalid username or password.", "danger")

    # Render login page with flash messages
    return render_template('login.html')

# registration page to create an account
@app.route('/register', methods=['GET', 'POST'])
def register():
    # if form submitted via post
    if request.method == 'POST':
       username = request.form.get('username')
       password = request.form.get('password')

       # check if username alr exists
       if User.get_by_username(username):
           flash("Username already exists. Please choose a different one!", 'warning')
           return redirect(url_for('register')) # take themm right back

       # hash pswd and add usr to db
       hashed_password = User.hash_password(password)
       User.create(username, hashed_password)
       flash("Account created! You can log in now!", 'success')
       return redirect(url_for('login'))

    return render_template('register.html') #  someone still need to code this lol

# home page :D - requires login
@app.route('/home')
@simple_login_required
def home():
    return render_template('home.html') #  someone still need to code this lol

# logout route - req login
@app.route('/logout')
@simple_login_required
def logout():
    session.pop('user_id', None)  # manually clear the user session
    flash("You have been logged out. Hope to see you back soon!", 'info')
    return redirect(url_for('main'))

# route for creating new blog post
@app.route('/post', methods=['GET', 'POST'])
@simple_login_required
def post():
    if request.method == 'POST':
        category = request.form.get('category')
        article = request.form.get('article')

        # create new post with current user as author
        BlogPost.create(category=category, article=article, author_id=session.get('user_id'))

        flash("Success! Your new blog post has been created!", 'success')
        return redirect(url_for('home'))
    return render_template('post.html') #some1 need to code this

# route for viewing blog posts by category
@app.route('/category/<category_name>')
def view_category(category_name):
    # query all posts w specific category
    posts = BlogPost.get_by_category(category_name)

    return render_template('category.html', posts=posts, category=category_name)

# route for editing blog post
@app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@simple_login_required
def edit_post(post_id):
    post = BlogPost.get(post_id)

    # make sure current user is author of post
    if post[3] != session.get('user_id'):  # Assuming `post[3]` is the author_id
        flash("Sorry but you do not have permission to edit this post!", 'danger')
        return redirect(url_for('home'))

    if request.method == 'POST':
        category = request.form.get('category')
        article = request.form.get('article')
        BlogPost.update(post_id, category, article)

        flash("Your blog post has been successfully edited! Nice work!", 'success')
        return redirect(url_for('view_category', category_name=category))

    return render_template('edit_post.html', post=post)

# route for deleting post
@app.route('/post/<int:post_id>/delete', methods=['POST'])
@simple_login_required
def delete_post(post_id):
    post = BlogPost.get(post_id)

    # make sure current user is author of post
    if post[3] != session.get('user_id'):  # 3 is the author_id
        flash("Sorry but you do not have permission to delete this post!", 'danger')
        return redirect(url_for('home'))

    BlogPost.delete(post_id) # delete post :(

    flash("Your blog post has unfortunately been deleted.", 'info')
    return redirect(url_for('home'))

# route to view recent posts
@app.route('/recent')
def view_recent_posts():
    posts = BlogPost.get_recent()
    return render_template('recent_posts.html', posts=posts)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
