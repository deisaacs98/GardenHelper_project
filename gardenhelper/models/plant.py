import json
import requests
from types import SimpleNamespace
import pandas as pd
from gardenhelper.auth import load_logged_in_user, login_required


class Plant:
    def __init__(self, _id, _common_name, _date_planted,
                 _date_harvested, _last_watering, _health_status, _height, _soil_ph, _light,_soil_moisture,
                 _amount_harvested,_gardener_id,_gardener):
        self.id = _id
        self.commonName = _common_name
        self.datePlanted = _date_planted
        self.dateHarvested = _date_harvested
        self.lastWatering = _last_watering
        self.healthStatus = _health_status
        self.height = _height
        self.soilPH = _soil_ph
        self.light = _light
        self.soilMoisture = _soil_moisture
        self.amountHarvested = _amount_harvested
        self.gardenerId = _gardener_id
        self.gardener = _gardener

    @staticmethod
    def plant_decoder(obj):
        return Plant(obj['id'], obj,['commonName'], obj['datePlanted'], obj['dateHarvested'], obj['lastWatering'],
                     obj['healthStatus'], obj['height'], obj['soilPH'], obj['light'], obj['soilMoisture'],
                     obj['gardenerId'], obj['gardener'])


##Not sure what I will be putting in here at the moment.
##Leaving framework for reference.
#response = requests.get('https://trefle.io/api/v1/plants/search?token=')

#json_data_dict = json.loads(response)
#plants = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))


###plants = plant.plant_decoder(json_data_dict)



