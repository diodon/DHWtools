import sys
import argparse

import urllib


def makeRange(rangeValue):
    rangeValue = str(rangeValue)
    rr = '[(' + rangeValue + '):(' + rangeValue + ')]'
    return rr


def makeDateRange(date_start, date_end):
    rr = '[(' + date_start + '):(' + date_end + ')]'

    return rr


def getDHW(latitude, longitude, date_start, date_end, fout):
    """
    function to harvest DHW and related variables from CRW ERDDAP server
    the results are stores in a csv file
    Eduardo Klein. ekleins@gmail.com

    :param latitude: latitude in decimal degrees
    :param longitude: longitude in decimal degrees
    :param date_start: start date in yyyy-mm-dd
    :param date_end: end date in yyyy-mm-dd
    :param fout: file name for the results
    :return: info about number of records found and output file name
    """

    serverURL = 'http://oos.soest.hawaii.edu/erddap/griddap/NOAA_DHW_5km.csv?'
    varNames = ['CRW_DHW', 'CRW_HOTSPOT', 'CRW_SST', 'CRW_SSTANOMALY']
    varNames_DHW = ['time',  'latitude', 'longitude']

    dateRange = makeDateRange(date_start, date_end)
    constrains = urllib.parse.quote(dateRange + makeRange(latitude) + makeRange(longitude))
    varList = varNames[0] + constrains
    for var in varNames[1:]:
        varList = varList + "," + var + constrains
    url = serverURL + varList
    try:
        urllib.request.urlretrieve(url, fout)
    except:
        print("Failed")


    return print('results written to {}'.format(fout))



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-lat', dest='latitude', help='latitude in decimal degrees', required=True)
    parser.add_argument('-lon', dest='longitude', help='longitude in decimal degrees', required=True)
    parser.add_argument('-from', dest='date_start', help='start date in yyyy-mm-dd', required=True)
    parser.add_argument('-to', dest='date_end', help='end date in yyyy-mm-dd', required=True)
    parser.add_argument('-fout', dest='fout', help='name of hte output CSV file', default='DHWoutput.csv', required=False)
    args = parser.parse_args()

    getDHW(args.latitude, args.longitude, args.date_start, args.date_end, args.fout)

