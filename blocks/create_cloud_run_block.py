from os import environ
from dotenv import load_dotenv
from prefect_gcp import CloudRunJob, GcpCredentials


load_dotenv()

def cloud_run_job(docker_image: str) -> None:
    cloud_run_job = CloudRunJob(
        image=docker_image,
        credentials=GcpCredentials.load(environ['GCP_CREDENTIALS_BLOCK']),
        region=environ['GCP_REGION'],
        timeout=3600
    )
    cloud_run_job.save(environ['GCP_CLOUD_RUN_JOB_BLOCK'], overwrite=True)

if __name__ == '__main__':
    docker_image = f'{environ["GCP_CONTAINER_REPOSITORY_ADDRESS"]}/{environ["DOCKER_IMAGE_NAME"]}:{environ["DOCKER_IMAGE_TAG"]}'
    print(docker_image)
    cloud_run_job(docker_image)