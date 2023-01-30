# form-based imports
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
# Let's user update jpg or png for profile pic, may not need
from flask_wtf.file import FileField, FileAllowed

# user-based imports
from flask_login import current_user
from portfoliowebsite.models import User

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    # Remember we don't save the actual password, just the hashed version.
    # It's the hashed version of the password we compare to authenticate
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords must match')])
    pass_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    # Making sure username is unique upon registration
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already')

# Lets user update email, username, and profile image
class UpdateUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    # File must be jpg or png or svg in order to be uploaded
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png', 'svg'])])
    submit = SubmitField('Update')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already')
