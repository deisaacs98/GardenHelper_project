import json
from types import SimpleNamespace
import requests
from flask import Flask, jsonify, request, redirect, flash, render_template, url_for, Blueprint, make_response, session
from .auth import login_required
from .auth import load_logged_in_user
from .db import get_db
from .api_keys import trefle_token
from .models import gardener
from .models.gardener import Gardener
from .models.plant import Plant
import html
import pandas as pd
import numpy as np
import sklearn as sklearn

bp = Blueprint('gardener', __name__)


@bp.route('/')
@login_required
def index():
    user_id = session.get('user_id')
    response = requests.get(f'https://localhost:44325/api/plant/gardener={user_id}/index', verify=False)
    print(response.content)
    #plants = Plant.plant_decoder(json.loads(response.content,object_hook=lambda d: SimpleNamespace(**d)))
    plants = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
    return render_template('gardener/index.html', garden=plants)


@ bp.route('/create', methods=('GET', 'POST'))
@ login_required
def create():
    user = load_logged_in_user
    if request.method == 'POST':

        Id = user.id
        FirstName = request.form['first_name']
        MiddleInitial = request.form['middle_initial']
        LastName = request.form['last_name']
        Email = request.form['email']
        AddressLine1 = request.form['address_line1']
        AddressLine2 = request.form['address_line2']
        City = request.form['city']
        State = request.form['state']
        Zip = request.form['zip']
        Phone = request.form['phone']
        error = None

        if not FirstName:
            error = 'First name is required.'
        if not LastName:
            error = 'Last name is required.'
        if not Email:
            error = 'Email address is required.'
        if not AddressLine1:
            error = 'Address is required.'
        if not City:
            error = 'City is required.'
        if not State:
            error = 'State is required.'
        if not Zip:
            error = 'Zip code is required.'
        if not Phone:
            error = 'Phone number is required.'
        if error is not None:
            flash(error)
        else:
            ###Add gardener to database.
            ##Need to geocode address here.
            requests.post('https://localhost:44325/api/plant/', verify=False)
            return redirect(url_for('gardener.index'))

    return render_template('gardener/create.html')


###Modified code from Flask tutorial, but will need to get plant by id. SQL query needs to be evaluated, probably will
###use Pandas/NumPy/SkLearn here...
###Also, thinking I need to use REST API instead of local username database...
###
###The login database is still necessary because it is the most practical way to have user accounts.
###I just think it would be wise to store the heavy data in the REST API.
@login_required
def get_plant(id, check_gardener=True):
    garden = pd.DataFrame(plants)
    plant = garden[garden["GardenerId"] == id]

    #if plant is None:
        #abort(404, "Plant id {0} doesn't exist.".format(id))

    #if check_gardener and plant['gardener_id'] != g.user['id']:
        #abort(403)

    return plant


@ bp.route('/<int:id>/update', methods=('GET', 'POST'))
@ login_required
def update(id):
    plant = get_plant(id)

    if request.method == 'POST':
        date_planted = request.form['date_planted']
        date_harvested = request.form['date_harvested']
        last_watering = request.form['last_watering']
        health_status = request.form['health_status']
        soil_ph = request.form['soil_ph']
        light = request.form['light']
        soil_moisture = request.form['soil_moisture']
        amount_harvested = request.form['amount_harvested']
        error = None

        if not date_planted:
            error = 'Date Planted is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET date_planted = ?, date_harvested = ?, last_watering = ?, health_status = ?, '
                'soil_ph = ?, light = ?, soil_moisture = ?, amount_harvested = ? ' 
                ' WHERE id = ?',
                (date_planted, date_harvested, last_watering, health_status, soil_ph, light, soil_moisture,
                 amount_harvested, id)
            )
            db.commit()
            return redirect(url_for('plant.index'))

    return render_template('plant/update.html', plant=plant)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_plant(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('plant.index'))





@bp.route('/search', methods=['GET', 'POST'])
def search_name():
    if request.method == 'POST' and gardener.first_search and not gardener.found_plant:
        gardener.first_search = False
        common_name = request.form['common_name']
        response = requests.get(f'https://trefle.io/api/v1/plants/search?token={trefle_token}&q={common_name}')
        search_results = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d)).data
        columns = ["common_name", "scientific_name", "family_common_name", "family"]
        return render_template('gardener/search_results.html', common_name=common_name, search_results=search_results,
                               columns=columns)
    elif request.method == 'POST' and not gardener.first_search and not gardener.found_plant:
        gardener.found_plant = True
        common_name = request.form['common_name']
        response = requests.get(f'https://trefle.io/api/v1/plants?token={trefle_token}&filter[common_name]='
                                f'{common_name}')
        search_results = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d)).data
        columns = ["common_name", "scientific_name", "family_common_name", "family"]
        return render_template('gardener/plant_details.html', page_title=common_name,
                               search_results=search_results, columns=columns)
    elif request.method == 'POST' and not gardener.first_search and gardener.found_plant:
        gardener.first_search = True
        gardener.found_plant = False
        common_name = request.form['common_name']
        user_id = session.get('user_id')
        plant = {'CommonName': common_name, 'GardenerId': user_id}
        response = requests.post('https://localhost:44325/api/plant/post-plant', json=plant, verify=False)
        print(response.content)

        #response = requests.get(f'https://trefle.io/api/v1/plants?token={trefle_token}&filter[common_name]='
                                #f'{common_name}')
        #search_results = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d)).data
        #columns = ["common_name", "scientific_name", "family_common_name", "family"]
        return redirect(url_for('gardener.index'))
    else:
        gardener.first_search = True
        return render_template('gardener/search.html')


@bp.route('/search_results', methods=['GET', 'POST'])
def view_plant(common_name, search_results, columns):
    if request.method == 'POST':
        response = requests.get(f'https://trefle.io/api/v1/plants?token={trefle_token}&filter[common_name]='
                                f'{common_name}')
        search_results = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d)).data
        columns = ["common_name", "scientific_name", "family_common_name", "family"]
        return render_template('gardener/plant_details.html', page_title=common_name,
                               search_results=search_results, columns=columns)
    else:
        return render_template('gardener/search_results.html', common_name=common_name, search_results=search_results,
                               columns=columns)
