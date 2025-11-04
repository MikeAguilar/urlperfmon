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
import urllib.error
import sys
import csv
import os
from datetime import datetime
from typing import Dict, Optional, Tuple

### Constants
BYTES_PER_MB = 1024 * 1024
BITS_PER_BYTE = 8
READ_CHUNK_SIZE = 1024

### Configurable Variables
download_size_MB = 10   # Download size in MegaBytes (Integer)
user_agent = 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'
request_timeout = 30    # Timeout for HTTP requests in seconds
verbose = True          # Enable verbose output (headers, detailed info)

# CSV Logging Configuration
enable_csv_logging = True           # Enable or disable CSV logging
csv_log_file = 'urlperfmon_log.csv' # Path to CSV log file
csv_include_headers_info = False    # Include detailed header information in CSV


def validate_config() -> bool:
    """
    Validate configuration variables.

    Returns:
        bool: True if configuration is valid, False otherwise
    """
    if download_size_MB <= 0:
        print("Error: download_size_MB must be a positive number")
        return False
    if request_timeout <= 0:
        print("Error: request_timeout must be a positive number")
        return False
    return True


def log_to_csv(log_data: Dict[str, any]) -> None:
    """
    Log performance data to CSV file.

    Args:
        log_data: Dictionary containing performance metrics and metadata
    """
    if not enable_csv_logging:
        return

    try:
        file_exists = os.path.isfile(csv_log_file)

        with open(csv_log_file, 'a', newline='') as csvfile:
            fieldnames = [
                'timestamp', 'url', 'status', 'file_size_mb',
                'downloaded_mb', 'download_speed_mbps', 'elapsed_seconds',
                'range_supported', 'http_status_code', 'error_message'
            ]

            if csv_include_headers_info:
                fieldnames.extend(['server_header', 'content_type'])

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write header if file is new
            if not file_exists:
                writer.writeheader()

            writer.writerow(log_data)

        if verbose:
            print(f"\n✓ Log entry saved to {csv_log_file}")

    except IOError as e:
        print(f"\nWarning: Could not write to CSV log file: {e}")
    except Exception as e:
        print(f"\nWarning: Unexpected error writing to CSV: {e}")


def download_file(url: str) -> Optional[Dict[str, any]]:
    """
    Download file from URL and measure performance metrics.

    Args:
        url: The URL to download from

    Returns:
        Dictionary containing performance metrics, or None if failed
    """
    log_data = {
        'timestamp': datetime.now().isoformat(),
        'url': url,
        'status': 'failure',
        'file_size_mb': 0,
        'downloaded_mb': 0,
        'download_speed_mbps': 0,
        'elapsed_seconds': 0,
        'range_supported': False,
        'http_status_code': 0,
        'error_message': ''
    }

    try:
        ### Do HEAD request to get info about the file
        if verbose:
            print("\n" + "="*60)
            print("Starting HEAD request...")
            print("="*60)

        start = time.time()
        req = urllib.request.Request(
            url,
            headers={'User-Agent': user_agent},
            method='HEAD'
        )

        try:
            response = urllib.request.urlopen(req, timeout=request_timeout)
        except urllib.error.HTTPError as e:
            log_data['error_message'] = f"HTTP Error {e.code}: {e.reason}"
            log_data['http_status_code'] = e.code
            print(f"\nError: HTTP {e.code} - {e.reason}")
            return log_data
        except urllib.error.URLError as e:
            log_data['error_message'] = f"URL Error: {e.reason}"
            print(f"\nError: Could not reach URL - {e.reason}")
            return log_data

        # Check if Content-Length is available
        if 'Content-Length' not in response.info():
            log_data['error_message'] = "Server did not provide Content-Length header"
            print("\nError: Server did not provide Content-Length. Cannot determine file size.")
            return log_data

        total_length = int(response.info()['Content-Length'])
        file_size_mb = total_length / BYTES_PER_MB
        log_data['file_size_mb'] = round(file_size_mb, 2)

        # Check if server supports range requests
        range_supported = response.info().get('Accept-Ranges', 'none') != 'none'
        log_data['range_supported'] = range_supported

        if verbose:
            print(f'\nHEAD Request headers:')
            for header in req.header_items():
                print(f"  {header[0]}: {header[1]}")
            print(f'\nHEAD Request Elapsed time: {time.time()-start:.3f} seconds')
            print(f'\nHEAD Response headers:')
            print(response.info())
            print(f"\nFile size: {file_size_mb:.2f} MB")
            print(f"Range requests supported: {range_supported}")

        if csv_include_headers_info:
            log_data['server_header'] = response.info().get('Server', 'Unknown')
            log_data['content_type'] = response.info().get('Content-Type', 'Unknown')

        ### Execute the byte-range GET request to download only the specified size
        bytes_downloaded = 0
        start = time.time()

        # Calculate byte range
        range_start = max(0, int(total_length) - (download_size_MB * BYTES_PER_MB))
        byte_range = f'bytes={range_start}-{total_length}'

        # If requested download size is larger than the file itself, download full file
        if range_start <= 2:
            byte_range = f'bytes=0-{total_length}'
            if verbose:
                print(f"\nNote: File is smaller than requested download size. Downloading entire file.")

        if verbose:
            print("\n" + "="*60)
            print("Starting GET request...")
            print("="*60)

        headers = {'User-Agent': user_agent}
        if range_supported:
            headers['Range'] = byte_range

        req = urllib.request.Request(url, headers=headers)

        if verbose:
            print(f'\nGET Request headers:')
            for header in req.header_items():
                print(f"  {header[0]}: {header[1]}")

        try:
            response = urllib.request.urlopen(req, timeout=request_timeout)
        except urllib.error.HTTPError as e:
            log_data['error_message'] = f"HTTP Error {e.code}: {e.reason}"
            log_data['http_status_code'] = e.code
            print(f"\nError: HTTP {e.code} - {e.reason}")
            return log_data
        except urllib.error.URLError as e:
            log_data['error_message'] = f"URL Error: {e.reason}"
            print(f"\nError: Could not download file - {e.reason}")
            return log_data

        log_data['http_status_code'] = response.getcode()

        if verbose:
            print(f'\nGET Response headers:')
            print(response.info())
            print(f"\nHTTP Status: {response.getcode()}")

            # Check if partial content was returned
            if range_supported and response.getcode() == 206:
                print("✓ Server honored range request (206 Partial Content)")
            elif range_supported and response.getcode() == 200:
                print("⚠ Server ignored range request (200 OK - full content)")

            print("\nDownloading...")

        # Download the file
        while True:
            data = response.read(READ_CHUNK_SIZE)
            bytes_downloaded += len(data)
            if not data:
                break

        endtime = time.time()
        elapsed = endtime - start
        downloaded_mb = bytes_downloaded / BYTES_PER_MB
        dlspeed = (bytes_downloaded * BITS_PER_BYTE / BYTES_PER_MB) / elapsed

        # Update log data with results
        log_data['status'] = 'success'
        log_data['downloaded_mb'] = round(downloaded_mb, 2)
        log_data['download_speed_mbps'] = round(dlspeed, 2)
        log_data['elapsed_seconds'] = round(elapsed, 2)
        log_data['error_message'] = ''

        # Print results
        print("\n" + "="*60)
        print("RESULTS")
        print("="*60)
        print(f"Downloaded: {downloaded_mb:.2f} MB")
        print(f"Download Speed: {dlspeed:.2f} Mbps")
        print(f"Time elapsed: {elapsed:.2f} seconds")
        print("="*60)

        return log_data

    except KeyboardInterrupt:
        log_data['error_message'] = "Interrupted by user"
        print("\n\nDownload interrupted by user")
        return log_data
    except Exception as e:
        log_data['error_message'] = f"Unexpected error: {str(e)}"
        print(f"\nUnexpected error: {e}")
        return log_data


def main():
    """Main entry point for the script."""
    # Validate configuration
    if not validate_config():
        sys.exit(1)

    # Get URL from command line or use default
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        print('Usage: ' + sys.argv[0] + ' http://valid.url/to/download/file')
        print('\nNo URL provided. Using default test URL...\n')
        url = 'http://dlassets.xboxlive.com/public/content/6e936e47-f486-4b69-a0ab-3c0c2937e920/24be444d-15a3-4ef3-9ceb-1edc12f4b178/1.0.0.7.71280a4d-fd1a-4b20-9f83-16b00e773c83/VolgarrTheViking_1.0.0.7_x64__r0pswf4f5397w'
        #url = "http://ipv4.download.thinkbroadband.com/512MB.zip"   ### This is another example of big file to download
        #url = input("Enter a valid URL: ")   ### Uncomment this line instead of the above one if you want to provide a user prompt to enter the URL

    print(f"Testing URL: {url}")
    print(f"Download size: {download_size_MB} MB")
    print(f"Timeout: {request_timeout} seconds")
    print(f"CSV Logging: {'Enabled' if enable_csv_logging else 'Disabled'}")

    # Perform download and get metrics
    log_data = download_file(url)

    # Log to CSV if enabled and we have data
    if log_data:
        log_to_csv(log_data)

        # Exit with appropriate code
        if log_data['status'] == 'success':
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()

