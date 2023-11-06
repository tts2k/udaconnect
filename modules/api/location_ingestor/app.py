import os
from flask import Flask, jsonify
from kafka import logging
from config import config_by_name

from flask_socketio import SocketIO

from services import send_location_to_kafka

env = os.getenv("FLASK_ENV") or "test"

app = Flask(__name__)
app.config.from_object(config_by_name[env or "test"])

gunicorn_logger = logging.getLogger('gunicorn.error')
gunicorn_logger.setLevel(logging.INFO)
app.logger.handlers = gunicorn_logger

socketio = SocketIO(app, cors_allowed_origins="*", async_mode="gevent")

@app.route('/healthz')
def health():
    return jsonify("healthy")

@socketio.on("update_location")
def update_location(data):
    gunicorn_logger.info(data)
    send_location_to_kafka(data)
    return {"status": "ok"}

if __name__ == "__main__":
    try:
        socketio.run(app, debug=True, use_reloader=True, log_output=True, host="0.0.0.0", port=5001)
    except KeyboardInterrupt:
        socketio.stop()

