from json_class import *
import json

def save_json(campaign_ticket, driver, datatier, name_sample):

    json_out = JSONPrototype(campaign_ticket['cmssw_release'], datatier , name_sample, driver)

    file_name = str(name_sample)+'_'+str(datatier)+'.json'

    print json_out.get_json_format()

    with open(file_name, 'w') as outfile:
        json.dump(json_out.get_json_format(), outfile)

