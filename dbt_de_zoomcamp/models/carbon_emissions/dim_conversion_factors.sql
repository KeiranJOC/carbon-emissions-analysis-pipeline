{{
    config(
        partition_by = {
            "field": "year",
            "data_type": "date",
            "granularity": "year"
        },
        cluster_by = [
            'scope',
            'category_level_1',
            'category_level_2',
            'category_level_3',
        ]
    )
}}

select
    *
    , {{ dbt_utils.generate_surrogate_key([
        'scope'
        , 'category_level_1'
        , 'category_level_2'
        , 'category_level_3'
        , 'category_level_4'
        , 'notes'
        , 'unit_of_measurement'
        , 'greenhouse_gas_unit'
        , 'greenhouse_gas_conversion_factor'
        , 'year'
    ]) }} as record_key
from {{ ref('stg_conversion_factors') }}
