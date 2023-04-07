from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, BooleanField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired
from data import db_session
from data.user import User
from data.categories import Category


class CreateJob(FlaskForm):
    team_leader = SelectField('Team Leader', choices=[], validators=[DataRequired()])
    job = StringField('Job', validators=[DataRequired()])
    categories = SelectMultipleField('Categories', choices=[])
    work_size = IntegerField('Work Size')
    collaborators = StringField('Collaborators')
    start_date = DateField('Start Date')
    end_date = DateField('End Date')
    is_finished = BooleanField('Is Finished')
    submit = SubmitField('Add job')

    def __init__(self, *args, **kwargs):
        super(CreateJob, self).__init__(*args, **kwargs)
        db_sess = db_session.create_session()
        users = db_sess.query(User).all()
        users_arr = [(str(user.id), user.fio) for user in users]
        self.team_leader.choices = users_arr
        categories = db_sess.query(Category).all()
        categories_arr = [(str(category.id), category.name) for category in categories]
        self.categories.choices = categories_arr