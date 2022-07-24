#!/usr/bin/python3
"""Export speedtest up- and download speed metrics to prometheus."""


import os
import socket
import speedtest
import time
from prometheus_client import start_http_server, Gauge

servers = []
# If you want to test against a specific server
# servers = [1234]

if 'SPEEDTEST_INTERVAL' in os.environ:
    test_interval = os.environ['SPEEDTEST_INTERVAL']
else:
    test_interval = 3600  # initiate speed test every 60 seconds

port = 9104

s = speedtest.Speedtest()

g_download = Gauge('download_speed', 'Download speed')
g_upload = Gauge('upload_speed', 'Upload speed')


def process_request(t):
    """Measure up- and download speed using speedtest."""
    print("Get servers")
    s.get_servers(servers)
    print("Get best servers")
    s.get_best_server()
    print("Test download speed")
    s.download()
    print("Test upload speed")
    s.upload()
    results_dict = s.results.dict()
    g_download.set(results_dict["download"])
    g_upload.set(results_dict["upload"])
    print("upload: %s" % (results_dict["upload"]))
    print("download: %s" % (results_dict["download"]))
    print("Sleeping {0} seconds".format(t))
    time.sleep(t)


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    print("Start http server on port {0}".format(port))
    start_http_server(port)
    # Generate some requests.
    while True:
        try:
            process_request(test_interval)
        except TypeError:
            print("TypeError returned from speedtest server")
        except socket.timeout:
            print("socket.timeout returned from speedtest server")

