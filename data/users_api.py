import flask
from . import db_session
from .user import User

blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/students/<st>')
def get_students(st):
    db_sess = db_session.create_session()
    data = st.split(', ')
    data = list(map(int, data))
    students = db_sess.query(User).filter(User.id.in_(data))

    return flask.jsonify(
        {
            'students':
                [item.to_dict(only=('name', 'surname', 'email'))
                 for item in students]
        }
    )
