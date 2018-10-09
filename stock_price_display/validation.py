import re


def validate_securities(securities):
    """Validates that the list of securities given falls within
    the list of securities this program covers
    """
    valid_securities = ['COF', 'GOOGL', 'MSFT']
    # drop duplicates and turn all to capitals
    securities = list(set([s.upper() for s in securities]))
    if not all([s in valid_securities for s in securities]):
        raise ValueError("This program analyzes pricing data "
                         "for {} only. Got {}"
                         .format(",".join(valid_securities),
                                 securities))
    return securities


def validate_date_range(start_date, end_date):
    """Validates that the start and end_dates given are in the correct
    format and fall between January and June of 2017
    """
    pattern = re.compile("^([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))$")
    for name, d in {'start': start_date, 'end': end_date}.items():
        if not pattern.match(d) or len(d) != 10:
            raise ValueError("Incorrectly-formatted {} date given. "
                             "Got {}. Must be formatted as YYYY-MM-DD"
                             .format(name, d))
        year, month, day = d.split("-")
        if year != '2017':
            raise ValueError("This program checks pricing for the year 2017 "
                             "only. Got {}".format(year))
        if int(month) not in range(1, 7):
            raise ValueError("This program checks pricing for Jan-June only. "
                             "Got {}".format(month))
    return start_date, end_date
