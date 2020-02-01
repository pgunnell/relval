#definition of a JSON for a request

class JSONPrototype():

    dataset_name = ''
    datatier = ''
    cmssw_release = ''

    def __init__(self,dataset_name,datatier,cmssw_release):
            
        self.dataset_name = dataset_name
        self.datatier = datatier
        self.cmssw_release = cmssw_release

    def get_json_format(self):
        
        json = {"dataset_name":self.dataset_name,"datatier":self.datatier,"cmssw_release":self.cmssw_release}
        return json

