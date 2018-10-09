def _format_date_to_month(df):
    """Given a dataframe with a date column, parse that into a month column"""
    df['month'] = df['date'].dt.month
    return df


def _format_data_to_currency(df, data_cols):
    """Transform data cols into str columns following the format $xx.xx"""
    for col in data_cols:
        df[col] = df[col].map('${:,.2f}'.format)
    return df


def _format_datetime_col_to_str(df, col):
    """"Transform datetime col into str column for display"""
    df[col] = df[col].dt.strftime('%Y-%m-%d')
    return df


def format_average_open_close(open_close_df):
    """Output open/close data in the following format:
    {ticker_name:
        [{'month': YYYY-MM, 'average_open': $xx.xx, 'average_close': $xx.xx},
         'month': YYYY-MM, 'average_open': $xx.xx, 'average_close': $xx.xx}]}
    """
    open_close_df['month'] = open_close_df['month'].astype(str)
    open_close_df['month'] = "2017-" + open_close_df['month']
    open_close_df = _format_data_to_currency(open_close_df, ['open', 'close'])
    open_close_df.sort_values(['ticker', 'month', 'open', 'close'],
                              inplace=True)
    open_close_df.rename(columns={'open': 'average_open', 'close':
                                  'average_close'}, inplace=True)
    res = {}
    for ticker in open_close_df['ticker'].unique():
        res[ticker] = (open_close_df.loc[open_close_df.ticker == ticker]
                       [['month', 'average_open', 'average_close']]
                       .to_dict(orient='records'))
    return res


def format_max_profit(profit_df):
    """Output max profit data in the following format:
    {ticker_name:
        [{'date': date, 'profit': profit}]
    """
    profit_df.sort_values(['ticker', 'date', 'profit'], inplace=True)
    profit_df = _format_data_to_currency(profit_df, ['profit'])
    profit_df = _format_datetime_col_to_str(profit_df, 'date')
    res = {}
    for ticker in profit_df['ticker'].unique():
        res[ticker] = (profit_df.loc[profit_df.ticker == ticker]
                       [['date', 'profit']].to_dict(orient='records'))
    return res


def format_busy_day(volume_df):
    """Output busy day data in the following format:
    {ticker_name:
        {avg_volume_num: [{'date': date, 'volume': volume},
                          {'date': date, 'volume': volume}]}}
    """
    volume_df.sort_values(['ticker', 'date', 'avg_volume', 'volume'],
                          inplace=True)
    volume_df['avg_volume'] = volume_df['avg_volume'].round(2)
    volume_df = _format_datetime_col_to_str(volume_df, 'date')
    res = {}
    for ticker in volume_df['ticker'].unique():
        res[ticker] = {}
        avg_volume = volume_df.loc[
                volume_df['ticker'] == ticker]['avg_volume'].unique().item()
        res[ticker]['avg_volume_{}'.format(avg_volume)] = (
            volume_df.loc[volume_df['ticker'] == ticker][['date', 'volume']]
            .to_dict(orient='records'))
    return res


def format_biggest_loser(delta):
    """Output biggest loser data in the following format:
    {ticker_name: {'num_days': num_days}
    """
    res = {delta.ticker: {'num_days': delta.num_days}}
    return res
