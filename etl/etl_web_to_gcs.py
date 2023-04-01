from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket


# @task(retries=3)
def fetch(dataset_url: str, sheet_name: str='') -> pd.DataFrame:
    
    if dataset_url.split('.')[-1] == 'xls':
        df = pd.read_excel(
            dataset_url,
            sheet_name='Factors by Category',
            engine='xlrd',
            header=4,
            index_col=None,
            usecols=[
                'Scope',
                'Level 1',
                'Level 2',
                'Level 3',
                'Level 4',
                'Column Text',
                'UOM',
                'GHG/Unit',
                'GHG Conversion Factor 2022',
            ]
        )
    else:
        df = pd.read_csv(dataset_url)

    return df


# @task(log_prints=True)
# def clean(df: pd.DataFrame) -> pd.DataFrame:
#     """Fix dtype issues"""
#     df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
#     df["tpep_dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"])
#     print(df.head(2))
#     print(f"columns: {df.dtypes}")
#     print(f"rows: {len(df)}")
#     return df


# @task()
# def write_local(df: pd.DataFrame, color: str, dataset_file: str) -> Path:
#     """Write DataFrame out locally as parquet file"""
#     path = Path(f"data/{color}/{dataset_file}.parquet")
#     df.to_parquet(path, compression="gzip")
#     return path


# @task()
# def write_gcs(path: Path) -> None:
#     """Upload local parquet file to GCS"""
#     gcs_block = GcsBucket.load("de-zoomcamp-gcs")
#     gcs_block.upload_from_path(from_path=path, to_path=path)
#     return


# @flow()
def etl_web_to_gcs() -> None:
    
    month = 'nov'
    year = 2022

    energy_consumption_dataset_file = f'ministry_of_justice_{month}-{year}'
    energy_consumption_dataset_url = f'http://www.ecodriver.uk.com/eCMS/Files/MOJ/ministryofjustice_{month}-{year}.csv'
    conversion_factors_dataset_file = f'ghg_conversion_factors-{year}'
    conversion_factors_dataset_url = f'https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1105317/ghg-conversion-factors-{year}-flat-format.xls'
    sheet_name = 'Factors by Category' # index of sheet in workbook
    
    df = fetch(conversion_factors_dataset_url)
    # df_clean = clean(df)
    # path = write_local(df_clean, color, dataset_file)
    # write_gcs(path)


if __name__ == "__main__":
    etl_web_to_gcs()

