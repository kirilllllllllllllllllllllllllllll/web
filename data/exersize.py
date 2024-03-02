import sqlalchemy
from .db_session import SqlAlchemyBase

class Exercise(SqlAlchemyBase):
    __tablename__ = 'exersize'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)

    teacher = sqlalchemy.Column(sqlalchemy.String)
    
    students = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    content = sqlalchemy.Column(sqlalchemy.String)

    right_answer = sqlalchemy.Column(sqlalchemy.String)

    results = sqlalchemy.Column(sqlalchemy.String)

    name_teacher = sqlalchemy.Column(sqlalchemy.String)

    surname_teacher = sqlalchemy.Column(sqlalchemy.String)

    file = sqlalchemy.Column(sqlalchemy.String, nullable=True)
