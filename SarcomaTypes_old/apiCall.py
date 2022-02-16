# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 20:04:52 2021

@author: hungd
"""

from bravado.client import SwaggerClient
cbioportal = SwaggerClient.from_url('https://www.cbioportal.org/api/api-docs', 
                                    config={"validate_requests":False,
                                            "validate_responses":False,
                                            "validate_swagger_spec": False})

for a in dir(cbioportal):    
    cbioportal.__setattr__(a.replace(' ', '_').lower(), cbioportal.__getattr__(a))
    
muts = cbioportal.mutations.getMutationsInMolecularProfileBySampleListIdUsingGET(molecularProfileId="msk_impact_2017_mutations", # {study_id}_mutations gives default mutations profile for study     
                                                                                 sampleListId="msk_impact_2017_all", # {study_id}_all includes all samples    
                                                                                 projection="DETAILED" # include gene info
                                                                                 ).result()

cancerTypes = cbioportal.Cancer_Types.getAllCancerTypesUsingGET().result()

