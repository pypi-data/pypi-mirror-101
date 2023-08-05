"""Module containing OHLCV class."""

import os

from aws.paramstore import ParameterStore
import pandas as pd
import psycopg2

from trading.etl.ohlcv.core.metadata import OHLCVMetadata
from trading.etl.ohlcv.core.metadata import SECONDS_TO_UNIT_MAPPING
from trading.etl.ohlcv.core.metadata import Timeframe

from trading.etl.ohlcv.core.errors import DBQueryGenerationError


__all__ = [
    # Class exports
    'OHLCV',
]


class OHLCVSeries(pd.Series):
    """Makes sure that slicing OHLCV data returns a new OHLCV as well."""

    @property
    def _constructor(self):
        return OHLCVSeries

    @property
    def _constructor_expanddim(self):  # pragma: no cover
        return OHLCV


class OHLCV(pd.DataFrame):
    """OHLCV (Opening, Highest, Lowest, Closing, Volume) dataframe."""

    _INDEX_COLUMN_NAME = 'timestamp'
    _DEFAULT_COLUMNS = [
        _INDEX_COLUMN_NAME,
        'open_price',
        'high_price',
        'low_price',
        'close_price',
        'volume'
    ]

    _RESAMPLE_FUNCTIONS = {
        'open_price': 'first',
        'high_price': 'max',
        'low_price': 'min',
        'close_price': 'last',
        'volume': 'sum',
    }

    # Allow transfer of data in new OHLCV frame
    _metadata = ['timeframe', 'metadata']

    def __init__(self, data):
        # Initialize parent DataFrame class using standard column and dtype
        super().__init__(data, columns=self._DEFAULT_COLUMNS)

        # Make the timeframe column the index of the dataframe
        self[self._INDEX_COLUMN_NAME] = pd.to_datetime(
            self[self._INDEX_COLUMN_NAME], unit='ms')

        # OHLCV metadata
        self.timeframe = self._detect_timeframe()
        self.metadata = OHLCVMetadata()

    @property
    def _constructor(self):
        return OHLCV

    @property
    def _constructor_sliced(self):
        return OHLCVSeries

    @property
    def timeframe(self):
        return self._timeframe

    @timeframe.setter
    def timeframe(self, value):
        # TODO: Resample
        self._timeframe = Timeframe(value)

    def _detect_timeframe(self):
        """Automagically get the timeframe."""
        # Don't even try if the there are less than two rows
        if len(self.index) < 2:
            return None

        # Get the average seconds difference between row timestamps
        average_timedelta = self[self._INDEX_COLUMN_NAME].diff()
        average_timedelta = int(average_timedelta.dt.total_seconds().mean())

        for duration_in_seconds, unit in SECONDS_TO_UNIT_MAPPING.items():
            # Ignore second timeframe if its more than a minute
            if duration_in_seconds == 1 and average_timedelta > 60:
                continue

            # Check if average timedelta is divisible by any of the conversions
            if average_timedelta % duration_in_seconds == 0:
                return f'{average_timedelta // duration_in_seconds}{unit}'

        # No more ways to detect the timeframe, just return None
        return None

    def generate_db_query(self):
        """Converts the OHLCV data into a PostgreSQL query string."""
        # Check internal properties to see if its possible to generate a query
        if not all([
            self.metadata.exchange, self.metadata.symbol,
            self.timeframe.interval, self.timeframe.unit]):
            raise DBQueryGenerationError('Internal metadata not set')

        try:
            # Create a local instance of OHLCV-related parameters
            env = os.environ.get('AWS_ENVIRONMENT', 'dev')
            paramstore = ParameterStore(f'/{env}/trading/etl/ohlcv/db/')

            # Create a DB connection to fetch exchange and market IDs
            db_connection = psycopg2.connect(
                database=paramstore['name'],
                user=paramstore['username'],
                password=paramstore['password'],
                host=paramstore['host'],
                port=paramstore['port'],
            )
            db_cursor = db_connection.cursor()

        except Exception as err:
            raise DBQueryGenerationError('Unable to connect to DB') from err

        # Get the market ID for building the query
        query = "SELECT id FROM markets WHERE exchange_id IN ("
        query += "SELECT id FROM exchanges WHERE "
        query += f"name = '{self.metadata.exchange}') AND "
        query += f"symbol = '{self.metadata.symbol}'"

        # Execute the query and fetch the market ID
        try:
            db_cursor.execute(query)
            market_id = db_cursor.fetchall()[0][0]
        except Exception as err:
            raise DBQueryGenerationError('Unable to fetch market ID') from err

        # Manipulate query values, add market ID
        query_values = [[market_id] + row for row in self.values.tolist()]
        query_columns = ['market_id'] + self._DEFAULT_COLUMNS

        query = f'INSERT INTO ohlcv_{self.timeframe} ('
        query += f'{", ".join(query_columns)}) VALUES '
        query += self._list_of_list_to_string(query_values)

        return query

    @staticmethod
    def _list_of_list_to_string(llist):
        qstr = lambda x: f"'{str(x)}'" if ' ' in str(x) else str(x)
        return ','.join(['(' + ','.join(map(qstr, e)) + ')' for e in llist])
