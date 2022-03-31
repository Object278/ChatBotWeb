#当model和app在同一个文件夹下的时候
#如果在model里import app里的db，再在app中引用model里的User和Post，会导致circular import
#会在User的import中报错，提示无法import User
#原因：1.直接python执行app.py的时候，python把app.py重命名为__main__
#然后，它开始从上往下执行，到达from model import User, Post的时候，它开始执行整个model
#文件，而不只是被import的部分。在执行到model里的from app import db的时候，你可能以为会
#无法引入db，因为db的定义在__main__里还没有执行，但是其实python它并没有看到过
#app这个名字的文件，因为它第一次执行的时候把app重命名__main__了，然后它开始再一次从头执行
#app这个文件，在执行到from model import User, Post的时候，它已经看到了model这个文件，
#所以from model通过了。
#但是仍未执行model这个文件里面User和Post的定义，所以在import User这里第一次报错了
#当把model文件里的import改为from __main__ import db的话，按照目前的代码布局，
#执行到这一行的时候它看到了__main__，所以from通过了，但是之后import db不能执行
#因为db的定义还没有被执行
#解决方法是不直接执行app.py，把整个应用包装为一个package，让import更简单
#方法：在当前文件夹下创建同名（FLASKSERVER）文件夹，里面创建__init__.py
#from model import User, Post

#这里从FlaskServer的Package的__init__.py引入app
from FlaskServer import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)