import json
import logging
from kafka import KafkaConsumer
from kafka.errors import KafkaError
from app.services import LocationService, logger
from app.config import KAFKA_URL

logging.getLogger('kafka').setLevel(logging.WARNING)

def safe_json_deserializer(v):
    if v is None:
        return

    try:
        return json.loads(v.decode('utf-8'))
    except json.decoder.JSONDecodeError:
        logger.error("Unable to decode JSON")
        return None

def run_kafka_consumer():
    consumer = KafkaConsumer(
        "update_location",
        bootstrap_servers=[KAFKA_URL],
        group_id="location_consumer",
        max_poll_records=10,
        value_deserializer=lambda v: safe_json_deserializer(v),
        auto_offset_reset="earliest",
        session_timeout_ms=6000,
        heartbeat_interval_ms=3000,
    )
    logger.info("Kafka consumer created")
    while True:
        try:
            msg_pack = consumer.poll(timeout_ms=1000)
        except KeyboardInterrupt:
            consumer.close()
            break;
        except KafkaError as e:
            logger.error(e)
        except Exception as e:
            logger.error(e)
            break
        else:
            for _, messages in msg_pack.items():
                LocationService.create(messages)
