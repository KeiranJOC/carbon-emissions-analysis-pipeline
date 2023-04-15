import pandas as pd

from pathlib import Path
from prefect import flow, task
from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket


@task(retries=3)
def fetch(dataset_url: str, year: int) -> pd.DataFrame:
    
    # conversion factors file is .xlsx; energy consumption files are .csv
    if dataset_url.split('.')[-1] == 'xlsx':
        df = pd.read_excel(
            dataset_url,
            engine='openpyxl',
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
                f'GHG Conversion Factor {year}',
            ]
        )
    else:
        df = pd.read_csv(dataset_url)

    return df


@task(log_prints=True)
def clean(df: pd.DataFrame) -> pd.DataFrame:

    df_clean = df.copy()

    # clean column names
    df_clean.columns = [x.replace(' ', '_').replace('/', '_').replace(':', '').lower() for x in df_clean.columns]

    # convert all columns to string
    df_clean = df_clean.fillna('')
    df_clean = df_clean.astype(str)

    # convert date column to datetime so that we can use it for partitioning
    if 'date' in df_clean.columns:
        df_clean['date'] = pd.to_datetime(df_clean['date'], dayfirst=True)
    
    print(f'Shape: {df_clean.shape}\n')

    return df_clean


@task()
def write_to_local(df: pd.DataFrame, dataset_file: str) -> Path:

    path = Path(f'data/{dataset_file}.parquet')
    df.to_parquet(path, compression='gzip')
    
    return path


@task()
def write_to_gcs(path: Path) -> None:

    gcs_block = GcsBucket.load('de-zoomcamp-gcs')
    gcs_block.upload_from_path(from_path=path, to_path=path)


@task()
def write_to_bq(df: pd.DataFrame, table_name: str) -> None:

    gcp_credentials_block = GcpCredentials.load('de-zoomcamp-gcp')

    df.to_gbq(
        destination_table=f'carbon_emissions_raw.{table_name}',
        project_id='spry-alignment-375710',
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        if_exists='append'
    )


@flow()
def load_dataset(year: int, table_name: str, file_info: dict) -> None:
    
    print(f"Dataset: {file_info['name']}")
    df = fetch(file_info['path'], year)
    df_clean = clean(df)
    path = write_to_local(df_clean, file_info['name'])
    write_to_gcs(path)
    write_to_bq(df_clean, table_name)


@flow()
def load_data_parent_flow(months: list[str] = ['nov'], years: list[int] = [2022]) -> None:

    for year in years:
        
        conversion_factors_file = {
            'path': f'data/ghg-conversion-factors-{year}-flat-format.xlsx',
            'name': f'ghg-conversion-factors-{year}',
        }
        load_dataset(year=year, table_name='conversion_factors_raw', file_info=conversion_factors_file)

        for month in months:    
            energy_consumption_file = {
                'path': f'http://www.ecodriver.uk.com/eCMS/Files/MOJ/ministryofjustice_{month}-{year}.csv',
                'name': f'ministry_of_justice_{month}-{year}',
            }
            load_dataset(year=year, table_name='energy_consumption_raw', file_info=energy_consumption_file)


if __name__ == '__main__':
    
    months = [
        'jan',
        'feb',
        'mar',
        'apr',
        'may',
        'jun',
        'jul',
        'aug',
        'sep',
        'oct',
        'nov',
        'dec',
    ]
    years = [2022]

    load_data_parent_flow(months=months, years=years)

