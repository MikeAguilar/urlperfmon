#!/usr/bin/python3
# 
# Re-writen for Python v3.7 on 7/21/2021
# Author:    Miguel Aguilar
# Project:   URL performance monitor
# Location:  Seattle, WA. Aug 5, 2015
# Script:    urlperfmon.py
# Syntax: python3 urlperfmon.py http://some.url/to/download/a/file

import time
import urllib.request
import sys

### Configurable Variables
download_size_MB = 10   # These are MegaBytes in Integer
user_agent = 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'

### Download only the download size value using the URL provided
def downloadFile(url):
    ### Do HEAD request to get info about the file
    start = time.time()
    req = urllib.request.Request(url, headers={'User-Agent':user_agent}, method='HEAD')
    response = urllib.request.urlopen(req)
    #print ("Response <Content-Length>: ", response.info()['Content-Length']) #DEBUG#
    total_length = int(response.info()['Content-Length'])
    print ('\n\rHEAD Request headers: ')
    print (req.header_items())
    print ('\n\rHEAD Request Elapsed time: ' + str(time.time()-start))
    print ('\n\rHEAD Response headers: ')
    print (response.info())


    ### Execute the byte-range GET request to download only the last 10MB of the file
    # data_list = []   #This is in case you want to save the data downloaded
    bytes_downloaded = 0
    start = time.time()
    range = 'bytes=' + str(int(total_length) - (download_size_MB * 1048576)) + '-' + str(total_length)     ### Range requested if from the end of the file
    ### If requested download size is larger than the file itself, the request will be for a full range from byte 0 to end of file
    if (int(total_length) - (download_size_MB * 1048576)) <= 2 :
        range = 'bytes=0-' + str(total_length)
    #print (range)   #DEBUG#
    req = urllib.request.Request(url, headers={'User-Agent':user_agent, 'Range': range})
    print('\n\rGET Request headers: ')
    print(req.header_items())
    response = urllib.request.urlopen(req)
    print('\n\rGET Response headers: ')
    print(response.info())
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
    print ("Downloaded: " + str(round((bytes_downloaded/1048576), 2)) + " MBytes")
    print ("Download Speed: " + str(round(dlspeed, 2)) + ' Mbps')
    print ("Time elapsed: " + str(round((endtime-start), 2)) + ' Seconds')
                
def main():
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        print ('usage: ', sys.argv[0] + ' http://valid.url/to/download/file')
        url = 'http://dlassets.xboxlive.com/public/content/6e936e47-f486-4b69-a0ab-3c0c2937e920/24be444d-15a3-4ef3-9ceb-1edc12f4b178/1.0.0.7.71280a4d-fd1a-4b20-9f83-16b00e773c83/VolgarrTheViking_1.0.0.7_x64__r0pswf4f5397w'
        #url = "http://ipv4.download.thinkbroadband.com/512MB.zip"   ### This is another example of big file to download
        #url = raw_input("Enter a valid URL: ")   ### Uncomment this line instead of the above one if you want to provide a user prompt to enter the URL
        
    downloadFile(url)


if __name__ == '__main__':
    main()

