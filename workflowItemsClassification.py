# -*- coding: utf-8 -*-
"""
Created on Mon May 17 15:39:44 2021

@author: dsoumat
"""

import pandas as pd
from hard_rules import applyHard_Rules
from items import getItemsWithADescription
from items import getItemsWithForcedFamily
from items import getItemsWith_MSN_and_Des
from items import getInputForClassifier
from items import getItemsWithoutFamily
from items import getInputForClassifier

def main():
    input_filename='C:\\Users\\dsoumat\\Desktop\\Items\\INPUT_ITEM_CODES_STEFANO@20210429.xlsx'
    data_before_HardRules=getItemsWithADescription(input_filename)
    data_after_hard_rules=applyHard_Rules(data_before_HardRules)
    items_with_Forced_Family=getItemsWithForcedFamily(data_after_hard_rules)
    item_without_Family=getItemsWithoutFamily(data_after_hard_rules)
    items_with_Machine_Section_Number_and_Des=getItemsWith_MSN_and_Des(data_after_hard_rules)
    input_data_for_classifier=getInputForClassifier(items_with_Machine_Section_Number_and_Des)
    classifier_output=pd.read_excel('C:\\Users\\dsoumat\\Desktop\\Items\\OUTPUT_CAPITAL_FAMILY.xlsx')
    classifier_output=classifier_output[items_with_Forced_Family.columns]
    output=classifier_output.append(items_with_Forced_Family)
    final_family_assignment=output.append(item_without_Family)
    final_family_assignment= final_family_assignment.to_excel('final_family_assignment.xlsx')               


     
if __name__ == "__main__":
    main()



