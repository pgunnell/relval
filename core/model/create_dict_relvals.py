#This script tries to build the dictionary for relval submission from the driver we have created before

def build_dictionary(chained_request,campaign):

    #API method to GET requests from chained request
    chain = chained_request['chain']
    request = []

    for single_request in chain:
        #request.append(mcm.get('requests', single_request))
        request.append(single_request)

    filename = 'master1_'+str(chain[0]['prepid'])+'.conf'

    file_dict = open(filename,"w") 
   
    file_dict.write("{'AcquisitionEra': %s ,\n" % chain[0]['cmssw_release'])
    file_dict.write("'CMSSWVersion': %s ,\n" % chain[0]['cmssw_release'])
    file_dict.write("'Campaign': %s \n" % campaign['prepid'])
    file_dict.write("'ConfigCacheUrl': 'https://cmsweb.cern.ch/couchdb',\n")


    #dict_relval = {'AcquisitionEra': request[0]['cmssw_release'],
    #               'CMSSWVersion': request[0]['cmssw_release'],
    #               'Campaign': campaign['prepid'] #request[0]['cmssw_release']+'_'+str(campaign['process_string'])+'-'+str(random(100000))
    #               'ConfigCacheUrl': 'https://cmsweb.cern.ch/couchdb',
    #               'DbsUrl': 'https://cmsweb.cern.ch/dbs/prod/global/DBSReader',
    #               'GlobalTag': campaign['conditions'],
    #               'Group': 'ppd',
    #               'Memory': 3000,
    #               'Multicore': 1,
    #               'PrepID': 'CMSSW_10_6_8__UL16-1579987288-TTbarLepton_13UP16',
    #               'ProcessingString': str(campaign['conditions'])+'_'+str(campaign['process_string']),
    #               'ProcessingVersion': 1,
    #               'RequestPriority': 500000,
    #               'RequestString': 'RV'+str(request[0]['cmssw_release'])+'_'+str(campaign['conditions'])+'_'+str(campaign['process_string']),
    #               'RequestType': 'TaskChain',
    #               'Requestor': 'pgunnell',
    #               'ScramArch': 'slc7_amd64_gcc820',
    #               'SizePerEvent': 1234,
    #               'SubRequestType': 'RelVal'}

    memory = 14000
    splittingalgo='LumiBased'

    for i in range(0,len(chain)):

        if(chain[i]['type']=='GEN-SIM'):
            splittingalgo='EventBased'
            memory = 3000
        else:
            splittingalgo='LumiBased'
            memory = 14000

        configCacheId = 1041+i

        dict_additions = ""
        dict_input = ""

        if(i>0):
            dict_additions = {
                'InputFromOutputModule': str(chain[i-1]['type'])+'output',
                'InputTask': chain[i-1]['dataset_name']+'_to_be_completed+str(chain_type)', 
                'LumisPerJob': 10}
            
            if(chain[i]['type']=='DIGI'):
                dict_input = "'MCPileup':%s",

        file_dict.write("{ 'Task%s':\n" % str(i))
        file_dict.write("{'AcquisitionEra': %s,\n" % chain[i]['cmssw_release'])
        #                 'Campaign': campaign['prepid'],\n
        #                 'ConfigCacheID': configcacheId,\n
        #                 'EventsPerJob': 100,\n
        #                 'GlobalTag': campaign['conditions'],\n
        #                        'KeepOutput': True,\n
        #                 'Memory': memory,\n
        #                 'Multicore': 1,\n
        #                 'PrimaryDataset': 'RelVal'+str(chain[i]['dataset_name']),\n
        #                 'ProcessingString': str(campaign['conditions'])+'_'+str(campaign['process_string']),\n
        #                 'ChainNumEvents': chain[i]['total_events'],\n
        #                 'Seeding': 'AutomaticSeeding',\n
        #                 'SplittingAlgo': splittingalgo,\n
        #                 'TaskName': chain['dataset_name']+'_to_be_completed', #str(chain['type'])\n
        #,dict_additions \n
        #dict_input\n
        file_dict.write("}\n")
        file_dict.write("}\n")
    
    file_dict.write("'TaskChain': 4,\n")
    file_dict.write("'TimePerEvent': 10}")
    file_dict.close()

    return file_dict
