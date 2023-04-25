from prefect import flow

from flows.ingest_carbon_emissions_raw import ingest_carbon_emissions_raw
from flows.transform_carbon_emissions import transform_carbon_emissions


@flow
def ingest_transform_carbon_emissions(
    months: list = ['nov'],
    years: list = ['2022']
):
    ingest_carbon_emissions_raw(months, years)
    transform_carbon_emissions()


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
    years = ['2022']

    ingest_transform_carbon_emissions(months, years)
