import json
from types import SimpleNamespace
import requests
from flask import Flask, jsonify, g, request, redirect, flash, render_template, url_for, Blueprint, make_response, \
    session, app
from .auth import login_required, login
from .auth import load_logged_in_user
from .db import get_db
from .api_keys import weather_key
from .api_keys import trefle_token
from .models import gardener
from gardenhelper import auth
from .models.gardener import Gardener
from .models.plant import Plant
import html
import pandas as pd
import numpy as np
import sklearn as sklearn
from datetime import datetime, timedelta, timezone, tzinfo
from time import time

bp = Blueprint('gardener', __name__)


@bp.route('/')
@login_required
def index():
    user_id = g.user['id']
    current_weather = get_current_weather()
    yesterdays_weather = get_historical_weather(days_ago=1)
    two_days = get_historical_weather(days_ago=2)
    three_days = get_historical_weather(days_ago=3)
    four_days = get_historical_weather(days_ago=4)
    five_days = get_historical_weather(days_ago=5)
    weather_df = get_weather_df(current_weather, yesterdays_weather, two_days, three_days, four_days, five_days)
    plants_response = requests.get(f'https://localhost:44325/api/plant/gardener={user_id}/index', verify=False)
    plants = json.loads(plants_response.content, object_hook=lambda d: SimpleNamespace(**d))
    columns = ["commonName", "datePlanted", "lastWatering", "healthStatus", "height", "soilPH",
               "light", "soilMoisture"]
    return render_template('gardener/index.html', garden=plants, columns=columns, current_weather=current_weather)


@login_required
def get_current_weather():
    lat = g.user['lat']
    lng = g.user['lng']
    current_weather_response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon='
                                            f'{lng}&units=imperial&appid={weather_key}')
    current_weather = json.loads(current_weather_response.content, object_hook=lambda d: SimpleNamespace(**d))
    return current_weather


def get_weather_df(current, yesterday, two_days, three_days, four_days, five_days):
    weather_df = pd.DataFrame(
        {
            "dt": [current.dt, yesterday.current.dt, two_days.current.dt, three_days.current.dt,
                   four_days.current.dt, five_days.current.dt],
            "temp": [current.main.temp, yesterday.current.temp, two_days.current.temp, three_days.current.temp,
                     four_days.current.temp, five_days.current.temp],
            #"temp_min": [current.main.temp_min, yesterday.current.temp_min, two_days.current.temp_min,
            #             three_days.current.temp_min, four_days.current.temp_min, five_days.current.temp_min],
            #"temp_max": [current.main.temp_max, yesterday.current.temp_max, two_days.current.temp_max,
            #             three_days.current.temp_max, four_days.current.temp_max, five_days.current.temp_max],
            "humidity": [current.main.humidity, yesterday.current.humidity, two_days.current.humidity,
                         three_days.current.humidity, four_days.current.humidity, five_days.current.humidity],
            "pressure": [current.main.pressure, yesterday.current.pressure, two_days.current.pressure,
                         three_days.current.pressure, four_days.current.pressure, five_days.current.pressure],
            "sunrise": [current.sys.sunrise, yesterday.current.sunrise, two_days.current.sunrise,
                        three_days.current.sunrise,four_days.current.sunrise, five_days.current.sunrise],
            "sunset": [current.sys.sunset, yesterday.current.sunrise, two_days.current.sunrise,
                       three_days.current.sunrise, four_days.current.sunrise, five_days.current.sunrise]
        }
    )
    print(weather_df)
    return weather_df


@login_required
def get_historical_weather(days_ago):
    lat = g.user['lat']
    lng = g.user['lng']
    today = datetime.today()
    utc_time = today.replace(tzinfo=timezone.utc)
    date = utc_time - timedelta(days=days_ago)
    historical_weather_response = requests.get(f'https://api.openweathermap.org/data/2.5/onecall/timemachine?'
                                               f'lat={lat}&lon={lng}&dt={int(date.timestamp())}&units=imperial&appid='
                                               f'{weather_key}')
    historical_weather = json.loads(historical_weather_response.content, object_hook=lambda d: SimpleNamespace(**d))
    print(historical_weather)
    return historical_weather


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


@login_required
@ bp.route('/<int:plant_id>/delete', methods=('GET', 'POST'))
def delete_plant(plant_id):
    if request.method == 'POST':
        confirmation = request.form['confirmation']
        if confirmation:
            response = requests.delete(f'https://localhost:44325/api/plant/{plant_id}', verify=False)
            print(response.content)
            return redirect(url_for('gardener.index'))
    return render_template('gardener/delete.html', plant_id=plant_id)



