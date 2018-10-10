import pytest

from stock_price_display import validation as v


@pytest.mark.parametrize('securities', [['CONF', 'GOOGL', 'MSFT'], ['CO'],
                                        ['GOOG', 'MSFT']])
def test_catches_invalid_securities(securities):
    with pytest.raises(ValueError) as exc:
        v.validate_securities(securities)
    assert 'program analyzes pricing data for ' in str(exc)


@pytest.mark.parametrize(
    'securities', [['cof', 'googl', 'msft'], ['COF', 'googl'],
                   ['GOOGL', 'MSFT'], ['GOOGl']])
def test_validates_lower_and_upper_case_securities(securities):
    res = v.validate_securities(securities)
    assert all([r.isupper() for r in res])


def test_catches_duplicate_securities():
    res = v.validate_securities(['googl', 'googl', 'msft'])
    assert sorted(res) == ['GOOGL', 'MSFT']


@pytest.mark.parametrize(
    'start_date', ['2017-1-1', '2017-01-1', '17-01-01', '17-1-1',
                   '01-01-2017', '01_01_2017', 'Jan 1, 2017'])
def test_catches_wrong_format_dates(start_date):
    with pytest.raises(ValueError) as exc:
        v.validate_date_range(start_date, '2017-01-01')
    assert "Incorrectly-formatted " in str(exc)


def test_catches_wrong_year():
    with pytest.raises(ValueError) as exc:
        v.validate_date_range('2018-01-01', '2018-06-01')
    assert 'checks pricing for the year 2017' in str(exc)


def test_catches_wrong_month():
    with pytest.raises(ValueError) as exc:
        v.validate_date_range('2017-07-01', '2017-08-01')
    assert 'checks pricing for Jan-June only' in str(exc)
