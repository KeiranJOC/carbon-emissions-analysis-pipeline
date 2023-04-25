import pandas as pd

from os import environ
from pathlib import Path
from dotenv import load_dotenv
from prefect import flow, task
from prefect_gcp import GcpCredentials, GcsBucket


load_dotenv()

@task(retries=3)
def fetch_conversion_factors_raw(path: str, year: str) -> pd.DataFrame:
    return pd.read_excel(
        path,
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
            'GHG',
            f'GHG Conversion Factor {year}',
        ]
    )


@task(retries=3)
def fetch_energy_consumption_raw(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


@task(log_prints=True)
def clean(df: pd.DataFrame, year: str) -> pd.DataFrame:
    # clean column names and convert to string to avoid PyArrow conversion errors when saving to Parquet
    # also remove the year from any column names and add it as a new column that can be used for partitioning
    df.columns = [x.replace(year, '').strip().replace(' ', '_').replace('/', '_').replace(':', '').lower() for x in df.columns]
    df = df.fillna('')
    df = df.astype(str)
    df['year'] = pd.to_datetime(year)

    # convert date column to date type so it can be used for partitioning
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], dayfirst=True)
    
    return df


@task()
def write_to_local(df: pd.DataFrame, file: str) -> Path:
    path = Path(f'flows/data/{file}.parquet')
    df.to_parquet(path, compression='gzip')
    
    return path


@task()
def write_to_gcs(path: Path) -> None:
    gcs_block = GcsBucket.load(environ['GCS_STORAGE_BLOCK'])
    gcs_block.upload_from_path(from_path=path, to_path=path)


@task()
def write_to_bq(df: pd.DataFrame, table_name: str) -> None:
    print(df.columns)
    gcp_credentials_block = GcpCredentials.load(environ['GCP_CREDENTIALS_BLOCK'])
    df.to_gbq(
        destination_table=f'{environ["BQ_INGESTION_SCHEMA"]}.{table_name}',
        project_id=environ['GCP_PROJECT_ID'],
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        if_exists='append'
    )

@flow()
def load_dataset(df, year: str, file_name: str, table_name: str) -> None:
    df_clean = clean(df, year)
    path = write_to_local(df_clean, file_name)
    write_to_gcs(path)
    write_to_bq(df_clean, table_name)


@flow
def ingest_carbon_emissions_raw(months: list[str] = ['nov'], years: list[str] = ['2022']) -> None:
    for year in years:
        conversion_factors_df = fetch_conversion_factors_raw(path=f'{environ["CONVERSION_FACTORS_RAW_DATA_URL_BASE"]}-{year}.{environ["CONVERSION_FACTORS_RAW_DATA_FILE_TYPE"]}', year=year)
        load_dataset(
            conversion_factors_df,
            year,
            file_name=f'{environ["CONVERSION_FACTORS_RAW_DATA_OUTPUT_BASE"]}-{year}',
            table_name=environ['BQ_CONVERSION_FACTORS_INGESTION_TABLE']
        )

        for month in months:    
            energy_consumption_df = fetch_energy_consumption_raw(path=f'{environ["ENERGY_CONSUMPTION_RAW_DATA_URL_BASE"]}_{month}-{year}.{environ["ENERGY_CONSUMPTION_RAW_DATA_FILE_TYPE"]}')
            load_dataset(
                energy_consumption_df,
                year,
                file_name=f'{environ["ENERGY_CONSUMPTION_RAW_DATA_OUTPUT_BASE"]}_{month}-{year}',
                table_name=environ['BQ_ENERGY_CONSUMPTION_INGESTION_TABLE']
            )


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
    years = [
        '2019',
        '2020',
        '2021',
        '2022'
    ]

    ingest_carbon_emissions_raw(months=months, years=years)
