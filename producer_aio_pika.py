import aio_pika
import asyncio
import uuid
import json
from datetime import datetime
import config
import logging

logging.basicConfig(
    format='%(asctime)s : %(levelname)s: %(funcName)s : %(message)s',
    level=logging.INFO
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
        host=config.RABBIT_MQ_HOST_ADDRESS,
        port=config.RABBIT_MQ_PORT,
        login=config.RABBIT_MQ_USERNAME,
        password=config.RABBIT_MQ_PASSWORD,
        reconnect_attempts=10,
        reconnect_interval=30,
    )
    channel = await connection.channel()
    # Create the  queue (if not exist)
    queue = await channel.declare_queue("test_queue", durable=True)
    logging.info(f"[x] Producer started to publish messages every {config.PUBLISH_DELAY} seconds")
    while True:
        await publish_message(channel)
        await asyncio.sleep(config.PUBLISH_DELAY)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
