from prefect import get_client
from prefect.deployments import Deployment
from load_data import load_data_parent_flow
from prefect_gcp import CloudRunJob, GcsBucket


client = get_client()

gcs_block = GcsBucket.load('de-zoomcamp-gcs-bucket')
cloud_run_job_block = CloudRunJob.load('prefect-data-ingestion-job')

deployment = Deployment.build_from_flow(
    flow=load_data_parent_flow,
    name='cloud-run-flow',
    storage=gcs_block,
    infrastructure=cloud_run_job_block,
)

if __name__ == '__main__':
    deployment.apply()