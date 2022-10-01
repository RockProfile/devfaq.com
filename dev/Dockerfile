FROM python:3.10-bullseye

RUN apt-get update && \
	apt-get install -y --no-install-recommends postgresql-client && \
	rm -rf /var/lib/apt/lists/*

WORKDIR /site
RUN pip install django
RUN pip install "python-dotenv"

EXPOSE 80
CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
