from FlaskServer import db, login_manager
from datetime import datetime
from flask import current_app
from itsdangerous import TimedSerializer as Serializer
#UserMixin用于给你的数据库中的Table添加四个LoginManager需求的Attribute和Method
from flask_login import UserMixin

#用来让LoginManager能够找到用户的函数，装饰器是一种标识
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#多继承
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    #20 means the length of the username is maximal 20 chars
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    #图片之后会被hash，产生一个20个字符的String
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    #这个代表User与Post类有关联，backref的效果代表在Post中添加了一个叫author的一个Column，可以获取到
    #创建它的User的repr方法的结果，但是Post中并没有真正包含author的Column。只是一种简单方法
    # lazy为True代表可以获取一个User创建的所有Posts
    #实际上因为这个只是一个关系，所以不会真正在Table里显示出来
    #它会在Post的表里用过ForeignKey来查找这个User的所有posts
    #这里的Post大写首字母是引用Post这个类，所以是首字母大写
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    #作为类方法，验证是否相等在外部
    @staticmethod
    def verify_reset_token(token, expires_sec=900):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, max_age=expires_sec)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    #post的时间就是当前时间，传入一个获取当前时间的函数
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    #user_id是User与Post两个表关联的点
    #这里user.id为小写的原因是因为在引用user这个Table的id这一列，Table Name和Column Name自动变为小写
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"User('{self.title}', '{self.date_posted}')"
#User与Post之间有1:n的关系