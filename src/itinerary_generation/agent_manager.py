import os
import importlib
import sys

# Insert custom directories to system path
sys.path.insert(1, "src")
sys.path.insert(2, "app")

# Import necessary modules
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.runnables.history import RunnableWithMessageHistory
from utils import llm, get_memory, get_prompt
from itinerary_generation.tools_lib import tools_list_itinerary_gen
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define the prompt ID for the agent
agent_prompt_id = "alq-ai-team/azal_itinerary_generator_agentprompt"

class AgentManager:
    """
    Manages the creation and initialization of agents with specific prompts and tools.
    """

    def __init__(self):
        """
        Initializes the AgentManager with a specific prompt ID.
        """
        self.prompt_id = agent_prompt_id

    def initialize_agent(self) -> RunnableWithMessageHistory:
        """
        Initializes the agent with the specified prompt and tools, and sets up the agent executor with message history.

        Returns:
            RunnableWithMessageHistory: The initialized agent with message history.

        Raises:
            Exception: If there is an error during the initialization of the agent.
        """
        try:
            # Fetch the prompt based on the provided prompt ID
            prompt = get_prompt(self.prompt_id)

            # Define the tools list for the itinerary generation
            tools_list = tools_list_itinerary_gen

            # Create the agent using the LLM, tools list, and prompt
            agent = create_openai_tools_agent(llm, tools_list, prompt)

            # Create the agent executor
            agent_executor = AgentExecutor(
                agent=agent,
                tools=tools_list,
                verbose=True,
                return_intermediate_steps=True,
                early_stopping_method="generate"
            )

            # Create the agent with message history
            agent_with_history = RunnableWithMessageHistory(
                agent_executor,
                lambda session_id: get_memory(session_id),
                input_messages_key="input",
                history_messages_key="chat_history",
            )

            return agent_with_history

        except Exception as e:
            # Handle exceptions and raise them with a message
            raise Exception(f"Error initializing agent: {str(e)}")


def execute_agent(in_params: dict):
    """
    Executes the agent with the provided input parameters.

    Args:
        in_params (dict): A dictionary containing the input parameters, including 'session_id' and 'query'.

    Returns:
        dict: The result of the agent execution.

    Raises:
        Exception: If there is an error during the execution of the agent.
    """
    session_id = in_params.get("session_id")
    agent_manager = AgentManager()

    try:
        print("Before Init")
        # Initialize the agent
        agent = agent_manager.initialize_agent()
        print("Agent Initialized")

        # Invoke the agent with the input query
        result = agent.invoke({
            "input": in_params["query"]
        }, {
            "configurable": {
                "session_id": session_id
            }
        })

    except Exception as e:
        print(f"Error during agent execution: {e}")
        # Return an error message in case of exception
        result = "Internal Error, If the issue persists please call admin"

    return result


# if __name__ == "__main__":
#     in_params = {
#         # "location": "izmir",
#         "query": "i would like to visit izmir for 4 days, I like leather based activities ",
#         # "number_of_days": 2,
#         "session_id": "23423sdf"
#
#     }
#     print(f"in_params TYPE: {type(in_params)}")
#     res = execute_agent(in_params)
#     print(res)
#     print("++++++++++++++++RESPONSE++++++++++++++")
#     print(res["output"])
