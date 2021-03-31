import functools

import requests
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from gardenhelper import gardener
from gardenhelper.db import get_db
from gardenhelper import gardener

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            user = db.execute(
                'SELECT * FROM user WHERE username = ?', (username,)
            ).fetchone()
            session.clear()
            session['user_id'] = user['id']
            first_name = request.form['first_name']
            middle_initial = request.form['middle_initial']
            last_name = request.form['last_name']
            email = request.form['email']
            address_line1 = request.form['address_line1']
            address_line2 = request.form['address_line2']
            city = request.form['city']
            state = request.form['state']
            zip_code = request.form['zip_code']
            phone = request.form['phone']
            gardener_data = {'Id': user['id'], 'FirstName': first_name, 'MiddleInitial': middle_initial,
                             'LastName': last_name, 'Email': email, 'AddressLine1': address_line1,
                             'AddressLine2': address_line2, 'City': city, 'State': state, 'Zip': zip_code,
                             'Phone': phone}
            response = requests.post('https://localhost:44325/api/plant/post-gardener', json=gardener_data,
                                     verify=False)
            print(response.content)
            return redirect(url_for('gardener.index'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('gardener.index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('gardener.index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

