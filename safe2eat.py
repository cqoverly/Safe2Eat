#! /usr/bin/env python

import restaurant_inspection
import map_search

#  Tuple of keys to iterate through for end display of output.
KEY_ORDER = ('Name', 'Address', 'Rating', 'Price Level', 'Inspection Date', 
            'Inspection Result', 'Inspection Score')

def get_info():
    # Get user's input for the search
    street = raw_input('Please enter the street address from which to base your search: ')
    city = raw_input('Please enter the zip code or the city of the address: ')
    dist = int(raw_input('How many miles are you willing to travel? '))
    address = street + ' ' + city
    # address = '3827 Interlake Ave N 98103'
    # dist = 5

    # address = '1415 12th Ave Seattle'
    # dist = 2

    print 'LOCATION INFO RECEIVED'

    # Get latitude, longitude for that address Using Google's Places API
    coords = map_search.get_start_loc(address)
    print 'COORDINATES RECEIVED'

    # Get restaurant listings based on search using Google's Places API
    rest_results = map_search.get_list(coords, dist)
    print 'SEARCH RESULTS RECEIVED'
    # Process results of rest_list
    rest_list = map_search.process_list(rest_results)
    print 'LIST PROCESSED'

    # get inspection data from king county government site (inspect_date, 
    # inspect_result[, score][, v_list])
    for item in rest_list:           #  TODO:  Create method.
        name = item['Name']
        address = item['Address']
        raw_report = restaurant_inspection.get_report(name, address)
        clean_report = restaurant_inspection.process_report(raw_report,
                                                             name, address)
        #  If an inspection was found.
        if clean_report != "No inspection information found.":
            item['Inspection Date'] = clean_report[0]
            item['Inspection Result'] = clean_report[1]
            #  If there were dangerous violations.
            if len(clean_report)>2:
                score, v_list = clean_report[2:]
                item['Inspection Score'] = score
                item['Violations'] = v_list

    # Display Results
    rest_number = 1                  
    for rest in rest_list:           #  TODO:  Create Method
        print '<<<<<<<<<<<<<<<<<< ',rest_number, ' >>>>>>>>>>>>>>>>>>>>>'  
        for key in KEY_ORDER:
            try:
                if rest[key]:
                    print key + ': ', rest[key]
            except KeyError:
                pass
        try:   # Test for 'Violations' key in restaurant dict.
            v_count = 1
            for v in rest['Violations']:  # Iterate through each violation.
                print 'Violation Description', str(v_count) + ':', v
                v_count += 1
        except KeyError:  # No dangerous violations exist to display.
            pass
        try:  #  Test for an inspection date.
            if rest['Inspection Date'] == '':
                print "No inspection information found."
        except KeyError:    # Both imply no inspections found.
            print "No inspection information found."
        rest_number += 1
        print '=========================================================='
        print
    print 'END OF LIST'
    print


    



if __name__ == '__main__':
     get_info()