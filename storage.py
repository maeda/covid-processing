import datetime
import json
import os
import dask.bag as db


from google.cloud.storage import Client


class Storage:

    def __init__(self, client: Client):
        self.protocol = os.getenv('STORAGE_PROTOCOL')
        self.bucket_name = os.getenv('BUCKET_NAME')
        self.client = client

    def store(self, data, process_date):
        path = process_date.strftime('dt=%Y-%m/')
        filename = f"{str(process_date)}.parquet"

        return data.to_parquet(
            os.path.join(self.protocol,
                         self.bucket_name,
                         'processed',
                         path,
                         filename))

    def read(self, process_date: datetime.date):
        path = process_date.strftime('%Y/%m/')
        filename = f"{str(process_date)}.json"

        return db.read_text(
            os.path.join(self.protocol,
                         self.bucket_name,
                         'raw',
                         path,
                         filename)) \
            .map(json.loads)
