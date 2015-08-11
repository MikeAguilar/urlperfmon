#!/usr/bin/python
# 
# Author:    Miguel Aguilar
# Project:   URL performance monitor with Local and Origin GeoLocation info
# Location:  Seattle, WA. Aug 5, 2015
# Script:    urlperfmon.py
# Output:    ./urlperfmon.csv


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
    total_length = int(response.info().getheader('Content-Length'))
    print ''
    print response.info()
    print ('HEAD Request Elapsed time: ' + str(time.time()-start))
    # print (type(response.info()))

    ### Define headers for request
    headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)-MikeBoss', \
                'Range' : ('bytes=' + str(int(total_length)-1048576)+'-') }
    strheaders = str(headers)

    ### Execute the GET request to download only the last 1MB of the file
    data_list = []
    bytes_so_far = 0
    start = time.time()
    print strheaders
    req = urllib2.Request(url, strheaders)
    response = urllib2.urlopen(req)
    while 1:
        data = response.read(1024)
        bytes_so_far += len(data)
        if not data:
            break
        sys.stdout.write("Downloaded: " + str(bytes_so_far))
        data_list.append(data)

    print ("Time elapsed: " + str(time.time()-start))
                
def Main():
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = raw_input("Enter a valid URL: ")
        
    downloadFile(url)


if __name__ == '__main__':
    Main()
    
    