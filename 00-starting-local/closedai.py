from __future__ import annotations
from transformers import pipeline

class Completion:
    @staticmethod
    def create(prompt: str):
        pass

generation = pipeline("text-generation", model="gpt2")

while True:
    text = input("Input: ")
    print("You entered: ", text, f"(length {len(text)}))")
    outputs = generation(text)
    import pdb; pdb.set_trace()
