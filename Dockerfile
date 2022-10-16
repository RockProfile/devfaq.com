FROM python:3.10-bullseye

RUN apt-get update && \
	apt-get install -y --no-install-recommends postgresql-client && \
	rm -rf /var/lib/apt/lists/*

WORKDIR /site

COPY dev/run /usr/bin/run

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN chmod +x /usr/bin/run

EXPOSE 8080
