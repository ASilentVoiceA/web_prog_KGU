import json
from datetime import datetime

from flask_login import login_user

from app import db
from app.models import User, History_search, Roles, Profile_status


def update_last_seen(user):
    user.last_seen = datetime.utcnow()
    db.session.commit()


def login_db(username, password, remember_me):
    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        return json.dumps({'status': 'Bad', 'error': 'Неверный логин или пароль'})

    if user.profile_status == 2:
        return json.dumps({'status': 'Bad', 'error': 'Профиль заблокирован'})

    login_user(user, remember=remember_me)

    return json.dumps({'status': 'OK'})


def register_db(username, password1, password2):
    if len(username) > 15:
        return json.dumps({'status': 'Bad', 'error': 'Логин длиннее 15 символов'})

    user = User.query.filter_by(username=username).first()
    if user is not None:
        return json.dumps({'status': 'Bad', 'error': 'Данный логин занят'})

    if password1 != password2:
        return json.dumps({'status': 'Bad', 'error': 'Пароли должны быть одинаковыми'})

    user = User(username=username, role=2, profile_status=1)
    user.set_password(password1)
    db.session.add(user)
    db.session.commit()

    login_user(user, remember=True)

    return json.dumps({'status': 'OK'})


def set_history_search(user, search_text):
    history = History_search(id_user=user.id, str_search=search_text, data=datetime.utcnow())

    db.session.add(history)
    db.session.commit()


def get_history_search(user):
    result = []

    history_user = History_search.query.filter_by(id_user=user.id).all()

    for item in history_user:
        result.append({'srt': item.str_search, 'data': item.data})

    return result


def get_info_user(user):
    role = Roles.query.filter_by(id=user.role).first().name
    profile_status = Profile_status.query.filter_by(id=user.profile_status).first().name

    result = {'role': role, 'profile_status': profile_status}

    return result


def block_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    user.profile_status = 2

    db.session.add(user)
    db.session.commit()


def unblock_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    user.profile_status = 1

    db.session.add(user)
    db.session.commit()
