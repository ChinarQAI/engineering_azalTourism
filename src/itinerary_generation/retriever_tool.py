import sys
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter
from langchain_core.runnables.history import RunnableWithMessageHistory



sys.path.insert(1, "src")
sys.path.insert(2, "app")

from custom_chain import ChainManager
from utils import es_client, setup_es_store, llm, get_memory


es_store = setup_es_store("azal_activities", es_client)


def get_activities_by_location_query(query: str, location: str, number_of_days: int, session_id: str):
    docs = es_store.similarity_search(
        query,
        k=10,
        filter=[{"term": {"metadata.location.keyword": location.lower()}}]
    )
    chain_manager = ChainManager()
    chain = chain_manager.create_chain("alq-ai-team/azal_chain_prompt")
    response = chain.invoke({
        "query": query,
        "context": docs
    })
    return response
