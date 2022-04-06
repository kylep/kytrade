"""pytest conf"""
import pytest


@pytest.fixture
def mock_time_series(mocker):
    """Alphavantage time series API call"""

    class MockTimeSeries:
        def __init__(self, key):
            pass

        def get_daily(self, ticker, outputsize):
            data = {
                "2000-02-02": {
                    "1. open": 11.11,
                    "2. high": 22.22,
                    "3. low": 10.10,
                    "4. close": 12.12,
                    "5. volume": 123123,
                }
            }
            return (data, None)

    mocker.patch("kytrade.api.client.alphavantage.TimeSeries", MockTimeSeries)
