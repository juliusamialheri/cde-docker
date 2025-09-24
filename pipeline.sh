#!/bin/bash

docker network create etl_network 2>/dev/null || true

# Start the database container
echo "Starting database container..."
docker run -d --name db --network etl_network \
    -e POSTGRES_USER=user \
    -e POSTGRES_PASSWORD=pass \
    -e POSTGRES_DB=mydb \
    postgres:latest

# Build the image
echo "Building ETL image..."
docker build -t etl_image .

# Run the container
echo "Running ETL pipeline..."
docker run --rm --name etl --network etl_network etl_image

echo "Cleaning up..."
docker stop db
docker rm db
docker network rm etl_network