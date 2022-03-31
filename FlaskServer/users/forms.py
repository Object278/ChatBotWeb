from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from FlaskServer.model import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=1, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        #User是继承了db.model的类，所以有query来寻找是否已经存在同名用户，不存在的话first返回None
        user = User.query.filter_by(username=username.data).first()
        if  user:
            raise ValidationError('That username is taken.')

    #用于查找email是否存在
    def validate_email(self, email):
        #User是继承了db.model的类，所以有query来寻找是否已经存在同名用户，不存在的话first返回None
        user = User.query.filter_by(email=email.data).first()
        if  user:
            raise ValidationError('That email is taken.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=1, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')
    #由于用户可能不更新自己的用户名和邮箱，所以有可能上传上来的用户名和以前一样
    #这样的话这里的validation会检测到错误，因为用户名和之前的重复了
    #因此需要让这两个检测仅在用户更改了当前内容的时候运行
    def validate_username(self, username):
        if username.data != current_user.username:
            #User是继承了db.model的类，所以有query来寻找是否已经存在同名用户，不存在的话first返回None
            user = User.query.filter_by(username=username.data).first()
            if  user:
                raise ValidationError('That username is taken.')

    def validate_email(self, email):
        if email.data != current_user.email:
        #User是继承了db.model的类，所以有query来寻找是否已经存在同名用户，不存在的话first返回None
            user = User.query.filter_by(email=email.data).first()
            if  user:
                raise ValidationError('That email is taken.')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])

    submit = SubmitField('Request Password Reset')

    #用于查找email是否不存在
    def validate_email(self, email):
        #User是继承了db.model的类，所以有query来寻找是否已经存在同名用户，不存在的话first返回None
        user = User.query.filter_by(email=email.data).first()
        if  None:
            raise ValidationError('There is no account with that email. You must register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
