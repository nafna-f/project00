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

#def login_required(f):
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
    posts = BlogPost.get_all()
    
    # Sample posts for demonstration
    posts = {
    "Politics": [
        {"title": "Topher Elected President with 372 Electoral Votes", 
         "content": "In a shocking twist, Topher has won the presidency with a sweeping majority, promising a new era of unparalleled humor and wisdom."},
        {"title": "Topher Declares Every Monday a National Holiday", 
         "content": "Topher, in his latest executive order, has declared every Monday a holiday, stating 'everyone deserves a little more weekend.'"},
        {"title": "Topher's First Act: Free WiFi Nationwide", 
         "content": "As his first official act, President Topher provides free WiFi across the nation, citing internet as a 'basic human right.'"}
    ],
    "Business": [
        {"title": "Topher's Startup 'LaughCo' Valued at $1 Billion", 
         "content": "Topher's latest venture, LaughCo, has taken the business world by storm, bringing humor into every aspect of life."},
        {"title": "Topher Buys Twitter, Renames It 'TopherTalk'", 
         "content": "In a surprising move, Topher buys Twitter and rebrands it to 'TopherTalk,' promising a social media revolution."},
        {"title": "Topher Coin: The Cryptocurrency Revolution", 
         "content": "Topher launches his own cryptocurrency, 'Topher Coin,' which gains instant popularity among meme investors."}
    ],
    "Lifestyle": [
        {"title": "Topher's 10 Tips for Maximum Laziness", 
         "content": "Topher shares his expert advice on achieving ultimate relaxation, with tips on napping, binge-watching, and lounging."},
        {"title": "Why Topher Thinks Ice Cream is a Breakfast Food", 
         "content": "Topher argues the case for ice cream as a healthy and balanced breakfast option in a controversial new trend."},
        {"title": "Topher's Guide to Wearing Pajamas Everywhere", 
         "content": "In this lifestyle piece, Topher encourages everyone to embrace comfort by normalizing pajamas for all occasions."}
    ],
    "Arts": [
        {"title": "Topher Stars in Blockbuster: 'The Life of Topher'", 
         "content": "The film 'The Life of Topher' becomes an instant hit, depicting his humorous and unpredictable journey to fame."},
        {"title": "Topher's Art Gallery: Only Stick Figures Allowed", 
         "content": "Topher opens an art gallery that exclusively features stick figures, creating a new artistic movement in the process."},
        {"title": "Topher's Stand-Up Comedy Revolutionizes Modern Art", 
         "content": "Topher takes to the stage, blending stand-up comedy with performance art in a unique and laugh-inducing way."}
    ]
}



    return render_template('main.html', username=user.username if user else None, posts=posts)

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
@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    if request.method == 'POST':
        category = request.form.get('category')
        article = request.form.get('article')
        BlogPost.create(category=category, article=article, author_id=session.get('user_id'))
        flash("Success! Your new blog post has been created!", 'success')
        return redirect(url_for('main'))
    return render_template('post.html')

# route for viewing blog posts by category
@app.route('/category/<string:category_name>')
def view_category(category_name):
    posts = BlogPost.get_by_category(category_name)
    username = None
    if 'user_id' in session:
        user = User.get(session['user_id'])
        username = user.username if user else None
    return render_template('category.html', username=username, posts=posts, category_name=category_name)


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
        return redirect(url_for('main'))  # Ensure this goes to the page where all posts are displayed
    
    return render_template('create_post.html')

@app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = BlogPost.get(post_id)
    if post.author_id != session['user_id']:
        flash("You can only edit your own posts.", 'danger')
        return redirect(url_for('main'))
    if request.method == 'POST':
        post.category = request.form.get('category')
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        BlogPost.update(post_id, post.category, post.title, post.content)
        flash("Post updated successfully!", 'success')
        return redirect(url_for('main'))
    return render_template('edit_post.html', post=post)

@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = BlogPost.get(post_id)
    if post.author_id == session['user_id']:
        BlogPost.delete(post_id)
        flash("Post deleted successfully.", 'info')
    else:
        flash("You can only delete your own posts.", 'danger')
    return redirect(url_for('main'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
