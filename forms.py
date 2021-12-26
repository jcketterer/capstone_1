from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, DateField
from wtforms.validators import DataRequired, Email, Length, Optional, InputRequired


class AddUserFrom(FlaskForm):

    username = StringField("Username", validators=[
                           InputRequired(), Length(min=1, max=20)])
    first_name = StringField("First Name", validators=[
        InputRequired(message='Please Enter First Name'), Length(max=30)])
    last_name = StringField("Last Name", validators=[
        InputRequired(message='Please Enter Last Name'), Length(max=30)])
    date_of_birth = DateField(
        "Date of Birth", format='%Y-%m-%d', validators=[InputRequired(message="Please enter you Date of Birth")])

    email = StringField("Email", validators=[
                        InputRequired(), Email(message='Please Enter A Valid Email'), Length(max=50)])
    fav_brewery = StringField("(Optional) Favorite Brewery")

    password = PasswordField("Password", validators=[
                             InputRequired(), Length(min=6, max=55)])


class LoginForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
