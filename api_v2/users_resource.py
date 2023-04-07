from flask import jsonify
from flask_restful import Resource, abort
from sqlalchemy.orm import Session

from data import db_session
from data.user import User
from ._checker import search_or_abort_if_not_found as search
from .users_parser import users_parser


class UsersResource(Resource):
    def get(self, user_id: int):
        user, _ = search(User, user_id)
        return jsonify(
            user.to_dict(only=('id', 'surname', 'name', 'age',
                               'position', 'speciality', 'address',
                               'email'))
        )

    def delete(self, user_id: int):
        user, session = search(User, user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, user_id: int):
        user, session = search(User, user_id)
        args = users_parser.parse_args()
        for key, value in args.items():
            if value is not None and key != 'password':
                setattr(user, key, value)
        if args['password'] is not None:
            user.set_password(args['password'])
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        users = db_sess.query(User).all()
        return jsonify(
            {
                'users':
                    [item.to_dict(only=('id', 'surname', 'name', 'position', 'email'))
                     for item in users]
            }
        )

    def post(self):
        args = users_parser.parse_args()
        session = db_session.create_session()
        if session.query(User).get(args.get('id')):
            abort(404, message='Id already exists')
        password = None
        if 'password' in args:
            password = args.pop('password')
        new_user = User(**args)
        if password is not None:
            new_user.set_password(password)
        session.add(new_user)
        session.commit()
        return jsonify({'success': 'OK'})
