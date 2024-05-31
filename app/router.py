import sys

import uvicorn
from fastapi import FastAPI, HTTPException

# Adding paths to import custom modules
sys.path.insert(1, "src")
sys.path.insert(2, "app")

