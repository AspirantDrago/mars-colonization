from typing import List, Optional
from datetime import timedelta

import sqlalchemy as sa
from sqlalchemy import orm

from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Jobs(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'jobs'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    team_leader = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    job = sa.Column(sa.String, nullable=True)
    work_size = sa.Column(sa.Integer, nullable=True)
    collaborators = sa.Column(sa.String, nullable=True)
    start_date = sa.Column(sa.Date, nullable=True)
    end_date = sa.Column(sa.Date, nullable=True)
    is_finished = sa.Column(sa.Boolean, nullable=True, default=False)
    is_started = sa.Column(sa.Boolean, nullable=True, default=True)

    user_team_leader = orm.relationship('User')

    categories = orm.relationship("Category",
                                  secondary="association",
                                  backref="jobs")

    def set_categories(self, session: orm.Session, categories: List[str]) -> None:
        from .categories import Category

        self.categories = [session.query(Category).get(int(_id)) for _id in categories]

    def get_categories_id(self) -> List[str]:
        return [str(category.id) for category in self.categories]

    def get_categories(self, separator: str) -> str:
        return separator.join(map(str, self.categories))

    @property
    def duration(self) -> Optional[timedelta]:
        if self.end_date is None or self.start_date is None:
            return None
        return self.end_date - self.start_date

    @property
    def duration_str(self) -> bool:
        if self.duration is None:
            return '-'
        text = ''
        if self.duration.days:
            text += f'{self.duration.days} дней '
        seconds = self.duration.seconds
        minutes = seconds // 60
        seconds %= 60
        hours = minutes // 60
        minutes %= 60
        if hours:
            text += f'{hours} часов '
        if minutes:
            text += f'{minutes} минут '
        if seconds:
            text += f'{seconds} секунд'
        return text
