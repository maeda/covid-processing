import datetime
import os
import unittest
import main
from unittest import mock

import settings

from unittest.mock import patch

from storage import Storage


class StorageTest(unittest.TestCase):
    @mock.patch.dict(os.environ, {'BUCKET_NAME': f"{os.path.dirname(main.__file__)}/tests/stubs/"})
    def test_should_read_bag_from_storage(self):
        with patch('google.cloud.storage.Client') as client_mock:
            storage = Storage(client_mock)
            data = storage.read(datetime.datetime(2020, 4, 21).date())
            result = data.compute()

            self.assertGreater(len(result), 0)
