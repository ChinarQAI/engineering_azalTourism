import sys

# Adding paths to import custom modules
sys.path.insert(1, "src")
sys.path.insert(2, "app")

from langchain_core.tools import tool, StructuredTool
from custom_chain import ChainManager

from utils import es_client, setup_es_store, llm, get_memory

es_store = setup_es_store("azal_activities", es_client)


def get_activities_by_location_query(in_params: dict):
    print("ENtered get activities")
    location = in_params["location"]
    query = f'{in_params["query"]} I am visiting for {in_params["number_of_days"]} days'

    docs = es_store.similarity_search(
        query,
        k=10,
        filter=[{"term": {"metadata.location.keyword": location}}]
    )
    chain = custom_chain.create_chain("alq-ai-team/azal_chain_prompt")
    response = chain.invoke({
        "query": query,
        "context": docs
    })
    return response


@tool
def itinerary_generator_tool(in_params: dict):
    """
    This is a Itinerary Generator Tool that you can use to generate Itinerary for a user, based on the query provided
    Args:
        in_params: A dict with values for query and location and number of days

    Returns:

    """

    response = get_activities_by_location_query(in_params)
    return response


# itinerary_generator_tool = StructuredTool.from_function( func=get_activities_by_location_query,
# name="itinerary_generator_tool", description=" This is a Itinerary Generator Tool that you can use to generate
# Itinerary for a user, based on the query provided",
#
# )

# Putting tools together
tools_list_itinerary_gen = [itinerary_generator_tool]
