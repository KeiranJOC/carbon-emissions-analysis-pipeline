#!/usr/bin/env bash

# run dbt flow
prefect deployment run transform-carbon-emissions/$PREFECT_DEPLOYMENT_NAME
