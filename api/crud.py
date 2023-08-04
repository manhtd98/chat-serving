from database import db_context
from models import User
from schemas import UserIn, UserOut


def get_user_chat_history(token, bucket):
    return {}

def crud_add_user(user: UserIn):
    db_user = User(**user.dict())
    with db_context() as db:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    return db_user


def crud_get_user_info(user_id: int):
    with db_context() as db:
        user = db.query(User).filter(User.id == user_id).first()
    if user:
        return UserOut(**user.__dict__)
    return None

