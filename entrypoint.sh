#!/bin/bash
echo "Script de inicialização do LocalStack executando..."
sleep 30

echo "Criando buckets S3"
awslocal s3 mb s3://image-input
awslocal s3 mb s3://image-processed

echo "Criando filas SQS"
awslocal sqs create-queue --queue-name new-image-input.fifo --attributes FifoQueue=true,ContentBasedDeduplication=true
awslocal sqs create-queue --queue-name new-image-processed.fifo --attributes FifoQueue=true,ContentBasedDeduplication=true

echo "Setup inicializado com sucesso"
