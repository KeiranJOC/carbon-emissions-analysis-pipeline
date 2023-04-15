select
    ec.site
    , ec.date
    , ec.time
    , ec.unit as energy_usage_unit_of_measurement
    , ec.amount as energy_usage_amount
    , mcm.greenhouse_gas_unit as greenhouse_gas_emissions_unit_of_measurement
    , ec.amount * cf.greenhouse_gas_conversion_factor as greenhouse_gas_emissions
    , ec.record_key
from {{ ref('fact_energy_consumption') }} as ec
left join {{ ref('dim_meter_category_mapping') }} as mcm
    on lower(ec.meter) like '%' || mcm.meter || '%'
left join {{ ref('dim_conversion_factors') }} as cf
    on mcm.category_level_1 = cf.category_level_1
    and mcm.category_level_2 = cf.category_level_2
    and mcm.category_level_3 = cf.category_level_3
    and mcm.category_level_4 = cf.category_level_4
    and mcm.unit_of_measurement = cf.unit_of_measurement
    and mcm.greenhouse_gas_unit = cf.greenhouse_gas_unit
where lower(ec.meter) like '%natural gas%'
    or lower(ec.meter) like '%grid electricity%'
