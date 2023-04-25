{{ config(materialized = 'view') }}

select
    ecr.site
    , ecr.meter
    , ecr.unit
    , ecr.date
    , ecr.0000
    , ecr.0030
    , ecr.0100
    , ecr.0130
    , ecr.0200
    , ecr.0230
    , ecr.0300
    , ecr.0330
    , ecr.0400
    , ecr.0430
    , ecr.0500
    , ecr.0530
    , ecr.0600
    , ecr.0630
    , ecr.0700
    , ecr.0730
    , ecr.0800
    , ecr.0830
    , ecr.0900
    , ecr.0930
    , ecr.1000
    , ecr.1030
    , ecr.1100
    , ecr.1130
    , ecr.1200
    , ecr.1230
    , ecr.1300
    , ecr.1330
    , ecr.1400
    , ecr.1430
    , ecr.1500
    , ecr.1530
    , ecr.1600
    , ecr.1630
    , ecr.1700
    , ecr.1730
    , ecr.1800
    , ecr.1830
    , ecr.1900
    , ecr.1930
    , ecr.2000
    , ecr.2030
    , ecr.2100
    , ecr.2130
    , ecr.2200
    , ecr.2230
    , ecr.2300
    , ecr.2330
from {{ source('carbon_emissions_raw', 'energy_consumption_raw') }} as ecr
-- drop any blank rows in the raw data
where ecr.site is not null
