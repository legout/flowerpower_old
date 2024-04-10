from .params import Params
from abc import ABC, abstractmethod


class Transformer(ABC):
    def __init__(self, cfg_path: str = "conf"):
        self._cfg_path = cfg_path

        self._params = Params(self._cfg_path)

    @abstractmethod
    def transform(self):
        pass

    @property
    def name(self):
        return self.__class__.__name__
