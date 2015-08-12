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
    # headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)-MikeBoss', \
                # 'Range' : ('bytes=' + str(int(total_length)-1048576)+'-') }
                # 'Range' : ('bytes=' + str(int(total_length)-1048576)+'-') }
    # strheaders = str(headers)

    ### Execute the GET request to download only the last 1MB of the file
    data_list = []
    bytes_downloaded = 0
    start = time.time()
    # print strheaders
    
    ### Range is only 10MB from the end of the file
    range = 'bytes=' + str(int(total_length)-10485760)+'-'+ str(total_length)
    print range
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)-MikeBoss')
    req.add_header('Range', range)
    response = urllib2.urlopen(req)
    while 1:
        data = response.read(1024)
        bytes_downloaded += len(data)
        if not data:
            break
        # sys.stdout.write("Downloaded: " + str(bytes_downloaded))
        # sys.stdout.flush()
        # data_list.append(data)
    
    print "\nMBytes downloaded: " + str((int(total_length)-(int(total_length)-(10485760))/1048576))
    print "Download Speed: " + str(((bytes_downloaded*8)/(1048576))/(time.time() - start))
    print ("Time elapsed: " + str(time.time()-start))
                
def Main():
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = raw_input("Enter a valid URL: ")
        
    downloadFile(url)


if __name__ == '__main__':
    Main()
    
    