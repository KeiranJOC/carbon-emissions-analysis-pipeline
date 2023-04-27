import logging

from os import environ
from dotenv import load_dotenv
from prefect.deployments import Deployment
from prefect_gcp import CloudRunJob, GcsBucket
from blocks.create_cloud_run_block import cloud_run_job
from flows.ingest_transform_carbon_emissions_orchestrator import transform_carbon_emissions
from flows.ingest_transform_carbon_emissions_orchestrator import ingest_carbon_emissions_raw
from flows.ingest_transform_carbon_emissions_orchestrator import ingest_transform_carbon_emissions


"""
Build deployments to ingest data, transform data, or both
"""

load_dotenv()

if __name__ == '__main__':    
    full_deployment = Deployment.build_from_flow(
        flow=ingest_transform_carbon_emissions,
        name=environ['PREFECT_DEPLOYMENT_NAME'],
        version='1',
        storage=GcsBucket.load(environ['GCS_STORAGE_BLOCK']),
        infrastructure=CloudRunJob.load(environ['GCP_CLOUD_RUN_JOB_BLOCK']),
    )
    full_deployment.apply()

    ingest_deployment = Deployment.build_from_flow(
        flow=ingest_carbon_emissions_raw,
        name=environ['PREFECT_DEPLOYMENT_NAME'],
        version='1',
        storage=GcsBucket.load(environ['GCS_STORAGE_BLOCK']),
        infrastructure=CloudRunJob.load(environ['GCP_CLOUD_RUN_JOB_BLOCK']),
    )
    ingest_deployment.apply()

    transform_deployment = Deployment.build_from_flow(
        flow=transform_carbon_emissions,
        name=environ['PREFECT_DEPLOYMENT_NAME'],
        version='1',
        storage=GcsBucket.load(environ['GCS_STORAGE_BLOCK']),
        infrastructure=CloudRunJob.load(environ['GCP_CLOUD_RUN_JOB_BLOCK']),
    )
    transform_deployment.apply()