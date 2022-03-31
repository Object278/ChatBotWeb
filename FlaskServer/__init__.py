from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from FlaskServer.config import Config
#将所有extinction Variable（db，login_manager之类的）放在create_app外
#进行初始化，不使用创建的app实例的任何信息，这样实例化出来的这些变量内部
#不存储当前应用的任何信息，让它们可以为多个应用所用。在create_app函数内部
#用init_app来进行初始化


#create_all和drop_all可以创建和删除所有数据库的文件和数据
db = SQLAlchemy()
#一个Class代表数据库中的一个表
#LoginManager在数据库中添加一些功能，在后台处理一些用户session的事情
login_manager = LoginManager()
#设置login页面的route为users文件夹中routes文件里的函数login
login_manager.login_view = 'users.login'
#改变提示用户登录才能访问account的flash message的类别为info，调整了背景颜色
login_manager.login_message_category = 'info'
#还需要修改的一点是用户没登陆时尝试访问account会被引导到login，login之后却被
#引导到home page，比较好的是login后直接进入account
#在用户没登陆时尝试访问account然后重定向到login的时候，url发生了变化，添加了
#next参数，代表之后用户想访问account，所以在login route中处理这种参数就好了
#http://localhost:5000/login?next=%2Faccount
mail = Mail()

#可以接收一个指明所有设置的类为参数
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    #import各个Blueprint的实例
    from FlaskServer.users.routes import users
    from FlaskServer.posts.routes import posts
    from FlaskServer.main.routes import main
    from FlaskServer.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    #因为routes文件中需要app这个变量先被定义，所以为了避免circular import，
    #需要把routes的import放在下面。import routes的原因是为了在运行应用的时候可以
    #找到定义的处理routes的函数

    #转换为Blueprint之后需要修改所有url_for函数的参数，因为以前的函数名现在变味了一个
    #Blueprint下的函数名，例如url_for('home')应改为url_for('main.home')
    return app
#定义了create_app函数之后因为__init__中没有app变量了，所以所有import和使用app
#变量的地方都无法使用，Flask的解决方法是有一个current_app，from flask import current_app
#使用current_app替代原来的app