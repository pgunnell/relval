from core.model.model_base import ModelBase

class Campaign(ModelBase):

    _ModelBase__schema = {
        # Database id
        '_id': '',
        # PrepID
        'prepid': '',
        # Energy in TeV
        'energy': 0.0,
        # Type LHE, MCReproc, Prod
        'type': '',
        # Step type: MiniAOD, NanoAOD, etc.
        'step': 'DR',
        # No need for CMSSW version
        #'cmssw_release': '',
        # User notes
        'notes': '',
        # List of dictionaries that have cmsDriver options (default to be modified, just a guideline, what is normally needed)
        'sequences': [{"conditions","GT_FromAlca","step","RAW2DIGI,L1Reco,RECO,EI,PAT,DQM:@rerecoCommon","datatier":"AOD,MINIAOD,DQM","eventcontent":"RECO,SKIM,ALCA,MINIAOD,DQMIO","era":"Run2_201XXX","extra":"--runUnscheduled","scenario":"pp","nThreads","8","customise":"Configuration/DataProcessing/RecoTLR.customisePostEra_Run2_201XXX"}],
        # Action history
        'history': [],
        # Default memory
        'memory': 2300}

    __lambda_checks = {
        'prepid': lambda prepid: ModelBase.matches_regex(prepid, '[a-zA-Z0-9]{1,50}'),
        'energy': lambda energy: energy >= 0.0,
        'step': lambda step: step in ['DR', 'MiniAOD', 'NanoAOD'],
        'memory': lambda memory: memory >= 0,
        'cmssw_release': lambda cmssw_release: 'CMSSW' in cmssw_release
    }

    def __init__(self, json_input=None):
        ModelBase.__init__(self, json_input)

    def check_attribute(self, attribute_name, attribute_value):
        if attribute_name in self.__lambda_checks:
            return self.__lambda_checks.get(attribute_name)(attribute_value)

        return True
