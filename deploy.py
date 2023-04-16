import subprocess

from os import environ
from dotenv import load_dotenv
from prefect.deployments import Deployment
from prefect_gcp import CloudRunJob, GcsBucket
from blocks.create_cloud_run_block import cloud_run_job
from flows.ingest_transform_carbon_emissions_orchestrator import ingest_transform_carbon_emissions


load_dotenv()
docker_image_name = f'{environ["GCP_CONTAINER_REPOSITORY_ADDRESS"]}/{environ["DOCKER_IMAGE_NAME"]}:{environ["DOCKER_IMAGE_TAG"]}'

if __name__ == '__main__':
    subprocess.run('python blocks/create_blocks.py', shell=True)
    
    subprocess.run(f'docker build -t {docker_image_name} .', shell=True)
    subprocess.run(f'docker push {docker_image_name}', shell=True)
    
    cloud_run_job(docker_image_name)
    
    # deployment = Deployment.build_from_flow(
    #     flow=ingest_transform_carbon_emissions,
    #     name=environ['PREFECT_DEPLOYMENT_NAME'],
    #     storage=GcsBucket.load(environ['GCS_BUCKET_BLOCK']),
    #     infrastructure=CloudRunJob.load(environ['GCP_CLOUD_RUN_JOB_BLOCK'])
    # )
    # deployment.apply()

    name=environ['PREFECT_DEPLOYMENT_NAME']
    storage_block = f'gcs/{environ["GCS_BUCKET_BLOCK"]}'
    infrastructure_block = f'cloud-run-job/{environ["GCP_CLOUD_RUN_JOB_BLOCK"]}'
    work_queue = 'default'
    subprocess.run(
        f'prefect deployment build flows/ingest_transform_carbon_emissions_orchestrator.py:ingest_transform_carbon_emissions --infra-block {infrastructure_block} --storage-block {storage_block} --work-queue {work_queue} --name {name} --apply'
    )