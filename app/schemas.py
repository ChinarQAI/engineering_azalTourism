from pydantic import BaseModel
from typing import List

class ActivitiesInput(BaseModel):
    minPrice: str
    maxPrice: str