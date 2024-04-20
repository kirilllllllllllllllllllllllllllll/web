from flask_wtf import FlaskForm
from wtforms import SubmitField, EmailField
from wtforms.validators import DataRequired


# форма для добавления ученика
class AddStudent(FlaskForm):
    email = EmailField('email ученика', validators=[DataRequired()])
    submit = SubmitField('Применить')
