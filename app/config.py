import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'yOU-cAN_nEVER_GUess'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_PORT = os.environ.get('MAIL_PORT') or 25
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['tonnieblair12@gmail.com']
    POSTS_PER_PAGE=15
    LANGUAGES=['en', 'sw', 'es']
    TRANSLATOR_KEY=os.environ.get('TRANSLATOR_KEY') or '7160d6bd655a1ed60da5'


# def validate_username(self,username):
#         user = User.query.filter_by(username=username.data).first()
#         if user:
#            raise ValidationError('This username has already been taken. Please choose a different one')
# def validate_email(self,email):
#         user = User.query.filter_by(email=email.data).first()
#         if user:
#            raise ValidationError('This email has already been taken. Please choose a different one') 

# def validate_username(self, username):
#     user = User.query.filter_by(username = username.data )
#     if user and user!=current_user:
#         raise ValidationError('This username is registered to us. Please choose a different one!')