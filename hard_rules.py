# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 20:55:36 2021

@author: dsoumat
"""

import pandas as pd
#import numpy as np
#import openpyxl 
def applyHard_Rules(dataframe1):
    #OLD DATASET
    #filename1=('Copy of fam_class_pipeline - input_step_3.xlsx')
    #filename1='INPUT_ITEM_CODES_STEFANO@20210429.xlsx'
    #Loading  data into the dataframe  dataframe1
    #filename1='item_with_description.xlsx'
    #dataframe1=pd.read_excel(filename1)
    #dataframe1.drop(columns='Unnamed: 0',inplace=True)
    #even though this step is not needed , it might be useful  to run several queries 
    #random_subset=dataframe1.sample(n=25)
    #print(dataframe1.columns.tolist())
    #Adding new  columns  FAMILY_PREDICTION,FAMILY_PRED_EXPLANATION,TECH,CAP_NOCAP to the existing dataframe
    dataframe1=dataframe1.assign(FAMILY_PREDICTION="",FAMILY_PRED_EXPLANATION="",TECH="",CAP_NOCAP="")
    #dataframe1['ORDERED_ITEM']=dataframe1['ORDERED_ITEM'].astype(str)
    #print(dataframe1.columns.tolist())
    #print(dataframe1.dtypes)
    #tuple containing order item's prefixes for items deemed to be auxiliary
    prefixes_aux=('I','V')
    ##tuple containing order item's prefixes for items not considered as  auxiliary
    prefixes_oth=('N','X','Y','1C','1P','1X','LC')
    #implementation of tdataframe1he hard rules which does not apply to the classifier
    dataframe1['FAMILY_PREDICTION'][dataframe1['ORDERED_ITEM'].str.startswith(prefixes_aux)]="AUX"
    dataframe1['FAMILY_PREDICTION'][dataframe1['ORDERED_ITEM'].str.startswith(prefixes_oth)]="OTH"
    dataframe1['FAMILY_PRED_EXPLANATION'][dataframe1['FAMILY_PREDICTION']!=""]="HARD RULES"
    dataframe1['CAP_NOCAP'][dataframe1['FAMILY_PRED_EXPLANATION']=="HARD RULES"]="NO CAP"
    #Printing a tuple containg item codes choosen random that enable  to speed up the query's execution 
    #print(tuple(set(random_subset['ORDERED_ITEM'].values)))
    dataframe1.to_excel('dataset_after_Hard_Rules.xlsx')
    return dataframe1
