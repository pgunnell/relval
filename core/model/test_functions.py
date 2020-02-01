from build_driver_relvals import *
from create_dict_relvals import *

print(define_samples('Phase2'))

campaign_ticket_json = {
    'prepid': 'minz',
    'conditions_globaltag': 'minz_v10_pre3',
    'processing_string': 'jenniminz',
    'cmssw_release':'CMSSW_10_2_18',
    'sample_tag':'Phase2',
    'pile_up':'NoPileUp',
    'high_statistics': False,
    'string_for_inputGS': 'MinzInput',
    'ReUseGenSim': True,
    'extension_number':0,
}

print(driver_GENSIM(campaign_ticket_json))
print('****')
print(driver_DIGI(campaign_ticket_json))
print('****')
print(driver_RECO(campaign_ticket_json))
print('****')
print(driver_NANO(campaign_ticket_json))

print('****')

campaign_json = { 
    'conditions' : 'minz',
    'process_string' : 'minz_ps',
    'prepid' : 'test_upload'
}      

chained_request_json = {
    'chain' : 
        {
            0:
            {
                'cmssw_release': 'CMSSW_10_2_18',
                'dataset_name': 'Minz1',
                'total_events': 10,
                'type': 'MiniMinz',
                'prepid' : 'Minz-1',
                'input_pileup_dataset':''
            },

            1:
            {
                'cmssw_release': 'CMSSW_10_2_18',
                'dataset_name': 'Minz2',
                'total_events': 10,
                'type': 'MiniMinz',
                'input_pileup_dataset':'',
                'prepid' : 'Minz-1'
            }
        }
}

print(chained_request_json['chain'][0])

dict_file = build_dictionary(chained_request_json,campaign_json)

import os
import urllib
import httplib
import imp
import sys
import time
import json

def makeRequest(url, params, encodeDict=False):
    ##TO-DO import json somewhere else globally. for now this fix is wmcontrol submission
    import json

    headers = {"Content-type": "application/json",
            "Accept": "application/json"}

    conn = httplib.HTTPSConnection(url, cert_file=os.getenv('X509_USER_PROXY'),
            key_file=os.getenv('X509_USER_PROXY'))

    ##TO-DO do we move it to top of file?
    __service_url  = "/reqmgr2/data/request"
    print "Will do POST request to:%s%s" % (url, __service_url)
    conn.request("POST", __service_url, json.dumps(params), headers)
    response = conn.getresponse()
    data = response.read()

    if response.status != 200:
        print 'could not post request with following parameters:'
        print json.dumps(params, indent=4)
        print
        print 'Response from http call:'
        print 'Status:', response.status, 'Reason:', response.reason
        print 'Explanation:'
        print data
        print "Exiting!"
        sys.exit(1)

    workflow = json.loads(data)['result'][0]['request']
    print 'Injected workflow:', workflow

    conn.close()
    return workflow

with open('master_example_forrelval.conf') as f:
  data = json.load(f)


#workFlow=makeRequest('cmsweb.cern.ch',data,encodeDict=True)

from json_class import *

json_test = JSONPrototype('minz','minminz','miminz')

print(json_test.get_json_format())


def upload_to_couch(cfg_name, section_name, user_name, group_name, test_mode=False, url=None):
    if test_mode:
        return "00000000000000000"

    if not os.path.exists(cfg_name):
        raise RuntimeError("Error: Can't locate config file %s." % cfg_name)

    # create a file with the ID inside to avoid multiple injections
    oldID = cfg_name + '.couchID'

    if os.path.exists(oldID):
        f = open(oldID)
        the_id = f.readline().replace('\n','')
        f.close()
        print cfg_name, 'already uploaded with ID', the_id, 'from', oldID
        return the_id

    try:
        loadedConfig = __loadConfig(cfg_name)
    except:
        #just try again !!
        time.sleep(2)
        loadedConfig = __loadConfig(cfg_name)

    where = COUCH_DB_ADDRESS
    if url:
        where = url

    configCache = ConfigCache(where, DATABASE_NAME)
    configCache.createUserGroup(group_name, user_name)
    configCache.addConfig(cfg_name)
    configCache.setPSetTweaks(makeTweak(loadedConfig.process).jsondictionary())
    configCache.setLabel(section_name)
    configCache.setDescription(section_name)
    configCache.save()

    print "Added file to the config cache:"
    print "  DocID:    %s" % configCache.document["_id"]
    print "  Revision: %s" % configCache.document["_rev"]

    f = open(oldID,"w")
    f.write(configCache.document["_id"])
    f.close()
    return configCache.document["_id"]
