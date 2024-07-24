import sys
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter
from langchain_core.runnables.history import RunnableWithMessageHistory

# Insert custom directories to system path
sys.path.insert(1, "src")
sys.path.insert(2, "app")

# Import custom modules
from custom_chain import ChainManager
from utils import es_client, setup_es_store, llm, get_memory

# Setup Elasticsearch store
es_store = setup_es_store("azal_activities", es_client)


def get_activities_by_location_query(query: str, location: str, number_of_days: int):
    """
    Fetch activities based on a query and location from Elasticsearch store and process the response using a custom chain.

    Args:
        query (str): The search query for activities.
        location (str): The location to filter activities by.
        number_of_days (int): The number of days to consider for activities.

    Returns:
        dict: The response from the custom chain containing the filtered activities.

    Raises:
        Exception: If there is any error during the process, it will be raised with a message.
    """
    try:
        # Fetch documents matching the query and location from Elasticsearch
        docs = es_store.similarity_search(
            query,
            k=10,
            filter=[{"term": {"metadata.location.keyword": location.lower()}}]
        )

        # Initialize ChainManager and create a chain
        chain_manager = ChainManager()
        chain = chain_manager.create_chain("alq-ai-team/azal_chain_prompt")

        # Invoke the chain with the required inputs
        response = chain.invoke({
            "query": query,
            "context": docs,
            "number_of_days": number_of_days
        })

        return response

    except Exception as e:
        # Handle exceptions and raise them with a message
        raise Exception(f"Error fetching activities: {str(e)}")
