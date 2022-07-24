import speedtest
import time
from prometheus_client import start_http_server, Summary, Gauge

# Specify server to be tested against or it is set at default
servers = []

s = speedtest.Speedtest()



# results_dict = s.results.dict()
# print results_dict

g_download = Gauge('download_speed', 'Download Speed')
g_upload = Gauge('upload_speed', 'Upload speed')

def process_request(t):
	s.get_servers(servers)
	s.get_best_server()
	s.download()
	s.upload()
	results_dict = s.results.dict()
	g_download.set(results_dict["download"])
	g_upload.set(results_dict["upload"])
	print results_dict["upload"]
  	print results_dict["download"]
	time.sleep(t)


if __name__ == '__main__':

	start_http_server(9104)

	while true:
		process_request(60)
