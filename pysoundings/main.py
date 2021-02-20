"""
# Behind the Scenes

These functions comprise the tiny backbone of this little module. They can be called if desired.
"""


__docformat__ = "numpy"


from bs4 import BeautifulSoup
import requests
import pandas
import io
import warnings


def build_param_dict(stnm, year, month, day_hour):
    """
    Builds a dictionary containing the station number, year, month, and day/hour for the desired atmospheric sounding data.
    
    Parameters
    ----------
    stnm : string
        String of the station identifier, e.g. '70261' for PAFA, Fairbanks Int'l Airport.
    year : string
        String of the year, e.g. '2021'.
    month : string
        String of the month, e.g. '01'.
    day_hour : string
        String of the combined day and hour, e.g. '0100' for the first day of the month as '01', and for the beginning of the day in UTC as '00'.

    Returns
    -------
    param_dict : dict
        A dictionary containing the station number, year, month, and day/hour of the desired date and location.
    """
    
    param_dict = {'STNM': stnm, 'YEAR': year, 'MONTH': month, 'FROM': day_hour, 'TO': day_hour}

    return param_dict


def build_url(param_dict):
    """
    Builds the URL needed to query [University of Wyoming, College of Engineering, Department of Atmospheric Science's website](http://weather.uwyo.edu/upperair/sounding.html) to get the proper sounding data.
    
    Parameters
    ----------
    param_dict : dict
        A dictionary containing the station number, year, month, and day/hour of the desired date and location.
    
    Returns
    -------
    full_url : string
        String of the query URL with the proper date and location of the desired atmospheric sounding.
    """
    
    base_url = 'http://weather.uwyo.edu/cgi-bin/sounding?TYPE=TEXT%3ALIST'

    full_url = base_url
    for key in param_dict.keys():
        full_url += '&' + key + '=' + param_dict[key]

    return full_url


def format_data(html_string):
    """
    Takes a string containing the html container that has the fixed width formatted atmospheric sounding data and stores it in a [pandas.DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html), as well as extracts the units for the data.
    
    Parameters
    ----------
    html_string : string
        A string of the html container that holds the atmospheric sounding data.

    Returns
    -------
    data : DataFrame
        A [pandas.DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) containing the atmospheric data with a labeled header.
    units : string
        String of the units of the pandas DataFrame columns.
    """
    
    fwf = html_string.split('\n')[5:-2]
    header = html_string.split('\n')[2].split()
    units = html_string.split('\n')[3]

    fwf_buffer = io.StringIO('\n'.join(fwf))

    data = pandas.read_fwf(fwf_buffer, names=header)

    return data, units


def pull_data(url):
    """
    This function makes an http request with the given URL to retrieve the atmospheric sounding data from the [University of Wyoming, College of Engineering, Department of Atmospheric Science's website](http://weather.uwyo.edu/upperair/sounding.html). It then puts the data into a [pandas.DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) and the units into a string.

    Parameters
    ----------
    url : string
        String of the url containing the information necessary to query the sounding database.

    Returns
    -------
    data : DataFrame
        A [pandas.DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) containing the atmospheric data with a labeled header.
    units : string
        String of the units of the pandas DataFrame columns.
    """
    
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    data_container = soup.pre

    if data_container == None:
        warnings.warn('No data found for the given parameters')
        data, units = None, None

    else: 
        data, units = format_data(data_container.prettify())

    return data, units
