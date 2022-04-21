from __future__ import annotations
from transformers import pipeline

class Completion:
    @staticmethod
    def create(prompt: str):
        pass

def generator_from_pipeline():
    return pipeline("text-generation", model="gpt2")

def generate_from_model():
    from transformers import GPT2Tokenizer, GPT2LMHeadModel
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    model = GPT2LMHeadModel.from_pretrained("gpt2")

    def _wrapper(text):
        encoded_inputs = tokenizer(text, return_tensors='pt')
        outputs = model.generate(
            encoded_inputs.input_ids,
            do_sample=True,
            temperature=0.9,
            max_length=100,
       )
        decoded_output = tokenizer.batch_decode(outputs)
        import pdb; pdb.set_trace()
    return _wrapper

generate = generate_from_model()

while True:
    text = input("Input: ")
    print("You entered: ", text, f"(length {len(text)}))")
    outputs = generate(text)
    import pdb; pdb.set_trace()
