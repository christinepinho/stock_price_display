import quandl
from stock_price_display.config import api_key
from stock_price_display import formatting as f


def get_prices(securities, start_date, end_date):
    """Given a set of securities and data range, returns open,
    close, high and close prices, as well as volume for each security
    for each date
    """
    quandl.ApiConfig.api_key = api_key
    data = quandl.get_table('WIKI/PRICES', ticker=securities,
                            qopts={'columns': ['ticker', 'date', 'high', 'low',
                                               'open', 'close', 'volume']},
                            date={'gte': start_date, 'lte': end_date})
    return data


def calculate_average_open_close(open_close_df):
    """Given a dataframe of tickers, dates, and open/close prices per day,
    calculate the average open and close of each security, by month
    """
    open_close_df = f._format_date_to_month(open_close_df)
    open_close_df = open_close_df.groupby(['month', 'ticker'],
                                          as_index=False).mean()
    return open_close_df[['month', 'ticker', 'open', 'close']]


def calculate_max_profit(profit_df):
    """Given a dataframe of tickers, dates, and high/low prices per day,
    calculate the max profit each security made in a single day
    """
    profit_df['profit'] = profit_df['high'] - profit_df['low']
    profit_df = profit_df.loc[profit_df.groupby(['ticker'])['profit'].idxmax()]
    return profit_df[['ticker', 'date', 'profit']]


def calculate_busy_day(volume_df):
    """Given a dataframe of tickers, dates, and volumes per day,
    calculate which days generated unusually high activity for securities
    """
    # create an avg volume dataframe to merge on
    avg_volume_df = volume_df[['date', 'ticker', 'volume']].copy(deep=True)
    avg_volume_df = avg_volume_df.groupby(['ticker'], as_index=False).mean()
    avg_volume_df.rename(columns={'volume': 'avg_volume'}, inplace=True)
    volume_df = volume_df.merge(avg_volume_df, on=['ticker'])

    # calculate higher than average volume
    volume_df = volume_df.loc[
        volume_df['volume'] > (1.1 * volume_df['avg_volume'])]
    return volume_df[['ticker', 'date', 'volume', 'avg_volume']]


def calculate_biggest_loser(delta_df):
    """Given a dataframe of tickers, dates, and open/close prices,
    calculate which security had the most losing days
    """
    delta_df['num_days'] = (delta_df['close'] < delta_df['open']).astype(int)
    delta_df = delta_df.groupby(['ticker'],
                                as_index=False)['num_days'].sum().max()
    return delta_df[['ticker', 'num_days']]

