# Import the Elasticsearch client setup from utils
from utils import es_client 

class IngestionPipeline:
    """
    A pipeline to ingest activities data into Elasticsearch.

    Attributes:
        location (str): The location for which activities are being ingested.
        activities (list): A list of activities related to the location.
    """
    
    def __init__(self, location: str, activities: list):
        """
        Initialize the IngestionPipeline with location and activities.

        Args:
            location (str): The location name.
            activities (list): A list of activities for the location.
        """
        self.location = location
        self.activities = activities
    
    # def embed_data(self):
    #     """
    #     Embed the activities using the OpenAI embeddings model.

    #     Returns:
    #         list: A list of embedded activities.
    #     """
    #     try:
    #         embeddings = embeddings_model.embed_documents(self.activities)
    #         return embeddings
    #     except Exception as e:
    #         print(f"Error embedding documents: {e}")
    #         return []
    
    def ingest_activities(self):
        """
        Ingest the activities data into Elasticsearch.

        This method indexes the provided location and activities into the 'azal_activities' index.
        """
        try:
            es_client.index(
                index="azal_activities",
                id=self.location,
                document={
                    "location": self.location,
                    "activities": self.activities,
                }
            )
        except Exception as e:
            print(f"Error ingesting data to ElasticSearch: {e}")

def activities_ingestion_driver(location: str, activities: list):
    """
    Driver function to ingest activities for a given location into Elasticsearch.

    Args:
        location (str): The location name.
        activities (list): A list of activities for the location.
    """
    try:
        # Create an instance of IngestionPipeline with the provided location and activities
        pipeline = IngestionPipeline(location, activities)
        
        # Use the ingest_activities method to insert data into Elasticsearch
        pipeline.ingest_activities()
    except Exception as e:
        print(f"Error during ingestion process: {e}")
