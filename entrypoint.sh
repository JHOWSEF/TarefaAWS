#!/bin/bash

set -e

echo "Aguardando LocalStack iniciar..."

# Aguarda LocalStack responder na porta 4566
until curl -s http://localstack:4566/_localstack/health | grep '"s3": "running"' > /dev/null; do
  echo "Aguardando LocalStack estar pronto..."
  sleep 5
done

echo "LocalStack está pronto. Iniciando configuração..."

echo "Criando buckets S3..."
awslocal s3 mb s3://image-input
awslocal s3 mb s3://image-processed

echo "Criando filas SQS..."
awslocal sqs create-queue --queue-name new-image-input.fifo --attributes FifoQueue=true,ContentBasedDeduplication=true
awslocal sqs create-queue --queue-name new-image-processed.fifo --attributes FifoQueue=true,ContentBasedDeduplication=true

echo "Setup concluído com sucesso!"
