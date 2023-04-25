import json

from os import environ
from prefect import flow
from blocks.dbt import Dbt
from dotenv import load_dotenv
from prefect_gcp import GcpCredentials, GcsBucket
from prefect_dbt.cli import BigQueryTargetConfigs, DbtCliProfile


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
