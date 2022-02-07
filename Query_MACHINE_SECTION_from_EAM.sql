
----- Questa query gira su DB ORACLE OSCAR


select distinct comp.material_code, 
comp.machine_section_number
from apps.NPEAM_DM_ASSET_COMPONENT COMP
where 1=1
and comp.material_code in {}
