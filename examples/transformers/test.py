from flowerpower.transform import Transformer
from params.test import Params


class Test(Transformer):
    def __init__(self, params: Params | None = None, cfg_path: str = "conf"):
        super().__init__(params, cfg_path)

    def transform(self):
        print(self.params)
        return self
