# -*- coding: utf-8 -*-
"""
Created on Tue May 11 20:43:50 2021

@author: dsoumat
"""


import pandas as pd

def parzializza_query(la_query_base,la_lista_in,la_connessione):
    split_number=437
    quanti_resto=len(la_lista_in)%split_number
    quanti_pieno=(int)(len(la_lista_in) - quanti_resto)/split_number

    

    lista_split=[]
    for i in range(int(quanti_pieno)):
        lista_split.append(split_number)
    if quanti_resto != 0:
        lista_split.append(quanti_resto)

    
   
    la_lista=[]
    for i in range(len(lista_split) ):
         elementi=lista_split[i]
         la_lista.append(list(la_lista_in)[i*split_number:(i*split_number)+elementi])

    PARTIAL_list =[]
    for i in range(len(la_lista)):
        tupla_ITEMS = tuple(la_lista[i])
        lo_sql_parziale = la_query_base.format(str(tupla_ITEMS))
        df_pd_parziale = pd.read_sql(lo_sql_parziale, con=la_connessione)
        PARTIAL_list.append(df_pd_parziale)
        df_QUERY_TOTALE = pd.concat(PARTIAL_list)
    return df_QUERY_TOTALE


