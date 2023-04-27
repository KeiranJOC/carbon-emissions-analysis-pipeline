#!/usr/bin/env bash

# data ingestion backfill - run separate flows for each year in parallel
prefect deployment run \
    ingest-carbon-emissions-raw/$PREFECT_DEPLOYMENT_NAME \
    -p 'months=["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]' \
    -p 'years=["2019"]'

prefect deployment run \
    ingest-carbon-emissions-raw/$PREFECT_DEPLOYMENT_NAME \
    -p 'months=["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]' \
    -p 'years=["2020"]'

prefect deployment run \
    ingest-carbon-emissions-raw/$PREFECT_DEPLOYMENT_NAME \
    -p 'months=["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]' \
    -p 'years=["2021"]'

prefect deployment run \
    ingest-carbon-emissions-raw/$PREFECT_DEPLOYMENT_NAME \
    -p 'months=["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]' \
    -p 'years=["2022"]'