import sys

# Insert custom directories to system path
sys.path.insert(1, "src")
sys.path.insert(2, "app")

# Import custom modules
from utils import llm, get_prompt
from langchain_core.output_parsers import StrOutputParser

class ChainManager:
    """
    Manages the creation of chains by combining prompts with language models.
    """

    def __init__(self):
        """
        Initializes the ChainManager.
        """
        pass

    def create_chain(self, prompt_id: str):
        """
        Creates a chain by fetching a prompt based on the provided ID and appending it to the chain.

        Args:
            prompt_id (str): The ID of the prompt used to generate the chain.

        Returns:
            chain: A chain formed by combining the fetched prompt with the model.

        Raises:
            Exception: If there is an error fetching the prompt or creating the chain.
        """
        try:
            # Fetch prompt based on the provided prompt ID
            prompt = get_prompt(prompt_id)
            parser = StrOutputParser()

            # Concatenate the fetched prompt with the model
            return prompt | llm | parser

        except Exception as e:
            # Handle exceptions and raise them with a message
            raise Exception(f"Error creating chain: {str(e)}")