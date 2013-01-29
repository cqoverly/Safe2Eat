#! /usr/bin/env python

"""
This module provides methods to retrieve restaurant health inspection reports. 
"""

import urllib
import urllib2
import httplib
from bs4 import BeautifulSoup

BASE_URL = 'http://info.kingcounty.gov/health/ehs/foodsafety/inspections/XmlRest.aspx?'

#  Potential paramater list for searches:
#           Business_Name - string

    # Business_Address - string

    # Zip_Code - string

    # Inspection_Start - valid date in format MM/DD/YYYY

    # Inspection_End - valid date in format MM/DD/YYYY

    # Inspection_Closed_Business (Valid values: All, No, Yes)

    # Violation_Points - Integer <= 999

    # City - string

def patch_http_response_read(func):
    """
    This function is purely a patch to get around an error created on the inspection site server. 
    The error created in the get_report() method was an httplib.IncompleteRead exception. Solution was
    found through stackoverflow which referenced the following link where the path is shown:

        http://bobrochel.blogspot.com/2010/11/bad-servers-chunked-encoding-and.html

    Patch was written by the creator of the blog.  Thanks! Saved my day.
    """

    def inner(*args):
        try:
            return func(*args)
        except httplib.IncompleteRead, e:
            return e.partial

    return inner

def get_report(restaurant_name, address):
    """
    Use King County Health site REST interaface, returns results in xml.
    Parse results with BeautifulSoup
    King County server is a flawed HTTP implementations, so patch is used to help get past
    the IncompleteRead error that kept the urllib2.urlopen(Url).read() from completing.
    """

    httplib.HTTPResponse.read = patch_http_response_read(httplib.HTTPResponse.read)
    name = restaurant_name
    addr = address
    split_addr = addr.split()
    search_addr = split_addr[0]  # + ' ' + split_addr[1]
    # print 'SEARCH ADDRES: ', search_addr
    # params = urllib.urlencode({'Business_Name': name})
    params = urllib.urlencode({'Business_Name': name, 'Business_Address': search_addr})
    url = BASE_URL + params
    # print url


    res = urllib2.urlopen(url)

    try:
        res = urllib2.urlopen(url)
        soup = BeautifulSoup(res)
        return soup
    except httplib.IncompleteRead, m:
        return m

def process_report(info, name, addr):
    """
    Takes the parsed report for the restaurant passed to get_report() and parses the values
    for each inspection item to be used in final output for restaurant listing. The info argument
    is a BeautifulSoup object holding the xml code.
    """

    listing = info.find('business')
    if not listing:
        return "No inspection information found."

    inspections = info.find_all('inspection') # Get list of all inspections.
    for i in inspections:
        if i.find('inspection_result').text.strip() != 'Complete':  # 'Complete' only used for
            last_inspect = i                                        #  training visits. Not real
            break                                                   #  inspections.
                                                                    #  Moves code to the first
                                                                    #  real inspection.

    inspect_date = last_inspect.find('inspection_date').text              #  First non 'Complete'
    inspect_result = last_inspect.find('inspection_result').text.strip()  #  inspection is what we want.

    if inspect_result == 'Unsatisfactory':
        score = last_inspect.find('inspection_score').text.strip()
        violations = last_inspect.find_all('violation')
        v_list = []
        for v in violations:
            desc =  v.find('violation_descr').text.strip() + ": " + str(v.find('violation_points').text) + "pts"
            v_list.append(desc)
        return (inspect_date, inspect_result, score, v_list)

    return (inspect_date, inspect_result)  


if __name__ == '__main__':
    test_name = 'Teriyaki Plus'
    test_addr = '4336 Roosevelt Way NE #B'

    test_name2 = 'Paseo'
    test_addr2 = '4225 Fremont Avenue North'

    test_name3 = 'Red Mill Burgers'
    test_addr3 = '312 Phinney Avenue North'

    info = get_report(test_name3, test_addr3)
    process_report(info, test_name3, test_addr3)
