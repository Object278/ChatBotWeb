from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('Titie', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

    def append_content(self, old_content, user_input, bot_output):
        return old_content + '\n' + 'You: ' + user_input + '\n' + 'Harry Potter Bot:' +bot_output