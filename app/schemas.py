from pydantic import BaseModel
from typing import List

class ActivitiesInput(BaseModel):
    activities: List[str]