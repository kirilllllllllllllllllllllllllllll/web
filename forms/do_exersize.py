from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired


class DoExercise(FlaskForm):
    answer = StringField('ответ:', validators=[DataRequired()])
    submit = SubmitField('Ответить')
