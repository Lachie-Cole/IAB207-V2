from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, DateTimeField, IntegerField
from wtforms.validators import InputRequired, Email, EqualTo, NumberRange
from flask_wtf.file import FileRequired, FileField, FileAllowed
from datetime import datetime

ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'}

class EventForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    genre = StringField('Genre', validators=[InputRequired()])
    artist_or_band = StringField('Artist or Band', validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired()])
    event_date = DateTimeField('Event Date', format='%Y-%m-%d %H:%M:%S',
                               validators=[InputRequired()], default=datetime.now)
    description = TextAreaField('Description', validators=[InputRequired()])
    tickets_available = IntegerField('Tickets Available',
                                     validators=[InputRequired(), NumberRange(min=1)])
    image = FileField('Event Image', validators=[
        FileRequired(message='Image cannot be empty'),
        FileAllowed(ALLOWED_FILE, message='Only supports PNG, JPG, JPEG')])
    submit = SubmitField("Create Event")

#User login
class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired('Enter user name')])
    password = PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

#User register
class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])

    #linking two fields - password should be equal to data entered in confirm
    password = PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    #submit button
    submit = SubmitField("Register")

#User comment
class CommentForm(FlaskForm):
  text = TextAreaField('Comment', [InputRequired()])
  submit = SubmitField('Create')
