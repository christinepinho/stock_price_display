# stock_price_display #

stock_price_display is a Python3 command-line application that allows the user to view stock price details
and analysis for Capital One (COF), Google (GOOGL), and Microsoft (MSFT) for any/all months between
January and June of 2017.

Specific analyses are turned on via command line switches and include:
* -average monthly open-close prices for each security per month,
* -maximum daily profit for each security across the date range,
* -the busiest day for each security based on a daily volume that is 10% higher than the monthly average
for that security, and
* -the security that had the most days of loss in the date range


## INSTALLATION ##

To install this program, simply run ```git clone git+https://github.com/christinepinho/stock_price_display```.
Then cd to the root of where this  directory was cloned and type ```pip install .```  
This way, all dependencies will also be installed.

Please note that this program is written in Python 3, and must be run in a Python 3 environment.


## USAGE ##

stock_price_display may be run via the command line. To run the program, **please navigate to the root 
of where you've cloned stock_price_display.**

The arguments to this program may be found using  ```python stock_price_display/app.py --help```

The only required argument is api-key, which references the API_KEY needed to access data from the
Quandl api. All other arguments, including list of securities, start and end dates, and the type of analysis
requested have intellegent defaults, as listed below.

### Typical Usage ###
To display average monthly open-close prices for January-June 2017 for Google, Microsoft, and Capital One,
you can just use the defaults, as listed below, and run ```python stock_price_display/app.py --api-key MY_API_KEY```

The program will always display average monthly open-close prices. However, if you would like to also see the
maximum daily profit, the busiest day, and the biggest loser for these securities for this date range, run 
```python stock_price_display/app.py --api-key MY_API_KEY --max-daily-profit --busy-day --biggest-loser```

To build your own tailor-made command, see the arguments list below.

### Required arguments ###
--api_key 
    Please pass in the api_key to the Quandl api as a str
    
### Optional arguments ###
*securities LIST
    *The space-separated list of tickers for which the user is requesting pricing analysis
    *OPTIONAL
    *DEFAULT is all three GOOGL, MSFT, and COF
*start-date-range DATE
    *Start of date range for which the user is requesting pricing analysis.
    *Format should be "YYYY-MM-DD
    *OPTIONAL
    *DEFAULT is '2017-01-01'
*end-date-range DATE
    *End of date range for which the user is requesting pricing analysis.
    *Format should be "YYYY-MM-DD
    *OPTIONAL
    *DEFAULT is '2017-06-31'
*max-daily-profit
    *Whether or not to display maximum daily profit for each security across the date range
    *OPTIONAL
   * DEFAULT is False, do not run this analysis
*busy-day
    *Whether or not to display the busiest day for each security
    *OPTIONAL
    *DEFAULT is False, do not run this analysis
*biggest-loser
    *Whether or not to display the security that had the most days of loss in the date range
    *OPTIONAL
    *DEFAULT is False, do not run this analysis
