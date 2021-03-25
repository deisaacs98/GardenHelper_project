import json
import requests
from types import SimpleNamespace


class Gardener:
    def __init__(self, _id, _first_name, _middle_initial, _last_name, _email, _address_line1,_address_line2, _city,
                 _state, _zip, _phone, _lat, _lng):
        self._id = _id
        self.first_name = _first_name
        self.middle_initial = _middle_initial
        self.last_name = _last_name
        self.email = _email
        self.address_line1 = _address_line1
        self.address_line2 = _address_line2
        self.city = _city
        self.state = _state
        self.zip = _zip
        self.phone = _phone
        self.lat = _lat
        self.lng = _lng

    @staticmethod
    def gardener_decoder(obj):
        return Gardener(obj['_id'], obj['_first_name'], obj['_middle_initial'], obj['_last_name'], obj['_email'],
                        obj['_address_line1'], obj['_address_line2'], obj['_city'],  obj['_state'],
                        obj['_zip'], obj['_phone'], obj['_lat'], obj['_lng'])


##Not sure what I will be putting in here at the moment.
##Leaving framework for reference.
#response = requests.get('put REST API url here')

#json_data_dict = json.loads(response)

#gardeners = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))


###gardeners = gerdener.gardener_decoder(json_data_dict)
