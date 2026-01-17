#!/bin/bash

# Setup script for Kafka Topics required by the Personalization Pipeline
KAFKA_BROKER="localhost:9092"

echo "Creating Kafka topics for Real-Time AI Personalization..."

kafka-topics --create --bootstrap-server $KAFKA_BROKER \
    --replication-factor 3 --partitions 6 \
    --topic customer.interactions.raw

kafka-topics --create --bootstrap-server $KAFKA_BROKER \
    --replication-factor 3 --partitions 3 \
    --topic ai.personalization.signals.high_priority

echo "Kafka Topic Setup Complete."