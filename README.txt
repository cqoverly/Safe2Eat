README.txt for safe2eat.py

Chris Overly
Internet Programming with Python
1/26/13

Assingment #3: API Mashup


Needed to run the program are the following:
    safe2eat.py
    map_search.py
    restaurant_inspection.py

You will also need to have an environment with the following non-standard modules available:
    BeautifulSoup4
    lxml or html5lib  -- I've run it both ways.

To run the program, run:
    python safe2eat.py

The scripts were written using python2.7.3.

My mashup uses two main source, Google Places and the King County Public Health site. 

The goal of my mashup is to take an address as input (only King County Addresses work for this example), and print out a list of 20 restaurants in the nearby vicinity. The user enters the address and the distance they are willing to travel. At present, I have only 20 listings, but I would like to enable a larger tally. To do so I would have to reissue the Places query using a 'next_page_token' which I have not yet written into the code. It would take a bit of re-conceiving. 

I had the google apis return json files, and stepped through them for the information I desired. The King County api only provided xml file, so I used BeautifulSoup to parse the file for me (with html5lib as the parser) and used it to step through the tags. Great tool.

Things I would like to do:
    
    When a result comes up with no inspection results, I would like to try to search again using slightly different parameters (ie, just the address, or just the first part of the name) as sometimes the parameters as set do not produce a result but just an address will, or just the first two words in the name. The search needs to be made more lenient.

    Also, I would like the ability to get more results, as I mentioned earlier.

    And oh so many other things to mention. Much refactoring is to be had!

That's it for now. 

-- Chris

PS  Having worked a little with lxml independent of BeautifulSoup and wonder, in this circumstance, if just using lxml.etree would be more efficient. I seem to be able to pull all the same information in a similar fasion to how I used BeautifulSoup and am wondering if there be a slight performance benefit to dropping BeautifulSoup and just using lxml.etree.

