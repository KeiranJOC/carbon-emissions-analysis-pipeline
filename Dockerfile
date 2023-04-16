FROM prefecthq/prefect:2.7.7-python3.9

# COPY requirements.txt .

# RUN pip install -r requirements.txt --trusted-host pypi.python.org --no-cache-dir

COPY blocks /opt/prefect/blocks
COPY flows /opt/prefect/flows
COPY dbt_de_zoomcamp /opt/prefect/dbt_de_zoomcamp
COPY setup.py /opt/prefect/setup.py
COPY requirements.txt /opt/prefect/requirements.txt

RUN pip install . --trusted-host pypi.python.org --no-cache-dir