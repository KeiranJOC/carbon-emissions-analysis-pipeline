import json

from os import environ
from prefect import flow
from blocks.dbt import Dbt
from dotenv import load_dotenv
from prefect_gcp import CloudRunJob, GcpCredentials, GcsBucket
from prefect_dbt.cli import BigQueryTargetConfigs, DbtCliProfile


"""
Create Prefect blocks for:
    - GCP credentials
    - GCS bucket for flow code storage
    - BigQuery target configuration for dbt
    - dbt profile
    - dbt project
    - Cloud Run Job to run deployments
"""

load_dotenv()

# GCP credentials
with open(environ['GCP_SERVICE_ACCOUNT_FILE'], 'r') as f:
    info = json.load(f)
credentials_block = GcpCredentials(service_account_info=info)
credentials_block.save(environ['GCP_CREDENTIALS_BLOCK'], overwrite=True)

# GCS bucket
storage_block = GcsBucket(
    gcp_credentials=GcpCredentials.load(environ['GCP_CREDENTIALS_BLOCK']),
    bucket=environ['GCS_BUCKET_NAME']
)
storage_block.save(environ['GCS_STORAGE_BLOCK'], overwrite=True)

# BQ target config
target_configs = BigQueryTargetConfigs(
    schema=environ['BQ_TRANSFORMATION_SCHEMA'],
    credentials=GcpCredentials.load(environ['GCP_CREDENTIALS_BLOCK']),
)
target_configs.save(environ['DBT_TARGET_CONFIG_BLOCK'], overwrite=True)

# dbt profile
dbt_cli_profile = DbtCliProfile(
    name=environ['DBT_CLI_PROFILE'],
    target=environ['DBT_CLI_TARGET'],
    target_configs=BigQueryTargetConfigs.load(environ['DBT_TARGET_CONFIG_BLOCK']),
)
dbt_cli_profile.save(environ['DBT_CLI_PROFILE_BLOCK'], overwrite=True)

# dbt project
dbt_project = Dbt(path_to_dbt_project=environ['DBT_PROJECT_NAME'])
dbt_project.save(environ['DBT_PROJECT_BLOCK'], overwrite=True)

# Cloud Run Job
docker_image = f'{environ["GCP_CONTAINER_REPOSITORY_ADDRESS"]}/{environ["DOCKER_IMAGE_NAME"]}:{environ["DOCKER_IMAGE_TAG"]}'
cloud_run_job = CloudRunJob(
    image=docker_image,
    credentials=GcpCredentials.load(environ['GCP_CREDENTIALS_BLOCK']),
    region=environ['GCP_REGION'],
    timeout=3600
)
cloud_run_job.save(environ['GCP_CLOUD_RUN_JOB_BLOCK'], overwrite=True)
