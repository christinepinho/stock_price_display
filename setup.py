from setuptools import setup, find_packages

setup(
    version='0.0.1',
    name='stock_price_display',
    description='Displays stock analysis for Google, Microsoft & Capital One',
    url='https://github.com/christinepinho/stock_price_display',
    author='Christine Pinho',
    author_email='christineapinho@gmail.com',
    install_requires=['pandas', 'quandl', 'argparse'],
    packages=find_packages())
