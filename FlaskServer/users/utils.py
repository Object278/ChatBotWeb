import os
import secrets
from PIL import Image
from flask import url_for, flash, current_app
from flask_mail import Message
from FlaskServer import mail

def save_picture(form_picture):
    #替换图片名字
    random_hex = secrets.token_hex(8)
    #不需要f_name，只取拓展名
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    #合成最终路径
    picture_path  = os.path.join(current_app.root_path, 'static//profile_pics', picture_fn)
    #resize Image来节省空间
    output_size = (125, 125)
    image = Image.open(form_picture)
    image.thumbnail(output_size)
    image.save(picture_path)
    #仍需更新数据库中的图片名
    #还可以在user更新图片之后删除原本的图片
    return picture_fn

def send_reset_email(user):
    flash('Currently you can not reset password., because it is not implemented.', 'info')
    return
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then ignore this email and no change will be done.
    '''
    mail.send(msg)