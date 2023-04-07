from argparse import Namespace
from datetime import datetime
from flask_restful import reqparse
from typing import Optional

from data.user import User
from data.categories import Category
from sqlalchemy.orm import Session


class JobsParser(reqparse.RequestParser):
    def __init__(self):
        super().__init__()
        self._session: Optional[Session] = None
        self.add_argument('id', required=False, type=int)
        self.add_argument('team_leader', dest="user_team_leader", required=False,
                                 type=lambda x: self._session.query(User).get(x))
        self.add_argument('is_finished', required=False, type=bool)
        self.add_argument('job', required=False)
        self.add_argument('start_date', required=False, type=lambda x: datetime.strptime(x, '%Y-%m-%d'))
        self.add_argument('end_date', required=False, type=lambda x: datetime.strptime(x, '%Y-%m-%d'))
        self.add_argument('categories', required=False, action='append',
                                 type=lambda x: self._session.query(Category).get(x))
        self.add_argument('collaborators', required=False, action='append',
                                 type=lambda x: self._session.query(User).get(x))

    def parse_args(self, session: Session) -> Namespace:
        self._session = session
        all_users = session.query(User).all()
        all_categories = session.query(Category).all()
        self.add_argument('team_leader', dest="user_team_leader", required=False,
                          choices=all_users,
                          type=lambda x: self._session.query(User).get(x))
        self.replace_argument('categories', required=False, action='append',
                              choices=all_categories,
                              type=lambda x: self._session.query(Category).get(x))
        self.add_argument('collaborators', required=False, action='append',
                          choices=all_users,
                          type=lambda x: self._session.query(User).get(x))
        return super().parse_args()


jobs_parser = JobsParser()
