import sys

from langchain.chains.query_constructor.base import AttributeInfo
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain_openai import OpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from operator import itemgetter

from langchain_core.runnables.history import RunnableWithMessageHistory

sys.path.insert(1, "src")
sys.path.insert(2, "app")

from utils import es_client, setup_es_store, llm, get_memory

es_store = setup_es_store("azal_activities", es_client)


class AgentManager:
    def __init__(self, user_preference: dict):
        self.user_preference = user_preference

    def initialize_agent(selfself) -> RunnableWithMessageHistory:
        prompt_id = "azal_init_gen"

        pass


# JUST SOME TEST CODE FOR DOC RETRIEVAL
def get_activities_by_location(index_name: str, location: str):
    query = {
        "query": {
            "term": {
                "location.keyword": location  # Use the keyword type for exact matching
            }
        }
    }
    response = es_client.search(index=index_name, body=query, _source=["activities"])
    if response['hits']['hits']:
        return response['hits']['hits'][0]['_source']['activities']
    else:
        return None


def get_itinerary_by_location(location, query):
    docs = es_store.similarity_search(
        query,
        k=10,
        filter=[{"term": {"metadata.location.keyword": location}}]
    )
    return docs


if __name__ == "__main__":
    # Setting up the query and location
    query = "Generate me an itinerary baout anything but leather, I am allergic to leather so no leather"
    location = "izmir"
    number_of_days = 5

    # Template for itinerary generation
    template = """You are an Itinerary Generator. You generate an itinerary from the context given. You also keep in 
    mind the user's preferences, the place they are visiting, and the number of days for their trip. Make sure the 
    itinerary you generate is relevant to the user's preferences and based on the context provided. Only output the 
    metadata part of the activities you think are most relevant to the user's preferences.

    Place of visit: {location}
    Number of days: {number_of_days}
    User Preference: {query}
    Context: {context}
    """

    # Initializing output parser
    parser = StrOutputParser()

    # Retrieving context for the itinerary
    context = get_itinerary_by_location(location, query)
    print("+++++CONTEXT+++++++++")
    print(f"LENGTH OF CONTEXT: {len(context)}")
    print(context)
    for doc in context:
        print(doc.metadata["activity_title"])

    # Setting up the prompt template for the chatbot
    prompt = ChatPromptTemplate.from_template(template)

    # Creating the chain
    chain = prompt | llm | parser

    # Generating the itinerary using the chain
    print("Itinerary generation using CHAIN")
    response = chain.invoke({
        "context": context,
        "location": location,
        "query": query,
        "number_of_days": number_of_days
    })

    print(response)
