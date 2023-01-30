# Blueprint since we want to register users as a blueprint in __init__.py file
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from portfoliowebsite import db
from portfoliowebsite.models import User, BlogPost
from portfoliowebsite.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from portfoliowebsite.users.picture_handler import add_profile_pic
from werkzeug.security import generate_password_hash,check_password_hash

users = Blueprint('users', __name__)


# view for registering a user
# we pass methods GET and POST since we're using our registration form here
@users.route('/register', methods=['GET','POST'])
def register():
    # Creating an instance of the registration form in user forms
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Registration Successful')
        # only after they've submitted the form do they get redirected to users.login
        return redirect(url_for('users.login'))


    # register.html is rendered first
    return render_template('register.html.j2', form=form)

# view for logging in a user
@users.route('/login', methods=['GET','POST'])
def login():
    # Create instance of the login form in user forms
    form = LoginForm()

    if form.validate_on_submit():
        # filter by the email provided to the login form
        # on registration we require every email to be unique, that's why
        # we can filter on a single email
        # we call first() so we get the string of username and not a list
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.check_password(form.password.data):

            login_user(user)
            flash('login successful')

            # if user was trying to visit a page that requires a login, we can
            # store this page in the next variable. This redirects user to that
            # page after logging in. request.args.get('next') grabs the page
            # the user was trying to access before logging in
            next = request.args.get('next')

            # next = None means they went to homepage.
            # not next[0]=='/' means next not equal to homepage, in this case
            # we set next equal to the homepage, then redirect them to next
            # so either they go to the webpage they were trying to view, or
            # they go to the homepage
            if next == None or not next[0]=='/':
                next = url_for('core.index')
            return redirect(next)

        elif user is None:
            return redirect(url_for('users.register'))

    return render_template('login.html.j2', form=form)


# view for logging out a user
@users.route('/logout')
@login_required
def logout():
    logout_user()

    # since we're using blueprints, we need to call core.index, not just index
    # index is the name of the function within core
    return redirect(url_for('users.login'))


# view to show table of users
@users.route('/view-users')
def view_users():
    print(User.query.all())
    return render_template('view_users.html.j2', values=User.query.all())



# view to show an account
@users.route('/account')
@login_required
def view_account():
    form = UpdateUserForm()
    if form.validate_on_submit():

        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data, username)
            current_user.profile_image = pic

        current_user.email = form.email.data
        db.session.commit()
        flash('User Account Updated')

        return redirect(url_for('users.view_account'))

    # User isn't submitting anything i.e. not "POST"
    elif request.method == "GET":
        form.email.data = current_user.email

    profile_image = url_for('static', filename='profile_pics/'+current_user.profile_image)

    return render_template('account.html.j2', form=form, profile_image=profile_image)


# view to show list of users blog posts
@users.route('/user_posts')
def user_posts():
    page = request.args.get('page',1,type=int)
    blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page,per_page=3)

    return render_template('view_posts.html.j2', user=current_user, blog_posts=blog_posts)
