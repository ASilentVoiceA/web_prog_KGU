import json
import os

from app import app, utility, db_work
from app.models import User
from flask import render_template, redirect, url_for, request, send_from_directory
from flask_login import logout_user, current_user, login_required


@app.before_request
def before_request():
    if current_user.is_authenticated:
        db_work.update_last_seen(current_user)
        if current_user.profile_status == 2:
            logout_user()


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/img'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/main', methods=['GET'])
@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')


@app.route('/main', methods=['POST'])
@app.route('/', methods=['POST'])
@login_required
def search():
    if 'movie_name' in request.form:
        movie_name = request.form['movie_name']
        if len(movie_name) > 0:
            db_work.set_history_search(current_user, movie_name)

            movie_list, error = utility.search_movie(movie_name)

            if len(movie_list) > 0:
                return render_template('result.html', movie_list=movie_list)
            else:
                return render_template('error_page.html', error=error)

    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return redirect(url_for('main'))

    if current_user.is_authenticated:
        return redirect(url_for('main'))

    username = request.form['username-login']
    password = request.form['password-login']
    remember_me = True if 'remember_me' in request.form else False

    return db_work.login_db(username, password, remember_me)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return redirect(url_for('main'))

    if current_user.is_authenticated:
        return redirect(url_for('main'))

    username = request.form['username-register']
    password1 = request.form['password1-register']
    password2 = request.form['password2-register']

    return db_work.register_db(username, password1, password2)


@app.route('/profile/<username>', methods=['GET'])
@login_required
def profile(username):
    if current_user.role == 1:
        user = User.query.filter_by(username=username).first()

        if user is None:
            return render_template('error_page.html', error='Пользователь не найден')
        history_user = db_work.get_history_search(user)
        info = db_work.get_info_user(user)

        return render_template('user.html', user=user, history=history_user, info=info)
    else:
        if current_user.username == username:
            history_user = db_work.get_history_search(current_user)

            return render_template('user.html', user=current_user, history=history_user)
        else:
            return render_template('error_page.html', error='Страница недоступна')


@app.route('/block_user', methods=['POST'])
@login_required
def block_user():
    if current_user.role == 1:
        user_id = request.form['user_id']

        db_work.block_user(user_id)

        return json.dumps({'status': 'OK'})

    return json.dumps({'status': 'Bad', 'error': 'Ошибка блокировки'})


@app.route('/unblock_user', methods=['POST'])
@login_required
def unblock_user():
    if current_user.role == 1:
        user_id = request.form['user_id']

        db_work.unblock_user(user_id)

        return json.dumps({'status': 'OK'})

    return json.dumps({'status': 'Bad', 'error': 'Ошибка разблокировки'})


@app.errorhandler(401)
def not_found_error(error):
    return render_template('error_page.html', error='Необходима авторизация')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('error_page.html', error='Страница не найдена')
