'''
Minerals: Nafiyu Murtaza, Ben Rudinski, Chloe Wong, Vedant Kothari
SoftDev
P00: Move Slowly and Fix Things
2024-10-31
Time Spent: 4
'''

from flask import render_template, redirect, url_for, flash, request, session
from app import app
from app.models import User, BlogPost
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def main():
    user = None
    if 'user_id' in session:
        user = User.get(session['user_id'])
    posts = BlogPost.get_all()  # Fetch all posts from the database

    # Define the order of categories
    ordered_categories = ["Politics", "Business", "Lifestyle", "Arts"]
    posts_by_category = {category: [] for category in ordered_categories}  # Initialize dictionary with ordered keys

    # Populate categories with posts
    for post in posts:
        if post.category in posts_by_category:
            posts_by_category[post.category].append(post)

    return render_template('main.html', username=user.username if user else None, posts=posts_by_category)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.get_by_username(username)
        if user and user.verify_password(user.password, password):
            session['user_id'] = user.id
            flash("Login successful!", "success")
            return redirect(url_for('main'))
        else:
            flash("Invalid username or password.", "danger")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Password validation (server-side)
        errors = []
        if password != confirm_password:
            errors.append("Passwords do not match.")
        if len(password) < 12:
            errors.append("Password must be at least 12 characters long.")
        if not any(c.islower() for c in password):
            errors.append("Password must contain at least one lowercase letter.")
        if not any(c.isupper() for c in password):
            errors.append("Password must contain at least one uppercase letter.")
        if not any(c.isdigit() for c in password):
            errors.append("Password must contain at least one number.")
        if not any(c.isalpha() for c in password):
            errors.append("Password must contain at least one letter.")

        if errors:
            for error in errors:
                flash(error, 'danger')
            return redirect(url_for('register'))

        if User.get_by_username(username):
            flash("Username already exists.", 'warning')
            return redirect(url_for('register'))

        User.create(username, password)
        flash("Account created! Log in now.", 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("You have been logged out.", 'info')
    return redirect(url_for('main'))

# Route for creating new blog post
@app.route('/post/create', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        category = request.form.get('category')
        author_id = session['user_id']  # Assume this stores the logged-in user ID

        # Create the new post
        BlogPost.create(category, title, content, author_id)

        flash("Post created successfully!", "success")
        return redirect(url_for('main'))
    
    return render_template('create_post.html')

# Route for editing a blog post
@app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = BlogPost.get(post_id)
    if post is None:
        flash("Post not found.", 'danger')
        return redirect(url_for('main'))
    if post.author_id != session['user_id']:
        flash("You can only edit your own posts.", 'danger')
        return redirect(url_for('main'))
    if request.method == 'POST':
        category = request.form.get('category')
        title = request.form.get('title')
        content = request.form.get('content')
        BlogPost.update(post_id, category, title, content)
        flash("Post updated successfully!", 'success')
        return redirect(url_for('main'))
    return render_template('edit_post.html', post=post)

# Route for deleting a blog post
@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = BlogPost.get(post_id)
    if post is None:
        flash("Post not found.", 'danger')
        return redirect(url_for('main'))
    if post.author_id == session['user_id']:
        BlogPost.delete(post_id)
        flash("Post deleted successfully.", 'info')
    else:
        flash("You can only delete your own posts.", 'danger')
    return redirect(url_for('main'))

# Search functionality
@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.args.get('query')
    if query:
        results = BlogPost.search(query)
        user = None
        if 'user_id' in session:
            user = User.get(session['user_id'])
        return render_template('search_results.html', username=user.username if user else None, posts=results, query=query)
    else:
        flash("Please enter a search term.", "warning")
        return redirect(url_for('main'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
