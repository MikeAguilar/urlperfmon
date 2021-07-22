#!/usr/bin/python3
# 
# Re-writen for Python v3.7 on 7/21/2021
# Author:    Miguel Aguilar
# Project:   URL performance monitor
# Location:  Seattle, WA. Aug 5, 2015
# Script:    urlperfmon.py
# Output:    ./urlperfmon.csv
# Syntax: urlperfmon.py http://some.url/to/download/a/file



import time
import urllib.request
#import ast
import sys


### Download only 1MB from the URL provided
def downloadFile(url):
    ### Do HEAD request to get info about the file
    start = time.time()
    req = urllib.request.Request(url, headers={'User-Agent':"Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"}, method='HEAD')
    response = urllib.request.urlopen(req)
    #print ("Response <Content-Length>: ", response.info()['Content-Length']) #DEBUG#
    total_length = int(response.info()['Content-Length'])
    print ('\n\rHEAD Request response headers: ')
    print (response.info())
    print ('HEAD Request Elapsed time: ' + str(time.time()-start))
    # print (type(response.info()))

    ### Execute the byte-range GET request to download only the last 10MB of the file
    # data_list = []   #This is in case you want to save the data downloaded
    bytes_downloaded = 0
    start = time.time()
    range = 'bytes=' + str(int(total_length)-10485760)+'-'+ str(total_length)     ### Range is only 10MB from the end of the file
    print (range)   #DEBUG#
    req = urllib.request.Request(url, headers={'User-Agent':"Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11", 'Range': range})
    response = urllib.request.urlopen(req)
    #print ("Response: ", response.info()) #DEBUG#
    while 1:
        data = response.read(1024)
        bytes_downloaded += len(data)
        if not data:
            break
        ### Uncomment the follwing lines to print results to screen and save data to dict
        # sys.stdout.write("Downloaded: " + str(bytes_downloaded))
        # sys.stdout.flush()
        # data_list.append(data)
    endtime = time.time()
    elapsed = endtime-start
    dlspeed = (bytes_downloaded*8/1048576)/elapsed
    print ("Downloaded: " + str(round((bytes_downloaded/1048576), 2)) + " MBytes")  #str(totaldl) +' MBytes'
    # print ("\nMBytes downloaded: " + str((int(total_length)-(int(total_length)-(10485760))/1048576)))
    print ("Download Speed: " + str(round(dlspeed, 2)) + ' Mbps') #str(((bytes_downloaded*8)/(1048576))/(time.time() - start))
    print ("Time elapsed: " + str(round((endtime-start), 2)) + ' Seconds') #str(round((time.time()-start), 2)) + " seconds"
                
def main():
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        print ('usage: ', sys.argv[0] + 'http://valid.url/to/download/file')
        url = "http://ipv4.download.thinkbroadband.com/512MB.zip" #Setting this URL as default
        #url = raw_input("Enter a valid URL: ")
        
    downloadFile(url)


if __name__ == '__main__':
    main()
    
