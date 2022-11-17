# Apache Airflow

**From**: https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html

### Guide

**Initializing Environment**

Setting the right Airflow user

```bash
mkdir -p ./dags ./logs ./plugins
echo -e "AIRFLOW_UID=$(id -u)" > .env
```


Initialize the database

```bash
docker compose up airflow-init
```

**Running Airflow**

```bash
docker-compose up
```

Shuld now run at [http://localhost:8080](http://localhost:8080)