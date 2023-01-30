#This file will hold a lot of our organizational logic
#Connecting the blueprints, connecting the login manager
#This file helps connect everything together.
#This helps us organize things so that when we run app.py it only has a few lines
from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Initialize Flask server
server = Flask(__name__)

# RGMP App
#from portfoliowebsite.rgmp_dash_app import init_rgmp_dashboard
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from flask import render_template_string

# Job Postings App
from portfoliowebsite.job_postings_dash_app import init_jobs_dashboard



# Initialize rgmp app
#rgmp_app = init_rgmp_dashboard(server)

# Initialize Job Postings app
jobs_app = init_jobs_dashboard(server)

server.config['SECRET_KEY'] = 'secret'
server.config['UPLOAD_FOLDER'] = 'static\\ratings_files'

# Database setup
basedir = os.path.abspath(os.path.dirname(__file__))
# Sets up the connection to the database
server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'users.db')
server.config['SQLALCHEMY_BINDS'] = {'ratings' : 'sqlite:///' + os.path.join(basedir, 'ratings.db')}
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(server)
Migrate(server,db)


# Login Configurations
login_manager = LoginManager()

# Configures application to have management of login users
#login_manager.init_app(server, rgmp_app)
login_manager.init_app(server, jobs_app)

#login_manager.init_app(server)

# In our app.py file when we're setting up views, we're going to have
# a view called login
login_manager.login_view = 'users.login'


from portfoliowebsite.core.views import core
from portfoliowebsite.error_pages.handlers import error_pages
from portfoliowebsite.users.views import users
from portfoliowebsite.actions.views import actions
from portfoliowebsite.blog_posts.views import blog_posts


server.register_blueprint(core)
server.register_blueprint(error_pages)
server.register_blueprint(users)
server.register_blueprint(actions)
server.register_blueprint(blog_posts)



app = DispatcherMiddleware(server, {
    #'/rgmp_app/': rgmp_app,
    '/jobs_app/':  jobs_app
})
