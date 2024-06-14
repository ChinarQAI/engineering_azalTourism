import sys

sys.path.insert(1, "src")
sys.path.insert(2, "app")

from utils import es_client, setup_es_store

es_store = setup_es_store("azal_activities", es_client)


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


if __name__ == "__main__":
    # Testing some retriever funcs
    query = "Suggest some activities in istanbul"
    docs = es_store.similarity_search(
        query, filter=[{"term": {"metadata.location.keyword": "Istanbul"}}]
    )
    print(docs)