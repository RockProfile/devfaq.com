FROM python:3.10-bullseye

RUN apt-get update && \
	apt-get install -y --no-install-recommends postgresql-client && \
	rm -rf /var/lib/apt/lists/*

WORKDIR /site

COPY run /usr/bin/run
RUN chmod +x /usr/bin/run
RUN pip install "django"
RUN pip install "python-dotenv"
RUN pip install "psycopg2"

EXPOSE 8080
