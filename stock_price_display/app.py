import json

from stock_price_display.argument_parsing import parse_args
from stock_price_display import formatting as f
from stock_price_display import calculation as c
from stock_price_display.validation import (validate_securities,
                                            validate_date_range)


def main(cli_args=None):
    """Runs the stock_price_display program"""
    # Bring in args and validate them
    args = parse_args(cli_args)
    securities = validate_securities(args.securities)
    start_date, end_date = validate_date_range(args.start_date, args.end_date)

    # Pull in data from Quandl API
    prices = c.get_prices(securities, start_date, end_date)

    # Run calculations
    results = []
    averages = c.calculate_average_open_close(prices)
    averages = f.format_average_open_close(averages)
    print("Average monthly open and close prices are: {}\n"
          .format(json.dumps(averages, indent=4)))
    results.append(averages)

    if args.max_daily_profit:
        profit = c.calculate_max_profit(prices)
        profit = f.format_max_profit(profit)
        print("Maximum daily profit for each security is: {} \n"
              .format(json.dumps(profit, indent=4)))
        results.append(profit)

    if args.busy_day:
        volume = c.calculate_busy_day(prices)
        volume = f.format_busy_day(volume)
        print("Days with 10 percent higher than average volume are: {} \n"
              .format(json.dumps(volume, indent=4)))
        results.append(volume)

    if args.biggest_loser:
        delta = c.calculate_biggest_loser(prices)
        delta = f.format_biggest_loser(delta)
        print("The security with the most days of loss is: {} \n"
              .format(json.dumps(delta, indent=4)))
        results.append(delta)
    return results


if __name__ == '__main__':
    main()
