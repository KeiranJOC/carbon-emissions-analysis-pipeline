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
        , ghg_unit as greenhouse_gas_unit
        , safe_cast(ghg_conversion_factor_2022 as numeric) as greenhouse_gas_conversion_factor
        , {{ dbt_utils.generate_surrogate_key([
            'scope'
            , 'level_1'
            , 'level_2'
            , 'level_3'
            , 'level_4'
            , 'column_text'
            , 'uom'
            , 'ghg_unit'
            , 'ghg_conversion_factor_2022'
        ]) }} as record_key
    from {{ source('carbon_emissions_raw', 'conversion_factors_raw') }}
)
where greenhouse_gas_conversion_factor is not null
