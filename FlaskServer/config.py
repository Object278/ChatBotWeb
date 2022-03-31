import os

class Config:
    SECRET_KEY = 'a0a163897244e7a0ce3fa50437a3a109'
    #SQLite数据库只是文件系统中的一个文件，三个斜线///代表当前文件的相对路径，数据库文件
    #会被创建在当前文件夹下
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')