import pytest
import pandas as pd

from stock_price_display import calculation as c


@pytest.mark.parametrize('securities', [['COF', 'GOOGL', 'MSFT'],
                         ['COF', 'GOOGL'], ['MSFT']])
def test_get_prices(securities):
    """Make sure the api returns the data we want"""
    df = c.get_prices(securities, '2017-01-01', '2017-06-31')
    assert set(df.columns) == set([
        'ticker', 'date', 'high', 'low', 'open', 'close', 'volume'])
    assert len(df) == len(df.date.unique()) * len(securities)


@pytest.fixture(scope='module')
def price_data():
    # Pick two days with data, so we can be sure we're getting two rows of data
    # per security
    return c.get_prices(['COF', 'GOOGL', 'MSFT'], '2017-01-01', '2017-06-31')


def test_avg_open_close_output_correct(price_data):
    """Test avg open/close against manual calculation for one security"""
    avg_df = price_data
    res = c.calculate_average_open_close(avg_df)

    avg_df = avg_df.loc[(avg_df['ticker'] == 'COF') &
                        (avg_df['date'] < '2017-02-01')]
    month_avg = avg_df['open'].sum() / len(avg_df)

    assert res.loc[(res['ticker'] == 'COF') & (res['month'] == 1),
                   'open'].item() == month_avg


def test_max_daily_profit_output_correct(price_data):
    """Test max profit against manual calculation for one security"""
    max_df = price_data
    res = c.calculate_max_profit(price_data)

    max_df = max_df.loc[(max_df['ticker'] == 'GOOGL')]
    max_df['profit'] = max_df['high'] - max_df['low']
    max_df = max_df.sort_values(by='profit', ascending=False).reset_index()
    max_profit = max_df.loc[0, 'profit']

    assert res.loc[(res['ticker'] == 'GOOGL'), 'profit'].item() == max_profit


def test_busy_day_output_correct(price_data):
    """Test busy day against manual calculation for one security"""
    volume_df = price_data
    res = c.calculate_busy_day(price_data)

    volume_df = volume_df.loc[(volume_df['ticker'] == 'MSFT')]
    avg_volume = volume_df['volume'].sum() / len(volume_df)
    volume_df['high_volume'] = volume_df['volume'] > 1.1 * avg_volume
    busy_days = volume_df.loc[volume_df['high_volume'] == True]

    assert (sorted(res.loc[res['ticker'] == 'MSFT'].date.unique() ==
                   busy_days.date.unique()))


def test_biggest_loser_output_correct(price_data):
    """Test biggest loser against manual calculation"""
    delta_df = price_data
    res = c.calculate_biggest_loser(delta_df)
    highest_loss = ('TBD', 0)
    for security in ['COF', 'GOOGL', 'MSFT']:
        check_df = delta_df.loc[delta_df['ticker'] == security]
        check_df['loss'] = check_df['close'] < check_df['open']
        check_df = (check_df.loc[check_df['loss'] == True])
        loss = len(check_df)
        if loss > highest_loss[1]:
            highest_loss = (security, loss)
    assert all(res == pd.DataFrame({'ticker': highest_loss[0],
                                    'num_days': highest_loss[1]}, index=[0]))

