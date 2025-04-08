from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
import shortuuid
import pymongo
import os
from typing import Optional

app = FastAPI(title="URL Shortener")

# MongoDB connection
client = pymongo.MongoClient(
    f"mongodb://{os.getenv('MONGO_USER', 'anosh')}:{os.getenv('MONGO_PASSWORD', '3214')}@mongodb:27017/"
)
db = client.url_shortener
urls_collection = db.urls

class URLRequest(BaseModel):
    long_url: HttpUrl
    custom_id: Optional[str] = None

class URLResponse(BaseModel):
    short_url: str
    long_url: HttpUrl

@app.post("/shorten", response_model=URLResponse)
async def create_short_url(url_request: URLRequest, request: Request):
    # Use custom ID or generate a short ID
    short_id = url_request.custom_id or shortuuid.uuid()[:7]
    
    # Check if ID already exists
    if url_request.custom_id and urls_collection.find_one({"_id": short_id}):
        raise HTTPException(status_code=400, detail="Custom ID already in use")
    
    # Store URL mapping
    urls_collection.insert_one({
        "_id": short_id,
        "long_url": str(url_request.long_url)
    })
    
    # Generate the short URL using the host from the request
    base_url = str(request.base_url).rstrip('/')
    short_url = f"{base_url}/{short_id}"
    
    return {"short_url": short_url, "long_url": url_request.long_url}

@app.get("/{short_id}")
async def redirect_to_url(short_id: str):
    # Lookup the original URL
    url_mapping = urls_collection.find_one({"_id": short_id})
    if not url_mapping:
        raise HTTPException(status_code=404, detail="URL not found")
    
    # Redirect to the original URL
    return RedirectResponse(url=url_mapping["long_url"])

@app.get("/")
async def read_root():
    return {"message": "URL Shortener API. Use /shorten to create a short URL."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True) 