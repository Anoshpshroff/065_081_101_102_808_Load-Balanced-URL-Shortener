# URL Shortener Service

A containerized URL shortening service built with FastAPI and MongoDB. This service allows you to create short URLs for sharing long links more efficiently.

## Table of Contents
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [Using Docker Compose](#using-docker-compose)
  - [Building and Running Manually](#building-and-running-manually)
- [API Documentation](#api-documentation)
  - [Create a Short URL](#create-a-short-url)
  - [Create a Custom Short URL](#create-a-custom-short-url)
  - [Access a Short URL](#access-a-short-url)
- [Technical Implementation](#technical-implementation)
- [Security Considerations](#security-considerations)
- [Troubleshooting](#troubleshooting)
- [Future Enhancements](#future-enhancements)

## Features

- **URL Shortening**: Convert long, unwieldy URLs into compact, shareable links
- **Custom Short IDs**: Define your own memorable short URL identifiers
- **Persistent Storage**: MongoDB backend ensures URLs are preserved even after service restarts
- **Containerized**: Fully Dockerized for easy deployment in any environment
- **Fast Redirects**: Optimized lookups for quick redirection to original URLs
- **Simple REST API**: Easy-to-use JSON API for programmatic access

## Architecture

This service consists of two main components:

1. **FastAPI Web Application**: Handles HTTP requests, URL shortening logic, and redirects
2. **MongoDB Database**: Stores the mappings between short URLs and original long URLs

The components are containerized using Docker and can be run together using Docker Compose.

## Prerequisites

- Docker (version 19.03 or higher)
- Docker Compose (version 1.27 or higher)
- Git (optional, for cloning the repository)

## Getting Started

### Using Docker Compose

The easiest way to run the application is using Docker Compose:

1. Clone this repository or download the source files
2. Navigate to the project directory
3. Run the following command:

```bash
docker-compose up -d
```

The service will be available at http://localhost:8000

### Building and Running Manually

If you prefer to build and run the containers separately:

1. Build the Docker image:
```bash
docker build -t url-shortener .
```

2. Create a Docker network:
```bash
docker network create url-shortener-network
```

3. Run MongoDB:
```bash
docker run -d --name mongodb -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=anosh \
  -e MONGO_INITDB_ROOT_PASSWORD=3214 \
  --network url-shortener-network mongo:4.4
```

4. Run the URL shortener service:
```bash
docker run -d --name url-shortener -p 8000:8000 \
  -e MONGO_USER=anosh -e MONGO_PASSWORD=3214 \
  --network url-shortener-network url-shortener
```

## API Documentation

### Create a Short URL

**Endpoint**: `POST /shorten`

**Request Body**:
```json
{
  "long_url": "https://example.com/very/long/url/that/needs/shortening"
}
```

**Response**:
```json
{
  "short_url": "http://localhost:8000/AbCdEfG",
  "long_url": "https://example.com/very/long/url/that/needs/shortening"
}
```

**Example**:
```bash
curl -X POST "http://localhost:8000/shorten" \
  -H "Content-Type: application/json" \
  -d '{"long_url": "https://example.com/very/long/url/that/needs/shortening"}'
```

### Create a Custom Short URL

**Endpoint**: `POST /shorten`

**Request Body**:
```json
{
  "long_url": "https://example.com/another/long/url",
  "custom_id": "my-custom-id"
}
```

**Response**:
```json
{
  "short_url": "http://localhost:8000/my-custom-id",
  "long_url": "https://example.com/another/long/url"
}
```

**Example**:
```bash
curl -X POST "http://localhost:8000/shorten" \
  -H "Content-Type: application/json" \
  -d '{"long_url": "https://example.com/another/long/url", "custom_id": "my-custom-id"}'
```

### Access a Short URL

Simply open the short URL in your browser or use:

```bash
curl -L "http://localhost:8000/{short_id}"
```

The `-L` flag tells curl to follow redirects, which will show you the content of the original URL.

## Technical Implementation

The service is built using:

- **FastAPI**: A modern, high-performance web framework for building APIs with Python
- **MongoDB**: A document-based NoSQL database for storing URL mappings
- **ShortUUID**: A library for generating compact, unique identifiers
- **Docker & Docker Compose**: For containerization and orchestration
- **PyMongo**: The Python driver for MongoDB

The URL shortening logic works by:
1. Accepting a long URL via the API
2. Generating a random 7-character ID or using the provided custom ID
3. Storing the mapping in MongoDB
4. Returning the short URL to the user

When a user accesses a short URL, the service:
1. Extracts the short ID from the URL
2. Looks up the original URL in MongoDB
3. Returns an HTTP redirect to the original URL

## Security Considerations

- Database credentials are injected via environment variables
- The MongoDB container uses authentication by default
- If deployed publicly, consider adding rate limiting and HTTPS

## Troubleshooting

**MongoDB Connection Issues**:
- Ensure MongoDB is running: `docker ps | grep mongodb`
- Check MongoDB logs: `docker logs mongodb`

**URL Shortener Issues**:
- Check URL shortener logs: `docker logs url-shortener`
- Verify network connectivity: `docker network inspect url-shortener-network`

## Future Enhancements

- Analytics for tracking URL visits
- User authentication for managing URLs
- URL expiration dates
- QR code generation for short URLs
- API rate limiting 