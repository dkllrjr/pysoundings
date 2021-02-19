from bs4 import BeautifulSoup
import requests
import pandas
import io
import warnings


def build_param_dict(stnm, year, month, day_hour):
    """
    """
    
    return {'STNM': stnm, 'YEAR': year, 'MONTH': month, 'FROM': day_hour, 'TO': day_hour}


def build_url(param_dict):
    """
    """
    
    base_url = 'http://weather.uwyo.edu/cgi-bin/sounding?TYPE=TEXT%3ALIST'

    full_url = base_url
    for key in param_dict.keys():
        full_url += '&' + key + '=' + param_dict[key]

    return full_url

def format_data(html_string):
    """
    """
    
    fwf = html_string.split('\n')[5:-2]
    header = html_string.split('\n')[2].split()
    units = html_string.split('\n')[3]

    fwf_buffer = io.StringIO('\n'.join(fwf))

    data = pandas.read_fwf(fwf_buffer, names=header)

    return data, units


def pull_data(url):
    """
    """
    
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    data_container = soup.pre

    if data_container == None:
        warnings.warn('No data found for the given parameters')
    else: 
        data, units = format_data(data_container.prettify())

    return data, units


def save_data(file_path, data, units):
    """
    """
    
    with open(file_path, 'a') as file:
        file.write('# units:' + units + '\n')
        data.to_csv(file)


def get(stnm, year, month, day_hour):
    """Pulls the atmospheric sounding data from the University of Wyoming's Department of Atmospheric Science for the station and date specified.

    This function calls all the necessary functions to build the url with the given date and station name, and then extracts the data from the loaded webpage from the University of Wyoming's Department of Atmospheric Science's website, http://weather.uwyo.edu/upperair/sounding.html, that contains the atmospheric sounding data.

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
    data : pandas.DataFrame
        A pandas DataFrame containing the atmospheric data with a labeled header.
    units : string
        String of the units of the pandas DataFrame columns.

    References
    ----------
    [1] University of Wyoming, College of Engineering, Department of Atmospheric Science, http://weather.uwyo.edu/upperair/sounding.html

    Examples
    --------

    >>> stnm, year, month, day_hour = '70261', '2021', '01', '0100'
    >>> data, units = get(stnm, year, month, day_hour)
    >>> data
           PRES   HGHT  TEMP  DWPT  RELH  MIXR   DRCT  SKNT   THTA   THTE   THTV
    0    1000.0     93   NaN   NaN   NaN   NaN    NaN   NaN    NaN    NaN    NaN
    1     994.0    134 -23.3 -25.7  81.0  0.48   85.0   1.0  250.3  251.6  250.3
    2     992.0    149 -19.3 -20.9  87.0  0.73   80.0   1.0  254.4  256.5  254.6
    3     990.0    164 -18.9 -20.9  84.0  0.73   75.0   2.0  255.0  257.0  255.1
    4     988.0    179 -15.7 -17.6  85.0  0.98   70.0   2.0  258.3  261.1  258.5
    ..      ...    ...   ...   ...   ...   ...    ...   ...    ...    ...    ...
    153    10.0  30830 -59.7 -89.7   1.0  0.01  345.0  94.0  795.6  795.8  795.7
    154     9.9  30893 -60.1 -90.1   1.0  0.01  345.0  95.0  796.5  796.6  796.5
    155     9.6  31090 -59.8 -90.1   1.0  0.01  345.0  98.0  804.9  805.0  804.9
    156     9.1  31394 -59.3 -90.0   1.0  0.01  345.0  94.0  818.0  818.2  818.0
    157     8.0  32229 -57.9 -89.9   1.0  0.02    NaN   NaN  855.2  855.4  855.2

    [158 rows x 11 columns]
    >>> units
    '    hPa     m      C      C      %    g/kg    deg   knot     K      K      K '
    """
    
    param_dict = build_param_dict(stnm, year, month, day_hour)
    url = build_url(param_dict)
    data, units = pull_data(url)

    return data, units
