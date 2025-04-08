# URL Shortener Service

A simple URL shortener service built with FastAPI and MongoDB.

## Features

- Create short URLs from long URLs
- Support for custom URL IDs
- Redirect from short URLs to original URLs

## Getting Started

### Using Docker Compose

The easiest way to run the application is using Docker Compose:

```bash
docker-compose up -d
```

The service will be available at http://localhost:8000

### Building and Running Manually

1. Build the Docker image:
```bash
docker build -t url-shortener .
```

2. Run the container:
```bash
docker run -p 8000:8000 --network=host url-shortener
```

## API Usage

### Create a Short URL

```bash
curl -X POST "http://localhost:8000/shorten" \
  -H "Content-Type: application/json" \
  -d '{"long_url": "https://example.com/very/long/url/that/needs/shortening"}'
```

### Create a Short URL with Custom ID

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