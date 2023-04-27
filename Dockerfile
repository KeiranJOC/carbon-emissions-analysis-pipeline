FROM prefecthq/prefect:2.10.5-python3.9

COPY blocks /opt/prefect/blocks
COPY flows /opt/prefect/flows
COPY dbt_de_zoomcamp /opt/prefect/dbt_de_zoomcamp
COPY .env /opt/prefect/.env
COPY setup.py /opt/prefect/setup.py
COPY requirements.txt /opt/prefect/requirements.txt

RUN pip install -r requirements.txt --trusted-host pypi.python.org --no-cache-dir