'''
Minerals: Nafiyu Murtaza, Ben Rudinski, Chloe Wong, Vedant Kothari
SoftDev
P00: Move Slowly and Fix Things
2024-10-31
Time Spent: 1.9
'''

from flask import render_template, redirect, url_for, flash, request, session
from app import app
from app.models import User, BlogPost
from functools import wraps

# Custom login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Main page route
@app.route('/')
def main():
    return render_template('main.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.get_by_username(username)

        if user:
            print("User found, verifying password...")  # Debug output
            if user.verify_password(user.password, password):
                session['user_id'] = user.id
                flash("Login successful!", "success")
                return redirect(url_for('home'))
            else:
                print("Password verification failed.")  # Debug output
                flash("Invalid username or password.", "danger")
        else:
            print("User not found.")  # Debug output
            flash("Invalid username or password.", "danger")
    return render_template('login.html')


# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
       username = request.form.get('username')
       password = request.form.get('password')
       if User.get_by_username(username):
           flash("Username already exists. Please choose a different one!", 'warning')
           return redirect(url_for('register'))
       User.create(username, password)
       flash("Account created! You can log in now!", 'success')
       return redirect(url_for('login'))
    return render_template('register.html')

# Home route (requires login)
@app.route('/home')
@login_required
def home():
    user_id = session.get('user_id')
    user = User.get_by_id(user_id) if user_id else None
    return render_template('home.html', current_user=user)

# Logout route
@app.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    flash("You have been logged out. Hope to see you back soon!", 'info')
    return redirect(url_for('main'))

# Route for creating new blog post
@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    if request.method == 'POST':
        category = request.form.get('category')
        article = request.form.get('article')
        BlogPost.create(category=category, article=article, author_id=session.get('user_id'))
        flash("Success! Your new blog post has been created!", 'success')
        return redirect(url_for('home'))
    return render_template('post.html')

# route for viewing blog posts by category
@app.route('/category/<category_name>')
def view_category(category_name):
    # query all posts w specific category
    posts = BlogPost.get_by_category(category_name)

    return render_template('category.html', posts=posts, category=category_name)

# route for editing blog post
@app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
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
@login_required
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
