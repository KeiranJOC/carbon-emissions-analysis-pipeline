#!/usr/bin/env bash

# building deployments did not upload the flow code stored in subdirectories to the storage bucket, so I need to upload them manually
gsutil -m cp -r blocks/ gs://de-data-lake_spry-alignment-375710
gsutil -m cp -r flows/ gs://de-data-lake_spry-alignment-375710
gsutil -m cp -r dbt_de_zoomcamp/ gs://de-data-lake_spry-alignment-375710