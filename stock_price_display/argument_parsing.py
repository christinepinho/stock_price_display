import argparse
import sys


def parse_args(cli_args=None):
    """Constructs parser for arguments coming thorugh the command line"""
    if cli_args is None:
        cli_args = sys.argv[1:]

    parser = argparse.ArgumentParser(description='Get securities pricing data')

    parser.add_argument("--securities", default=['COF', 'GOOGL', 'MSFT'],
                        type=str, nargs="+", action='store',
                        help='The space-separated list of securites for which '
                             'the user is requesting pricing analysis')

    parser.add_argument("--start-date-range", dest='start_date',
                        default="2017-01-01", type=str, action='store',
                        help='Start of date range for which the user is '
                             'requesting pricing analysis. Format should be '
                             '"YYYY-MM-DD')

    parser.add_argument("--end-date-range", dest='end_date',
                        default="2017-06-31", type=str,  action='store',
                        help='End of date range for which the user is '
                             'requesting pricing analysis. Format should be '
                             '"YYYY-MM-DD')

    parser.add_argument("--max-daily-profit", dest='max_daily_profit',
                        default=False, action='store_true',
                        help='Whether or not to display maximum daily profit '
                             'for each security across the date range')

    parser.add_argument("--busy-day", dest='busy_day',
                        default=False, action='store_true',
                        help='Whether or not to display the busiest day for '
                             'each security')

    parser.add_argument("--biggest-loser", dest='biggest_loser',
                        default=False, action='store_true',
                        help='Whether or not to display the security that had '
                             'the most days of loss in the date range')

    return parser.parse_args(cli_args)

