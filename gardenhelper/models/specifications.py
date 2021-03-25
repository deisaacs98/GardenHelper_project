import json
import requests
from types import SimpleNamespace


class Specifications:
    def __init__(self, _id, _growth_rate, _average_height, _maximum_height, _toxicity):
        self.id = _id
        self.growth_rate = _growth_rate
        self.average_height = _average_height
        self.maximum_height = _maximum_height
        self.toxicity = _toxicity

    @staticmethod
    def specifications_decoder(obj):
        return Specifications(obj['_id'], obj['_growth_rate'],obj['_average_height'], obj['_maximum_height'],
                              obj['_toxicity'])


##Not sure what I will be putting in here at the moment.
##Leaving framework for reference.
#response = requests.get('put REST API url here')

#json_data_dict = json.loads(response)

#gardeners = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))


###gardeners = gerdener.gardener_decoder(json_data_dict)
