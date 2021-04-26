class Distribution:
    def __init__(self, _id, _native, _introduced, _doubtful, _absent, _extinct):
        self.id = _id
        self.native = _native
        self.introduced = _introduced
        self.doubtful = _doubtful
        self.absent = _absent
        self.extinct = _extinct

    @staticmethod
    def distribution_decoder(obj):
        return Distribution(obj['_id'], obj['_native'], obj['_introduced'], obj['_doubtful'],  obj['_absent'],
                            obj['_extinct'])


##Not sure what I will be putting in here at the moment.
##Leaving framework for reference.
#response = requests.get('put REST API url here')

#json_data_dict = json.loads(response)

#gardeners = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))


###gardeners = gerdener.gardener_decoder(json_data_dict)
