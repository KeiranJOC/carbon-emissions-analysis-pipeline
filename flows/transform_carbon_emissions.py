from os import environ
from prefect import flow
from blocks.dbt import Dbt
from dotenv import load_dotenv


load_dotenv()

@flow
def transform_carbon_emissions():
    dbt = Dbt.load(environ['DBT_PROJECT_BLOCK'])
    # dbt.dbt_cli('dbt debug')
    dbt.dbt_cli('dbt deps')
    dbt.dbt_cli('dbt compile')
    dbt.dbt_run_from_manifest()


if __name__ == '__main__':
    transform_carbon_emissions()
