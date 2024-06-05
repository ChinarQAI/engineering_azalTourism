import sys

# Adding paths to import custom modules
sys.path.insert(1, "src")
sys.path.insert(2, "app")

from langchain_core.tools import tool

@tool
def itinerary_generator(query: str):
    pass