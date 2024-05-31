from elasticsearch import Elasticsearch  
from dotenv import load_dotenv  
import os 

# Load environment variables from a .env file
load_dotenv()

def setup_es_client() -> Elasticsearch:
    """
    Set up and return an Elasticsearch client using environment variables.

    This function reads the Elasticsearch API key and endpoint from environment variables,
    initializes an Elasticsearch client, and returns it.

    Returns:
        Elasticsearch: An initialized Elasticsearch client.
    """
    # Load environment variables for Elasticsearch API and endpoint
    ES_API = os.environ.get("ES_API")
    ES_ENDPOINT = os.environ.get("ES_ENDPOINT")

    # Initialize the Elasticsearch client
    es_client = Elasticsearch(
        ES_ENDPOINT,
        api_key=ES_API
    )

    return es_client

# Create the Elasticsearch client by calling the setup function
es_client = setup_es_client()


