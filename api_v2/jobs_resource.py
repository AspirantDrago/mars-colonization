from flask import jsonify
from flask_restful import Resource, abort

from data import db_session
from data.user import User
from data.jobs import Jobs
from data.categories import Category
from ._checker import search_or_abort_if_not_found as search
from .jobs_parser import jobs_parser


class JobsResource(Resource):
    def get(self, job_id: int):
        job, _ = search(Jobs, job_id)
        return jsonify(
            job.to_dict(only=('id', 'job', 'work_size', 'collaborators',
                              'start_date', 'end_date', 'is_finished',
                              'user_team_leader.id', 'user_team_leader.surname',
                              'user_team_leader.name',
                              'categories.id', 'categories.name'))
        )

    def delete(self, job_id: int):
        job, session = search(Jobs, job_id)
        session.delete(job)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, job_id: int):
        job, session = search(Jobs, job_id)
        args = jobs_parser.parse_args(session)
        if 'id' in args:
            del args['id']
        if args['collaborators'] is not None:
            args['collaborators'] = ', '.join(map(lambda usr: str(usr.id), args['collaborators']))
        for key, value in args.items():
            if value is not None:
                setattr(job, key, value)
        session.commit()
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):
    def get(self):
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

    def post(self):
        session = db_session.create_session()
        args = jobs_parser.parse_args(session)
        if session.query(Jobs).get(args.get('id')):
            abort(404, message='Id already exists')
        args['collaborators'] = ', '.join(map(lambda usr: str(usr.id), args['collaborators']))
        new_job = Jobs(**args)
        session.add(new_job)
        session.commit()
        return jsonify({'success': 'OK'})
