import json
import requests
from types import SimpleNamespace


class Growth:
    def __init__(self, _id, days_to_harvest, _description, _sowing, _ph_maximum, _ph_minimum,
                 _light, _atmospheric_humidity, _grow_months, _bloom_months, _fruit_months, _row_spacing, _spread,
                 _minimum_precipitation, _maximum_precipitation, _minimum_temperature, _maximum_temperature,
                 _soil_humidity):
        self.id = _id
        self.days_to_harvest = days_to_harvest
        self.description = _description
        self.sowing = _sowing
        self.ph_maximum = _ph_maximum
        self.ph_minimum = _ph_minimum
        self.light = _light
        self.atmospheric_humidity = _atmospheric_humidity
        self.grow_months = _grow_months
        self.bloom_months = _bloom_months
        self.fruit_months = _fruit_months
        self.row_spacing = _row_spacing
        self.spread = _spread
        self.minimum_precipitation = _minimum_precipitation
        self.maximum_precipitation = _maximum_precipitation
        self.minimum_temperature = _minimum_temperature
        self.maximum_temperature = _maximum_temperature
        self.soil_humidity = _soil_humidity

    @staticmethod
    def gardener_decoder(obj):
        return Growth(obj['_id'], obj['days_to_harvest'],obj['_description'], obj['_sowing'],  obj['_ph_maximum'],
                      obj['_ph_minimum'], obj['_light'], obj['_atmospheric_humidity'],  obj['_grow_months'],
                      obj['_bloom_months'], obj['_fruit_months'], obj['_row_spacing'], obj['_spread'],
                      obj['_minimum_precipitation'], obj['_maximum_precipitation'], obj['_minimum_temperature'],
                      obj['_maximum_temperature'], obj['_soil_humidity'])


##Not sure what I will be putting in here at the moment.
##Leaving framework for reference.
#response = requests.get('put REST API url here')

#json_data_dict = json.loads(response)

#gardeners = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))


###gardeners = gerdener.gardener_decoder(json_data_dict)
