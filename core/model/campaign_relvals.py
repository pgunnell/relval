from core.model.model_base import ModelBase

class Campaign(ModelBase):

    _ModelBase__schema = {
        # Database id
        '_id': '',
        # PrepID
        'prepid': '',
        # No need for CMSSW version
        'cmssw_release': '',
        #Sample tag
        'sample_tag': '',
        # User notes
        'notes': '',
        # User notes
        'link_prodmon': '',
        #history
        'history': []
    }

    __lambda_checks = {
        'prepid': lambda prepid: ModelBase.matches_regex(prepid, '[a-zA-Z0-9]{1,50}'),
        'link_prodmon': lambda link_prodmon: ModelBase.matches_regex(link_prodmon, '[a-zA-Z0-9]{1,50}'),
        'sample_tag': lambda sample_tag: sample_tag in ['Phase2', 'Run3', 'Run2_2016'],
        'cmssw_release': lambda cmssw_release: 'CMSSW' in cmssw_release
    }

    def __init__(self, json_input=None):
        ModelBase.__init__(self, json_input)

    def check_attribute(self, attribute_name, attribute_value):
        if attribute_name in self.__lambda_checks:
            return self.__lambda_checks.get(attribute_name)(attribute_value)

        return True
