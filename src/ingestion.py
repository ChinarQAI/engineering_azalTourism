from langchain_openai import OpenAIEmbeddings
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os
load_dotenv()


ES_API= os.environ.get("ES_API")
ES_ENDPOINT= os.environ.get("ES_ENDPOINT")
OPENAI_API_KEY= os.environ.get("OPENAI_API_KEY")


es_client= Elasticsearch(
    ES_ENDPOINT,
    api_key= ES_API

)

embeddings_model = OpenAIEmbeddings()
class IngestionPipeline:
    def __init__(self, location: str, activities: list):
        self.location= location
        self.activities= activities
    
    # def embed_data(self):
    #     try:
    #         embeddings= embeddings_model.embed_documents(self.activities)
    #         return embeddings
    #     except Exception as e:
    #         print(f"Error embedding documents: {e}")
    #         return []
    
    def ingest_activities(self):
        try:
            es_client.index(
            index="azal_activities",
            id=self.location,
            document={
                "location": self.location,
                "activities": self.activities,
            })
        except Exception as e:
            print(f"Error ingesting data to ElasticSearch: {e}")
        
def activities_ingestion_driver(location: str, activities: list):
    try:
        # Create an instance of IngestionPipeline with the provided location and activities
        pipeline = IngestionPipeline(location, activities)
        
        # Use the ingest_activities method to insert data into Elasticsearch
        pipeline.ingest_activities()
    except Exception as e:
        print(f"Error during ingestion process: {e}")




# def ingest_activities(location: str, activities: list):

#     # es_client.indices.create(index="azal_activities")
#     es_client.index(
#         index="azal_activities",
#         id=location,
#         document={
#             "location": location,
#             "activities": activities,
#             "embeddings": embeddings
#         }
# )
#     print("INgestion comlete")


if __name__== "__main__":
    activities_istanbul = [
        "Visit the Hagia Sophia",
        "Explore the Blue Mosque",
        "Walk through the Topkapi Palace",
        "Cruise on the Bosphorus",
        "Visit the Grand Bazaar",
        "Tour the Basilica Cistern",
        "Explore the Dolmabahce Palace",
        "Walk around Taksim Square",
        "Visit the Istanbul Modern Art Museum",
        "Stroll through the Spice Bazaar",
        "Take a walk on Istiklal Street",
        "Visit the Chora Church",
        "Explore the Istanbul Archaeology Museums",
        "Enjoy a Turkish bath at a hammam",
        "Visit the Galata Tower",
        "Relax at Emirgan Park",
        "Tour the Suleymaniye Mosque",
        "Explore the Rahmi M. Koç Museum",
        "Visit the Miniaturk Park",
        "Take a ferry to the Princes' Islands",
        "Explore the Yedikule Fortress",
        "Walk through the Ortaköy neighborhood",
        "Visit the Istanbul Aquarium",
        "Explore the Istanbul Military Museum",
        "Visit the Sakip Sabanci Museum",
        "Enjoy a meal at a rooftop restaurant",
        "Attend a Whirling Dervishes show",
        "Take a boat tour of the Golden Horn",
        "Visit the Istanbul Toy Museum",
        "Explore the Beylerbeyi Palace"
    ]
    activities_ingestion_driver("istanbul", activities_istanbul)
   