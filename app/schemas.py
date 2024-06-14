from pydantic import BaseModel
from typing import List

class ActivitiesInput(BaseModel):
    """
    Represents input data for ingesting activities into an application.

    Attributes:
        location (str): The name of the location where the activity takes place.
        activity_address (str): The street address of the activity location.
        activity_title (str): The title or name of the activity.
        duration (str): The duration of the activity, e.g., "2 Hours".
        activity_description (str): A detailed description of the activity.
        min_price (str): The minimum price of the activity.
        max_price (str): The maximum price of the activity.
    """
    location: str
    activity_address: str
    activity_title: str
    duration: str
    activity_description: str
    min_price: str
    max_price: str
