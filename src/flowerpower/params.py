from dataclasses import make_dataclass, asdict
from typing import Any
import toml
import yaml
import json
import os


def dict_to_dataclass(d) -> Any:
    """
    Convert a dictionary to a dataclass instance.

    Args:
        d (dict): The dictionary to be converted.

    Returns:
        Any: The dataclass instance created from the dictionary.
    """
    fields = {
        k: (dict_to_dataclass(v) if isinstance(v, dict) else v) for k, v in d.items()
    }
    Params = make_dataclass("Params", fields=fields)
    return Params(**fields)


class Params:
    def __init__(self, cfg_path: str = "conf") -> Any:
        self._cfg_path = cfg_path
        self._params = self._load_params()

    def _load_params(self) -> Any:
        """
        Load parameters from various file formats like toml, yaml, and json,
        and convert them to a dataclass.

        Returns:
            Any: The loaded and converted dataclass.
        """
        params_path = os.path.join(self._cfg_path, "params")

        if os.path.exists(params_path + ".toml"):
            with open(params_path + ".toml") as f:
                return dict_to_dataclass(toml.load(f))

        elif os.path.exists(params_path + ".yaml"):
            with open(params_path + ".yaml") as f:
                return dict_to_dataclass(yaml.safe_load(f))

        elif os.path.exists(params_path + ".yml"):
            with open(params_path + ".yml") as f:
                return dict_to_dataclass(yaml.safe_load(f))

        elif os.path.exists(params_path + ".json"):
            with open(params_path + ".json") as f:
                return dict_to_dataclass(json.load(f))

        raise Exception(f"Could not find params at {params_path}")

    def __getattr__(self, name: str | None) -> Any:
        return self._params if name is None else self._params.__getattribute__(name)

    def __get__(self, name: str | None) -> Any:
        return self._params if name is None else self._params.__getattribute__(name)

    def get(self, name: str | None, asdict: bool = False) -> Any | dict:
        """
        This function returns the specified attribute or the entire parameters dictionary.

        Args:
            name (str | None): The name of the attribute to retrieve, or None to retrieve the entire
            parameters dictionary.
            asdict (bool, optional): If True, the return value will be converted to a dictionary.
            Defaults to False.

        Returns:
            Any | dict: The specified attribute, the entire parameters dictionary, or a dictionary
            representation of the parameters.
        """
        if asdict:
            return asdict(self._params) if name is None else asdict(getattr(self, name))
        return self._params if name is None else self._params.__getattribute__(name)

    def __getitem__(self, name: str | None) -> Any:
        return self._params if name is None else self._params.__getattribute__(name)

    def asdict(self, name: str | None = None) -> dict:
        """
        Return a dictionary representation of the object with the specified name if provided,
        otherwise return a dictionary representation of the object's parameters.

        Parameters:
            name (str): The name of the attribute to get the dictionary representation from.
            Defaults to None.

        Returns:
            dict: A dictionary representation of the object or the specified attribute.
        """
        return asdict(self._params) if name is None else asdict(getattr(self, name))

    def attrs(self, name: str | None = None) -> tuple:
        return (
            tuple(self._params.__dict__.keys())
            if name is None
            else tuple(getattr(self, name).__dict__.keys())
        )
