from app import db

class User(db.Model):
    # primary key for individual identification
    id = db.Column(db.Integer, primary_key=True)

    # username column, ensures no two users can have same usrname
    username = db.Column(db.String(20), unique=True, nullable=False)

    # hashed for security
    password = db.Column(db.String(60), nullable=False)

    # relationship with BlogPosts, so we can access a users posts via 'user.posts'
    posts = db.relationship('BlogPost', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}')"

# BlogPost model for db
class BlogPost(db.Model):
    # id
    id = db.Column(db.Integer, primary_key=True)

    # category column to store category of content
    category = db.Column(db.String(100), nullable=False)

    # article to store blog contnet
    article = db.Column(db.Text, nullable=False)

    # foreign key authorid, referencing the user's id
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"BlogPost('{self.category}', '{self.article[:20]}...')"