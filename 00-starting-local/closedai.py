from __future__ import annotations
import torch
import numpy
from transformers import pipeline
from onnxruntime import InferenceSession

class Completion:
    @staticmethod
    def create(prompt: str):
        pass

def generator_from_pipeline():
    return pipeline("text-generation", model="gpt2")

def generate_from_model():
    from transformers import GPT2Tokenizer, GPT2LMHeadModel, GPT2Model
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    model = GPT2LMHeadModel.from_pretrained("gpt2")

    def _wrapper(text):
        encoded_inputs = tokenizer(text, return_tensors='pt')
        outputs = model(**encoded_inputs)
        import pdb; pdb.set_trace()
        outputs = model.generate(
            encoded_inputs.input_ids,
            do_sample=True,
            temperature=0.9,
            max_length=100,
        )
        decoded_output = tokenizer.batch_decode(outputs)
        return decoded_output

    return _wrapper

def generate_from_model_onnx():
    from transformers import GPT2Tokenizer, GPT2LMHeadModel, GPT2Model
    from transformers.modeling_outputs import BaseModelOutputWithPastAndCrossAttentions, CausalLMOutputWithCrossAttentions
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    model = GPT2LMHeadModel.from_pretrained("gpt2")
    session = InferenceSession("onnx/model.onnx")

    all_hidden_states = []
    def onnx_eval(self, input_ids, **kwargs):
        print("Using ONNX")
        # assert kwargs['return_dict'] is True, "only support return_dict mode"
        # assert kwargs['use_cache'] is None
        # assert kwargs['output_attentions'] is None

        # Add the input_ids, then pre-process for ONNX.
        kwargs["input_ids"] = input_ids
        onnx_input_names = dict((inp.name, inp) for inp in session.get_inputs())
        onnx_inputs = {}
        # for key in onnx_input_names:
        #     if key.startswith("past_key_values"):
        #         continue
        #     else:
        #         onnx_inputs[key] = value = kwargs[key]

        #     if isinstance(value, torch.Tensor):
        #         onnx_inputs[key] = value.numpy()

        onnx_inputs["input_ids"] = input_ids.numpy()
        onnx_inputs["attention_mask"] = kwargs['attention_mask'].numpy().astype('float32')

        past_sequence = 0
        (batch, sequence) = onnx_inputs["input_ids"].shape

        for name in onnx_input_names:
            if name.startswith("past_key_values"):
                onnx_input = onnx_input_names[name]
                shape = []

                for dim in onnx_input.shape:
                    dim = str(dim)
                    dim = dim.replace('batch', str(batch))
                    dim = dim.replace('past_sequence + sequence', str(past_sequence + sequence))
                    dim = dim.replace('sequence', str(sequence))
                    shape.append(int(dim))
                dtype = onnx_input.type[7:-1]
                if dtype == "float":
                    dtype += "32"
                onnx_inputs[name] = numpy.zeros(shape=shape, dtype=dtype)

        # Run ONNX outputing hidden state
        out_names = [x.name for x in session.get_outputs()]
        import pdb; pdb.set_trace()
        outputs = session.run(output_names=out_names, input_feed=onnx_inputs)
        name_to_output = dict(zip(out_names, outputs))
        past_key_values = [[None, None]] * 12
        for name in name_to_output:
            output = name_to_output[name]
            if name.startswith("present"):
                (_, number, key_or_value) = name.split(".")
                if key_or_value == "key":
                    index = 0
                elif key_or_value == "value":
                    index = 1
                else:
                    raise Exception("ll")

                past_key_values[int(number)][index] = torch.from_numpy(output)

        for i, value in enumerate(past_key_values):
            past_key_values[i] = tuple(past_key_values[i])

        past_key_values = tuple(past_key_values)
        logits = torch.from_numpy(name_to_output["logits"])

        # import pdb; pdb.set_trace()

        return CausalLMOutputWithCrossAttentions(logits=logits, past_key_values=past_key_values)

    GPT2LMHeadModel.__call__ = onnx_eval

    def _wrapper(text):
        encoded_inputs = tokenizer(text, return_tensors='pt')
        outputs = model(**encoded_inputs)
        outputs = model.generate(
            encoded_inputs.input_ids,
            do_sample=True,
            temperature=0.9,
            max_length=100,
        )
        import pdb; pdb.set_trace()
        decoded_output = tokenizer.batch_decode(outputs)
        return decoded_output

    return _wrapper

generate = generate_from_model()
generate = generate_from_model_onnx()

while True:
    text = "foo" # input("Input: ")
    print("You entered: ", text, f"(length {len(text)}))")
    outputs = generate(text)
    print(outputs)
