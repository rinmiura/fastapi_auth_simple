import bcrypt

from .models import User, session_local


def get_user(username: str, password: str):
    with session_local() as db:
        user = db.query(User).filter(User.username == username).first()

        if user is not None and verify_password(password, user.password):
            return user

        return None


def check_user(username):
    with session_local() as db:
        return (db
                .query(User)
                .filter(User.username == username)
                .first())


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def register_user(username, password):
    with session_local() as db:
        db.add(User(username=username, password=password))
        db.commit()


def verify_password(raw_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(raw_password.encode('utf-8'), hashed_password.encode('utf-8'))


def generate_session_token():
    return "zc9w4twfjjg34"