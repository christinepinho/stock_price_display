from setuptools import setup

setup(
    version='0.0.1',
    name='stock_price_display',
    description='Displays stock analysis for Google, Microsoft & Capital One',
    url='https://github.com/christinepinho/stock_price_display',
    author='Christine Pinho',
    author_email='christineapinho@gmail.com',
    install_requires=['quandl', 'argparse'],
    packages=['stock_price_display'])
