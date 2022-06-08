import time

from typing import Union, Optional, List

from fastapi import FastAPI, Request
from engine import get_engine
from pydantic import BaseModel


class Prompt(BaseModel):
    prompt: str

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

#TODO make this not log every time
@app.get("/healthz")
def healthy():
    return { "healthy": "ok" }


@app.post("/engines/{engine_name}/completions")
def complete_with_engine(engine_name: str, prompt: Prompt):
    engine = get_engine(engine_name)
    response = engine.complete(prompt.prompt)
    return { "engine_name": engine_name, "prompt": prompt.prompt, "response": response }
