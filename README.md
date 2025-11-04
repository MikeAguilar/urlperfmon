# urlperfmon

A Python-based URL performance monitoring tool designed to test download speeds, measure network performance, and log detailed metrics from different geographic locations.

## Overview

`urlperfmon` is a command-line utility that downloads files from specified URLs and measures key performance metrics including download speed, latency, and file transfer times. Originally designed for deployment on remote VMs to test CDN performance and geographic correlation with server locations, it now includes comprehensive CSV logging, robust error handling, and detailed performance analytics.

## Features

- **Performance Monitoring**: Measures download speed (Mbps), elapsed time, and data transferred
- **CSV Logging**: Automatically logs all test results to CSV file for historical analysis
- **Smart Range Requests**: Downloads only a specified portion of large files to save bandwidth
- **Server Capability Detection**: Automatically detects if servers support HTTP range requests
- **Robust Error Handling**: Gracefully handles network errors, timeouts, and HTTP errors
- **Configurable Timeouts**: Prevents hanging on slow or unresponsive servers
- **Verbose Output Mode**: Detailed HTTP headers and request/response information for debugging
- **Type-Safe Code**: Includes type hints and comprehensive documentation

## Requirements

- Python 3.7 or higher
- Standard library modules (no external dependencies required):
  - `urllib.request`
  - `csv`
  - `time`
  - `sys`
  - `os`
  - `datetime`
  - `typing`

## Installation

1. Clone the repository:
```bash
git clone https://github.com/MikeAguilar/urlperfmon.git
cd urlperfmon
```

2. Make the script executable (optional):
```bash
chmod +x urlperfmon.py
```

3. No additional dependencies needed!

## Usage

### Basic Usage

```bash
python3 urlperfmon.py <URL>
```

### Examples

```bash
# Test download speed from a specific URL
python3 urlperfmon.py "https://example.com/largefile.zip"

# Test with a CDN endpoint
python3 urlperfmon.py "https://cdn.example.com/assets/video.mp4"

# Test using default URL (if no URL provided)
python3 urlperfmon.py
```

### Sample Output

```
Testing URL: https://example.com/file.zip
Download size: 10 MB
Timeout: 30 seconds
CSV Logging: Enabled

============================================================
Starting HEAD request...
============================================================

HEAD Request headers:
  User-agent: Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11

HEAD Request Elapsed time: 0.123 seconds

HEAD Response headers:
...

File size: 500.00 MB
Range requests supported: True

============================================================
Starting GET request...
============================================================

GET Request headers:
  User-agent: Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11
  Range: bytes=490000000-500000000

GET Response headers:
...

HTTP Status: 206
✓ Server honored range request (206 Partial Content)

Downloading...

============================================================
RESULTS
============================================================
Downloaded: 10.00 MB
Download Speed: 85.32 Mbps
Time elapsed: 0.94 seconds
============================================================

✓ Log entry saved to urlperfmon_log.csv
```

## Configuration

All configuration variables are located at the top of `urlperfmon.py` (lines 24-33):

### General Configuration

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `download_size_MB` | int | `10` | Size of data to download in MegaBytes |
| `user_agent` | str | `'Mozilla/5.0...'` | User-Agent header for HTTP requests |
| `request_timeout` | int | `30` | Timeout for HTTP requests in seconds |
| `verbose` | bool | `True` | Enable detailed output with headers and debug info |

### CSV Logging Configuration

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `enable_csv_logging` | bool | `True` | Enable or disable CSV logging |
| `csv_log_file` | str | `'urlperfmon_log.csv'` | Path to CSV log file |
| `csv_include_headers_info` | bool | `False` | Include server/content-type headers in CSV |

### Customization Example

Edit the configuration section in `urlperfmon.py`:

```python
### Configurable Variables
download_size_MB = 5        # Download only 5MB instead of 10MB
user_agent = 'MyCustomBot/1.0'
request_timeout = 60        # Wait up to 60 seconds
verbose = False             # Quiet mode - minimal output

# CSV Logging Configuration
enable_csv_logging = True
csv_log_file = '/var/log/urlperfmon.csv'  # Custom log location
csv_include_headers_info = True            # Include server details
```

## CSV Log Format

The CSV log file contains the following columns:

| Column | Description |
|--------|-------------|
| `timestamp` | ISO 8601 timestamp of when the test was run |
| `url` | The URL that was tested |
| `status` | Test status: `success` or `failure` |
| `file_size_mb` | Total file size in megabytes |
| `downloaded_mb` | Amount of data actually downloaded in MB |
| `download_speed_mbps` | Download speed in megabits per second |
| `elapsed_seconds` | Time taken for download in seconds |
| `range_supported` | Whether server supports HTTP range requests |
| `http_status_code` | HTTP response code (200, 206, 404, etc.) |
| `error_message` | Error description if test failed |
| `server_header` | Server software (if `csv_include_headers_info=True`) |
| `content_type` | Content MIME type (if `csv_include_headers_info=True`) |

### Sample CSV Output

```csv
timestamp,url,status,file_size_mb,downloaded_mb,download_speed_mbps,elapsed_seconds,range_supported,http_status_code,error_message
2025-11-04T10:30:45.123456,https://example.com/file.zip,success,500.0,10.0,85.32,0.94,True,206,
2025-11-04T10:35:12.789012,https://badurl.com/file.zip,failure,0,0,0,0,False,404,HTTP Error 404: Not Found
```

## How It Works

1. **HEAD Request**: First, the script sends an HTTP HEAD request to determine:
   - File size (Content-Length header)
   - Server capabilities (Accept-Ranges header)
   - Server information

2. **Range Calculation**: Based on the file size and configured `download_size_MB`, it calculates which byte range to request (typically the last N megabytes)

3. **GET Request**: Sends an HTTP GET request with a Range header to download only the specified portion

4. **Performance Measurement**: Records:
   - Total bytes downloaded
   - Time elapsed
   - Download speed calculation (Mbps)

5. **CSV Logging**: Writes all metrics and metadata to the CSV log file

6. **Error Handling**: If any errors occur (network, HTTP, timeout), they're caught, logged, and reported

## Use Cases

- **CDN Testing**: Deploy on VMs in different regions to test CDN performance
- **Network Performance Monitoring**: Regular scheduled tests to track network speed over time
- **Server Performance Analysis**: Compare download speeds from different servers
- **Geographic Performance**: Correlate download speeds with client/server locations
- **Troubleshooting**: Detailed HTTP headers help diagnose connectivity issues
- **Bandwidth Testing**: Quick verification of available bandwidth

## Error Handling

The script gracefully handles various error conditions:

- **Network Errors**: Connection failures, DNS resolution issues
- **HTTP Errors**: 404 Not Found, 403 Forbidden, 500 Server Error, etc.
- **Timeouts**: Configurable timeout prevents hanging on slow servers
- **Missing Headers**: Validates that Content-Length is present
- **Keyboard Interrupts**: Clean exit on Ctrl+C
- **Unexpected Errors**: Catches and logs any unexpected exceptions

All errors are logged to the CSV file with descriptive error messages.

## Exit Codes

- `0`: Success - download completed successfully
- `1`: Failure - error occurred (see CSV log or console output for details)

## Deployment on Remote VMs

### Example: Testing from Multiple Locations

```bash
# On VM in US-East
ssh user@vm-us-east.example.com
git clone https://github.com/MikeAguilar/urlperfmon.git
cd urlperfmon
python3 urlperfmon.py "https://your-cdn.com/test-file.bin"

# On VM in EU-West
ssh user@vm-eu-west.example.com
git clone https://github.com/MikeAguilar/urlperfmon.git
cd urlperfmon
python3 urlperfmon.py "https://your-cdn.com/test-file.bin"

# Compare CSV logs from both locations
```

### Automated Scheduled Testing

Use cron to run periodic tests:

```bash
# Run every hour and append to log
0 * * * * cd /home/user/urlperfmon && /usr/bin/python3 urlperfmon.py "https://example.com/test.bin" >> /var/log/urlperfmon_cron.log 2>&1
```

## Recent Changes (v2.0 - November 2025)

### Major Improvements

This version includes a comprehensive rewrite with significant enhancements:

#### 🆕 New Features
- **CSV Logging System**: Automatic logging of all test results with timestamps, metrics, and error information
- **Configuration Variables**: New settings for CSV logging, timeouts, and verbosity control
- **Range Request Validation**: Automatic detection of server range request support
- **Enhanced Error Handling**: Comprehensive try-except blocks for all network operations
- **Type Hints & Documentation**: Full type annotations and docstrings for better code quality

#### 🔧 Code Quality Improvements
- **Fixed Variable Naming**: Renamed `range` variable to `byte_range` (avoids Python built-in conflict)
- **Constants Definition**: Replaced magic numbers with named constants (`BYTES_PER_MB`, `BITS_PER_BYTE`, `READ_CHUNK_SIZE`)
- **Function Documentation**: Added comprehensive docstrings to all functions
- **Configuration Validation**: New `validate_config()` function ensures safe settings
- **Better Code Structure**: Improved organization and readability

#### 🛡️ Reliability & Resilience
- **Timeout Support**: Configurable request timeouts prevent hanging
- **HTTP Error Handling**: Graceful handling of all HTTP error codes
- **Network Error Handling**: Proper handling of connection failures and DNS issues
- **Interrupt Handling**: Clean exit on keyboard interrupt (Ctrl+C)
- **Exit Codes**: Proper exit codes for success (0) and failure (1)

#### 📊 Output & Reporting
- **Improved Formatting**: Clear section headers and organized output
- **Verbose Mode**: Toggle detailed headers and debugging information
- **Status Indicators**: Visual indicators (✓, ⚠) for better UX
- **CSV Integration**: Automatic logging with customizable fields

#### 🔍 Technical Enhancements
- **Server Capability Detection**: Checks `Accept-Ranges` header
- **Response Code Validation**: Validates partial content (206) vs full content (200)
- **Header Inspection**: Optional logging of server and content-type headers
- **Better Error Messages**: Descriptive error messages for troubleshooting

### Migration Notes

If you're upgrading from the original version:

1. **CSV Logging**: Enabled by default - set `enable_csv_logging = False` to disable
2. **Timeout**: Default 30-second timeout - adjust `request_timeout` if needed
3. **Verbose Output**: More detailed output - set `verbose = False` for quiet mode
4. **Exit Codes**: Script now returns proper exit codes (0/1)

### Breaking Changes

None - the script remains backward compatible with the original usage pattern. All new features are additive.

## License

See [LICENSE](LICENSE) file for details.

## Author

- **Miguel Aguilar** - Original author
- Location: Seattle, WA
- Project start: August 5, 2015
- Python 3.7 rewrite: July 21, 2021
- Major upgrade: November 2025

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## Troubleshooting

### Common Issues

**Problem**: "Error: Server did not provide Content-Length"
- **Solution**: Some servers don't provide file size information. Try a different URL or server.

**Problem**: "HTTP Error 403: Forbidden"
- **Solution**: Server may be blocking automated requests. Try changing the `user_agent` variable.

**Problem**: "URL Error: Name or service not known"
- **Solution**: DNS resolution failed. Check your internet connection and URL.

**Problem**: CSV file not created
- **Solution**: Check `enable_csv_logging = True` and ensure write permissions in the directory.

### Getting Help

For issues or questions:
1. Check the CSV log file for detailed error messages
2. Run with `verbose = True` to see detailed HTTP headers
3. Open an issue on GitHub with the error message and URL being tested

## Version History

- **v2.0** (November 2025) - Major upgrade with CSV logging, error handling, and code quality improvements
- **v1.1** (July 2021) - Python 3.7 compatibility update
- **v1.0** (August 2015) - Initial release
