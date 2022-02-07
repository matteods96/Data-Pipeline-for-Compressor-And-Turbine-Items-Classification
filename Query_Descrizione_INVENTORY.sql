select inve.segment1 as ITEM_CODE,
inve.description as ITEM_DESCRIPTION
from OSCAR_ODS.MTL_SYSTEM_ITEMS_B_VW  INVE 
where INVE.organization_id = 85
and inve.segment1 in {}