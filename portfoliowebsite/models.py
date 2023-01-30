from portfoliowebsite import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
# Let's us check is_authenticated
from flask_login import UserMixin
import datetime

# This decorator allows Flask to load the user
# Once the user is logged in, we can show them pages specific to their user ID
@login_manager.user_loader
def load_user(user_id):
    print(User.query.get(user_id))
    print(User.query.all())
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    profile_image = db.Column(db.String(20), nullable=False, default='user-icon.svg')
    author = db.relationship('BlogPost', backref='author', lazy=True)
    password_hash = db.Column(db.String(128))

    # backref is what we call the relationship between file and user
    # The file in this case is the suitability files being uploaded

    # posts = db.relationship('File', backref='author', lazy=True)

    def __init__(self, email, password):
        self.email = email
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"Email {self.email}"

# How to create binded tables in sqlite
# db.create_all(bind=['Ratings', 'Another_Table'])
# db.create_all(bind='Ratings')
# Then sqlite3 ratings
# This lets us do .tables, and .exit and other commands since we're in that database
class Ratings(db.Model):
    __bind_key__ = 'ratings'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=False, index=True)
    security_id = db.Column(db.String(64), unique=False,index=True)
    symbol = db.Column(db.String(64), unique=False,index=True)
    description = db.Column(db.String(255), unique=False,index=True)
    risk = db.Column(db.String(64), unique=False,index=True)
    objectives = db.Column(db.String(64), unique=False,index=True)
    risk_explanation = db.Column(db.String(255), unique=False, index=True)

    def __init__(self, date, security_id, symbol, description, risk, objectives, risk_explanation):
        self.date = date
        self.security_id = security_id
        self.symbol = symbol
        self.description = description
        self.risk = risk
        self.objectives = objectives
        self.risk_explanation = risk_explanation

class BlogPost(db.Model):
    # Setup the relationship to the User table
    users = db.relationship(User)

    # Model for the Blog Posts on Website
    id = db.Column(db.Integer, primary_key=True)
    # Notice how we connect the BlogPost to a particular author
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    title = db.Column(db.String(140), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __init__(self, title, text, user_id):
        self.title = title
        self.text = text
        self.user_id =user_id


    def __repr__(self):
        return f"Post Id: {self.id} --- Date: {self.date} --- Title: {self.title}"
