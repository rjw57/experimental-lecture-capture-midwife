FROM uisautomation/python:3.7-alpine

WORKDIR /usr/src/app

ADD requirements* /usr/src/app

RUN pip install -r requirements.txt

ADD midwife.py /usr/src/app

EXPOSE 80

# We can only use one gunicorn worker since we store all payloads in local
# memory and workers have no shared state.
CMD gunicorn \
	--name midwife \
	--bind :80 \
	--workers 1 \
	--log-level=info \
	--log-file=- \
	--access-logfile=- \
	--capture-output \
	midwife:app
