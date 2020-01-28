from core.model.model_base import ModelBase

class Flow(ModelBase):

    _ModelBase__schema = {
        # Database id
        '_id': '',
        # PrepID
        'prepid': '',
        # List of allowed source campaigns prepids
        'source_campaigns': [],
        # List of statuses for the flow
        'status': '',
        # Target campaign prepid
        'target_campaign': ''}

    __lambda_checks = {
        'prepid': lambda prepid: ModelBase.matches_regex(prepid, '[a-zA-Z0-9]{1,50}')
        'status': lambda status: status in ['new','submit','tasksubmit'])
    }

    def __init__(self, json_input=None):
        ModelBase.__init__(self, json_input)
        self.collection = 'flows'

    def check_attribute(self, attribute_name, attribute_value):
        if attribute_name in self.__lambda_checks:
            return self.__lambda_checks.get(attribute_name)(attribute_value)

        return True

    def add_source_campaign(self, source_campaign):
        source_campaign_prepid = source_campaign.get('prepid')
        source_campaigns = self.get('source_campaigns')
        target_campaign_prepid = self.get('target_campaign')
        if source_campaign_prepid == target_campaign_prepid:
            raise Exception('Campaign %s cannot be added as a source campaign as it is a target campaign' % (target_campaign_prepid))

        if source_campaign_prepid in source_campaigns:
            raise Exception('Campaign %s alrady exists as %s source campaign' % (source_campaign_prepid, self.get_prepid()))

        source_campaigns.append(source_campaign_prepid)
        self.set('source_campaigns', source_campaigns)

    def remove_source_campaign(self, source_campaign):
        source_campaign_prepid = source_campaign.get('prepid')
        source_campaigns = self.get('source_campaigns')
        if source_campaign_prepid not in source_campaigns:
            raise Exception('Campaign %s is not %s source campaign' % (source_campaign_prepid, self.get_prepid()))

        source_campaigns.remove(source_campaign_prepid)
        self.set('source_campaigns', source_campaigns)

    def set_target_campaign(self, target_campaign):
        if not target_campaign:
            self.set('target_campaign', '')
            return

        target_campaign_prepid = target_campaign.get('prepid')
        source_campaigns = self.get('source_campaigns')
        if target_campaign_prepid in source_campaigns:
            raise Exception('Campaign %s is already a source campaign' % (target_campaign_prepid))

        self.set('target_campaign', target_campaign_prepid)
