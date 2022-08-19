from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email
from flask_wtf import FlaskForm


class LoginForm(FlaskForm):
    """Login Form."""

    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=55)])

class RegisterForm(FlaskForm):
    """User registration form."""

    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=55)])
    email = StringField("Email", validators=[InputRequired(), Email(), Length(max=50)])
    first_name = StringField("First Name", validators=[InputRequired(), Length(max=50)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(max=30)])


class FeedBackForm(FlaskForm):
    """Add feedback form."""

    title = StringField("Title", validators=[InputRequired(), Length(max=100)])
    content = StringField("Content", validators=[InputRequired()])

class DeleteForm(FlaskForm):
    """Handled in app.py"""