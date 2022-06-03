from typing import Union, Optional, List

from fastapi import FastAPI
from .engine import get_engine
from pydantic import BaseModel


class Prompt(BaseModel):
    prompt: str

app = FastAPI()



@app.post("/engines/{engine_name}/completions")
def complete_with_engine(engine_name: str, prompt: Prompt):
    engine = get_engine(engine_name)
    response = engine.complete(prompt.prompt)
    return { "engine_name": engine_name, "prompt": prompt.prompt, "response": response }
