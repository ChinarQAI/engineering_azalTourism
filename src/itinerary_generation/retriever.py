from utils import es_client

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

    index_name= "azal_activities"
    location= "bursa"
    activities= get_activities_by_location(index_name, location)
    print(type(activities))
    # Print the activities
    print(activities)