import json
from elasticsearch import Elasticsearch
from langchain_community.chat_message_histories import ElasticsearchChatMessageHistory
from dotenv import load_dotenv
import os
from langchain_elasticsearch import ElasticsearchStore
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# Load environment variables from a .env file
load_dotenv()

from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(api_key=os.environ.get("OPENAI_API_KEY"))


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


def setup_llm() -> object:
    """
    Initialize the large language model.

    Returns:
        object: A Large Language Model instance.
    """

    # load the json string from the env
    llm_settings_str = os.environ.get("MODEL_SETTINGS")

    # Parse the JSON string into a dictionary
    llm_settings = json.loads(llm_settings_str)

    # Create and configure the ChatOpenAI model instance
    llm_model = ChatOpenAI(
        model_name=llm_settings.get("model_name"),
        streaming=llm_settings.get("streaming"),
        callbacks=[StreamingStdOutCallbackHandler()],
        verbose=True
    )
    return llm_model


# Setting up llm Model
llm = setup_llm()


def get_memory(session_id) -> object:
    """
    Retrieve conversational memory for a given session ID.

    Args:
        session_id (str): The session ID for which memory is requested.

    Returns:
        object: Conversational Memory object.
    """
    # Create an ES MessageHistory instance for storing message history
    message_history = ElasticsearchChatMessageHistory(
        es_url=os.environ.get("ES_ENDPOINT"), es_api_key=os.environ.get("ES_API"), index="itin-memory",
        session_id=session_id, esnsure_ascii=True
    )
    return message_history


def get_prompt(prompt_id) -> str:
    """
    Fetch a prompt from the Langchain hub.

    Args:
        prompt_id (str): The ID of the prompt to fetch.

    Returns:
        str: The fetched prompt.
    """
    return hub.pull(prompt_id)


def setup_es_store(index_name: str, es_client: Elasticsearch):
    """
       Sets up and returns an ElasticsearchStore index for storing embeddings and for RAG.

       Args:
           index_name (str): The name of the Elasticsearch index where embeddings will be stored.
           es_client (Elasticsearch): An instance of the Elasticsearch client connected to the Elasticsearch cluster.

       Returns:
           ElasticsearchStore: An instance of ElasticsearchStore configured with the provided index name,
                                embeddings, and Elasticsearch connection.

       """
    es_vector_store = ElasticsearchStore(
        embedding=embeddings,
        index_name=index_name,
        es_connection=es_client
    )
    return es_vector_store
