import json
import requests
from types import SimpleNamespace


class Plant:
    def __init__(self, _id, _growth_id, _specifications_id, _images_id, _distribution_id, _date_planted,
                 _date_harvested, _last_watering, _health_status, _height, _soil_ph, _light,_soil_moisture,
                 _amount_harvested):
        self.id = _id
        self.growth_id = _growth_id
        self.specifications_id = _specifications_id
        self.images_id = _images_id
        self.distribution_id = _distribution_id
        self.date_planted = _date_planted
        self.date_harvested = _date_harvested
        self.last_watering = _last_watering
        self.health_status = _health_status
        self.height = _height
        self.soil_ph = _soil_ph
        self.light = _light
        self.soil_moisture = _soil_moisture
        self.amount_harvested = _amount_harvested

    @staticmethod
    def plant_decoder(obj):
        return Plant(obj['_id'], obj['_date_planted'], obj['_date_harvested'], obj['_last_watering'],
                     obj['_health_status'], obj['_height'], obj['_soil_ph'], obj['_light'], obj['_soil_moisture'])


##Not sure what I will be putting in here at the moment.
##Leaving framework for reference.
response = requests.get('https://trefle.io/api/v1/plants/search?token=')

#json_data_dict = json.loads(response)
plants = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))


###plants = plant.plant_decoder(json_data_dict)
