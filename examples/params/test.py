from dataclasses import dataclass


@dataclass
class A:
    a: int


@dataclass
class B:
    b: int


@dataclass
class Params:
    a: A
    b: B
