#!/bin/bash

BOOTSTRAP_SERVER="broker:29092"
PARTITIONS=3
REPLICATION_FACTOR=1

TOPICS=(
  "account-created"
  "account-updated"
  "user-deleted"
  "user-updated"
  "AccountEvent"
  "account-event"
)

KAFKA_BIN="/opt/kafka/bin/kafka-topics.sh"

echo "Creating Kafka topics..."

for TOPIC in "${TOPICS[@]}"; do
  echo "Creating topic: $TOPIC"

  $KAFKA_BIN \
    --create \
    --if-not-exists \
    --bootstrap-server "$BOOTSTRAP_SERVER" \
    --replication-factor "$REPLICATION_FACTOR" \
    --partitions "$PARTITIONS" \
    --topic "$TOPIC"

  if [ $? -eq 0 ]; then
    echo "✔ Successfully created (or already exists): $TOPIC"
  else
    echo "✖ Failed to create: $TOPIC"
  fi

  echo "-----------------------------"
done

echo "Done."