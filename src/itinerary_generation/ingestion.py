import os
import sys

sys.path.insert(1, "src")
sys.path.insert(2, "app")

# Import the Elasticsearch client setup from utils
from utils import es_client, setup_es_store, embeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain.schema import Document

es_store = setup_es_store("azal_activities", es_client)


class IngestionPipeline:
    """
        Initialize the IngestionPipeline with location and activities.

        Args:
            location (str): The location name.
            activity_address (str): The street address of the activity
            activity_title (str): The title of the activity.
            duration (str): The duration of the activity.
            activity_description (str): The description of the activity.
            min_price (str): The minimum price of the activity.
            max_price (str): The maximum price of the activity.
        """

    def __init__(self, location: str, activity_address: str, activity_title: str, duration: str,
                 activity_description: str, min_price: str, max_price: str):
        """
        Ingest the activity data into Elasticsearch.

        This method indexes the provided location and activity into the 'azal_activities' index.
        """
        self.location = location
        self.activity_address = activity_address
        self.activity_title = activity_title
        self.duration = duration
        self.activity_description = activity_description
        self.min_price = min_price
        self.max_price = max_price

    def ingest_activities(self):
        """
        Ingest the activities data into Elasticsearch.

        This method indexes the provided location and activities into the 'azal_activities' index.
        """
        try:
            # Create a document from the activity description
            document = Document(page_content=self.activity_description)
            loader = TextLoader(self.activity_description)

            # Split the document into smaller chunks

            text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
            docs = text_splitter.split_documents([document])
            for i, doc in enumerate(docs):
                doc.metadata["location"] = self.location.lower()
                doc.metadata["activity_address"] = self.activity_address.lower()
                doc.metadata["activity_title"] = self.activity_title.lower()
                doc.metadata["activity_description"] = self.activity_description.lower()
                doc.metadata["min_price"] = self.min_price.lower()
                doc.metadata["max_price"] = self.max_price.lower()
                doc.metadata["duration"] = self.duration.lower()

            es_store.from_documents(
                docs,  # from_documents expects a list of documents
                embeddings,
                index_name=f"azal_activities",
                es_connection=es_client,

            )

            es_store.client.indices.refresh(index="azal_activities")

        except Exception as e:
            print(f"Error ingesting data to Elasticsearch: {e}")


def activities_ingestion_driver(location: str, activity_address: str, activity_title: str, duration: str,
                                activity_description: str,
                                min_price: str, max_price: str):
    """
    Driver function to ingest activities for a given location into Elasticsearch.

    Args:

        location (str): The location name.
        activity_address (str): The street address of the activity
        activity_title (str): The title of the activity.
        duration (str): The duration of the activity.
        activity_description (str): The description of the activity.
        min_price (str): The minimum price of the activity.
        max_price (str): The maximum price of the activity.
    """
    try:
        # Create an instance of IngestionPipeline with the provided details
        pipeline = IngestionPipeline(location, activity_address, activity_title, duration, activity_description,
                                     min_price, max_price)

        # Use the ingest_activities method to insert data into Elasticsearch
        pipeline.ingest_activities()
    except Exception as e:
        print(f"Error during ingestion process: {e}")

if __name__ == "__main__":
    activities_ingestion_driver(
        location="Istanbul",
        activity_title="Bosphorus Cruise",
        activity_address="Eminönü, 34112 Fatih/Istanbul",
        duration="2 Hours",
        activity_description="Experience the 'Bosphorus Cruise', a 2-hour journey through the heart of Istanbul. Cruise along the Bosphorus Strait, where Europe meets Asia, and enjoy stunning views of historic landmarks, palaces, and fortresses. Prices range from $20 to $50. Refreshments are available onboard.",
        min_price="20",
        max_price="50"
    )




