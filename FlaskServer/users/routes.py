from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from FlaskServer import db
from werkzeug import security
from FlaskServer.model import User, Post
from FlaskServer.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm, 
                                    RequestResetForm, ResetPasswordForm)
from FlaskServer.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        #返回hash后的password字符串
        hashed_password = security.generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        #防止用户注册时使用已经存在的用户名和邮箱，因为这两项已经标注了不可重复在数据库里
        #所以添加重复用户的时候数据库会报错，需要处理一下，较好的处理方式是在forms文件里
        #定义自己的validation规则防止重复，这样可以轻松展示出哪里有问题
        db.session.add(user)
        db.session.commit()
        
        #需要更新layout.html来让flash信息能够出现在任何界面上
        flash(f'Account created for {form.username.data}! You are now able to log in', 'success')
        #使用url_for找到当前文件的home函数，之后redirect到home页面
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        #如果User存在并且数据库中password的hash可以对应到输入的password，则登录
        if user and security.check_password_hash(user.password, form.password.data):
            login_user(user, form.remember.data)
            #登录后尝试获取next参数，代表用户接下来想访问的页面，如果没有返回None（使用get方法）
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route("/logout")
def logout():
    #由于调用这个函数的就是要logout的user所以不需要传参
    logout_user()
    return redirect(url_for('main.home'))

#account界面只有登录之后才能看到，学习如何限制页面访问
@users.route("/account", methods=['GET', 'POST'])
#现在LoginManager知道需要login才能访问account，但是还需要告诉它login页面的route是什么
@login_required
def account():
    form = UpdateAccountForm()
    #使用post请求
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        #这里相当于update了数据库，所以需要commit
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('users.account'))
    #使用get请求，并且默认在form里填入当前的username和email
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    #数据库中当前用户的image_file时有默认值的，所以一定能取得一个图片
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


#展示某个User的所有Post
@users.route("/user/<string:username>")
def user_post(username):
    #使用Post.query.paginate方法给posts分页
    #使用时间排序posts，让新发表的在最上面
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(per_page=5)
    return render_template('user_post.html', posts=posts, user=user)

@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    #确保在reset password之前已经logout
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your Password', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    #确保在reset password之前已经logout
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        #返回hash后的password字符串
        hashed_password = security.generate_password_hash(form.password.data)
        #防止用户注册时使用已经存在的用户名和邮箱，因为这两项已经标注了不可重复在数据库里
        #所以添加重复用户的时候数据库会报错，需要处理一下，较好的处理方式是在forms文件里
        #定义自己的validation规则防止重复，这样可以轻松展示出哪里有问题
        user.password = hashed_password
        db.session.commit()
        
        #需要更新layout.html来让flash信息能够出现在任何界面上
        flash(f'Password updated for {form.username.data}! You are now able to log in', 'success')
        #使用url_for找到当前文件的home函数，之后redirect到home页面
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
