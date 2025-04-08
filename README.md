# URL Shortener Service

A containerized URL shortening service built with FastAPI and MongoDB. This service allows you to create short URLs for sharing long links more efficiently.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Quick Start Guide (Copy-Paste)](#quick-start-guide-copy-paste)
- [Step-by-Step Installation](#step-by-step-installation)
- [How to Use the URL Shortener](#how-to-use-the-url-shortener)
- [Data Persistence](#data-persistence)
- [Viewing and Managing Your Data](#viewing-and-managing-your-data)
- [Troubleshooting](#troubleshooting)
- [Advanced Usage](#advanced-usage)
- [Technical Details](#technical-details)

## Features

- **URL Shortening**: Convert long, unwieldy URLs into compact, shareable links
- **Custom Short IDs**: Define your own memorable short URL identifiers
- **Persistent Storage**: MongoDB backend ensures URLs are preserved even after system restarts
- **Containerized**: Fully Dockerized for easy deployment in any environment
- **Fast Redirects**: Optimized lookups for quick redirection to original URLs
- **Simple REST API**: Easy-to-use JSON API for programmatic access

## Prerequisites

- Docker installed on your system ([Get Docker](https://docs.docker.com/get-docker/))
- Basic familiarity with terminal/command line

## Quick Start Guide (Copy-Paste)

For those who just want to get it running quickly, copy and paste these commands:

```bash
# Create a persistent volume for MongoDB data
docker volume create mongodb_data

# Start MongoDB container
docker run -d --name mongodb -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=anosh \
  -e MONGO_INITDB_ROOT_PASSWORD=3214 \
  -v mongodb_data:/data/db mongo:4.4

# Create a Docker network for the containers
docker network create url-shortener-network

# Connect MongoDB to the network
docker network connect url-shortener-network mongodb

# Clone the repository (if you haven't already)
git clone https://github.com/Anoshpshroff/Load-Balanced-URL-Shortener.git
cd Load-Balanced-URL-Shortener

# Build the URL shortener container
docker build -t url-shortener .

# Start the URL shortener container
docker run -d --name url-shortener -p 8000:8000 \
  --network url-shortener-network \
  -e MONGO_USER=anosh -e MONGO_PASSWORD=3214 \
  url-shortener

# Service is now available at http://localhost:8000
```

After running these commands, your URL shortener will be available at http://localhost:8000

## Step-by-Step Installation

### 1. Create a Persistent Volume for MongoDB

First, we need to create a Docker volume to store MongoDB data permanently:

```bash
docker volume create mongodb_data
```

### 2. Start the MongoDB Container

```bash
docker run -d --name mongodb -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=anosh \
  -e MONGO_INITDB_ROOT_PASSWORD=3214 \
  -v mongodb_data:/data/db mongo:4.4
```

This command:
- Creates a MongoDB container named "mongodb"
- Makes it accessible on port 27017
- Sets username and password credentials
- Mounts the persistent volume we created

### 3. Create and Configure a Docker Network

Create a network for containers to communicate:

```bash
docker network create url-shortener-network
```

Connect MongoDB to this network:

```bash
docker network connect url-shortener-network mongodb
```

### 4. Get the URL Shortener Code

Clone the repository:

```bash
git clone https://github.com/Anoshpshroff/Load-Balanced-URL-Shortener.git
cd Load-Balanced-URL-Shortener
```

### 5. Build the URL Shortener Container

```bash
docker build -t url-shortener .
```

### 6. Start the URL Shortener Service

```bash
docker run -d --name url-shortener -p 8000:8000 \
  --network url-shortener-network \
  -e MONGO_USER=anosh -e MONGO_PASSWORD=3214 \
  url-shortener
```

This command:
- Creates a container named "url-shortener"
- Makes it accessible on port 8000
- Connects it to the same network as MongoDB
- Sets database credentials

### 7. Verify Everything is Running

```bash
docker ps
```

You should see both containers running:
- mongodb
- url-shortener

## How to Use the URL Shortener

### Creating a Short URL

To create a short URL, you can use curl from terminal:

```bash
curl -X POST "http://localhost:8000/shorten" \
  -H "Content-Type: application/json" \
  -d '{"long_url": "https://www.example.com/very/long/url/that/needs/shortening"}'
```

Sample response:
```json
{
  "short_url": "http://localhost:8000/AbCdEfG", 
  "long_url": "https://www.example.com/very/long/url/that/needs/shortening"
}
```

### Creating a Custom Short URL

You can also specify your own custom ID:

```bash
curl -X POST "http://localhost:8000/shorten" \
  -H "Content-Type: application/json" \
  -d '{"long_url": "https://github.com/Anoshpshroff/Load-Balanced-URL-Shortener", "custom_id": "github"}'
```

Sample response:
```json
{
  "short_url": "http://localhost:8000/github", 
  "long_url": "https://github.com/Anoshpshroff/Load-Balanced-URL-Shortener"
}
```

### Using Your Short URLs

Simply visit the short URL in your browser:
```
http://localhost:8000/AbCdEfG
```

Or test with curl (using -L to follow the redirect):
```bash
curl -L "http://localhost:8000/AbCdEfG"
```

## Data Persistence

Your URL data is stored in a persistent Docker volume named `mongodb_data`. This means:

- Your data will survive container restarts
- Your data will remain even after system restarts
- Your URLs will continue working as long as you don't delete this volume

If you ever need to restart your containers, just run these commands:

```bash
# Stop the containers
docker stop mongodb url-shortener

# Remove the containers
docker rm mongodb url-shortener

# Start the containers again (with the same volume)
docker run -d --name mongodb -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=anosh \
  -e MONGO_INITDB_ROOT_PASSWORD=3214 \
  -v mongodb_data:/data/db mongo:4.4

docker network connect url-shortener-network mongodb

docker run -d --name url-shortener -p 8000:8000 \
  --network url-shortener-network \
  -e MONGO_USER=anosh -e MONGO_PASSWORD=3214 \
  url-shortener
```

Your data will still be there!

## Viewing and Managing Your Data

### Accessing MongoDB Shell

To see what URLs are stored in your database:

```bash
docker exec -it mongodb mongo --username anosh --password 3214
```

Once in the MongoDB shell, run these commands:

```
# Switch to the URL shortener database
use url_shortener

# Show all collections
show collections

# View all stored URLs
db.urls.find().pretty()

# Find a specific short URL by ID
db.urls.findOne({_id: "github"})

# Exit the shell when done
exit
```

### Example Output

Here's what you might see:

```
> use url_shortener
switched to db url_shortener
> show collections
urls
> db.urls.find().pretty()
{ "_id" : "AbCdEfG", "long_url" : "https://www.example.com/very/long/url/that/needs/shortening" }
{
        "_id" : "github",
        "long_url" : "https://github.com/Anoshpshroff/Load-Balanced-URL-Shortener"
}
> exit
bye
```

## Troubleshooting

### If Containers Won't Start

Check if there are conflicting containers:

```bash
docker ps -a
```

Stop and remove any conflicting containers:

```bash
docker stop mongodb url-shortener
docker rm mongodb url-shortener
```

### If URLs Aren't Working

Check if containers are running:

```bash
docker ps
```

Check logs for errors:

```bash
docker logs url-shortener
docker logs mongodb
```

### If Data is Lost After Restart

Ensure you're using the volume properly:

```bash
docker volume ls
```

You should see `mongodb_data` in the list.

Verify the volume is being mounted correctly:

```bash
docker inspect mongodb | grep -A 10 Mounts
```

You should see the volume mounted at `/data/db`.

## Advanced Usage

### Using Docker Compose (Alternative Method)

Instead of running the commands separately, you can use Docker Compose:

1. Create or modify `docker-compose.yml`:

```yaml
version: '3.8'

services:
  mongodb:
    image: mongo:4.4
    container_name: mongodb
    restart: always
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
    environment:
      MONGO_INITDB_ROOT_USERNAME: anosh
      MONGO_INITDB_ROOT_PASSWORD: 3214
    networks:
      - app-network

  url-shortener:
    build: .
    container_name: url-shortener
    restart: always
    ports:
      - "8000:8000"
    depends_on:
      - mongodb
    environment:
      - MONGO_USER=anosh
      - MONGO_PASSWORD=3214
    networks:
      - app-network

networks:
  app-network:
    driver: bridge

volumes:
  mongodb_data:
```

2. Start everything with one command:

```bash
docker-compose up -d
```

3. Stop everything:

```bash
docker-compose down
```

## Technical Details

The service is built using:

- **FastAPI**: A modern, high-performance web framework for building APIs with Python
- **MongoDB**: A document-based NoSQL database for storing URL mappings
- **ShortUUID**: A library for generating compact, unique identifiers
- **Docker**: For containerization and isolation
- **PyMongo**: The Python driver for MongoDB

The URL shortening logic works by:
1. Accepting a long URL via the API
2. Generating a random 7-character ID or using the provided custom ID
3. Storing the mapping in MongoDB with the ID as the primary key
4. Returning the short URL to the user

When a user accesses a short URL, the service:
1. Extracts the short ID from the URL
2. Looks up the original URL in MongoDB using the ID
3. Returns an HTTP redirect to the original URL 