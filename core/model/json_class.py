#definition of a JSON for a request

class JSONPrototype():

    dataset_name = ''
    datatier = ''
    cmssw_release = ''

    def __init__(self,dataset_name,datatier,cmssw_release,driver='to_be_defined'):
            
        self.dataset_name = dataset_name
        self.datatier = datatier
        self.cmssw_release = cmssw_release
        self.driver = driver

    def get_json_format(self):
        
        #this should be the request json file
        json = {"dataset_name":self.dataset_name,"datatier":self.datatier,"cmssw_release":self.cmssw_release,"driver":self.driver}
        return json

