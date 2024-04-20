from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField, FileField
from wtforms.validators import DataRequired


# форма для добавления домашнего задания
class AddExersize(FlaskForm):
    name = StringField('название задания', validators=[DataRequired()])
    content = TextAreaField('текст задания', validators=[DataRequired()])
    right_answer = StringField('правильный ответ', validators=[DataRequired()])
    img = FileField('изображение, если оно нужно (в формате png, jpg, jpeg)')
    submit = SubmitField('Применить')
