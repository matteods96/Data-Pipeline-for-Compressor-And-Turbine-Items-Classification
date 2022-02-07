----- Questa query gira su DB ARGO



select 

esi.item_number as ORDERED_ITEM,
nvl(lang1.ENG,inve.description) as FINAL_DESCRIPTION

from
CUST_FPH_ODS.egp_system_items_b esi

inner join (select inv.description, inv.item_code  from cust_og_bit_dm.dm_d011_inventory_items inv where inv.organization_id = 86 ) inve
on ( inve.item_code = esi.ITEM_NUMBER)


left join 
(
select
lang.attribute_char1 ITA,
lang.attribute_char2 ENG,
lang.attribute_char3 FRA,
lang.attribute_char4 SPA,
lang.attribute_char5 GER,
lang.attribute_char6 POR,
lang.inventory_item_id
from
CUST_FPH_ODS.ego_item_eff_b lang
where 1=1
and lang.context_code (+)='OG_MULTI_LANGUAGE_ITEM_DESC'
and lang.organization_id (+)= 300000001634001
) lang1
on (lang1.inventory_item_id =esi.inventory_item_id)

where 1=1
and esi.organization_code = 'GIM'
and esi.ITEM_NUMBER in {}
