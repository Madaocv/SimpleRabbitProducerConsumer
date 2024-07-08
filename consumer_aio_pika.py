import asyncio
import aio_pika
import json
import logging
import os
RABBIT_MQ_HOST_ADDRESS = os.getenv('RABBIT_MQ_HOST_ADDRESS', '127.0.0.1')
RABBIT_MQ_PORT = int(os.getenv('RABBIT_MQ_PORT', 5672))
RABBIT_MQ_USERNAME = os.getenv('RABBIT_MQ_USERNAME', 'guest')
RABBIT_MQ_PASSWORD = os.getenv('RABBIT_MQ_PASSWORD', 'guest')

logging.basicConfig(
    format='%(asctime)s : %(levelname)s: %(funcName)-15s : %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler("logs/shared.log"),
        logging.StreamHandler()
    ]
)


async def consume_message(message: aio_pika.IncomingMessage):
    try:
        body = json.loads(message.body.decode())
        logging.info(f"[<] Received message: {body}")
        # Message approve
        await message.ack()
        logging.info("[+] Message acknowledged")
    except Exception as e:
        # Message rejected
        await message.reject(requeue=True)
        logging.info(f"[!] Error processing message: {e}. Message returned to the queue")


async def main():
    connection: aio_pika.RobustConnection = await aio_pika.connect(
        host=RABBIT_MQ_HOST_ADDRESS,
        port=RABBIT_MQ_PORT,
        login=RABBIT_MQ_USERNAME,
        password=RABBIT_MQ_PASSWORD,
        reconnect_attempts=10,
        reconnect_interval=30,
    )
    async with connection:
        channel = await connection.channel()
        # Create the  queue (if not exist)
        queue = await channel.declare_queue("test_queue", durable=True)
        await queue.consume(consume_message)
        logging.info("[x] Consumer awaiting for messages ...")
        await asyncio.Future()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
