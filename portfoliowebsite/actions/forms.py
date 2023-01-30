# form-based imports
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
# Let's user upload files
from flask_wtf.file import FileField, FileAllowed
import datetime


# user-based imports
from flask_login import current_user
from portfoliowebsite.models import User


class DataForm(FlaskForm):
    security_id = StringField('Security_id', validators=[DataRequired()])
    symbol = StringField('Symbol', validators=[DataRequired()])
    description =StringField('Description', validators=[DataRequired()])
    risk = StringField('Risk', validators=[DataRequired()])
    objectives = StringField('Objectives', validators=[DataRequired()])
    submit = SubmitField('Submit')

class UploadFile(FlaskForm):
    date = StringField('Date', validators=[DataRequired()], render_kw={"placeholder": "YYYY-MM-DD"})
    file = FileField('File', validators=[FileAllowed(['xls','xlsx','csv'])])
    submit = SubmitField('Upload File')

    def validate_date(form, field):
        try:
            datetime.datetime.strptime(field.data, '%Y-%m-%d')
        except ValueError:
            raise ValidationError('Incorrect date format, should be YYYY-MM-DD')

class QueryDB(FlaskForm):
    symbol = StringField('Symbol', render_kw={"placeholder": "Symbol"})
    submit = SubmitField('Submit')
