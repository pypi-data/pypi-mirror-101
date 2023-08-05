# Onlyfunction Pubsub

### Installation

Add dependency in your `requirements.txt` file

only-pubsub

## Kafka

from only-pubsub import Kafka

kafka = Kafka('access_key', 'secretkey')

kafka.publish('topic', 'key', 'message')

## RabbitMQ

from only-pubsub import RabbitMQ

rabbit = RabbitMQ('access_key', 'secretkey')

rabbit.publish('topic', 'message')


## License
MIT License