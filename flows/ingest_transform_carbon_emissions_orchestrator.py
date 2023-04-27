from prefect import flow

from flows.ingest_carbon_emissions_raw import ingest_carbon_emissions_raw
from flows.transform_carbon_emissions import transform_carbon_emissions


"""
Parent flow that loads the raw data into BigQuery for a selected month then performs transformations using dbt
"""


@flow
def ingest_transform_carbon_emissions(
    months: list = ['nov'],
    years: list = ['2022']
):
    ingest_carbon_emissions_raw(months, years)
    transform_carbon_emissions()


if __name__ == '__main__':
    months = ['mar']
    years = ['2023']

    ingest_transform_carbon_emissions(months, years)
