import torch
import numpy as np

from transformers import GPT2LMHeadModel
from transformers.modeling_outputs import CausalLMOutputWithCrossAttentions
from transformers import GPT2Tokenizer

from onnxruntime import InferenceSession

MAX_SEQUENCE_LENGTH = 100

class Task:
    """A complete ML task such as text generation, or classification."""
    def __init__(self):
        pass

    def preprocess(self, *args):
        raise NotImplementedError()

    def postprocess(self, *args):
        raise NotImplementedError()

    def inference(self, *args):
        raise NotImplementedError()

class ONNXTask(Task):
    def __init__(self, model_file: str):
        self.model_file = model_file

    def inference(self, *args):
        return super().inference(*args)

def generator_from_onnx(model_file):

    model = GPT2LMHeadModel.from_pretrained("gpt2")
    session = InferenceSession(model_file)

    def onnx_forward(*args, **kwargs):
        input_ids = kwargs["input_ids"]
        onnx_inputs = {}
        # gpt2 onnx model expects an extra dimension for some reason
        onnx_inputs["input1"] = np.expand_dims(input_ids.numpy(), axis=0)
        onnx_out_names = [x.name for x in session.get_outputs()]
        outputs = session.run(input_feed=onnx_inputs, output_names=onnx_out_names)
        # unwrap the extra dimension
        logits = torch.tensor(outputs[0][0])
        res = CausalLMOutputWithCrossAttentions(logits=logits)
        return res

    model.forward = onnx_forward

    def _wrapper(encoded_inputs):
        return model.generate(
            encoded_inputs.input_ids,
            do_sample=True,
            temperature=0.9,
            max_length=MAX_SEQUENCE_LENGTH,
        )

    return _wrapper

class ONNXGeneration(ONNXTask):
    def __init__(self, model_file: str) -> None:
        super().__init__(model_file)
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        self.model = generator_from_onnx(self.model_file)

    def preprocess(self, text):
        encoded_inputs = self.tokenizer(text, return_tensors="pt")
        return encoded_inputs

    def postprocess(self, outputs):
        decoded_output = self.tokenizer.batch_decode(outputs)
        return decoded_output

    def inference(self, inputs):
        return self.model(inputs)
