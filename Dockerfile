FROM python:3.11-bullseye

RUN apt-get update && \
    apt-get install -y --no-install-recommends postgresql-client && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /site

COPY dev/run /usr/bin/run

COPY requirements.txt requirements.txt
COPY requirements.txt requirements-dev.txt

RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt
RUN chmod +x /usr/bin/run

CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]

EXPOSE 8080
