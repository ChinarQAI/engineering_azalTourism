import sys

# Adding paths to import custom modules
sys.path.insert(1, "src")
sys.path.insert(2, "app")

import uvicorn
from fastapi import FastAPI, HTTPException

# Import the ActivitiesInput schema for request validation
from schemas import ActivitiesInput

# Import the activities_ingestion_driver function from the ingestion module
from src.itinerary_generation.ingestion import activities_ingestion_driver

# Creating a FastAPI instance
app = FastAPI()

@app.get("/")
async def root():
    """
    Root endpoint of the FastAPI application.

    Returns:
        dict: A dictionary containing a message indicating that the service is healthy and running.
    """
    return {"message": "Service is healthy and running."}

@app.post("/ingest/{location}")
async def ingest_activities(location: str, activities_input: ActivitiesInput):
    """
    Endpoint to ingest activities for a given location.

    Args:
        location (str): The name of the location.
        activities_input (ActivitiesInput): An ActivitiesInput object containing a list of activities.

    Raises:
        HTTPException: If there is an error during the ingestion process.

    Returns:
        dict: A dictionary indicating the success of the ingestion process.
    """
    try:
        # Use the activities_ingestion_driver to ingest activities for the given location
        activities_ingestion_driver(location, activities_input.activities)
        return {"message": f"Activities for {location} ingested successfully."}
    except Exception as e:
        # Log the exception and raise an HTTPException with status code 500
        print(f"Error Ingesting Data via Endpoint {e}")
        raise HTTPException(status_code=500, detail="Error ingesting data")

# If the script is executed directly, run the ASGI server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
