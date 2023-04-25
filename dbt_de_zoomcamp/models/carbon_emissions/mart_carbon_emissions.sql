{{
    config(
        partition_by = {
            "field": "timestamp",
            "data_type": "timestamp",
            "granularity": "month"
        },
        cluster_by = [
            'site',
            'energy_type'
        ]
    )
}}

with map_conversion_factors as (
  select
      mcm.energy_type
      , mcm.greenhouse_gas_unit as greenhouse_gas_emissions_unit_of_measurement
      , cf.greenhouse_gas_conversion_factor
      , cf.year
from {{ ref('dim_energy_category_mapping') }} as mcm
left join {{ ref('dim_conversion_factors') }} as cf
      on mcm.category_level_1 = cf.category_level_1
      and mcm.category_level_2 = cf.category_level_2
      and mcm.category_level_3 = cf.category_level_3
      and mcm.unit_of_measurement = cf.unit_of_measurement
      and mcm.greenhouse_gas_unit = cf.greenhouse_gas_unit
)

, calculate_emissions as (
  select
      ec.site
      , ec.timestamp
      , ec.energy_type
      , ec.unit as energy_usage_unit_of_measurement
      , ec.amount as energy_usage_amount
      , mcf.greenhouse_gas_emissions_unit_of_measurement
      , ec.amount * mcf.greenhouse_gas_conversion_factor as greenhouse_gas_emissions
      , ec.record_key
  from {{ ref('fact_energy_consumption') }} as ec
  left join map_conversion_factors as mcf
      on ec.energy_type = mcf.energy_type
      and cast(date_trunc(ec.timestamp, year) as date) = mcf.year
  where ec.energy_type in (
      'Grid Electricity'
      , 'Natural Gas'
      , 'Water'
  )
)

select * from calculate_emissions
