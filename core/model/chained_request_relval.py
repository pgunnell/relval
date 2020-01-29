from core.model.model_base import ModelBase

class ChainedRequest(ModelBase):

    _ModelBase__schema = {
        # Database id
        '_id': '',
        # PrepID
        'prepid': '',
        # Notes
        'notes': '',
        # List of requests in the chained request
        'chain': []}

    __lambda_checks = {
        'prepid': lambda prepid: ModelBase.matches_regex(prepid, '[a-zA-Z0-9]{1,50}')
    }

    def __init__(self, json_input=None):
        ModelBase.__init__(self, json_input)

    def check_attribute(self, attribute_name, attribute_value):
        if attribute_name in self.__lambda_checks:
            return self.__lambda_checks.get(attribute_name)(attribute_value)

        return True
