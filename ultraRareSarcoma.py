# -*- coding: utf-8 -*-
"""
Created on Sun Feb 13 13:52:41 2022

@author: hungd
"""

#%% Imports

from bravado.client import SwaggerClient
import pandas as pd

#%% For Testing

filterOn = 'sarcoma'

#%% Start cbiportal client

def startCbiportalClient():
    cbioportal = SwaggerClient.from_url('https://www.cbioportal.org/api/api-docs',
                                    config={"validate_requests":False,"validate_responses":False,"validate_swagger_spec":False})
    return cbioportal

#%% Get all studies

def getListOfAllStudies(cbioportal):
    # Get all studies from client
    studies = cbioportal.Studies.getAllStudiesUsingGET().result()
    
    # Make a list of all study Ids
    studyIds = []
    for study in studies:
        studyIds.append(study.studyId)
    return studyIds

#%% Filter down list of studies to only those we care about based on CANCER_TYPE_DETAILED

def filterOnCancerTypeDetailed(cbioportal, studyIds, filterOn):
    df = pd.DataFrame()
    # Get clinical data for each study
    for i in range(len(studyIds)):
        clinDataInStudy = cbioportal.Clinical_Data.getAllClinicalDataInStudyUsingGET(studyId=studyIds[i]).result()
        
        # Find CANCER_TYPE_DETAILED
        for j in range(len(clinDataInStudy)):
            sample = clinDataInStudy[j]
            
            # Continue if not CANCER_TYPE_DETAILED
            if sample.clinicalAttributeId != 'CANCER_TYPE_DETAILED':
                continue

            # Filter down to sarcoma data
            if filterOn.lower() not in sample.value.lower():
                continue
            
            # Get Data
            cancerTypeDetailed = sample.value
            patientId = sample.patientId
            sampleId = sample.sampleId
            studyId = sample.studyId
            
            # Create temp df
            df_temp = pd.DataFrame({'cancerTypeDetailed': [cancerTypeDetailed],
                                    'patientId': [patientId], 
                                    'sampleId': [sampleId],
                                    'studyId': [studyId]})
            
            # Append df_temp to main df
            df = pd.concat([df, df_temp])
            
    # Get filtered stuides
    filteredStudies = list(set(list(df['studyId'])))
    return df, filteredStudies

#%% Add clinical data by patient

def addClinicalDataByPatient(cbioportal, df):
    # Get patient from each line of df
    for i in range(len(df)):
        print(i, 'out of', len(df))
        sample = cbioportal.Clinical_Data.getAllClinicalDataOfPatientInStudyUsingGET(patientId=df['patientId'].iloc[i], 
                                                                                     studyId=df['studyId'].iloc[i]).result()
        
        # Add each column to df from sample
        for j in range(len(sample)):
            if sample[j].clinicalAttributeId not in list(df.columns):
                df[sample[j].clinicalAttributeId] = None
            df[sample[j].clinicalAttributeId].iloc[i] = sample[j].value
    return df
        
#%% Add clinical data by Sample

def addClinicalDataBySample(cbioportal, df):
    # Get patient from each line of df
    for i in range(len(df)):
        print(i, 'out of', len(df))
        sample = cbioportal.Clinical_Data.getAllClinicalDataOfSampleInStudyUsingGET(sampleId=df['sampleId'].iloc[i], 
                                                                                    studyId=df['studyId'].iloc[i]).result()
        
        # Add each column to df from sample
        for j in range(len(sample)):
            if sample[j].clinicalAttributeId not in list(df.columns):
                df[sample[j].clinicalAttributeId] = None
            df[sample[j].clinicalAttributeId].iloc[i] = sample[j].value
    return df
    
#%% Get all Sample list Ids

def getSampleListIds(cbioportal):
    sampleLists = cbioportal.Sample_Lists.getAllSampleListsUsingGET().result()
    df_sampleListId = pd.DataFrame()
    for sample in sampleLists:
        studyId = sample.studyId
        sampleListId = sample.sampleListId
        df_temp = pd.DataFrame({'studyId': [studyId], 'sampleListId': [sampleListId]})
        df_sampleListId = pd.concat([df_sampleListId, df_temp])
    return df_sampleListId
    
#%% Get Molecular Profile Ids

def getMolecularProfileIds(cbioportal):
    molecularProfiles = cbioportal.Molecular_Profiles.getAllMolecularProfilesUsingGET().result()
    df_molecularProfileId = pd.DataFrame()
    for profile in molecularProfiles:
        studyId = profile.studyId
        molecularProfileId = profile.molecularProfileId
        df_temp = pd.DataFrame({'studyId': [studyId], 'molecularProfileId': [molecularProfileId]})
        df_molecularProfileId = pd.concat([df_molecularProfileId, df_temp])
    return df_molecularProfileId

#%% Merge SampleListIds with MolecularProfileIds

def mergeSampleListsWithMolecularProfile(df_sampleListId, df_molecularProfileId):
    df_molProf_sampleList_id = pd.merge(df_molecularProfileId, df_sampleListId, how='inner', on='studyId')
    return df_molProf_sampleList_id

#%% Filter down to only studies we care about

def filterMolProfSampleListByStudies(df_molProf_sampleList_id, filteredStudies):
    # Create column that indicates that it is a study we care about
    df_molProf_sampleList_id['studyOfInterest'] = False
    
    for i in range(len(df_molProf_sampleList_id)):
        if df_molProf_sampleList_id['studyId'].iloc[i] in filteredStudies:
            df_molProf_sampleList_id['studyOfInterest'].iloc[i] = True
    
    # Filter down to only studies we care about
    df_molProf_sampleList_id = df_molProf_sampleList_id[df_molProf_sampleList_id['studyOfInterest']]
    return  df_molProf_sampleList_id

#%% Get Mutation Data

def getMutationData(cbioportal, df_molProf_sampleList_id):
    df_mut = pd.DataFrame()
    for i in range(len(df_molProf_sampleList_id)):
        if i % 100 == 0:
            print('i =', i, 'out of', len(df_molProf_sampleList_id))
        try:
            sample = cbioportal.Mutations.getMutationsInMolecularProfileBySampleListIdUsingGET(molecularProfileId=df_molProf_sampleList_id['molecularProfileId'].iloc[i], 
                                                                                               sampleListId=df_molProf_sampleList_id['sampleListId'].iloc[i]).result()
        except:
            continue
        
        # Fill in temp table with each entry in sample
        for j in range(len(sample)):
            if j % 100 == 0:
                print('j =', j, 'out of', len(sample))
            df_temp = pd.DataFrame({'studyId': [sample[j].studyId],
                                    'patientId': [sample[j].patientId],
                                    'sampleId': [sample[j].sampleId],
                                    'alleleSpecificCopyNumber': [sample[j].alleleSpecificCopyNumber],
                                    'aminoAcidChange': [sample[j].aminoAcidChange],
                                    'center': [sample[j].center],
                                    'chr': [sample[j].chr],
                                    'driverFilter': [sample[j].driverFilter],
                                    'driverFilterAnnotation': [sample[j].driverFilterAnnotation],
                                    'driverTiersFilter': [sample[j].driverTiersFilter],
                                    'driverTiersFilterAnnotation': [sample[j].driverTiersFilterAnnotation],
                                    'endPosition': [sample[j].endPosition],
                                    'entrezGeneId': [sample[j].entrezGeneId],
                                    'fisValue': [sample[j].fisValue],
                                    'functionalImpactScore': [sample[j].functionalImpactScore],
                                    'gene': [sample[j].gene],
                                    'keyword': [sample[j].keyword],
                                    'linkMsa': [sample[j].linkMsa],
                                    'linkPdb': [sample[j].linkPdb],
                                    'linkXvar': [sample[j].linkXvar],
                                    'molecularProfileId': [sample[j].molecularProfileId],
                                    'mutationStatus': [sample[j].mutationStatus],
                                    'mutationType': [sample[j].mutationType],
                                    'namespaceColumns': [sample[j].namespaceColumns],
                                    'ncbiBuild': [sample[j].ncbiBuild],
                                    'normalAltCount': [sample[j].normalAltCount],
                                    'normalRefCount': [sample[j].normalRefCount],
                                    'proteinChange': [sample[j].proteinChange],
                                    'proteinPosEnd': [sample[j].proteinPosEnd],
                                    'proteinPosStart': [sample[j].proteinPosStart],
                                    'referenceAllele': [sample[j].referenceAllele],
                                    'refseqMrnaId': [sample[j].refseqMrnaId],
                                    'startPosition': [sample[j].startPosition],
                                    'tumorAltCount': [sample[j].tumorAltCount],
                                    'tumorRefCount': [sample[j].tumorRefCount],
                                    'uniquePatientKey': [sample[j].uniquePatientKey],
                                    'uniqueSampleKey': [sample[j].uniqueSampleKey],
                                    'validationStatus': [sample[j].validationStatus],
                                    'variantAllele': [sample[j].variantAllele],
                                    'variantType': [sample[j].variantType]})
            df_mut = pd.concat([df_mut, df_temp])
    return df_mut
    
#%% Main

if __name__ == '__main__':
    
    # Connect to Cbioportal
    cbioportal = startCbiportalClient()
    
    # Get study Ids
    studyIds = getListOfAllStudies(cbioportal)
    
    # Filter down list of studies to only those we care about based on CANCER_TYPE_DETAILED
    df, filteredStudies = filterOnCancerTypeDetailed(cbioportal, studyIds, filterOn)
    
    # Get all SampleListIds
    df_sampleListId  = getSampleListIds(cbioportal)
    
    # Get Molecular Profile Ids
    df_molecularProfileId = getMolecularProfileIds(cbioportal)
    
    # Merge SampleListIds with MolecularProfileIds 
    df_molProf_sampleList_id = mergeSampleListsWithMolecularProfile(df_sampleListId, df_molecularProfileId)
    
    # Filter down to only studies we care about
    df_molProf_sampleList_id = filterMolProfSampleListByStudies(df_molProf_sampleList_id, filteredStudies)
    
    # Get Mutations
    df_mut = getMutationData(cbioportal, df_molProf_sampleList_id)
    
    
        