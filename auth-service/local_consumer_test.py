from confluent_kafka import Consumer, KafkaException, KafkaError
import json

conf = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "account-created-listener",
    "auto.offset.reset": "earliest",  # read from beginning if no committed offset
}

consumer = Consumer(conf)

topic = "account-created"
consumer.subscribe([topic])

print(f"Listening to topic: {topic}")

try:
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                raise KafkaException(msg.error())

        value = msg.value().decode("utf-8")

        try:
            data = json.loads(value)
        except json.JSONDecodeError:
            data = value

        print("Received event:")
        print(data)

except KeyboardInterrupt:
    print("Stopping consumer...")

finally:
    consumer.close()