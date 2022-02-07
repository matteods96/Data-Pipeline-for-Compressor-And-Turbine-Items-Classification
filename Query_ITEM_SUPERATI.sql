
--- Questa query gira su Db ARGO

SELECT distinct
IT.SEGMENT1 NEW_CODE,
IT2.SEGMENT1 OLD_CODE,
gim.PATH,
gim.REL_PATH

FROM
(
SELECT distinct

         GIM.INVENTORY_ITEM_ID
        ,GIM.ORGANIZATION_ID
        --,RELATED_ITEM_ID
        ,CONNECT_BY_ROOT GIM.RELATED_ITEM_ID FINAL_RELATED_ITEM
        ,SYS_CONNECT_BY_PATH(ITLIST.SEGMENT1, '>') PATH
        
        ,SYS_CONNECT_BY_PATH(GIM.relationship_type_id, '>') REL_PATH
          FROM (
          select * from rep_osc.MTL_RELATED_ITEMS
           where  
           relationship_type_id in ('8','4','6')and
            RELATED_ITEM_ID not in ( 
                          SELECT distinct INVENTORY_ITEM_ID
                          FROM CUST_OG_BIT_DW.MTL_SYSTEM_ITEMS_VL_DWH
                          where segment1 like 'SOURCEBOOK%' or segment1 like 'BLOCCATO%' )
           ) GIM,
           
          CUST_OG_BIT_DW.MTL_SYSTEM_ITEMS_VL_DWH ITLIST
         
          
          where GIM.RELATED_ITEM_ID=ITLIST.INVENTORY_ITEM_ID
          
          
          --start with related item not in MTL_RELATED_ITEMS_DWH table, means they don't have related items of any kind
          START WITH RELATED_ITEM_ID IN
                (
                SELECT
                IT.INVENTORY_ITEM_ID
                FROM
                 (SELECT 
                 INVENTORY_ITEM_ID
                 , SEGMENT1 
                 FROM 
                 CUST_OG_BIT_DW.MTL_SYSTEM_ITEMS_VL_DWH
                  WHERE ORGANIZATION_ID IN (
                  '93'
                  --,'8212'
                  --,'8213'
                  ) 
                )IT
                ,  
                
                (
          select * from rep_osc.MTL_RELATED_ITEMS 
           where 
           relationship_type_id in ('8','4','6') and
                       RELATED_ITEM_ID not in ( 
                          SELECT distinct INVENTORY_ITEM_ID
                          FROM CUST_OG_BIT_DW.MTL_SYSTEM_ITEMS_VL_DWH
                          where segment1 like 'SOURCEBOOK%' or segment1 like 'BLOCCATO%' )
           ) GIM
           
           
                WHERE 
                IT.INVENTORY_ITEM_ID = GIM.INVENTORY_ITEM_ID (+)
                AND GIM.INVENTORY_ITEM_ID IS NULL
                )
          CONNECT BY   PRIOR  GIM.INVENTORY_ITEM_ID =  GIM.RELATED_ITEM_ID 
          
          
          
  ) GIM      
     

,(SELECT INVENTORY_ITEM_ID,ORGANIZATION_ID,SEGMENT1
FROM CUST_OG_BIT_DW.MTL_SYSTEM_ITEMS_VL_DWH
WHERE ORGANIZATION_ID IN
('93','8212','8213'
))IT


,(SELECT INVENTORY_ITEM_ID,ORGANIZATION_ID,SEGMENT1
FROM CUST_OG_BIT_DW.MTL_SYSTEM_ITEMS_VL_DWH
WHERE ORGANIZATION_ID IN
('93','8212','8213'
))IT2

WHERE 1=1
and GIM.FINAL_RELATED_ITEM = IT.INVENTORY_ITEM_ID
and GIM.INVENTORY_ITEM_ID = IT2.INVENTORY_ITEM_ID