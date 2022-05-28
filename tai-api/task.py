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
