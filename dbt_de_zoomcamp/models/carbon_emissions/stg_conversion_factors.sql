{{ config(materialized = 'view') }}

select *
from (
    select
        scope
        , level_1 as category_level_1
        , level_2 as category_level_2
        , level_3 as category_level_3
        , level_4 as category_level_4
        , column_text as notes
        , uom as unit_of_measurement
        , ghg as greenhouse_gas_unit
        , safe_cast(ghg_conversion_factor as numeric) as greenhouse_gas_conversion_factor
        , cast(year as date) as year
    from {{ source('carbon_emissions_raw', 'conversion_factors_raw') }}
)
-- drop any blank rows from the raw data, or rows where we couldn't convert the conversion factor to a number
where greenhouse_gas_conversion_factor is not null
