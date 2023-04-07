import sqlalchemy as sa
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Category(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'category'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=True)

    def __str__(self) -> str:
        return self.name

    def __repr__(self):
        return f'<Category> {self.id} {self.name}'


association_table = sa.Table(
    'association',
    SqlAlchemyBase.metadata,
    sa.Column('jobs', sa.Integer,
                      sa.ForeignKey('jobs.id')),
    sa.Column('category', sa.Integer,
                      sa.ForeignKey('category.id'))
)

