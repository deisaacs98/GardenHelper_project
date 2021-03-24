import json
import requests
from types import SimpleNamespace


class gardener:
    def __init__(self, _id, ):
        self._id = _id


    @staticmethod
    def gardener_decoder(obj):
        return gardener(obj['_id'])


##Not sure what I will be putting in here at the moment.
##Leaving framework for reference.
#response = requests.get('put REST API url here')

#json_data_dict = json.loads(response)

#gardeners = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))


###gardeners = gerdener.gardener_decoder(json_data_dict)
