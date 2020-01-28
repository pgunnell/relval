from core.model.model_base import ModelBase

#These are the only features which are needed for a request
#No need for not keeping output -> output will always be kept

class Request(ModelBase):

    _ModelBase__schema = {
        # Database id
        '_id': '',
        # PrepID
        'prepid': '',
        # Energy in TeV
        'energy': 0.0,
        # Step type: MiniAOD, NanoAOD, etc.
        'step': '',
        # CMSSW version
        'cmssw_release': '',
        # User notes
        'notes': '',
        # Input dataset name
        'input_dataset_name': '',
        # Output dataset name
        'output_dataset_name': '',
        # List of dictionaries that have cmsDriver options
        'sequences': [],
        # Action history
        'history': [],
        # Status 
        'status': 'new', #it should be either approved, submitted, done (nothing else)
        # Workflow name in computing when submitted 
        'reqmgr_name': '', 
        # time event
        'time_event': 5.0, 
        # size event
        'size_event': 2000, 
        # priority
        'priority': 110000, 
        #runs for data injections
        'runs': [],
        #type, depends on the datatier of the requests
        'type':'',
        # process string
        'process_string': '', 
        # Default memory
        'memory': 14000,
        #all the following will be filled in after injection (they will be created at the time of the injection)
        #request id (to be filled in the dictionary of injection)
        'request_id': '',
        #reco cfg (to be filled in the dictionary of injection)
        'reco_cfg': '',
        #harvest cfg (to be filled in the dictionary of injection)
        'harvest_cfg': ''
        #dataset name (this is just the first split of the input dataset name, can be done automatically)
        'dataset_name': ''
    }

    __lambda_checks = {
        'prepid': lambda prepid: ModelBase.matches_regex(prepid, '[a-zA-Z0-9]{1,50}'),
        'energy': lambda energy: energy >= 0.0,
        'time_event': lambda time_event: time_event >= 0.0,
        'size_event': lambda size_event: size_event >= 0.0,
        'priority': lambda priority: priority >= 0.0,
        'DQM': lambda DQM: isinstance(DQM,bool),
        'Reco': lambda Reco: isinstance(Reco,bool),
        'step': lambda step: step in ['RAW2DIGI','L1Reco','RECO','EI','PAT','DQM','NANO'] or ['ALCARECO'] in step or ['DQM'] in step,
        'datatier': lambda datatier: datatier in ['AOD', 'MiniAOD', 'NanoAOD', 'DQMIO', 'USER', 'ALCARECO'],
        'memory': lambda memory: memory >= 0,
        'type' : lambda type_req: type_req in ['GEN-SIM','FEVTDEBUG','GEN-SIM-RAW','GEN-SIM-DIGI-RAW','GEN-SIM-DIGI-RAW-HLT','NANOAOD','AODSIM','MINIAOD','FEVTDEBUGHLT']
        'cmssw_release': lambda cmssw_release: 'CMSSW' in cmssw_release,
        'reco_cfg': lambda reco_cfg: ModelBase.matches_regex(reco_cfg, '[a-zA-Z0-9]{1,50}'),
        'harvest_cfg': lambda harvest_cfg: ModelBase.matches_regex(harvest_cfg, '[a-zA-Z0-9]{1,50}'),
        'process_string': lambda process_string: ModelBase.matches_regex(process_string, '[a-zA-Z0-9]{1,50}'),
        'request_id': lambda request_id: ModelBase.matches_regex(request_id, '[a-zA-Z0-9]{1,50}'),
        'dataset_name': lambda dataset_name: ModelBase.matches_regex(dataset_name, '[a-zA-Z0-9]{1,50}')
    }

    def __init__(self, json_input=None):
        ModelBase.__init__(self, json_input)

    def check_attribute(self, attribute_name, attribute_value):
        if attribute_name in self.__lambda_checks:
            return self.__lambda_checks.get(attribute_name)(attribute_value)

        return True
