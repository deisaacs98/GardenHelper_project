import json
import requests
from types import SimpleNamespace
import pandas as pd
from gardenhelper.api_keys import trefle_token


class Species:
    def __init__(self, _id, _growth_id, _distribution_id, _specifications_id, _images_id, _image_url,
                 _common_name, _scientific_name, _status, _rank, _family_common_name, _family, _genus_id,
                 _genus, _edible_part, _edible, _vegetable, _observations):
        self.id = _id
        self.growth_id = _growth_id
        self.distribution_id = _distribution_id
        self.specifications_id = _specifications_id
        self.images_id = _images_id
        self.image_url = _image_url
        self.common_name = _common_name
        self.scientific_name = _scientific_name
        self.status = _status
        self.rank = _rank
        self.family_common_name = _family_common_name
        self.family = _family
        self.genus_id = _genus_id
        self.genus = _genus
        self.edible_part = _edible_part
        self.edible = _edible
        self.vegetable = _vegetable
        self.observations = _observations

    @staticmethod
    def species_decoder(obj):
        return Species(obj['_id'], obj['_growth_id'], obj['_distribution_id'],  obj['_specifications_id'],
                       obj['_images_id'], obj['_images_url'], obj['common_name'], obj['_scientific_name'],
                       obj['_status'],  obj['_rank'], obj['_family_common_name'], obj['_family'], obj['_genus_id'],
                       obj['_genus'], obj['_edible_part'], obj['_edible'], obj['_vegetable'], obj['_observations'])


##Not sure what I will be putting in here at the moment.
##Leaving framework for reference.




###gardeners = gerdener.gardener_decoder(json_data_dict)
