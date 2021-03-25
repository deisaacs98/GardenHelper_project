import json
import requests
from types import SimpleNamespace


class Images:
    def __init__(self, _id, _flower, _leaf, _habit, _fruit, _bark, _other):
        self.id = _id
        self.flower = _flower
        self.leaf = _leaf
        self.habit = _habit
        self.fruit = _fruit
        self.bark = _bark
        self.other = _other

    @staticmethod
    def images_decoder(obj):
        return Images(obj['_id'], obj['_flower'],obj['_leaf'], obj['_habit'], obj['_fruit'],
                      obj['_bark'], obj['_other'])


##Not sure what I will be putting in here at the moment.
##Leaving framework for reference.
#response = requests.get('put REST API url here')

#json_data_dict = json.loads(response)

#gardeners = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))


###gardeners = gerdener.gardener_decoder(json_data_dict)
