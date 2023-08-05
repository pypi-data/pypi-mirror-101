# Onlyfunction Pubsub

### Installation

Add dependency in your `requirements.txt` file

onlyfunction-pubsub

## Kafka

from onlyfunction-pubsub import Kafka

kafka = Kafka('access_key', 'secretkey')

kafka.publish('topic', 'key', 'message')

## RabbitMQ

from onlyfunction-pubsub import RabbitMQ

rabbit = RabbitMQ('access_key', 'secretkey')

rabbit.publish('topic', 'message')


## License
MIT License