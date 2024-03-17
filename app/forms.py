from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User
from flask_login import current_user
from flask_babel import lazy_gettext as _l

class LoginForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators = [DataRequired()])
    remember = BooleanField(_l('Remember Me')) 
    submit = SubmitField(_l('Login'))

class RegistrationForm(LoginForm):
    username = StringField(_l('Username'), validators =[DataRequired(), Length(min=2, max=20)])
    confirm_password = PasswordField(_l('Confirm Password'), validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Register'))

           
class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators =[DataRequired(), Length(min=2, max=20)])
    about_me = StringField(_l('About me'), validators =[Length(min=0 , max=255)])
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

class PostForm(FlaskForm):
    post = TextAreaField(_l('Post'), validators=[DataRequired(), Length(min=1, max=255)])
    submit = SubmitField(_l('Submit'))

class ResetPasswordRequestForm(FlaskForm):
    email= StringField(_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Request Password Reset'))

class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Request Password Reset'))