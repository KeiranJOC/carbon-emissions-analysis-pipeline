#!/usr/bin/env bash

# data ingestion backfill - run flows in parallel
prefect deployment run \
    ingest-carbon-emissions-raw/cloud-run-deployment \
    -p 'months=["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]' \
    -p 'years=["2019"]'

prefect deployment run \
    ingest-carbon-emissions-raw/cloud-run-deployment \
    -p 'months=["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]' \
    -p 'years=["2020"]'

prefect deployment run \
    ingest-carbon-emissions-raw/cloud-run-deployment \
    -p 'months=["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]' \
    -p 'years=["2021"]'

prefect deployment run \
    ingest-carbon-emissions-raw/cloud-run-deployment \
    -p 'months=["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]' \
    -p 'years=["2022"]'