import json
import requests
from types import SimpleNamespace


class Gardener:
    def __init__(self, _id, _first_name, _middle_initial, _last_name, _email, _address_line1,_address_line2, _city,
                 _state, _zip, _phone, _lat, _lng, _plants):
        self.Id = _id
        self.FirstName = _first_name
        self.MiddleInitial = _middle_initial
        self.LastName = _last_name
        self.Email = _email
        self.AddressLine1 = _address_line1
        self.AddressLine2 = _address_line2
        self.City = _city
        self.State = _state
        self.Zip = _zip
        self.Phone = _phone
        self.Lat = _lat
        self.Lng = _lng
        self.Plants = _plants

    @staticmethod
    def gardener_decoder(obj):
        return Gardener(obj['_id'], obj['_first_name'], obj['_middle_initial'], obj['_last_name'], obj['_email'],
                        obj['_address_line1'], obj['_address_line2'], obj['_city'],  obj['_state'],
                        obj['_zip'], obj['_phone'], obj['_lat'], obj['_lng'], obj['_plants'])


##Not sure what I will be putting in here at the moment.
##Leaving framework for reference.
#response = requests.get('put REST API url here')

#json_data_dict = json.loads(response)

#gardeners = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
#response = requests.get('https://localhost:44325/api/gardener/{id}')

###gardeners = gardener.gardener_decoder(json_data_dict)
response = requests.get('https://trefle.io/api/v1/plants/search?token=')

#json_data_dict = json.loads(response)
plants = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))