import pytest
from itertools import permutations

from stock_price_display.app import main


def test_invalid_securites_caught():
    with pytest.raises(ValueError):
        main(cli_args=("--securities CONF goog NsFT").split())


def test_invalid_dates_caught():
    with pytest.raises(ValueError):
        main(cli_args=("--start-date-range 1-1-17").split())
    with pytest.raises(ValueError):
        main(cli_args=("--end-date-range 6/31/17").split())


def test_incorrectly_named_args_caught():
    with pytest.raises(SystemExit):
        main(cli_args="--start_date_range 2017-01-01".split())
    with pytest.raises(SystemExit):
        main(cli_args="--security MSFT --start-date-range 2017-01-01".split())


def test_avg_open_close_returned():
    res = main(cli_args=("--securities COF GOOGL MSFT --start-date-range "
                         "2017-01-01 --end-date-range 2017-03-01").split())
    assert len(res) == 1  # results list only contains one dict result
    assert list(res[0].keys()) == ['COF', 'GOOGL', 'MSFT']
    assert len(res[0]['COF']) == 3  # one for each month included
    assert res[0]['COF'][0]['month'] == '2017-01'
    assert len(res[0]['COF'][0]['average_open']) == 6  # ensure form is $xx.xx


def test_max_daily_profit_returned():
    pass


def test_busy_day_returned():
    pass


def test_biggest_loser_returned():
    pass


@pytest.mark.parametrize('analyses', permutations(['--max-daily-profit',
                                                   '--busy-day',
                                                   '--biggest-loser']))
def test_combo_returned(analyses):
    num_analyses = len(analyses)
    analyses = " ".join(a for a in analyses)
    res = main(cli_args="--securities COF GOOGL MSFT "
                        "{}".format(analyses).split())
    assert len(res) == num_analyses + 1  # avg monthly open/close always given
