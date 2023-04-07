from flask_restful import reqparse

users_parser = reqparse.RequestParser()
users_parser.add_argument('id', required=False, type=int)
users_parser.add_argument('surname', required=False)
users_parser.add_argument('name', required=False)
users_parser.add_argument('age', required=False, type=int)
users_parser.add_argument('position', required=False)
users_parser.add_argument('speciality', required=False)
users_parser.add_argument('address', required=False)
users_parser.add_argument('email', required=False)
users_parser.add_argument('password', required=False)
