#!/usr/bin/python
# 
# Author:    Miguel Aguilar
# Project:   URL performance monitor with Local and Origin GeoLocation info
# Location:  Seattle, WA. Aug 5, 2015
# Script:    ip2geo.py
# Logs:      ./geoInfo.log
#

import time
import urllib2
import ast
import sys

### Download only 1MB from the URL provided
def downloadFile(url):
    ### Do HEAD request to get info about the file
    start = time.time()
    req = urllib2.Request(url)
    req.get_method = lambda : 'HEAD'
    response = urllib2.urlopen(req)
    # total_length = response.info()
    total_length = 0
    print ''
    print response.info()
    print ('Elapsed time: ' + str(time.time()-start))
    # print (type(response.info()))

    ### Define headers for request
    headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)-MikeBoss', \
                'Range' : (str(total_length-104857600)+':')  }
                
                
def Main():
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = raw_input("Enter a valid URL: ")
        
    downloadFile(url)

if __name__ == '__main__':
    Main()
    
    