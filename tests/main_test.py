import json
import os
import unittest
from unittest import mock
from unittest.mock import patch, Mock

from flask import Flask, request

import main
import dask.dataframe as dd


class MainTest(unittest.TestCase):
    def setUp(self) -> None:
        self.bucket_name = os.getenv('BUCKET_NAME')

        self.app = Flask(__name__)

        @self.app.route('/', methods=['POST'])
        def endpoint():
            return main.run(request)

    def tearDown(self) -> None:
        os.remove(os.path.join(os.path.dirname(main.__file__), 'tests', 'stubs', 'processed', 'dt=2020-04', '2020-04-21.parquet'))

    @mock.patch.dict(os.environ, {'BUCKET_NAME': f"{os.path.dirname(main.__file__)}/tests/stubs/"})
    @mock.patch('flask.request')
    def test_should_save_summary_data(self, request_mock):
        request_mock.get_json.return_value = {'process_date': '2020-04-21'}

        with patch('google.cloud.storage.Client') as client_mock:
            main.run(request_mock)
            dataframe = dd.read_parquet(os.path.join(os.path.dirname(main.__file__), 'tests', 'stubs', 'processed', 'dt=2020-04', '2020-04-21.parquet'))
            dataframe = dataframe.compute()
            self.assertIs(248, len(dataframe))
