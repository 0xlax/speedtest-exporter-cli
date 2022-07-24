FROM debain:latest

RUN apt-get update && apt-get install -y \
	python-pip


RUN mkdir /app
COPY run-speedtest.py /app/
RUN pip install speedtest-cli
RUN pip install prometheus-client

EXPOSE 9104
ENTRYPOINT ["/usr/bin/python", "-u", "/app/run-speedtest.py"]

