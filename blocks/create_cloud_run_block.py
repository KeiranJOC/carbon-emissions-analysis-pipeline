from os import environ
from dotenv import load_dotenv
from prefect_gcp import CloudRunJob, GcpCredentials


load_dotenv()

def cloud_run_job(docker_image_name: str) -> None:
    cloud_run_job = CloudRunJob(
        image=docker_image_name,
        credentials=GcpCredentials.load(environ['GCP_CREDENTIALS_BLOCK']),
        region=environ['GCP_REGION'],
    )
    cloud_run_job.save(environ['GCP_CLOUD_RUN_JOB_BLOCK'], overwrite=True)
