from csv import excel_tab
from transformers import pipeline

class Engine:
    def complete(self, prompt: str) -> str:
        pass

class HFGPT2Engine(Engine):
    def __init__(self):
        self.generator = pipeline('text-generation', model = 'gpt2')

    def complete(self, prompt: str) -> str:
        return self.generator(prompt, max_length = 30, num_return_sequences=3)

class UnknownEngine(Exception):
    pass

ENGINE_MAP = {
    "hf-gpt-2": HFGPT2Engine()
}

def get_engine(engine_name: str) -> Engine:
    engine = ENGINE_MAP.get(engine_name, None)
    if engine:
        return engine
    else:
        raise UnknownEngine(f"Engine not found: {engine_name}")
