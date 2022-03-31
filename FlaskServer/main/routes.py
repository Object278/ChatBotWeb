from flask import render_template, request, Blueprint
from FlaskServer.model import Post

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    #使用Post.query.paginate方法给posts分页
    #使用时间排序posts，让新发表的在最上面
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5)
    return render_template('home.html', posts=posts)

@main.route('/about')
def about():
    return render_template('about.html')