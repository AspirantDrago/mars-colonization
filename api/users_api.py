from flask import Blueprint, jsonify, request

from data import db_session
from data.user import User

users_api_blueprint = Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@users_api_blueprint.route('/api/users', methods=['GET'])
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=('id', 'surname', 'name', 'position', 'email'))
                 for item in users]
        }
    )


@users_api_blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id: int):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': f'User with id={user_id} not found!'}), 404
    return jsonify(
        user.to_dict(only=('id', 'surname', 'name', 'age',
                          'position', 'speciality', 'address',
                          'email'))
    )


@users_api_blueprint.route('/api/users', methods=['POST'])
def create_user():
    if not request.json:
        return jsonify({'error': 'Empty request'}), 400
    elif not all(key in ['id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'password']
                 for key in request.json):
        return jsonify({'error': 'Bad request'}), 400
    db_sess = db_session.create_session()
    if db_sess.query(User).get(request.json.get('id')):
        return jsonify({'error': 'Id already exists'}), 400
    password = None
    if 'password' in request.json:
        password = request.json.pop('password')
    new_user = User(**request.json)
    if password is not None:
        new_user.set_password(password)
    db_sess.add(new_user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@users_api_blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id: int):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'}), 404
    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@users_api_blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id: int):
    if not request.json:
        return jsonify({'error': 'Empty request'}), 400
    elif not all(key in ['surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'password']
                        for key in request.json):
        return jsonify({'error': 'Bad request'}), 400
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    try:
        if not user:
            raise Exception('Not found')
        for key in ('surname', 'name', 'age', 'position', 'speciality', 'address', 'email'):
            if request.json.get(key) is not None:
                setattr(user, key, request.json[key])
        if 'password' in request.json:
            user.set_password(request.json['password'])
    except Exception as e:
        db_sess.rollback()
        return jsonify({'error': str(e)}), 400
    else:
        db_sess.merge(user)
        db_sess.commit()
        return jsonify({'success': 'OK'})
