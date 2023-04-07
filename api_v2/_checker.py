from typing import Any, Optional
from flask_restful import abort
from sqlalchemy.orm import Session

from data import db_session


def search_or_abort_if_not_found(cls: type, _id: int) -> tuple[Optional[Any], Optional[Session]]:
    session = db_session.create_session()
    result = session.query(cls).get(_id)
    if not result:
        abort(404, message=f"Object <{cls.__name__}> with id={_id} not found")
        return None, None
    return result, session
