# -*- coding: utf-8 -*-
"""
Created on Wed May 26 09:56:19 2021

@author: dsoumat
"""
import pandas as pd
#from query import run_query
from special_function import parzializza_query
import cx_Oracle

#Given the input  filename the function returns a dataset containing all valid ORDERED_ITEM values 


def getDatasetWithValidItems(input_filename):
   
    dataframe=pd.read_excel(input_filename)
    '''
    username = 'SSO105703068'
    password = 'pCq59leB'
    dsn ='(DESCRIPTION=(LOAD_BALANCE=ON)(TRANSPORT_CONNECT_TIMEOUT=3)(RETRY_COUNT=3)'\
         '(ADDRESS=(PROTOCOL=TCP)(HOST=127.0.0.1)(PORT=9168))'\
         '(ADDRESS=(PROTOCOL=TCP)(HOST=127.J380.0.1)(PORT = 9170))'\
         '(CONNECT_DATA=(SERVER=DEDICATED)(SERVICE_NAME=argo)))'
    connection = cx_Oracle.connect(username, password, dsn)
    la_lista = list(set(dataframe.ORDERED_ITEM.astype(str).tolist()))
    query_file = open('C:\\Users\\dsoumat\Desktop\Items\Query_ITEM_SUPERATI.sql', "r")
    sql=query_file.read()
    #dataframe_with_new_Description=parzializza_query(sql,la_lista,connection)
    dataframe1=parzializza_query(sql,la_lista,connection)
    dataframe1.to_excel('C:\\Users\\dsoumat\\Desktop\\Items\\Superseded_ITEMS')
    '''
    filename1='C:\\Users\\dsoumat\\Desktop\\Items\\Superseded_ITEMS.xlsx'
    dataframe1=pd.read_excel(filename1)

    dataframe_final = pd.merge(dataframe,dataframe1,left_on='ORDERED_ITEM', right_on='OLD_CODE', how='left')
    dataframe_final.to_excel('valid.xlsx')
    dataframe_final['DESCRIPTION'].fillna("",inplace=True)
    dataframe_final['NEW_CODE'].fillna("",inplace=True)
    dataframe_final['OLD_CODE'].fillna("",inplace=True)
    dataframe_final=dataframe_final.assign(FINAL_ITEM="")
    dataframe_final['FINAL_ITEM']=dataframe_final['NEW_CODE']
    dataframe_final['FINAL_ITEM'][dataframe_final['NEW_CODE']==""]=dataframe_final['ORDERED_ITEM'][dataframe_final['NEW_CODE']==""]
    dataframe_final.to_excel('datasetWithFinalItem.xlsx')
    dataframe_final['ORDERED_ITEM']=dataframe_final['FINAL_ITEM']
    dataframe_final=dataframe_final[['ORDERED_ITEM','DESCRIPTION']]
    print(dataframe_final.head())
    return dataframe_final


def getItemsWithADescription(input_filename):
    dataframe_final=getDatasetWithValidItems(input_filename)
    
    df_with_Description=dataframe_final[dataframe_final['DESCRIPTION']!=""]
    df_with_Description.to_excel('df_with_Description.xlsx')
    
    df_without_Description=dataframe_final[dataframe_final['DESCRIPTION']==""]
    
    df_without_Description.to_excel('df_without_Description.xlsx')
    
    username = 'SSO105703068'
    password = 'pCq59leB'
    
    dsn ='(DESCRIPTION=(LOAD_BALANCE=ON)(TRANSPORT_CONNECT_TIMEOUT=3)(RETRY_COUNT=3)'\
         '(ADDRESS=(PROTOCOL=TCP)(HOST=127.0.0.1)(PORT=9168))'\
         '(ADDRESS=(PROTOCOL=TCP)(HOST=127.J380.0.1)(PORT = 9170))'\
         '(CONNECT_DATA=(SERVER=DEDICATED)(SERVICE_NAME=argo)))'
    connection = cx_Oracle.connect(username, password, dsn)
    la_lista = list(set(df_without_Description.ORDERED_ITEM.astype(str).tolist()))
    query_file = open('C:\\Users\\dsoumat\Desktop\Items\Query_Descrizione_INVENTORY.sql', "r")
    sql=query_file.read()
    dataframe_with_new_Description=parzializza_query(sql,la_lista,connection)
    dataframe_with_new_Description.to_excel('dataframeDescriptionFromInventory.xlsx')
    dataframe_with_new_Description.columns=['ORDERED_ITEM','DESCRIPTION'] 
    item_with_description=df_with_Description.append(dataframe_with_new_Description,ignore_index = True)
    item_with_description.to_excel('item_with_description.xlsx')
    return item_with_description




    

def getItemsWithForcedFamily(dataframe):
    dataframe=dataframe[dataframe['FAMILY_PRED_EXPLANATION']=="HARD RULES"]
    dataframe.to_excel('items_with_forced_family.xlsx')
    return dataframe

def getItemsWithoutForcedFamily(dataframe):
     df=dataframe[dataframe['FAMILY_PRED_EXPLANATION']!="HARD RULES"]
     #print(" the number of  items without forced family is:",df.shape[0])
     df.to_excel('items_without_forced_family.xlsx') 
     return  df
    
def getItemWithMSNFromEAM(dataframe):
    items_without_forced_family= getItemsWithoutForcedFamily(dataframe)
    
    #c2=run_query('oscaroltp',r'C:\\Users\dsoumat\Desktop\Items\second_Query_MACHINE_SECTION_from_EAM.txt')
    username = 'GEOG_FORMS_USERDB'
    password = 'USERAU77FRM'
    hostname = 'oscaroltp-db.og.ge.com'
    port = '10110'
    servicename = 'oscaroltp'
    dsn ='(DESCRIPTION=(LOAD_BALANCE=ON)(TRANSPORT_CONNECT_TIMEOUT=3)(RETRY_COUNT=3)'\
         '(ADDRESS=(PROTOCOL=TCP)(HOST=127.0.0.1)(PORT=9172))'\
         '(ADDRESS=(PROTOCOL=TCP)(HOST=127.0.0.1)(PORT = 9174))'\
         '(ADDRESS=(PROTOCOL=TCP)(HOST=127.0.0.1)(PORT = 9176))'\
         '(ADDRESS=(PROTOCOL=TCP)(HOST=127.0.0.1)(PORT = 9178))'\
         '(CONNECT_DATA=(SERVER=DEDICATED)(SERVICE_NAME=oscaroltp)))' 
   
    connection = cx_Oracle.connect(username, password, dsn)
    la_lista = list(set(items_without_forced_family.ORDERED_ITEM.astype(str).tolist()))
    query_file = open('C:\\Users\\dsoumat\Desktop\Items\Query_MACHINE_SECTION_from_EAM.sql', "r")
    sql=query_file.read()
    dataframe_with_Machine_Section_Number=parzializza_query(sql,la_lista,connection)
    dataframe_with_Machine_Section_Number.to_excel('sectionNumberEAM.xlsx')
    return dataframe_with_Machine_Section_Number

def getItemsSetInEAM(dataframe):
    return set(dataframe['MATERIAL_CODE'].values)

def getItemsnotInEAM(from_eam,data_after_hard_rules):
    return list(set(getItemsWithoutForcedFamily(data_after_hard_rules)['ORDERED_ITEM'].values)-getItemsSetInEAM(from_eam))

def getItemsWithoutFamily(dataframe):
    item_not_in_EAM=getItemsnotInEAM(getItemWithMSNFromEAM(dataframe),dataframe)
    iwf=dataframe[dataframe['ORDERED_ITEM'].isin(item_not_in_EAM)]
    iwf['FAMILY_PREDICTION']='NO MSN '
    iwf['FAMILY_PRED_EXPLANATION']='NOT IN EAM'
    iwf['CAP_NOCAP']='NO CAP'
    iwf.to_excel('item_without_Family.xlsx')
    #if len(item_not_in_EAM)<1:
    return iwf



    
        
       
   
def getItemsWith_MSN_and_Des(dataframe):
    #dataframe_with_Machine_Section_Number=dataframe
    df_with_Machine_Section_Number_and_Des=pd.merge(getItemsWithoutForcedFamily(dataframe),getItemWithMSNFromEAM(dataframe),left_on='ORDERED_ITEM', right_on='MATERIAL_CODE', how='left')
    df_with_Machine_Section_Number_and_Des.to_excel('df_with_Machine_Section_Number_and_Des.xlsx')
    df_with_Machine_Section_Number_and_Des=df_with_Machine_Section_Number_and_Des[['ORDERED_ITEM','DESCRIPTION','MACHINE_SECTION_NUMBER','FAMILY_PREDICTION','FAMILY_PRED_EXPLANATION','TECH','CAP_NOCAP']]
    return df_with_Machine_Section_Number_and_Des

def getDatasetWithStandardDescription(dataframe):
    username = 'SSO105703068'
    password = 'pCq59leB'
    hostname = 'argo-prod-db.og.ge.com'
    port = '10110'
    servicename = 'argoprod'
    dsn ='(DESCRIPTION=(LOAD_BALANCE=ON)(TRANSPORT_CONNECT_TIMEOUT=3)(RETRY_COUNT=3)'\
         '(ADDRESS=(PROTOCOL=TCP)(HOST=127.0.0.1)(PORT=9168))'\
         '(ADDRESS=(PROTOCOL=TCP)(HOST=127.J380.0.1)(PORT = 9170))'\
         '(CONNECT_DATA=(SERVER=DEDICATED)(SERVICE_NAME=argo)))'
    connection = cx_Oracle.connect(username, password, dsn)
    la_lista = list(set(dataframe.ORDERED_ITEM.astype(str).tolist()))
    query_file = open('C:\\Users\\dsoumat\Desktop\Items\Query_FPH_DESCRIPTION .sql', "r")
    sql=query_file.read()
    fusion_product_hub=parzializza_query(sql,la_lista,connection)
    fusion_product_hub.to_excel('fusion_product_hub.xlsx')
    df_with_standard_description=pd.merge(dataframe,fusion_product_hub,left_on='ORDERED_ITEM',
                                          right_on='ORDERED_ITEM', how='left')
    df_with_standard_description['FINAL_DESCRIPTION'].fillna("",inplace=True)
    condition=df_with_standard_description['FINAL_DESCRIPTION']!=""
    df_with_standard_description['DESCRIPTION'][condition]=df_with_standard_description['FINAL_DESCRIPTION'][condition]
    df_with_standard_description.to_excel('df_with_standard_description.xlsx')
    return df_with_standard_description



    
def getInputForClassifier(dataframe):
    df=getDatasetWithStandardDescription(dataframe)
    df_input=df[['ORDERED_ITEM','DESCRIPTION','MACHINE_SECTION_NUMBER']]
    df_input.to_excel('input_for_Classifier.xlsx')
    return df_input

    
    
    
    
    
    
    
    
    