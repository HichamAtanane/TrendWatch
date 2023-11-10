# Base image
FROM python:3.11.6 
# Set /airflow as our workdir
WORKDIR /airflow
# Copy the requirements.txt first to /airflow
COPY ./requirements.txt /airflow
# install python3.11-dev libpq-dev to install psycopg2 
RUN apt update && apt install -y python3.11-dev libpq-dev
# install project requirements
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --no-cache-dir --upgrade -r ./requirements.txt
# Copy the entire project to the /airflow directory
COPY . /airflow
# installing airflow
ENV AIRFLOW_HOME=/airflow
# When starting airflow do not load example dags
ENV AIRFLOW__CORE__LOAD_EXAMPLES='false'
# Install airflow-2.7.3 for python3.11
RUN python3 -m pip install "apache-airflow==2.7.3" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.7.3/constraints-3.11.txt"
# Initialize the metadata database
RUN python3 -m airflow db init
# Create airflow user
RUN python3 -m airflow users create \
    --username airflow \
    --password airflow \
    --firstname Peter \
    --lastname Parker \
    --role Admin \
    --email spiderman@superhero.org
# Start Airflow
CMD ["python3","-m","airflow","standalone"]
