from typing import Union, Optional, List

from fastapi import FastAPI
from .engine import get_engine

app = FastAPI()

@app.post("/engines/{engine_name}/completions")
def complete_with_engine(engine_name: str, prompt: Optional[Union[str, List[str]]] = None):
    engine = get_engine(engine_name)
    response = engine.complete(prompt)
    return { "engine_name": engine_name, "prompt": prompt, "response": response }
