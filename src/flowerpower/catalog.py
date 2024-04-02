import os
from dataclasses import dataclass, make_dataclass, asdict
import toml
import yaml
import json
from typing import Any


@dataclass
class CatalogItem:
    type: str
    path: str


class Catalog:
    def __init__(self, cfg_path="conf"):
        self.cfg_path = cfg_path
        self._catalog = self._load_catalog()

    def _load_catalog(self):
        catalog_path = os.path.join(self.cfg_path, "catalog")

        if os.path.exists(catalog_path + ".toml"):
            with open(catalog_path + ".toml") as f:
                catalog_items = toml.load(f)

        elif os.path.exists(catalog_path + ".yaml"):
            with open(catalog_path + ".yaml") as f:
                catalog_items = yaml.safe_load(f)

        elif os.path.exists(catalog_path + ".yml"):
            with open(catalog_path + ".yml") as f:
                catalog_items = yaml.safe_load(f)

        elif os.path.exists(catalog_path + ".json"):
            with open(catalog_path + ".json") as f:
                catalog_items = json.load(f)

        else:
            raise Exception(f"Could not find catalog at {catalog_path}")

        return make_dataclass(
            "Catalog",
            fields={name: CatalogItem(**item) for name, item in catalog_items},
        )

    def __getattr__(self, name: str | None) -> Any:
        return self._catalog if name is None else self._catalog.__getattribute__(name)

    def __get__(self, name: str | None) -> Any:
        return self._catalog if name is None else self._catalog.__getattribute__(name)

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
            return (
                asdict(self._catalog) if name is None else asdict(getattr(self, name))
            )
        return self._catalog if name is None else self._catalog.__getattribute__(name)

    def __getitem__(self, name: str | None) -> Any:
        return self._catalog if name is None else self._catalog.__getattribute__(name)

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
        return asdict(self._catalog) if name is None else asdict(getattr(self, name))

    def items(self) -> tuple:
        return tuple(self._catalog.__dict__.keys())
