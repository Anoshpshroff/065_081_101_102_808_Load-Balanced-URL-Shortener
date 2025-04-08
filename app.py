from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
import shortuuid
import pymongo
import os
import time
import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="URL Shortener")

# MongoDB connection parameters
mongo_user = os.getenv('MONGO_USER', 'anosh')
mongo_password = os.getenv('MONGO_PASSWORD', '3214')
mongo_host = os.getenv('MONGO_HOST', 'mongodb')
mongo_port = os.getenv('MONGO_PORT', '27017')

# Build connection string
mongo_uri = f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}/"

# Initialize MongoDB client with retry logic
client = None
db = None
urls_collection = None
max_retries = 5
retry_delay = 5  # seconds

for attempt in range(max_retries):
    try:
        logger.info(f"Connecting to MongoDB (attempt {attempt+1}/{max_retries})...")
        client = pymongo.MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        # Test connection
        client.admin.command('ping')
        # Initialize database and collection
        db = client.url_shortener
        urls_collection = db.urls
        logger.info("Successfully connected to MongoDB")
        break
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {str(e)}")
        if attempt < max_retries - 1:
            logger.info(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            logger.error("Max retries reached. Could not connect to MongoDB.")
            client = None
            db = None
            urls_collection = None

class URLRequest(BaseModel):
    long_url: HttpUrl
    custom_id: Optional[str] = None

class URLResponse(BaseModel):
    short_url: str
    long_url: HttpUrl

@app.post("/shorten", response_model=URLResponse)
async def create_short_url(url_request: URLRequest, request: Request):
    if client is None or db is None or urls_collection is None:
        raise HTTPException(status_code=503, detail="Database connection is not available")
    
    # Use custom ID or generate a short ID
    short_id = url_request.custom_id or shortuuid.uuid()[:7]
    
    # Check if ID already exists
    if url_request.custom_id and urls_collection.find_one({"_id": short_id}):
        raise HTTPException(status_code=400, detail="Custom ID already in use")
    
    try:
        # Store URL mapping
        urls_collection.insert_one({
            "_id": short_id,
            "long_url": str(url_request.long_url)
        })
        
        # Generate the short URL using the host from the request
        base_url = str(request.base_url).rstrip('/')
        short_url = f"{base_url}/{short_id}"
        
        return {"short_url": short_url, "long_url": url_request.long_url}
    except Exception as e:
        logger.error(f"Error saving URL: {str(e)}")
        raise HTTPException(status_code=500, detail="Error saving URL")

@app.get("/")
async def read_root():
    db_status = "Connected" if client is not None else "Disconnected"
    return {
        "message": "URL Shortener API. Use /shorten to create a short URL.",
        "database_status": db_status
    }

@app.get("/_health")
async def health_check():
    """Health check endpoint for Kubernetes liveness probe"""
    if client is None:
        raise HTTPException(status_code=503, detail="Database connection is not available")
    
    try:
        # Simple ping to check MongoDB connection
        client.admin.command('ping')
        return {"status": "healthy"}
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Database is not responding")

# This needs to be last to avoid conflicts with other routes
@app.get("/{short_id}")
async def redirect_to_url(short_id: str):
    if client is None or db is None or urls_collection is None:
        raise HTTPException(status_code=503, detail="Database connection is not available")
    
    try:
        # Lookup the original URL
        url_mapping = urls_collection.find_one({"_id": short_id})
        if not url_mapping:
            raise HTTPException(status_code=404, detail="URL not found")
        
        # Redirect to the original URL
        return RedirectResponse(url=url_mapping["long_url"])
    except pymongo.errors.PyMongoError as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True) 