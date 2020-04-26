import datetime

import pytz

import settings
from storage import Storage


class CovidProcessing:
    def __init__(self, storage):
        self.storage = storage

    def __call__(self, process_date):

        def get_countries(data):
            return data.get('Countries')

        bag = self.storage.read(process_date)
        bag = bag \
            .map(get_countries) \
            .flatten()

        dataframe = bag.to_dataframe(meta={
            "Country": str,
            "CountryCode": str,
            "Slug": str,
            "NewConfirmed": 'Int64',
            "TotalConfirmed": 'Int64',
            "NewDeaths": 'Int64',
            "TotalDeaths": 'Int64',
            "NewRecovered": 'Int64',
            "TotalRecovered": 'Int64',
            "Date": 'datetime64[ns]'
        })

        self.storage.store(dataframe.compute(), process_date)


def run(request):
    from google.cloud import storage
    app = CovidProcessing(Storage(storage.Client()))
    data = request.get_json(silent=True)
    if not data:
        data = {"process_date": str(datetime.datetime.now(tz=pytz.timezone("America/Sao_Paulo")).date())}
    process_date = datetime.datetime.strptime(data.get('process_date'), '%Y-%m-%d').date()
    app(process_date)
