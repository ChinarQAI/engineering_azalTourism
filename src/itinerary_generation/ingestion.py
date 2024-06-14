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
            activity_title (str): The title of the activity.
            duration (str): The duration of the activity.
            activity_description (str): The description of the activity.
            min_price (str): The minimum price of the activity.
            max_price (str): The maximum price of the activity.
        """

    def __init__(self, location: str, activity_title: str, duration: str, activity_description: str, min_price: str,
                 max_price: str, activity_address: str):
        """
        Ingest the activity data into Elasticsearch.

        This method indexes the provided location and activity into the 'azal_activities' index.
        """
        self.location = location
        self.activity_title = activity_title
        self.activity_description = activity_description
        self.duration = duration
        self.min_price = min_price
        self.max_price = max_price
        self.activity_address = activity_address

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
                doc.metadata["activity_title"] = self.activity_title
                doc.metadata["activity_description"] = self.activity_description
                doc.metadata["min_price"] = self.min_price
                doc.metadata["max_price"] = self.max_price
                doc.metadata["duration"] = self.duration
                doc.metadata["location"] = self.location
                doc.metadata["activity_address"] = self.activity_address

            es_store.from_documents(
                docs,  # from_documents expects a list of documents
                embeddings,
                index_name=f"azal_activities",
                es_connection=es_client,

            )

            es_store.client.indices.refresh(index="azal_activities")

        except Exception as e:
            print(f"Error ingesting data to Elasticsearch: {e}")


def activities_ingestion_driver(location: str, activity_title: str, duration: str, activity_description: str,
                                min_price: str, max_price: str, activity_address: str):
    """
    Driver function to ingest activities for a given location into Elasticsearch.

    Args:
        activity_address: The street address of the activity
        location (str): The location name.
        activity_title (str): The title of the activity.
        duration (str): The duration of the activity.
        activity_description (str): The description of the activity.
        min_price (str): The minimum price of the activity.
        max_price (str): The maximum price of the activity.
    """
    try:
        # Create an instance of IngestionPipeline with the provided details
        pipeline = IngestionPipeline(location, activity_title, duration, activity_description, min_price, max_price,
                                     activity_address)

        # Use the ingest_activities method to insert data into Elasticsearch
        pipeline.ingest_activities()
    except Exception as e:
        print(f"Error during ingestion process: {e}")
