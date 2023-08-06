# Onlyfunction Pubsub

### Installation

Add dependency in your `requirements.txt` file

ofpubsub

## Kafka

from ofpubsub import Kafka

kafka = Kafka('access_key', 'secretkey')

kafka.publish('topic', 'key', 'message')

## RabbitMQ

from ofpubsub import RabbitMQ

rabbit = RabbitMQ('access_key', 'secretkey')

rabbit.publish('topic', 'message')


## License
MIT License

