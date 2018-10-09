import pytest
import pandas as pd
from datetime import datetime, timedelta

from stock_price_display import formatting as f


@pytest.fixture(scope='module')
def today():
    return datetime.today()


@pytest.fixture(scope='module')
def tomorrow(today):
    return today + timedelta(1)


@pytest.fixture(scope='function')
def df_to_format(today):
    days = pd.date_range(today, today + timedelta(3))
    open_price = [1234.59090906] * 4
    return pd.DataFrame({'date': days, 'open': open_price})


def test_format_datetime_funcs(df_to_format):
    df_to_format = f._format_date_to_month(df_to_format)
    assert df_to_format['month'].unique() == [datetime.now().month]
    df_to_format = f._format_datetime_col_to_str(df_to_format, 'date')
    # series remains an 'o' dtype, but each value should be a string
    assert all(type(val) == str for val in df_to_format['date'].unique())


def test_format_currency(df_to_format):
    df_to_format = f._format_data_to_currency(df_to_format, ['open'])
    assert df_to_format['open'].unique() == ['$1,234.59']


def test_format_average_open_close():
    test_data = pd.DataFrame({'ticker': ['GOOGL'] * 2,
                              'month': [1, 2],
                              'open': [823, 828],
                              'close': [824, 827]})
    formatted_dict = f.format_average_open_close(test_data)
    assert formatted_dict == {'GOOGL': [{'month': '2017-1',
                                         'average_open': '$823.00',
                                         'average_close': '$824.00'},
                                        {'month': '2017-2',
                                         'average_open': '$828.00',
                                         'average_close': '$827.00'}]}


def test_format_max_profit(today, tomorrow):
    days = pd.date_range(today, tomorrow)
    test_data = pd.DataFrame({'ticker': ['COF', 'MSFT'],
                              'date': days,
                              'profit': [2.0000, 1.2456]})
    formatted_dict = f.format_max_profit(test_data)
    assert formatted_dict == {
        'COF': [{'date': today.strftime('%Y-%m-%d'),
                 'profit': '$2.00'}],
        'MSFT': [{'date': tomorrow.strftime('%Y-%m-%d'),
                  'profit': '$1.25'}]}


def test_format_busy_day(today, tomorrow):
    test_data = pd.DataFrame({'ticker': ['COF', 'COF', 'MSFT'],
                              'date': [today, today + timedelta(1), today],
                              'avg_volume': [123456.042, 123456.042, 120000.0],
                              'volume': [148147.2, 148147.2, 144000]})
    formatted_dict = f.format_busy_day(test_data)
    assert formatted_dict == {
        'COF': {'avg_volume_123456.04': [
            {'date': today.strftime('%Y-%m-%d'), 'volume': 148147.2},
            {'date': tomorrow.strftime('%Y-%m-%d'), 'volume': 148147.2}]},
        'MSFT': {'avg_volume_120000.0': [
            {'date': today.strftime('%Y-%m-%d'), 'volume': 144000}]}}


def test_format_biggest_loser():
    test_data = pd.Series(['MSFT', 56], ['ticker', 'num_days'])
    formatted_dict = f.format_biggest_loser(test_data)
    assert formatted_dict == {'MSFT': {'num_days': 56}}
