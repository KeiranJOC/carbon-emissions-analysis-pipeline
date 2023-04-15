from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket


# copy your own service_account_info dictionary from the json file you downloaded from google
# IMPORTANT - do not store credentials in a publicly available repository!

credentials_block = GcpCredentials(
    # enter your credentials from the json file inside the dict - delete after block has been created
    service_account_info={}
)
credentials_block.save('de-zoomcamp-gcp', overwrite=True)

bucket_block = GcsBucket(
    gcp_credentials=GcpCredentials.load('de-zoomcamp-gcp'),
    bucket='de-data-lake_spry-alignment-375710', # replace with the name of the "data-lake-bucket" resource that Terraform created
)

bucket_block.save('de-zoomcamp-gcs', overwrite=True)