FROM python:3.8-alpine

WORKDIR .

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8000

COPY . .
CMD [ \
  "gunicorn", \
  "-b", "0.0.0.0:8000", \
  "-k", "geventwebsocket.gunicorn.workers.GeventWebSocketWorker", \
  "-w", "1", \
  "app:app" \
]
