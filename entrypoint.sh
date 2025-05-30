#!/bin/sh

sleep 10 

# Cria buckets
awslocal s3 mb s3://image-input
awslocal s3 mb s3://image-output

# Cria filas FIFO
awslocal sqs create-queue --queue-name new-image-input.fifo --attributes FifoQueue=true,ContentBasedDeduplication=true
awslocal sqs create-queue --queue-name new-image-processed.fifo --attributes FifoQueue=true,ContentBasedDeduplication=true

