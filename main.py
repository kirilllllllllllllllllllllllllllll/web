from flask import Flask, render_template, redirect, url_for
from data import db_session, users_api
from forms.register_teacher import RegisterTeacher
from forms.login_teacher import LoginTeacher
from forms.do_exersize import DoExercise
from forms.add_student import AddStudent
from forms.add_exersize import AddExersize
from data.user import User
from data.exersize import Exercise

from requests import get

from flask_login import login_user
from flask_login import login_required
from flask_login import LoginManager
from flask_login import logout_user
from flask_login import current_user
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kirik1234pro_secret_key'
app.config['UPLOAD_FOLDER'] = os.getcwd() + "\static\img"


login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_teacher(teacher_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(teacher_id)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterTeacher()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        if form.type.data == 'учитель':
            teacher = User(
                name=form.name.data,
                surname=form.surname.data,
                email=form.email.data,
                type='учитель',
                students='0'
            )
            teacher.set_password(form.password.data)
            db_sess.add(teacher)
            db_sess.commit()
            return redirect('/login')
        elif form.type.data == 'ученик':
            student = User(
                name=form.name.data,
                surname=form.surname.data,
                email=form.email.data,
                type='ученик'
            )
            student.set_password(form.password.data)
            db_sess.add(student)
            db_sess.commit()
            return redirect('/login')
        else:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="нужно выбрать или учитель, или ученик")
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginTeacher()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            if user.type == 'учитель':
                login_user(user, remember=form.remember_me.data)
                return redirect("/teacher")
            else:
                login_user(user, remember=form.remember_me.data)
                return redirect("/student")

        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/teacher")
def teacher():
    try:
        if current_user.type != 'учитель':
            logout()
    except Exception:
        return render_template("teacher.html",
                               exercises=[])
    else:
        db_sess = db_session.create_session()
        return render_template("teacher.html", exercises=db_sess.query(Exercise).filter(Exercise.teacher == current_user.id))


@app.route("/")
def index():
    # db_sess = db_session.create_session()
    # news = db_sess.query(News).filter(News.is_private != True)
    return render_template("index.html")


@login_manager.user_loader
def load_student(student_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(student_id)


@app.route("/student")
def student():
    try:
        if current_user.type != 'ученик':
            logout()
    except Exception:
        return render_template("student.html", exercises=[])
    else:
        db_sess = db_session.create_session()
        name = str(current_user.id)
        data = db_sess.query(Exercise).all()
        data2 = []
        for i in data:
            if name in i.students:
                data2.append(i)
        print(data2)
        return render_template("student.html", exercises=data2)


@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    form = AddStudent()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user:
            if user.type == 'ученик':
                teacher = db_sess.query(User).filter(User.id == current_user.id).first()
                st = teacher.students
                if st == '0':
                    st = str(user.id)
                elif str(user.id) not in st:
                    st = st + ', ' + str(user.id)
                else:
                    return render_template('add_student.html',
                                           message="Пользователь с такой почтой уже является вашим учеником",
                                           form=form)
                teacher.students = st
                db_sess.commit()
                return redirect("/teacher")

            return render_template('add_student.html',
                                   message="Пользователь с такой почтой является учителем",
                                   form=form)

        return render_template('add_student.html',
                               message="Пользователя с такой почтой нет",
                               form=form)
    return render_template('add_student.html', title='Авторизация', form=form)


@app.route('/add_exersize', methods=['GET', 'POST'])
def add_exersize():
    form = AddExersize()
    if form.validate_on_submit():
        f = form.img.data


        if f.filename != '':

            type = f.filename.split('.')[-1]
            if type in ['jpg', 'jpeg', 'png', 'bmp']:
                exersize = Exercise(
                    name=form.name.data,
                    content=form.content.data,
                    students=current_user.students,
                    right_answer=form.right_answer.data,
                    teacher=current_user.id,
                    file='0',
                    results='0',
                    name_teacher=current_user.name,
                    surname_teacher=current_user.surname
                )
                db_sess.add(exersize)
                db_sess.commit()

                st = str(exersize.id) + '.' + type

                print(st)
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], st))
                exersize.file = st
                db_sess.commit()
            else:
                return render_template('add_exersize.html', message="Неверный формат", title='Добавление задачи', form=form)
        else:
            exersize = Exercise(
                name=form.name.data,
                content=form.content.data,
                students=current_user.students,
                right_answer=form.right_answer.data,
                teacher=current_user.id,
                file='0',
                results='0',
                name_teacher=current_user.name,
                surname_teacher=current_user.surname
            )
            db_sess.add(exersize)
            db_sess.commit()
        return redirect('/teacher')

    return render_template('add_exersize.html', title='Добавление задачи', form=form)


@app.route('/list_students')
def list_students():
    users = get('http://localhost:8080/api/students/' + current_user.students).json()
    print(users)
    users = [{'email': 'почта', 'name': 'имя', 'surname': 'фамилия'}] + users['students']
    return render_template('list_students.html', title='Список учеников', data=users)


@app.route('/look_exercise/<id>')
def look_exercise(id):
    db_sess = db_session.create_session()
    exercise = db_sess.query(Exercise).filter(Exercise.id == id, Exercise.teacher == current_user.id).first()
    if exercise:
        st = exercise.results
        data = list(map(lambda a: (a[1:a.find(', ')], a[a.find(', ') + 2:-1]), st.split('; ')))
        return render_template('look_exercise.html', title='Результаты', data=data)
    else:
        pass


@app.route('/do_exercise/<int:id>', methods=['GET', 'POST'])
def do_exersize(id):
    db_sess = db_session.create_session()
    exercise = db_sess.query(Exercise).filter(Exercise.id == id).first()
    form = DoExercise()
    if form.validate_on_submit():
        answer = form.answer.data
        if answer == exercise.right_answer:
            if exercise.results == '0':
                exercise.results = f'({current_user.surname} {current_user.name}, +)'
            else:
                exercise.results += f'; ({current_user.surname} {current_user.name}, +)'
        else:
            if exercise.results == '0':
                exercise.results = f'({current_user.surname} {current_user.name}, -)'
            else:
                exercise.results += f'; ({current_user.surname} {current_user.name}, -)'
        st = exercise.students
        ids = st.split(', ')
        ids.remove(str(current_user.id))
        exercise.students = ', '.join(ids)
        db_sess.commit()
        return redirect('/student')
    return render_template('do_exercise.html', title='Решение задания', form=form, exercise=exercise)



if __name__ == '__main__':
    db_session.global_init("db/vklasse.db")
    db_sess = db_session.create_session()
    print(os.getcwd() + '\statiс\img')
    app.register_blueprint(users_api.blueprint)
    app.run(port=8080, host='127.0.0.1')
