from flask import render_template, url_for, flash, redirect, request, abort,Blueprint
from flask_login import current_user, login_required
from FlaskServer import db
from FlaskServer.model import Post
from FlaskServer.posts.forms import PostForm
from FlaskServer.chatbot.chat import Bot

posts = Blueprint('posts', __name__)

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content='You: ' + form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created.', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')

#创建包含变量的route，代表不同的post，post_id是数据库自动加上的int，因为它是primaryKey
#post.html展示一个post的内容，需要在home的template中加上post的link
@posts.route("/post/<int:post_id>")
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        #update Post内容，不添加新内容就不用使用add方法
        bot = Bot(0)
        bot.wakeup()
        bot_response = bot.send_message(form.content.data)
        if bot_response == 'BotError':
            flash('NOTICE: There might be an error on the bot. Please contact the administator: zli18876@gmail.com', 'danger')
        elif bot_response == 'OtherError':
            flash('NOTICE: Please wait a minute and try again. If you still get a NOTICE, Please contact the administator: zli18876@gmail.com', 'info')
        else:
            post.title = form.title.data
            post.content = form.append_content(post.content, form.content.data, bot_response)
            db.session.commit()
            #flash('Your post has been updated!', 'success')
            return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        #用户先GET请求到update这个页面，之后填完表之后POST上交，第一次GET
        #的时候把当前的内容显示进去
        #显示当前的Post内容，和修改用户信息那里一样
        form.title.data = post.title
        #form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')

#按下delete确定按钮之后，向这个方法发送POST方法，包含post_id
@posts.route("/post/<int:post_id>/delete", methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
