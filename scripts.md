```
bq mkdef \
    --source_format=PARQUET \
    --hive_partitioning_mode=AUTO \
    --hive_partitioning_source_uri_prefix=gs://covid_datasets-dev/processed/ \
    gs://covid_datasets-dev/processed/*.parquet > summary

bq mk --external_table_definition=summary covid-274702:covid.summary	
```