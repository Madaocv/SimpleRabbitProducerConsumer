import asyncio
import aio_pika
import uuid
import json
from datetime import datetime
import os
import logging
RABBIT_MQ_HOST_ADDRESS = os.getenv('RABBIT_MQ_HOST_ADDRESS', '127.0.0.1')
RABBIT_MQ_PORT = int(os.getenv('RABBIT_MQ_PORT', 5672))
RABBIT_MQ_USERNAME = os.getenv('RABBIT_MQ_USERNAME', 'guest')
RABBIT_MQ_PASSWORD = os.getenv('RABBIT_MQ_PASSWORD', 'guest')
PUBLISH_DELAY = float(os.getenv('PUBLISH_DELAY', 1))
logging.basicConfig(
    format='%(asctime)s : %(levelname)s: %(funcName)-15s : %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler("logs/shared.log"),
        logging.StreamHandler()
    ]
)


async def publish_message(channel):
    message = {
        "message_id": str(uuid.uuid4()),
        "created_on": datetime.now().isoformat()
    }
    await channel.default_exchange.publish(
        aio_pika.Message(body=json.dumps(message).encode()),
        routing_key="test_queue"
    )
    logging.info(f"[>] Sent: {message}")


async def main():
    connection: aio_pika.RobustConnection = await aio_pika.connect(
        host=RABBIT_MQ_HOST_ADDRESS,
        port=RABBIT_MQ_PORT,
        login=RABBIT_MQ_USERNAME,
        password=RABBIT_MQ_PASSWORD,
        reconnect_attempts=10,
        reconnect_interval=30,
    )
    channel = await connection.channel()
    # Create the  queue (if not exist)
    queue = await channel.declare_queue("test_queue", durable=True)
    logging.info(f"[x] Producer started to publish messages every {PUBLISH_DELAY} seconds")
    while True:
        await publish_message(channel)
        await asyncio.sleep(PUBLISH_DELAY)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
