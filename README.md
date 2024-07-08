# SimpleRabbitProducerConsumer README 

This project demonstrates the use of RabbitMQ with asynchronous Python consumers and producers using the `aio-pika` library. The setup involves Docker containers for RabbitMQ, the producer, and the consumer.
![General Workflow](img/workflow.png)
*General Workflow*

#### Table of Contents
    1. [Project Structure](#project-structure)
    2. [Prerequisites](#prerequisites)
    3. [Setup and Installation](#setup-and-installation)
    4. [Running the Project](#running-the-project)
    5. [Viewing Logs](#viewing-logs)
    6. [Configuration](#configuration)
    7. [Cleanup](#cleanup)

### Project Structure

```
SimpleRabbitProducerConsumer/
├── producer_aio_pika.py
├── consumer_aio_pika.py
├── Dockerfile.producer
├── Dockerfile.consumer
├── docker-compose.yml
├── logs/
└── wait-for-it.sh
```

### Prerequisites

- Docker
- Docker Compose
- Python 3.8+

### Setup and Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/SimpleRabbitProducerConsumer.git
   cd SimpleRabbitProducerConsumer
   ```

2. **Ensure Docker is running.**

3. **Build the Docker images:**
   ```sh
   docker-compose build
   ```

### Running the Project

1. **Start the services:**
   1.1 Front mode: Runs all containers in the foreground.
   ```sh
   docker-compose up
   ```

   ![Logs Example](img/logs.png)
   *Logs Example*

   1.2 Or Background mode: Runs all containers in the background (detached mode).
   ```sh
   docker-compose up -d
   ```
2. The `wait-for-it.sh` script ensures that the producer and consumer wait for RabbitMQ to be fully ready before attempting to connect.

### Viewing Logs

Logs for both the producer and the consumer are written to a shared volume. To view the logs:

1. **Access any running container (e.g., the producer):**
   ```sh
   docker exec -it producer /bin/sh
   ```

2. **Navigate to the logs directory:**
   ```sh
   cd /logs
   cat shared.log
   ```

### Configuration

Environment variables used in the project can be configured in the `docker-compose.yml` file:

- `RABBIT_MQ_HOST_ADDRESS`: RabbitMQ host address (default: `rabbitmq`)
- `RABBIT_MQ_PORT`: RabbitMQ port (default: `5672`)
- `RABBIT_MQ_USERNAME`: RabbitMQ username (default: `guest`)
- `RABBIT_MQ_PASSWORD`: RabbitMQ password (default: `guest`)
- `PUBLISH_DELAY`: Delay between message publications by the producer (default: `5` seconds)


### Cleanup

To stop and remove all containers, networks, and volumes associated with the project:

```sh
docker-compose down
```
