# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 20:14:41 2021

@author: hungd
"""

#%% imports

import pandas as pd
import os
import numpy as np
import json

#%% Output Path

output = os.getcwd() + r"\Results.xlsx"

#%% Read Files

def getFiles():
    myFiles = []
    root = os.getcwd()
    for path, subdirs, files in os.walk(root):
        for name in files:
            myFiles.append(os.path.join(path, name))
    return myFiles
        
#%% Clinical Data

def clinicalData(nameOfSarcoma, myFile):
           
    # Read Data
    if myFile.endswith(".csv"):
        df_cd = pd.read_csv(myFile)
    else:
        df_cd = pd.read_csv(myFile, delimiter="\t")
        
    # Get Sarcoma Type From Data
    nameOfSarcomaFromData = df_cd["Cancer Type Detailed"].iloc[0]
    
    # Number of Samples
    numberOfSamples = df_cd["Patient ID"].count()
    
    # Number of Patients
    numberOfPatients = df_cd["Patient ID"].drop_duplicates().count()
    
    # Mutations Blank
    mutationsBlank = df_cd[df_cd["Mutation Count"].isna()]["Patient ID"].count()
    
    # Mutations <= 2
    mutationsLT2 = df_cd[df_cd["Mutation Count"] <= 2]["Patient ID"].count()
    
    # Mutations 3-5
    mutations3To5 = df_cd[(df_cd["Mutation Count"] >= 3) & 
                          (df_cd["Mutation Count"] <= 5)]["Patient ID"].count()
    
    # Mutations 6-17
    mutations6To17 = df_cd[(df_cd["Mutation Count"] >= 6) & 
                          (df_cd["Mutation Count"] <= 17)]["Patient ID"].count()
    
    # Mutations >17
    mutationsGT17 = df_cd[df_cd["Mutation Count"] > 17]["Patient ID"].count()
            
    # Rename age column
    df_cd = df_cd.rename(columns={"Age at Which Sequencing was Reported": "age"})
    
    # Get unique patients and age
    df_age = df_cd[["Patient ID", "age"]].drop_duplicates().reset_index()
    
    # Convert Age to number
    df_age.loc[df_age["age"] == "<18", "age"] = 17
    df_age.loc[df_age["age"] == ">89", "age"] = 90
    
    # Convert Age to a Number if it can, otherwise convert to -99
    for i in range(len(df_age)):
        try:
            df_age.loc[i, "age"] = int(df_age.loc[i, "age"])
        except:
            df_age.loc[i, "age"] = np.nan
    ageCatchAll = df_age["age"].isna().sum()
    
    # Age < 18
    ageLT18 = df_age[df_age["age"] < 18]["Patient ID"].count()
    
    # Age 18-40
    age18To40 = df_age[(df_age["age"] >= 18) & 
                      (df_age["age"] <= 40)]["Patient ID"].count()
    
    # Age 41-60
    age41To60 = df_age[(df_age["age"] >= 41) & 
                      (df_age["age"] <= 60)]["Patient ID"].count()
    
    # Age > 60
    ageGT60 = df_age[df_age["age"] > 60]["Patient ID"].count()
    
    # Sex
    df_sex = df_cd[["Patient ID", "Sex"]].drop_duplicates().reset_index()
    numberOfMales = df_sex[df_sex["Sex"] == "Male"]["Patient ID"].count()
    numberOfFemales = df_sex[df_sex["Sex"] == "Female"]["Patient ID"].count()
    sexCatchAll = df_sex[(df_sex["Sex"] != "Male") & (df_sex["Sex"] != "Female")]["Patient ID"].count()
    
    # Ethnicity 
    df_ethnicity = df_cd[["Patient ID", "Ethnicity Category"]].drop_duplicates().reset_index()
    numberHispanic = df_ethnicity[df_ethnicity["Ethnicity Category"] == "Spanish/Hispanic"]["Patient ID"].count()
    numberNonhispanic = df_ethnicity[df_ethnicity["Ethnicity Category"] == "Non-Spanish/non-Hispanic"]["Patient ID"].count()
    ethnicityCatchAll = df_ethnicity[(df_ethnicity["Ethnicity Category"] != "Spanish/Hispanic") & 
                                     (df_ethnicity["Ethnicity Category"] != "Non-Spanish/non-Hispanic")]["Patient ID"].count()
    
    # Race (White, Black, Asian, Native American, Other)
    df_race = df_cd[["Patient ID", "Primary Race"]].drop_duplicates().reset_index()
    numberOfWhite = df_race[df_race["Primary Race"] == "White"]["Patient ID"].count()
    numberOfBlack = df_race[df_race["Primary Race"] == "Black"]["Patient ID"].count()
    numberOfAsian = df_race[df_race["Primary Race"] == "Asian"]["Patient ID"].count()
    numberOfPacificIslander = df_race[df_race["Primary Race"] == "Pacific Islander"]["Patient ID"].count()
    numberOfNativeAmerican = df_race[df_race["Primary Race"] == "Native American"]["Patient ID"].count()
    raceCatchAll = df_race[(df_race["Primary Race"] != "White") & 
                           (df_race["Primary Race"] != "Black") & 
                           (df_race["Primary Race"] != "Asian") & 
                           (df_race["Primary Race"] != "Pacific Islander") & 
                           (df_race["Primary Race"] != "Native American")]["Patient ID"].count()
    
    # Type of Cancer
    numberOfPrimary = df_cd[df_cd["Sample Type"] == "Primary"]["Patient ID"].count()
    numberOfMetastasis = df_cd[df_cd["Sample Type"] == "Metastasis"]["Patient ID"].count()
    sampleTypeCatchAll = df_cd[(df_cd["Sample Type"] != "Primary") & 
                               (df_cd["Sample Type"] != "Metastasis")]["Patient ID"].count()
    
    # Create Table
    df_cd_out = pd.DataFrame({"Sarcoma Name From File": [nameOfSarcoma],
                              "Cancer Type Detailed": [nameOfSarcomaFromData],
                              "Samples (n)": [numberOfSamples],
                              "Patients (n)": [numberOfPatients],
                              "Mutations (<=2)": [mutationsLT2 + mutationsBlank],
                              "Mutations (3-5)": [mutations3To5],
                              "Mutations (6-17)": [mutations6To17],
                              "Mutations (>17)": [mutationsGT17],
                              "Age (<18)": [ageLT18],
                              "Age (18-40)": [age18To40],
                              "Age (41-60)": [age41To60],
                              "Age (>=61)": [ageGT60],
                              "Age (Catch-All)": [ageCatchAll],
                              "Male": [numberOfMales], 
                              "Female": [numberOfFemales],
                              "Sex (Catch-All)": [sexCatchAll],
                              "Spanish/Hispanic": [numberHispanic],
                              "Non-Spanish/Non-Hispanic": [numberNonhispanic],
                              "Ethnicity (Catch-All)": [ethnicityCatchAll],
                              "White": [numberOfWhite],
                              "Black": [numberOfBlack], 
                              "Asian": [numberOfAsian], 
                              "Pacific Islander": [numberOfPacificIslander],
                              "Native American": [numberOfNativeAmerican], 
                              "Race (Catch-All)": [raceCatchAll],
                              "Primary": [numberOfPrimary],
                              "Metastasis": [numberOfMetastasis],
                              "Sample Type (Catch-All)": sampleTypeCatchAll})
    return df_cd, df_cd_out, nameOfSarcomaFromData
    
#%% Mutated Genes

def mutatedGenes(nameOfSarcoma, nameOfSarcomaDict, myFile):
    
    # Read Data
    if myFile.endswith(".csv"):
        df_mg = pd.read_csv(myFile)
    else:
        df_mg = pd.read_csv(myFile, delimiter="\t")
        
    df_mg["Sarcoma Name From File"] = nameOfSarcoma
    df_mg["Cancer Type Detailed"] = nameOfSarcomaDict[nameOfSarcoma]
    df_mg_out = df_mg[["Sarcoma Name From File", "Cancer Type Detailed", "Gene", "#", "Is Cancer Gene (source: OncoKB)"]].sort_values("#", ascending=False)
    return df_mg_out

#%% Structural Variant Genes

def structuralVariantGenes(nameOfSarcoma, nameOfSarcomaDict, myFile):
    
    # Read Data
    if myFile.endswith(".csv"):
        df_sv = pd.read_csv(myFile)
    else:
        df_sv = pd.read_csv(myFile, delimiter="\t")
        
    df_sv["Sarcoma Name From File"] = nameOfSarcoma
    df_sv["Cancer Type Detailed"] = nameOfSarcomaDict[nameOfSarcoma]
    df_sv_out = df_sv[["Sarcoma Name From File", "Cancer Type Detailed", "Gene", "#", "Is Cancer Gene (source: OncoKB)"]].sort_values("#", ascending=False)
    return df_sv_out

#%% CNA Genes

def CNAGenes(nameOfSarcoma, nameOfSarcomaDict, myFile):
    
    # Read Data
    if myFile.endswith(".csv"):
        df_cna = pd.read_csv(myFile)
    else:
        df_cna = pd.read_csv(myFile, delimiter="\t")

    df_cna["Sarcoma Name From File"] = nameOfSarcoma
    df_cna["Cancer Type Detailed"] = nameOfSarcomaDict[nameOfSarcoma]
    df_cna_out = df_cna[["Sarcoma Name From File", "Cancer Type Detailed", "Gene", "CNA", "#", "Is Cancer Gene (source: OncoKB)"]].sort_values("#", ascending=False)
    return df_cna_out
        
#%% Run Script

if __name__ == "__main__":
    
    # Define Tables
    df_cd_combined = pd.DataFrame()
    df_cd_master = pd.DataFrame()
    df_mg_master = pd.DataFrame()
    df_sv_master = pd.DataFrame()
    df_cna_master = pd.DataFrame()
    
    # Load name of sarcoma dictionary
    if os.path.exists("TypesDict.txt"):
        with open("TypesDict.txt") as json_file:
            nameOfSarcomaDict = json.load(json_file)
    else:
        nameOfSarcomaDict = {}
    
    # Get Files
    myFiles = getFiles()
    
    for i in range(len(myFiles)):
        print("Working on", myFiles[i])
        
        # Name of Sarcoma
        myFile = os.path.split(myFiles[i])[1]
        firstUnderscoreIdx = myFile.find("_")
        nameOfSarcoma = myFile[:firstUnderscoreIdx]
        
        # Add Name of Sarcoma from File name to dictionary (Will be overridden if sarcoma is in cd)
        if nameOfSarcoma not in nameOfSarcomaDict:
            nameOfSarcomaDict[nameOfSarcoma] = ""
        
        # Skip this script
        if myFile.endswith(".py"):
                continue
            
        # Clinical Data
        if myFile.endswith("_clinical_data.csv") or myFile.endswith("_clinical_data.tsv"):
            df_cd, df_cd_out, nameOfSarcomaFromData = clinicalData(nameOfSarcoma, myFiles[i])
            df_cd_combined = pd.concat([df_cd_combined, df_cd])
            df_cd_master = pd.concat([df_cd_master, df_cd_out])
            if nameOfSarcoma == "AllSarc" or nameOfSarcoma == "BnSarc" or nameOfSarcoma == "STS":
                # This is a special exception for the project where we want to group these together
                pass
            else:
                nameOfSarcomaDict[nameOfSarcoma] = nameOfSarcomaFromData  
            
        # Mutated Ganes
        elif myFile.endswith("_Mutated_Genes.csv") or myFile.endswith("_Mutated_Genes.txt"):
            df_mg_out = mutatedGenes(nameOfSarcoma, nameOfSarcomaDict, myFiles[i])
            df_mg_master = pd.concat([df_mg_master, df_mg_out])
            
        # Structural Variant Genes.csv
        elif myFile.endswith("_Structural_Variant_Genes.csv") or myFile.endswith("_Structural_Variant_Genes.txt"):
            df_sv_out = structuralVariantGenes(nameOfSarcoma, nameOfSarcomaDict, myFiles[i])
            df_sv_master = pd.concat([df_sv_master, df_sv_out])
            
        # CNA Genes
        elif myFile.endswith("_CNA_Genes.csv") or myFile.endswith("_CNA_Genes.txt"):
            df_cna_out = CNAGenes(nameOfSarcoma, nameOfSarcomaDict, myFiles[i])
            df_cna_master = pd.concat([df_cna_master, df_cna_out])
        else:
            print("\tFile is not in proper format:", myFile)
    
    # Group clinical data by Sequence Assay ID and count 
    df_cd_combined_group = df_cd_combined.groupby(["Cancer Type", "Cancer Type Detailed", "Sequence Assay ID"])["Sequence Assay ID"].count().to_frame("Count Sequence Assay ID").reset_index()
    df_cd_combined_group.drop_duplicates()
    
    # Create Pivot Tables for #
    df_mg_pivot_num = pd.pivot_table(df_mg_master, values="#", index="Gene", columns="Cancer Type Detailed", aggfunc=np.sum, fill_value=0)
    df_sv_pivot_num = pd.pivot_table(df_sv_master, values="#", index="Gene", columns="Cancer Type Detailed", aggfunc=np.sum, fill_value=0)
    df_cna_pivot_num = pd.pivot_table(df_cna_master, values="#", index="Gene", columns="Cancer Type Detailed", aggfunc=np.sum, fill_value=0)
    
    # Create Pivot Tables for Is Cancer Gene (source: OncoKB)
    df_mg_forPivot = df_mg_master.copy()
    df_sv_forPivot = df_sv_master.copy()
    df_cna_forPivot = df_cna_master.copy()
    
    df_mg_forPivot["Is Cancer Gene (source: OncoKB)"] = df_mg_forPivot["Is Cancer Gene (source: OncoKB)"].apply(lambda x: 1 if x == "Yes" else 0)
    df_sv_forPivot["Is Cancer Gene (source: OncoKB)"] = df_sv_forPivot["Is Cancer Gene (source: OncoKB)"].apply(lambda x: 1 if x == "Yes" else 0)
    df_cna_forPivot["Is Cancer Gene (source: OncoKB)"] = df_cna_forPivot["Is Cancer Gene (source: OncoKB)"].apply(lambda x: 1 if x == "Yes" else 0)
    
    df_mg_pivot_isGene = pd.pivot_table(df_mg_forPivot, values="Is Cancer Gene (source: OncoKB)", index="Gene", columns="Cancer Type Detailed", aggfunc=np.sum, fill_value=0)
    df_sv_pivot_isGene = pd.pivot_table(df_sv_forPivot, values="Is Cancer Gene (source: OncoKB)", index="Gene", columns="Cancer Type Detailed", aggfunc=np.sum, fill_value=0)
    df_cna_pivot_isGene = pd.pivot_table(df_cna_forPivot, values="Is Cancer Gene (source: OncoKB)", index="Gene", columns="Cancer Type Detailed", aggfunc=np.sum, fill_value=0)
    
    # Add Totals for #
    df_mg_pivot_num.loc["Total", :] = df_mg_pivot_num.sum(axis=0)
    df_mg_pivot_num.loc[:, "Total"] = df_mg_pivot_num.sum(axis=1)
    df_sv_pivot_num.loc["Total", :] = df_sv_pivot_num.sum(axis=0)
    df_sv_pivot_num.loc[:, "Total"] = df_sv_pivot_num.sum(axis=1)
    df_cna_pivot_num.loc["Total", :] = df_cna_pivot_num.sum(axis=0)
    df_cna_pivot_num.loc[:, "Total"] = df_cna_pivot_num.sum(axis=1)
    
    # Add Totals for isGene
    df_mg_pivot_isGene.loc["Total", :] = df_mg_pivot_isGene.sum(axis=0)
    df_mg_pivot_isGene.loc[:, "Total"] = df_mg_pivot_isGene.sum(axis=1)
    df_sv_pivot_isGene.loc["Total", :] = df_sv_pivot_isGene.sum(axis=0)
    df_sv_pivot_isGene.loc[:, "Total"] = df_sv_pivot_isGene.sum(axis=1)
    df_cna_pivot_isGene.loc["Total", :] = df_cna_pivot_isGene.sum(axis=0)
    df_cna_pivot_isGene.loc[:, "Total"] = df_cna_pivot_isGene.sum(axis=1)
    
    # Write to excel
    with pd.ExcelWriter(output) as writer:
        df_cd_master.to_excel(writer, sheet_name="Clinical Data", index=False)
        df_cd_combined_group.to_excel(writer, sheet_name="Sequence Assay ID", index=False)
        df_mg_master.to_excel(writer, sheet_name="Mutated Genes", index=False)
        df_mg_pivot_num.to_excel(writer, sheet_name="Mutated Genes Pivot Num", index=True)
        df_mg_pivot_isGene.to_excel(writer, sheet_name="Mutated Genes Pivot isGene", index=True)
        df_sv_master.to_excel(writer, sheet_name="SV Genes", index=False)
        df_sv_pivot_num.to_excel(writer, sheet_name="SV Genes Pivot Num", index=True)
        df_sv_pivot_isGene.to_excel(writer, sheet_name="SV Genes Pivot isGene", index=True)
        df_cna_master.to_excel(writer, sheet_name="CNA Genes", index=False)
        df_cna_pivot_num.to_excel(writer, sheet_name="CNA Genes Pivot Num", index=True)
        df_cna_pivot_isGene.to_excel(writer, sheet_name="CNA Genes Pivot isGene", index=True)
    
    with open("TypesDict.txt", "w") as outfile:
        json.dump(nameOfSarcomaDict, outfile, indent=4)
    print("Complete")
    
            
            
            
    