import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Department(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'departments'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column(sa.String, nullable=True)
    chief = sa.Column(sa.Integer, sa.ForeignKey('users.id'), nullable=True)
    members = sa.Column(sa.String, nullable=True)
    email = sa.Column(sa.String, nullable=True)

    user_shef = orm.relationship('User')
