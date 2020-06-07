from app import db
from app.models import User, Roles, Profile_status


def add_roles():
    roles_admin = Roles(name='Администратор')
    roles_user = Roles(name='Пользователь')

    db.session.add(roles_admin)
    db.session.add(roles_user)

    db.session.commit()


def add_profile_status():
    roles_act = Profile_status(name='Активен')
    roles_block = Profile_status(name='Заблокирован')

    db.session.add(roles_act)
    db.session.add(roles_block)

    db.session.commit()


def add_admin():
    admin = User(username='admin', role=1, profile_status=1)
    admin.set_password('123')

    db.session.add(admin)

    db.session.commit()


if __name__ == '__main__':
    add_roles()
    add_profile_status()
    add_admin()

