FROM python:3.14-bookworm

RUN apt-get update && \
    apt-get install -y --no-install-recommends postgresql-client && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /site

COPY dev/run /usr/bin/run

RUN chmod +x /usr/bin/run

EXPOSE 8080
