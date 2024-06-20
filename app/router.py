import sys

# Adding paths to import custom modules
sys.path.insert(1, "src")
sys.path.insert(2, "app")

import uvicorn
from fastapi import FastAPI, HTTPException

# Import the ActivitiesInput schema for request validation
from schemas import ActivitiesInput, BulkActivitiesInput

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


@app.post("/itinerary/ingest/")
async def ingest_activities(activities_input: ActivitiesInput):
    """
    Endpoint to ingest activities for a given location.

    Args:
        activities_input (ActivitiesInput): An ActivitiesInput object containing details of activities to ingest.
            - location (str): The name of the location for which activities are being ingested.
            - activity_address (str): The street address of the activity.
            - activity_title (str): The title of the activity.
            - duration (str): The duration of the activity.
            - activity_description (str): The description of the activity.
            - min_price (str): The minimum price of the activity.
            - max_price (str): The maximum price of the activity.
    Raises:
        HTTPException: If there is an error during the ingestion process.

    Returns:
        dict: A dictionary indicating the success of the ingestion process.
    """
    try:
        # Use the activities_ingestion_driver to ingest activities for the given location
        activities_ingestion_driver(activities_input.location,
                                    activities_input.activity_address,
                                    activities_input.activity_title,
                                    activities_input.duration,
                                    activities_input.activity_description,
                                    activities_input.min_price,
                                    activities_input.max_price)
        return {"message": f"Activities for {activities_input.location} ingested successfully."}
    except Exception as e:
        # Log the exception and raise an HTTPException with status code 500
        print(f"Error Ingesting Data via Endpoint {e}")
        raise HTTPException(status_code=500, detail="Error ingesting data")


@app.post("/itinerary/bulk-ingest")
async def bulk_ingest(activities_input: BulkActivitiesInput):
    """
        Endpoint to ingest activities for a given location.

        Args:
            activities_input (ActivitiesInput): An ActivitiesInput object containing details of activities to ingest.
                - activities (List[Activity]): A list of Activity objects containing activity details.
        Raises:
            HTTPException: If there is an error during the ingestion process.

        Returns:
            dict: A dictionary indicating the success of the ingestion process.
        """
    try:
        for activity in activities_input.activities:
            activities_ingestion_driver(
                activity.location,
                activity.activity_address,
                activity.activity_title,
                activity.duration,
                activity.activity_description,
                activity.min_price,
                activity.max_price
            )
        return {"message": f"Activities ingested sucessfully."}
    except Exception as e:
        # Log the exception and raise an HTTPException with status code 500
        print(f"Error Ingesting Data via Endpoint {e}")
        raise HTTPException(status_code=500, detail="Error ingesting data")


# If the script is executed directly, run the ASGI server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
