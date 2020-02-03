#Build drivers for the different options which are specified in the campaign ticket
#The rationale is to have almost completely prepared drivers for the relvals campaigns specified in the ticket

from json_class import *

def build_driver_main(campaign_ticket):

    #Each driver will have four/five requests chained into a task chain
    #Here we chain all the drivers into a list which can be used for the requests
    #The choice of four or five drivers is dictated by the fact of reusing GEN-SIM or not
    driver=[]
    
    if(not(campaign_ticket['ReUseGenSim'])):
        driver.append(driver_GENSIM(campaign_ticket))

    driver.append(driver_DIGI(campaign_ticket))
    driver.append(driver_RECO_MINIAOD(campaign_ticket))
    driver.append(driver_NANOAOD(campaign_ticket))
    driver.append(driver_HARVEST(campaign_ticket))

    #this is a list of drivers
    return driver

def driver_GENSIM(campaign_ticket):

    number_events = 9000
    conditions=campaign_ticket['conditions_globaltag']
    
    if(campaign_ticket['high_statistics']):
        number_events = 100000

    driver_arguments=get_driver_arguments(campaign_ticket['sample_tag'])

    #one gets a list from that
    GEN_samples = define_samples(campaign_ticket['sample_tag'])

    driver = []

    for i in GEN_samples:

        driver.append('cmsDriver step1 Configuration/Generator/'+str(i)+'.py --conditions '+str(driver_arguments['conditions'])+' --era '+str(driver_arguments['era'])+' --beamspot '+str()+' --geometry '+str(driver_arguments['geometry'])+' -n '+str(number_events)+' --eventcontent FEVTDEBUG -s GEN,SIM --datatier GEN-SIM --fileout file:step1.root --python_name '+str(i)+'_GS_cfg.py --nThreads 8') 

    return driver

def driver_DIGI(campaign_ticket):

    conditions=campaign_ticket['conditions_globaltag']

    driver_arguments=get_driver_arguments(campaign_ticket['sample_tag'])
    driver_forPU='to_be_defined'

    if(campaign_ticket['pile_up']=='premix'):
        driver_forPU='--procModifiers premix_stage2 --datamix PreMix --pileup_input das:/RelValPREMIXUP15_PU25/'+str(campaign_ticket['string_for_inputGS'])+'/PREMIX'

    elif(campaign_ticket['pile_up']=='NoPileUp'):
        driver_forPU='--pileup NoPileUp'

    if(campaign_ticket['pile_up']=='classical_mixing'):
        driver_forPU='--pileup '+str(driver_arguments['pile_up_scenario'])+' --pileup_input das:/RelVal'+str(i)+'/'+str(campaign_ticket['string_for_inputGS'])+'/GEN-SIM'
        
    driver=[]
        
    if(campaign_ticket['ReUseGenSim']):
        
        GEN_samples = define_samples(campaign_ticket['sample_tag'])

        for i in GEN_samples:
            driver.append('cmsDriver step2 --conditions '+str(driver_arguments['conditions'])+' --era '+str(driver_arguments['era'])+' --python_name '+str(i)+'_DIGI_cfg.py --geometry '+str(driver_arguments['geometry'])+' --eventcontent FEVTDEBUGHLT -s DIGI:pdigi_valid,DATAMIX,L1,DIGI2RAW,HLT:'+str(driver_arguments['HLT'])+' --datatier GEN-SIM-DIGI-RAW-HLTDEBUG --fileout file:step2.root --nThreads 8 --filein dbs:/RelVal'+str(i)+'/'+str(campaign_ticket['string_for_inputGS'])+'/GEN-SIM '+driver_forPU)

    else:

        driver.append('cmsDriver step2 --conditions '+str(driver_arguments['conditions'])+' --python_name step2_DIGI_cfg.py --era '+str(driver_arguments['era'])+' --geometry '+str(driver_arguments['geometry'])+' --eventcontent FEVTDEBUGHLT -s DIGI:pdigi_valid,DATAMIX,L1,DIGI2RAW,HLT:'+str(driver_arguments['HLT'])+' --datatier GEN-SIM-DIGI-RAW-HLTDEBUG --fileout file:step2.root --nThreads 8 --filein file:step1.root '+str(driver_forPU))

    return driver


def driver_RECO(campaign_ticket):

    conditions=campaign_ticket['conditions_globaltag']

    driver_arguments=get_driver_arguments(campaign_ticket['sample_tag'])

    driver_forPU=''

    driver = []

    if(campaign_ticket['pile_up']=='premix'):
        driver_forPU='--procModifiers premix_stage2'

    GEN_samples = define_samples(campaign_ticket['sample_tag'])

    for i in GEN_samples:

        driver.append('cmsDriver step3 --conditions '+str(driver_arguments['conditions'])+' --era '+str(driver_arguments['era'])+' --geometry '+str(driver_arguments['geometry'])+' --eventcontent RECOSIM,MINIAODSIM,DQM -s RAW2DIGI,L1Reco,RECO,RECOSIM,EI,PAT,VALIDATION:@standardValidation+@miniAODValidation,DQM:@standardDQM+@ExtraHLT+@miniAODDQM --python_name '+str(i)+'_RECO_MINIAOD_cfg.py --datatier GEN-SIM-RECO,MINIAODSIM,DQMIO --nThreads 8 --filein file:step2.root --fileout file:step3.root '+str(driver_forPU))

    return driver

def driver_NANO(campaign_ticket):

    conditions=campaign_ticket['conditions_globaltag']

    driver_arguments=get_driver_arguments(campaign_ticket['sample_tag'])

    driver = []

    GEN_samples = define_samples(campaign_ticket['sample_tag'])

    for i in GEN_samples:

        driver.append('cmsDriver step4 --conditions '+str(driver_arguments['conditions'])+' --era '+str(driver_arguments['era'])+' --python_name '+str(i)+'_NANO_cfg.py --eventcontent NANOEDMAODSIM -s NANO --datatier NANOAODSIM --nThreads 8 --filein file:step3_inMINIAODSIM.root --fileout file:step4.root')

    return driver

def driver_DQM(campaign_ticket):

    conditions=campaign_ticket['conditions_globaltag']

    driver_arguments=get_driver_arguments(campaign_ticket['sample_tag'])

    driver = []

    for i in GEN_samples:
        driver='cmsDriver HARVEST --filetype DQM --conditions '+str(driver_arguments['conditions'])+' --era '+str(driver_arguments['era'])+' --python_name '+str(i)+'_DQM_cfg.py -s HARVESTING:@rerecoCommon --filein file:RECO_RAW2DIGI_L1Reco_RECO_ALCA_EI_PAT_DQM_inDQM.root --fileout file:step4.root'

    return driver

def get_driver_arguments(sample_tag_of_campaign):

    tag = sample_tag_of_campaign

    geometry = 'geometry_default'
    beamspot = 'to_be_defined'
    era='to_be_defined'
    conditions_from_autoCond='to_be_defined'
    pile_up='to_be_defined'
    HLT='to_be_defined'

    driver_arguments = {}

    if(tag=='Run3'):
        geometry = 'DB:Extended'
        beamspot = 'Run3RoundOptics25ns13TeVLowSigmaZ'
        era='Run3'
        conditions_from_autoCond='auto:phase1_2021_realistic'
        pile_up='Run3_Flat55To75_PoissonOOTPU'
        
    elif(tag=='Phase2'):
        geometry = 'Extended2026D52'
        beamspot = 'HLLHC14TeV'
        era='Phase2C9'
        conditions_from_autoCond='auto:phase2_realistic_T15'
        pile_up='AVE_200_BX_25ns'

    elif(tag=='Run2_2016' or tag=='MinBias_PU_sample_2016' or tag=='premix_library_2016'):
        geometry = 'DB:Extended'
        beamspot = 'Realistic25ns13TeV2016Collision'
        era='Run2_2016'
        conditions_from_autoCond='auto:run2_mc'
        pile_up='2016_25ns_UltraLegacy_PoissonOOTPU'
        HLT='@relvals2016'

    elif(tag=='Run2_2017' or tag=='MinBias_PU_sample_2017' or tag=='premix_library_2017'):
        geometry = 'DB:Extended'
        beamspot = 'Realistic25ns13TeVEarly2017Collision'
        era='Run2_2017'
        conditions_from_autoCond='auto:phase1_2017_realistic'
        pile_up='2017_25ns_UltraLegacy_PoissonOOTPU'

    elif(tag=='Run2_2018' or tag=='MinBias_PU_sample_2018' or tag=='premix_library_2018'):
        geometry = 'DB:Extended'
        beamspot = 'Realistic25ns13TeVEarly2018Collision'
        era='Run2_2018'
        conditions_from_autoCond='auto:phase1_2018_realistic'
        pile_up='2018_25ns_UltraLegacy_PoissonOOTPU'

    driver_arguments['geometry']=geometry
    driver_arguments['beamspot']=beamspot
    driver_arguments['era']=era
    driver_arguments['conditions']=conditions_from_autoCond
    driver_arguments['pile_up_scenario']=pile_up
    driver_arguments['HLT']=HLT

    return driver_arguments


def define_samples(sample_tag_of_campaign):

    tag = sample_tag_of_campaign

    cfg_list = []

    if(tag=='Run3'):
        cfg_list.append('TTbar_14TeV_TuneCUETP8M1_cfi')
        cfg_list.append('MinBias_14TeV_cfi')
        cfg_list.append('QCD_Pt-15To7000_14TeV_cfi')

    elif(tag=='Run2_2016' or tag=='Run2_2017' or tag=='Run2_2018'):
        cfg_list.append('TTbar_13TeV_TuneCUETP8M1_cfi')
        cfg_list.append('MinBias_13TeV_cfi')
        cfg_list.append('ZEE_cfi')
        cfg_list.append('ZMM_cfi')

    elif(tag=='Phase2'):
        cfg_list.append('ZEE_14TeV_TuneCUETP8M1_cfi')
        cfg_list.append('ZMM_14TeV_TuneCUETP8M1_cfi')

    elif(tag=='MinBias_PU_sample_2016' or tag=='MinBias_PU_sample_2017' or tag=='MinBias_PU_sample_2018'):
        cfg_list.append('MinBias_13TeV_cfi')

    elif(tag=='premix_library_2016' or tag=='premix_library_2017' or tag=='premix_library_2018'):
        cfg_list.append('SingleNeutrino_cfi')

    return cfg_list

def create_json_requests(campaign_ticket):

    json_request_GS = []
    json_request_DIGI = []
    json_request_HLT = [] #if ever needed
    json_request_RECOMINIAOD = []
    json_request_DQM = []

    GEN_samples = define_samples(campaign_ticket['sample_tag'])
    ReUseGS = campaign_ticket['ReUseGenSim']


    for name_sample in GEN_samples:
        if(ReUseGS):
            #basic json file for GS request
            json_request_GS.append(JSONPrototype(str(name_sample)+'_GS','GEN-SIM',campaign_ticket['cmssw_release']).get_json_format())

        json_request_DIGI.append(JSONPrototype(str(name_sample)+'_DIGI','FEVTDEBUGHLT',campaign_ticket['cmssw_release']).get_json_format())
        #for now, we don't fill the HLT one
        json_request_RECOMINIAOD.append(JSONPrototype(str(name_sample)+'_RECO_MINIAOD','AODSIM,MINIAOD',campaign_ticket['cmssw_release']).get_json_format())
        json_request_DQM.append(JSONPrototype(str(name_sample)+'_HARVEST','DQMIO',campaign_ticket['cmssw_release']).get_json_format())

    #it returns a list of json files which can be used to create the requests in the tool
    return json_request_GS,json_request_DIGI,json_request_HLT,json_request_RECOMINIAOD,json_request_DQM

