#This script tries to build the dictionary for relval submission from the driver we have created before

def build_dictionary(chained_request,campaign):

    #API method to GET requests from chained request
    chain = chained_request['chain']
    request = []

    for single_request in chain:
        request.append(mcm.get('requests', single_request))

    dict_relval = {'AcquisitionEra': request[0]['cmssw_release'],
                   'CMSSWVersion': request[0]['cmssw_release'],
                   'Campaign': campaign['prepid'] #request[0]['cmssw_release']+'_'+str(campaign['process_string'])+'-'+str(random(100000))
                   'ConfigCacheUrl': 'https://cmsweb.cern.ch/couchdb',
                   'DbsUrl': 'https://cmsweb.cern.ch/dbs/prod/global/DBSReader',
                   'GlobalTag': campaign['conditions'],
                   'Group': 'ppd',
                   'Memory': 3000,
                   'Multicore': 1,
                   'PrepID': 'CMSSW_10_6_8__UL16-1579987288-TTbarLepton_13UP16',
                   'ProcessingString': str(campaign['conditions'])+'_'+str(campaign['process_string']),
                   'ProcessingVersion': 1,
                   'RequestPriority': 500000,
                   'RequestString': 'RV'+str(request[0]['cmssw_release'])+'_'+str(campaign['conditions'])+'_'+str(campaign['process_string']),
                   'RequestType': 'TaskChain',
                   'Requestor': 'pgunnell',
                   'ScramArch': 'slc7_amd64_gcc820',
                   'SizePerEvent': 1234,
                   'SubRequestType': 'RelVal'}

    memory = 14000
    splittingalgo='LumiBased'

    for i in range(0,len(chain)):

        if(request[i]['type']=='GEN-SIM'):
            splittingalgo='EventBased'
            memory = 3000
        elif:
            splittingalgo='LumiBased'
            memory = 14000

        configCacheId = 1041+i

        dict_additions = ''
        dict_input = ''

        if(i>0):
            dict_additions = "
                'InputFromOutputModule': str(request[i-1]['type'])+'output',
                'InputTask': request['dataset_name']+'_to_be_completed+str(request_type)', 
                'LumisPerJob': 10"
           
                if(request[i]['type']=='DIGI'):
                    dict_input = "'MCPileup':%s", %request[i]['input_pileup_dataset']

        dict_relval.append('Task'+str(i):
            {'AcquisitionEra': request[i]['cmssw_release'],
             'Campaign': campaign['prepid'],
             'ConfigCacheID': configcacheId,
             'EventsPerJob': 100,
             'GlobalTag': campaign['conditions'],
             'KeepOutput': True,
             'Memory': memory,
             'Multicore': 1,
             'PrimaryDataset': 'RelVal'+str(request[i]['dataset_name']),
             'ProcessingString': str(campaign['conditions'])+'_'+str(campaign['process_string'])
             'RequestNumEvents': request[i]['total_events'],
             'Seeding': 'AutomaticSeeding',
             'SplittingAlgo': splittingalgo,
             'TaskName': request['dataset_name']+'_to_be_completed', #str(request['type'])
             dict_additions
             dict_input
         }
        )


    dict_relval+="
            'TaskChain': 4,
            'TimePerEvent': 10}"

    return dict_relval
