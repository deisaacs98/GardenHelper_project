import json
from types import SimpleNamespace
import requests
from flask import Flask, jsonify, request, redirect, flash, render_template, url_for, Blueprint, make_response, session, \
    app
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
    plants = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
    columns = ["commonName", "datePlanted", "lastWatering", "healthStatus", "height", "soilPH",
               "light", "soilMoisture"]
    return render_template('gardener/index.html', garden=plants, columns=columns)


@login_required
def get_plant(plant_id, check_gardener=True):
    user_id = session.get('user_id')
    response = requests.get(f'https://localhost:44325/api/plant/gardener={user_id}/plant={plant_id}', verify=False)
    plant = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
    return plant


@login_required
@ bp.route('/<int:plant_id>/update', methods=('GET', 'POST'))
def update(plant_id):
    if request.method == 'POST':
        species_id = np.double(request.form['species_id'])
        common_name = request.form['common_name']
        image_url = request.form['image_url']
        gardener_id = int(request.form['gardener_id'])
        date_planted = str(request.form['date_planted'])
        date_harvested = str(request.form['date_harvested'])
        last_watering = str(request.form['last_watering'])
        health_status = request.form['health_status']
        height = np.double(request.form['height'])
        soil_ph = np.double(request.form['soil_ph'])
        light = np.double(request.form['light'])
        soil_moisture = np.double(request.form['soil_moisture'])
        amount_harvested = np.double(request.form['amount_harvested'])
        plant = {'Id': plant_id, 'SpeciesId': species_id, 'CommonName': common_name, 'ImageUrl': image_url,
                 'DatePlanted': date_planted, 'DateHarvested': date_harvested, 'LastWatering': last_watering,
                 'HealthStatus': health_status, 'Height': height, 'SoilPH': soil_ph, 'Light': light,
                 'SoilMoisture': soil_moisture, 'AmountHarvested': amount_harvested, 'GardenerId': gardener_id}
        response = requests.put('https://localhost:44325/api/plant/', json=plant, verify=False)
        print(response.content)
        return redirect(url_for('gardener.index'))
    else:
        user_id = session.get('user_id')
        response = requests.get(f'https://localhost:44325/api/plant/gardener={user_id}/plant={plant_id}', verify=False)
        plant = json.loads(response.content)
    return render_template('gardener/update.html', plant_id=plant_id, plant=plant, species_id=int(plant[0]["speciesId"]),
                           gardener_id=int(plant[0]["gardenerId"]))


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
        image_url = request.form['image_url']
        species_id = np.double(request.form['species_id'])
        user_id = session.get('user_id')
        plant = {'CommonName': common_name, 'SpeciesId': species_id, 'ImageUrl': image_url,  'GardenerId': user_id}
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
