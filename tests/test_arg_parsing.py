from stock_price_display import argument_parsing
from stock_price_display.config import api_key


def test_runs_with_all_defaults():
    args = argument_parsing.parse_args()

    assert args.securities == ['COF', 'GOOGL', 'MSFT']
    assert args.start_date == '2017-01-01'
    assert args.end_date == '2017-06-31'
    assert args.max_daily_profit is False
    assert args.busy_day is False
    assert args.biggest_loser is False


def test_runs_with_all_defined():
    cli_args = (
        "--securities COF MSFT "
        "--start-date-range 2017-05-01 "
        "--end-date-range 2017-06-31 "
        "--max-daily-profit "
        "--busy-day "
        "--biggest-loser ".format(api_key).split())
    args = argument_parsing.parse_args(cli_args)

    assert args.securities == ['COF', 'MSFT']
    assert args.start_date == '2017-05-01'
    assert args.end_date == '2017-06-31'
    assert args.max_daily_profit is True
    assert args.busy_day is True
    assert args.biggest_loser is True
