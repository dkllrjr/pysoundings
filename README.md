# pysoundings

**pysoundings** is just a simple little module designed to pull atmospheric sounding data from the [University of Wyoming, College of Engineering, Department of Atmospheric Science's website](http://weather.uwyo.edu/upperair/sounding.html). All you need is the station number and the date and this module will return a [pandas.DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) containing the sounding data. You may still want to go to the website to determine what stations are available, but there are data from a lot of stations in the United States.

## Installation

The package is available on [PyPi](https://pypi.org/):

```bash
$ pip install pysoundings
```
