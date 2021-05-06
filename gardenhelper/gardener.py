import json
from types import SimpleNamespace
import requests
from flask import g, request, redirect, render_template, url_for, Blueprint, session
from gardenhelper import auth
from .auth import login_required
from .api_keys import weather_key
from .api_keys import trefle_token
from .models import gardener
import html
import pandas as pd
import numpy as np
import sklearn as sklearn
from datetime import datetime, timedelta, timezone, tzinfo, date
from time import time
from gardenhelper.db import get_db

bp = Blueprint('gardener', __name__)


@bp.route('/')
@login_required
def index():
    db = get_db()
    user = g.user
    user_id = user['id']
    lat = user['lat']
    lng = user['lng']
    current_weather = get_current_weather(user=g.user)
    #yesterdays_weather = get_historical_weather(user=g.user, days_ago=1)
    #two_days = get_historical_weather(user=g.user, days_ago=2)
    #three_days = get_historical_weather(user=g.user, days_ago=3)
    #four_days = get_historical_weather(user=g.user, days_ago=4)
    #weather_df = get_weather_df(current_weather, yesterdays_weather, two_days, three_days, four_days)
    plants_response = requests.get(f'https://localhost:44325/api/plant/gardener={user_id}/index', verify=False)
    plants = json.loads(plants_response.content, object_hook=lambda d: SimpleNamespace(**d))
    columns = ["commonName", "datePlanted", "lastWatering", "healthStatus"]
    market_response = requests.get(f'http://search.ams.usda.gov/farmersmarkets/v1/data.svc/locSearch?lat={lat}'
                                   f'&lng={lng}')
    markets = json.loads(market_response.content, object_hook=lambda d: SimpleNamespace(**d))
    print(markets)
    market1_id = markets.results[0].id
    market2_id = markets.results[1].id
    market3_id = markets.results[2].id
    market1_response = requests.get(f'http://search.ams.usda.gov/farmersmarkets/v1/data.svc/mktDetail?id={market1_id}')
    market1 = json.loads(market1_response.content, object_hook=lambda d: SimpleNamespace(**d))
    market2_response = requests.get(f'http://search.ams.usda.gov/farmersmarkets/v1/data.svc/mktDetail?id={market2_id}')
    market2 = json.loads(market2_response.content, object_hook=lambda d: SimpleNamespace(**d))
    market3_response = requests.get(f'http://search.ams.usda.gov/farmersmarkets/v1/data.svc/mktDetail?id={market3_id}')
    market3 = json.loads(market3_response.content, object_hook=lambda d: SimpleNamespace(**d))
    nearby_markets = [market1, market2, market3]
    print(market1)
    return render_template('gardener/index.html', garden=plants, columns=columns, current_weather=current_weather,
                           nearby_markets=nearby_markets, markets=markets)


@login_required
def get_current_weather(user):
    lat = user['lat']
    lng = user['lng']
    current_weather_response = requests.get(f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon='
                                            f'{lng}&units=imperial&appid={weather_key}')
    current_weather = json.loads(current_weather_response.content, object_hook=lambda d: SimpleNamespace(**d))
    print(current_weather)
    return current_weather


def get_weather_df(current, yesterday, two_days, three_days, four_days):
    weather_df = pd.DataFrame(
        {
            "dt": [current.dt, yesterday.daily.dt, two_days.daily.dt, three_days.daily.dt,
                   four_days.daily.dt],
            "#temp": [current.main.temp, yesterday.current.temp, two_days.current.temp, three_days.current.temp,
                     four_days.current.temp],
            "temp_min": [current.main.temp_min, yesterday.daily.temp.min, two_days.daily.temp.min,
                         three_days.daily.temp_min, four_days.daily.temp_min],
            "temp_max": [current.main.temp.max, yesterday.daily.temp.max, two_days.daily.temp.max,
                         three_days.daily.temp.max, four_days.daily.temp.max],
            "humidity": [current.main.humidity, yesterday.daily.humidity, two_days.daily.humidity,
                         three_days.daily.humidity, four_days.daily.humidity],
            "pressure": [current.main.pressure, yesterday.daily.pressure, two_days.daily.pressure,
                         three_days.daily.pressure, four_days.daily.pressure],
            "sunrise": [current.sys.sunrise, yesterday.daily.sunrise, two_days.daily.sunrise,
                        three_days.daily.sunrise,four_days.daily.sunrise],
            "sunset": [current.sys.sunset, yesterday.daily.sunrise, two_days.daily.sunrise,
                       three_days.daily.sunrise, four_days.daily.sunrise]
        }
    )
    return weather_df


@login_required
def get_historical_weather(user, days_ago):
    lat = user['lat']
    lng = user['lng']
    today = datetime.today()
    utc_time = today.replace(tzinfo=timezone.utc)
    date = utc_time - timedelta(days=days_ago)
    historical_weather_response = requests.get(f'https://api.openweathermap.org/data/2.5/onecall/timemachine?'
                                               f'lat={lat}&lon={lng}&dt={int(date.timestamp())}&units=imperial&appid='
                                               f'{weather_key}')
    historical_weather = json.loads(historical_weather_response.content, object_hook=lambda d: SimpleNamespace(**d))
    return historical_weather


@login_required
def get_plant(plant_id):
    user_id = session.get('user_id')
    response = requests.get(f'https://localhost:44325/api/plant/gardener={user_id}/plant={plant_id}', verify=False)
    plant = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
    return plant


@login_required
@ bp.route('/<int:plant_id>/update', methods=('GET', 'POST'))
def update(plant_id):
    user_id = session.get('user_id')
    response = requests.get(f'https://localhost:44325/api/plant/gardener={user_id}/plant={plant_id}', verify=False)
    plant = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
    if request.method == 'POST':
        image_url = request.form['image_url']
        health_status = request.form['health_status']
        height = np.double(request.form['height'])
        soil_ph = np.double(request.form['soil_ph'])
        light = np.double(request.form['light'])
        soil_moisture = np.double(request.form['soil_moisture'])
        watered_today = request.form.get('watered_today')
        if watered_today == "True":
            last_watering = str(datetime.now())
            watered = True
        else:
            last_watering = plant[0].lastWatering
            watered = False
        plant = plant[0]
        plant = {'Id': plant_id, 'SpeciesId': plant.speciesId, 'CommonName': plant.commonName,
                 'ImageUrl': image_url, 'DatePlanted': plant.datePlanted, 'LastWatering': last_watering,
                 'HealthStatus': health_status, 'Height': height, 'SoilPH': soil_ph, 'Light': light,
                 'SoilMoisture': soil_moisture, 'Edible': plant.edible, 'MinTemp': plant.minTemp,
                 'MaxTemp': plant.maxTemp, 'MinPH': plant.minPH, 'MaxPH': plant.maxPH,
                 'MinPrecipitation': plant.minPrecipitation, 'MaxPrecipitation': plant.maxPrecipitation,
                 'SoilHumidity': plant.soilHumidity, 'AtmosphericHumidity': plant.atmosphericHumidity,
                 'GardenerId': plant.gardenerId}
        log = {'PlantId': plant_id, 'Date': str(datetime.now()), 'ImageUrl': image_url,
               'WateredToday': bool(watered), 'HealthStatus': health_status, 'Height': height, 'SoilPH': soil_ph,
               'Light': light, 'SoilMoisture': soil_moisture}
        response = requests.put('https://localhost:44325/api/plant/', json=plant, verify=False)
        post_response = requests.post('https://localhost:44325/api/plant/post-log', json=log, verify=False)
        #if plant['edible']:
        #    edible_log = {'PlantId':plant_id, 'Date': str(datetime.today()), 'Quality': quality,
        #                  'Harvested': harvested, 'DaysToHarvest': health_status, 'AmountHarvested': height}
        return redirect(url_for('gardener.index'))
    else:
        log_response = requests.get(f'https://localhost:44325/api/plant/plant={plant_id}/index', verify=False)

        plant_logs = json.loads(log_response.content, object_hook=lambda d: SimpleNamespace(**d))
        if len(plant_logs) > 0:
            log_columns = ['date', 'wateredToday', 'healthStatus', 'height', 'soilPH', 'light', 'soilMoisture']
            df = pd.read_json(log_response.content)
            print(df)
            print(df['date'])
            date_labels = df['date'].to_list()
            dates = []
            for date_label in date_labels:
                log_date = datetime.date(date_label)
                dates.append(str(log_date))
            height_labels = df['height'].to_list()
            ph_labels = df['soilPH'].to_list()
            light_labels = df['light'].to_list()
            moisture_labels = df['soilMoisture'].to_list()
            log_dates = html.unescape(dates)
            height_logs = html.unescape(height_labels)
            ph_logs = html.unescape(ph_labels)
            light_logs = html.unescape(light_labels)
            moisture_logs = html.unescape(moisture_labels)
            return render_template('gardener/update.html', plant_id=plant_id, plant=plant, plant_logs=plant_logs,
                                   log_columns=log_columns, log_dates=log_dates, height_logs=height_logs, ph_logs=ph_logs,
                                   light_logs=light_logs, moisture_logs=moisture_logs)
        else:
            log_columns = ['date', 'wateredToday', 'healthStatus', 'height', 'soilPH', 'light', 'soilMoisture']

            return render_template('gardener/update.html', plant_id=plant_id, plant=plant, plant_logs=plant_logs,
                                   log_columns=log_columns, log_dates=[], height_logs=[],
                                   ph_logs=[], light_logs=[], moisture_logs=[])


@bp.route('/search', methods=('GET', 'POST'))
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
        gardener.first_search = True
        common_name = request.form['common_name']
        species_id = request.form['species_id']
        response = requests.get(f'https://trefle.io/api/v1/species/{species_id}?token={trefle_token}')
        result = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d)).data
        print(result)
        return render_template('gardener/plant_details.html', page_title=common_name, result=result)
    elif request.method == 'POST' and gardener.first_search and gardener.found_plant:
        gardener.found_plant = False
        common_name = request.form['common_name']
        image_url = request.form['image_url']
        species_id = np.double(request.form['species_id'])
        user_id = session.get('user_id')
        plant = {'CommonName': common_name, 'SpeciesId': species_id, 'DatePlanted': str(datetime.now()),
                 'ImageUrl': image_url, 'GardenerId': user_id}
        response = requests.post('https://localhost:44325/api/plant/post-plant', json=plant, verify=False)

        #response = requests.get(f'https://trefle.io/api/v1/plants?token={trefle_token}&filter[common_name]='
                                #f'{common_name}')
        #search_results = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d)).data
        #columns = ["common_name", "scientific_name", "family_common_name", "family"]
        return redirect(url_for('gardener.index'))
    else:
        gardener.first_search = True
        return render_template('gardener/search.html')


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


@login_required
@bp.route('/water_plants', methods=('GET', 'POST'))
def water_plants():
    current_weather = get_current_weather(user=g.user)
    #yesterdays_weather = get_historical_weather(user=user, days_ago=1)
    #two_days = get_historical_weather(user=user, days_ago=2)
    #three_days = get_historical_weather(user=user, days_ago=3)
    #four_days = get_historical_weather(user=user, days_ago=4)
    #weather_df = get_weather_df(current_weather, yesterdays_weather, two_days, three_days, four_days)
    if current_weather.daily[0].pop < 50:
        auth.send_text(g.user, "You should water your plants today.")
    else:
        auth.send_text(g.user, "You do not need to water your plants today.")
    return redirect(url_for('gardener.index'))

