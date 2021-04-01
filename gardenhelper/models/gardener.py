import json
import requests
from types import SimpleNamespace
import pandas as pd
from gardenhelper.auth import login_required
from gardenhelper.auth import load_logged_in_user

##Model is not necessary at this point, but leaving in case it is useful later.
class Gardener:

    def __init__(self, _id, _first_name, _middle_initial, _last_name, _email, _address_line1, _address_line2, _city,
                 _state, _zip, _phone, _lat, _lng):
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


    @staticmethod
    def gardener_decoder(obj):
        return Gardener(obj['_id'], obj['_first_name'], obj['_middle_initial'], obj['_last_name'], obj['_email'],
                        obj['_address_line1'], obj['_address_line2'], obj['_city'],  obj['_state'],
                        obj['_zip'], obj['_phone'], obj['_lat'], obj['_lng'])


first_search = True
found_plant = False
