```
bq mkdef \
    --source_format=PARQUET \
    --hive_partitioning_mode=AUTO \
    --hive_partitioning_source_uri_prefix=gs://covid_datasets-dev/processed/ \
    gs://covid_datasets-dev/processed/*.parquet > countries

bq mk --external_table_definition=countries covid-274702:covid.countries	
```