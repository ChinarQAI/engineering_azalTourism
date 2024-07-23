import os
import importlib

import sys

sys.path.insert(1, "src")
sys.path.insert(2, "app")

from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.runnables.history import RunnableWithMessageHistory

# from tools_lib import tools_list
from utils import llm, get_memory, get_prompt

from tools_lib import tools_list_itinerary_gen

from dotenv import load_dotenv

load_dotenv()

agent_prompt_id = "alq-ai-team/azal_itinerary_generator_agentprompt"


class AgentManager:
    def __init__(self):
        self.prompt_id = agent_prompt_id

    def initialize_agent(self) -> RunnableWithMessageHistory:
        prompt = get_prompt(self.prompt_id)

        tools_list = tools_list_itinerary_gen
        agent = create_openai_tools_agent(llm, tools_list, prompt)

        #       creating agent executer
        agent_executer = AgentExecutor(
            agent=agent,
            tools=tools_list,
            verbose=True,
            return_intermediate_steps=True,
            early_stopping_method="generate"
        )
        agent_with_history = RunnableWithMessageHistory(
            agent_executer,
            lambda session_id: get_memory(session_id),
            input_messages_key="input",
            history_messages_key="chat_history",

        )

        return agent_with_history


def execute_agent(in_params: dict):
    session_id = in_params["session_id"]
    agent_manager = AgentManager()
    required_fields = ["location", "query", "number_of_days"]
    if not all(field in in_params for field in required_fields):
        print("ERROER")
        raise ValueError("Missing required fields in in_params")
    try:
        print("Before Init")
        agent = agent_manager.initialize_agent()
        print("Agent Initialized")
        result = agent.invoke({
            "input": in_params
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


if __name__ == "__main__":
    in_params = {
        "location": "istanbul",
        "query": "i would like to visit mosques",
        "number_of_days": 6,
        "session_id": "uwuwuw"
    }
    res = execute_agent(in_params)
    print(res)
