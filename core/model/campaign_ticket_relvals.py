"""
Module that contains CampaignTicket class
"""
from core.model.model_base import ModelBase


class CampaignTicket(ModelBase):
    """
    Campaign ticket has a list of input datasets, a campaign and a processing string
    Campaign ticket can be used to create requests for each input dataset
    """

    _ModelBase__schema = {
        # Database id (required by CouchDB)
        '_id': '',
        # Document revision (required by CouchDB)
        '_rev': '',
        # PrepID
        'prepid': '',
        # Name of campaign that is used as template for requests
        'conditions_globaltag': '',
        # Processing string for this ticket (label at the time of the submission)
        'processing_string': '',
        # List of prepids of requests that were created from this ticket
        'created_requests': [],
        # Status is either new or done
        'status': 'new',
        # User notes
        'notes': '',
        #CMSSW_release
        'cmssw_release':'CMSSW_ToBeIncludeFromValManagers',
        #sample tag (to be chosen from a list)
        'sample_tag':'',
        #pile_up production (to be chosen from a list)
        'pile_up':'',
        #high_statistics production (True or False)
        'high_statistics': False,
        #string for GS input
        'string_for_inputGS':''
        #GEN-SIM samples to be re-used?
        'ReUseGenSim': False,
        #extension number (just a number, if a similar sample was already submitted, observed especially in Phase II)
        'extension_number':0,
        # Action history
        'history': []
    }

    _lambda_checks = {
        'prepid': lambda prepid: ModelBase.matches_regex(prepid, '[a-zA-Z0-9_\\-]{1,50}'),
        'conditions_globaltag': lambda gt: ModelBase.matches_regex(gt, '[a-zA-Z0-9_\\-]{1,50}'),
        'cmssw_release': lambda cmssw_release: ModelBase.matches_regex(cmssw_release, '[a-zA-Z0-9_\\-]{1,50}'),
        'processing_string': lambda ps: ModelBase.matches_regex(ps, '[a-zA-Z0-9_]{0,100}'),
        'status': lambda status: status in ('new', 'done'),
        'sample_tag': lambda sample_tag: sample_tag in ('Run2_2016', 'Run2_2017', 'Run2_2018', 'fastSim_2016', 'fastSim_2017','fastSim_2018' 'Run3', 'PhaseII','customized'),
        'pile_up': lambda pile_up: pile_up in ('classical_mixing', 'premix','no_pile_up'),
        'high_statistics': lambda high_statistics: isinstance(high_statistics,bool),
        'ReUseGenSim': lambda ReUseGenSim: isinstance(ReUseGenSim,bool),
        'extension_number': lambda extension_number: isinstance(extension_number,int),
        'string_for_inputGS': lambda string_for_inputGS: ModelBase.matches_regex(string_for_inputGS, '[a-zA-Z0-9_\\-]{1,50}')
    }

    def __init__(self, json_input=None):
        ModelBase.__init__(self, json_input)
