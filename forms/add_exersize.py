from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField, FileField
from wtforms.validators import DataRequired


class AddExersize(FlaskForm):
    name = StringField('название задания', validators=[DataRequired()])
    content = TextAreaField('текст задания', validators=[DataRequired()])
    img = FileField('изображение, если оно нужно')
    submit = SubmitField('Применить')
