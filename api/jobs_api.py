from flask import Blueprint, jsonify, request
import datetime

from data import db_session
from data.jobs import Jobs
from data.user import User
from data.categories import Category

jobs_api_blueprint = Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@jobs_api_blueprint.route('/api/jobs', methods=['GET'])
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('id', 'job', 'work_size', 'collaborators',
                                    'start_date', 'end_date', 'is_finished',
                                    'user_team_leader.id', 'user_team_leader.surname',
                                    'user_team_leader.name',
                                    'categories.id', 'categories.name'))
                 for item in jobs]
        }
    )


@jobs_api_blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    if not request.json:
        return jsonify({'error': 'Empty request'}), 400
    elif not all(key in ['id', 'team_leader', 'is_finished', 'job', 'start_date', 'end_date', 'work_size', 'categories', 'collaborators']
                 for key in request.json):
        return jsonify({'error': 'Bad request'}), 400
    db_sess = db_session.create_session()
    if db_sess.query(Jobs).get(request.json.get('id')):
        return jsonify({'error': 'Id already exists'}), 400
    team_leader = db_sess.query(User).get(request.json.get('team_leader'))
    if not team_leader:
        return jsonify({'error': 'Team leader not found'}), 400
    collaborators_ids = request.json.get('collaborators', [])
    collaborators_objs = db_sess.query(User).filter(User.id.in_(collaborators_ids)).all()
    if len(collaborators_objs) != len(collaborators_ids):
        return jsonify({'error': 'Collaborators not found'}), 400
    categories_ids = request.json.get('categories', [])
    categories_objs = db_sess.query(Category).filter(Category.id.in_(categories_ids)).all()
    if len(categories_objs) != len(categories_ids):
        return jsonify({'error': 'Categories not found'}), 400
    new_job = Jobs(
        team_leader=request.json.get('team_leader'),
        collaborators=', '.join(map(str, collaborators_ids)),
    )
    for key in ('id', 'job', 'work_size', 'is_finished'):
        if request.json.get(key) is not None:
            setattr(new_job, key, request.json[key])
    for key in ('start_date', 'end_date'):
        if key in request.json:
            try:
                setattr(new_job, key, datetime.datetime.strptime(request.json[key], '%Y-%m-%d'))
            except Exception:
                pass
    new_job.categories = categories_objs
    db_sess.add(new_job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@jobs_api_blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id: int):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': f'Job with id={job_id} not found!'}), 404
    return jsonify(
        job.to_dict(only=('id', 'job', 'work_size', 'collaborators',
                          'start_date', 'end_date', 'is_finished',
                          'user_team_leader.id', 'user_team_leader.surname',
                          'user_team_leader.name',
                          'categories.id', 'categories.name'))
    )


@jobs_api_blueprint.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id: int):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'}), 404
    db_sess.delete(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@jobs_api_blueprint.route('/api/jobs/<int:job_id>', methods=['PUT'])
def edit_job(job_id: int):
    if not request.json:
        return jsonify({'error': 'Empty request'}), 400
    elif not all(key in ['team_leader', 'is_finished', 'job', 'start_date', 'end_date', 'work_size', 'categories', 'collaborators']
                 for key in request.json):
        return jsonify({'error': 'Bad request'}), 400
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    try:
        if not job:
            raise Exception('Not found')
        if 'team_leader' in request.json:
            team_leader = db_sess.query(User).get(request.json['team_leader'])
            if not team_leader:
                raise Exception('Team leader not found')
            job.team_leader = team_leader
        for item, cls in {
            'collaborators': User,
            'categories': Category
        }.items():
            if item in request.json:
                ids = request.json.get(item, [])
                objs = db_sess.query(cls).filter(cls.id.in_(ids)).all()
                if len(objs) != len(ids):
                    raise Exception(f'{cls.__name__} not found')
                if item == 'collaborators':
                    setattr(job, item, ', '.join(map(str, ids)))
                else:
                    setattr(job, item, objs)
        for key in ('job', 'work_size', 'is_finished'):
            if request.json.get(key) is not None:
                setattr(job, key, request.json[key])
        for key in ('start_date', 'end_date'):
            if key in request.json:
                setattr(job, key, datetime.datetime.strptime(request.json[key], '%Y-%m-%d'))
    except Exception as e:
        db_sess.rollback()
        return jsonify({'error': str(e)}), 400
    else:
        db_sess.merge(job)
        db_sess.commit()
        return jsonify({'success': 'OK'})
