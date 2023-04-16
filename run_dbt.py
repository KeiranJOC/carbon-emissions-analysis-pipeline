from prefect import flow
from prefect_dbt.cli import DbtCoreOperation


@flow
def run_dbt():
    
    dbt_job = DbtCoreOperation.load('dbt-job')
    result = dbt_job.run()

    return result


if __name__ == '__main__':
    run_dbt()