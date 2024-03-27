from dataclasses import dataclass
import msgspec
import os

@dataclass
class Params:
    ...


class Transformer:
    def __init__(self, params: Params | None = None, cfg_path: str = "conf"):
        self.cfg_path = cfg_path
        if params is None:
            self._load_params()
        else:
            self.params = params

    def _load_params(self):
        path = os.path.join(self.cfg_path , f"params/{self.name}.toml")
        print(path)
        self.params = msgspec.toml.decode(open(path).read(), type=Params)

    def transform(self):
        ...

    @property
    def name(self):
        return self.__class__.__name__.lower()