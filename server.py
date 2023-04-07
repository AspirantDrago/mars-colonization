import os

from flask import Flask, render_template, redirect, abort, make_response, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api

from data import db_session
from data.jobs import Jobs
from data.user import User
from forms.user import RegisterForm, LoginForm
from forms.jobs import CreateJob
from api import jobs_api, users_api
from api_v2 import users_resource, jobs_resource


app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def index():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return render_template('index.html', jobs=jobs)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Invalid email or password",
                               form=form)
    return render_template('login.html', title='Sign in', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_required
@app.route('/addjob', methods=['GET', 'POST'])
def add_job():
    form = CreateJob()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if not db_sess.query(User).get(form.team_leader.data):
            return render_template('addjob.html', title='New job',
                                   form=form,
                                   message="Invalid team leader")
        new_job = Jobs(
            team_leader=form.team_leader.data,
            job=form.job.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            is_finished=form.is_finished.data,
            categories=form.categories.data,
        )
        db_sess.add(new_job)
        db_sess.commit()
        return redirect('/')
    return render_template('addjob.html', title='New job', header='Adding a job', form=form)


@login_required
@app.route('/jobs/<int:job_id>', methods=['GET', 'POST'])
def change_job(job_id: int):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        abort(404)
    if job.user_team_leader != current_user and not current_user.is_admin():
        abort(403)
    form = CreateJob()
    if form.validate_on_submit():
        job.team_leader = form.team_leader.data
        job.job = form.job.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.start_date = form.start_date.data
        job.end_date = form.end_date.data
        job.is_finished = form.is_finished.data
        job.set_categories(db_sess, form.categories.data)
        db_sess.merge(job)
        db_sess.commit()
        return redirect('/')
    form.team_leader.default = job.team_leader
    form.process()
    form.job.data = job.job
    form.work_size.data = job.work_size
    form.collaborators.data = job.collaborators
    form.start_date.data = job.start_date
    form.end_date.data = job.end_date
    form.is_finished.data = job.is_finished
    form.categories.data = job.get_categories_id()
    print(job.get_categories_id())
    return render_template('addjob.html', title='Change job', header='Changing a job', form=form)


@app.route('/job_delete/<int:job_id>', methods=['GET', 'POST'])
@login_required
def job_delete(job_id: int):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        abort(404)
    if job.user_team_leader != current_user and not current_user.is_admin():
        abort(403)
    db_sess.delete(job)
    db_sess.commit()
    return redirect('/')


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


def main():
    db_session.global_init('db/mars.db')
    app.register_blueprint(jobs_api.jobs_api_blueprint)
    app.register_blueprint(users_api.users_api_blueprint)
    api.add_resource(users_resource.UsersResource, '/api/v2/users/<int:user_id>')
    api.add_resource(users_resource.UsersListResource, '/api/v2/users')
    api.add_resource(jobs_resource.JobsResource, '/api/v2/jobs/<int:job_id>')
    api.add_resource(jobs_resource.JobsListResource, '/api/v2/jobs')
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)


if __name__ == '__main__':
    main()
