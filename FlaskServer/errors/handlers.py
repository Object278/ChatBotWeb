from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)

#@errors.app_errorhandler可以在整个应用的层面上运行
#@errors.errorhandler只能在当前Blueprint的层面上运行
@errors.app_errorhandler(404)
def error_404(error):
    #return的render_template后面默认跟的是状态码200，这里需要改成状态码404
    return render_template('errors/404.html'), 404

@errors.app_errorhandler(403)
def error_403(error):
    #return的render_template后面默认跟的是状态码200，这里需要改成状态码404
    return render_template('errors/403.html'), 403

@errors.app_errorhandler(500)
def error_404(error):
    #return的render_template后面默认跟的是状态码200，这里需要改成状态码404
    return render_template('errors/500.html'), 500
