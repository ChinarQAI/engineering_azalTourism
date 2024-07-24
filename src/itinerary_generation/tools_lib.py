import sys

# Adding paths to import custom modules
sys.path.insert(1, "src")
sys.path.insert(2, "app")

from langchain_core.tools import tool, StructuredTool
from itinerary_generation.retriever_tool import get_activities_by_location_query

from utils import es_client, setup_es_store, llm, get_memory
from langchain.pydantic_v1 import BaseModel, Field


class ItineraryGenerationInput(BaseModel):
    location: str
    query: str
    number_of_days: int
    session_id: str


es_store = setup_es_store("azal_activities", es_client)

@tool
def itinerary_generator_tool(query: str, location: str, number_of_days: int):
    """
    Itinerary Generator Tool

    This tool generates an itinerary for a user based on the provided query, location, and number of days.

    Args:
        query (str): The user's query detailing the type of activities or preferences for the itinerary.
        location (str): The destination where the user wants to go.
        number_of_days (int): The number of days for the visit.

    Returns:
        dict: A dictionary containing the generated itinerary based on the input parameters.
    """

    # response = get_activities_by_location_query(query, location, number_of_days)
    response = get_activities_by_location_query(query, location, number_of_days)
    return response


# itinerary_generator_tool = StructuredTool.from_function(
#     func=get_activities_by_location_query,
#     name="itinerary_generator_tool",
#     description="This is a Itinerary Generator Tool that you can use to generate Itinerary for a user, based on the "
#                 "query provided",
#     args_schema=ItineraryGenerationInput

# )

# Putting tools together
tools_list_itinerary_gen = [itinerary_generator_tool]
