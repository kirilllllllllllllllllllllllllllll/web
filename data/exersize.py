import sqlalchemy
from .db_session import SqlAlchemyBase

class Exersize(SqlAlchemyBase):
    __tablename__ = 'exersize'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    teacher = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    
    students = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    file = sqlalchemy.Column(sqlalchemy.String, nullable=True)
