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

with unpivot_records as (
    select
        site
        , meter
        , unit
        , date
        , parse_time('%H%M', time) as time
        , safe_cast(amount as numeric) as amount
    from {{ ref('stg_energy_consumption') }} as ec
    unpivot(amount for time in (
        ec.0000
        , ec.0030
        , ec.0100
        , ec.0130
        , ec.0200
        , ec.0230
        , ec.0300
        , ec.0330
        , ec.0400
        , ec.0430
        , ec.0500
        , ec.0530
        , ec.0600
        , ec.0630
        , ec.0700
        , ec.0730
        , ec.0800
        , ec.0830
        , ec.0900
        , ec.0930
        , ec.1000
        , ec.1030
        , ec.1100
        , ec.1130
        , ec.1200
        , ec.1230
        , ec.1300
        , ec.1330
        , ec.1400
        , ec.1430
        , ec.1500
        , ec.1530
        , ec.1600
        , ec.1630
        , ec.1700
        , ec.1730
        , ec.1800
        , ec.1830
        , ec.1900
        , ec.1930
        , ec.2000
        , ec.2030
        , ec.2100
        , ec.2130
        , ec.2200
        , ec.2230
        , ec.2300
        , ec.2330
    ))
)

, create_timestamps as (
    select
        site
        , meter
        , unit
        , case
            when lower(meter) like '%natural gas%' then 'Natural Gas'
            when lower(meter) like '%grid electricity%' then 'Grid Electricity'
            when lower(meter) like '%water%' then 'Water'
            when lower(meter) like '%imported energy%' then 'Imported Energy'
            else null
        end as energy_type
        , parse_timestamp('%F %T', date || time) as timestamp
        , amount
    from unpivot_records
)

select
    *
    , {{ dbt_utils.generate_surrogate_key([
        'site'
        , 'meter'
        , 'timestamp'
    ]) }} as record_key
from create_timestamps
where amount is not null -- drop rows that we have no meter readings for
