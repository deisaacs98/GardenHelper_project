import functools
import json
import os
from datetime import datetime, timedelta
from types import SimpleNamespace

import requests
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from twilio.rest import Client
from werkzeug.security import check_password_hash, generate_password_hash
from gardenhelper.api_keys import weather_key
from gardenhelper.db import get_db
from gardenhelper import api_keys
bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        middle_initial = request.form['middle_initial']
        last_name = request.form['last_name']
        address_line1 = request.form['address_line1']
        address_line2 = request.form['address_line2']
        city = request.form['city']
        state = request.form['state']
        zip_code = request.form['zip_code']
        email = request.form['email']
        phone = request.form['phone']
        geo_response = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?address={address_line1}+'
                                    f'{address_line2},+{city},+{state}+{zip_code}&key={api_keys.geocoding_key}')
        lat_lng = json.loads(geo_response.content)
        res = lat_lng["results"]
        geo = res[0]["geometry"]["location"]
        lat = geo["lat"]
        lng = geo["lng"]
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not first_name:
            error = 'First name is required.'
        elif not last_name:
            error = 'Last name is required.'
        elif not address_line1:
            error = 'Address is required.'
        elif not city:
            error = 'City is required.'
        elif not state:
            error = 'State is required.'
        elif not zip_code:
            error = 'Zip code is required.'
        elif not email:
            error = 'Email address is required.'
        elif not phone:
            error = 'Phone number is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password, first_name, middle_initial, last_name, address_line1, '
                'address_line2, city, state, zip_code, email, phone, lat, lng) VALUES (?, ?, ?, ?, ?, '
                '?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (username, generate_password_hash(password), first_name, middle_initial, last_name, address_line1,
                 address_line2, city, state, zip_code, email, phone, lat, lng)
            )
            db.commit()
            user = db.execute(
                'SELECT * FROM user WHERE username = ?', (username,)
            ).fetchone()
            send_text(user, "Thank you for registering with Garden Helper!")
            session.clear()
            session['user_id'] = user['id']

            #gardener_data = {'UserId': user['id'], 'FirstName': first_name, 'MiddleInitial': middle_initial,
            #                 'LastName': last_name, 'Email': email, 'AddressLine1': address_line1,
            #                 'AddressLine2': address_line2, 'City': city, 'State': state, 'Zip': zip_code,
            #                 'Phone': phone, 'Lat': lat, 'Lng': lng}
            #response = requests.post('https://localhost:44325/api/plant/post-gardener', json=gardener_data,
            #                         verify=False)
            #print(response.content)
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


def send_text(user, text_message):
    client = Client(api_keys.twilio_sid, api_keys.twilio_token)
    message = client.messages \
                    .create(
                        body=text_message,
                        from_=api_keys.twilio_number,
                        to="+1" + user['phone']
                    )
    print(message.sid)

#def send_reminders():
#    db = get_db()
#    users = db.execute(
#        'SELECT * FROM user'
#    ).fetchall()
#    for user in users:
#        #send_alert = water_plants(user)
#        send_alert=True
#        if send_alert:
#            account_sid = os.environ[api_keys.twilio_sid]
#            auth_token = os.environ[api_keys.twilio_token]
#            client = Client(account_sid, auth_token)
#
#            message = client.messages \
#                .create(
#                    body="Hello, this is Garden Helper with a friendly reminder to water your plants! ",
#                    from_=api_keys.twilio_number,
#                    to="+1" + user['phone']
#                )
#            print(message.sid)
