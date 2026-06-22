from dataclasses import dataclass
from typing import Tuple

@dataclass
class DynaPartSet:
    name: str
    id: int
    parts: list

@dataclass
class DynaCoordinateSys:
    name: str
    id: int
    node: int  
@dataclass
class PiperEntity:
    name: str
    keyword: str
    id: list

@dataclass
class PiperLandmarks:
    name: str
    keyword: str
    id: int

@dataclass
class PiperKeywordRef:
    kw: str
    id: int


@dataclass
class FrameRef:
    keyword: PiperKeywordRef


@dataclass
class PiperJointEntityRef:
    name: str
    frame: FrameRef


@dataclass
class PiperJointRecord:
    name: str
    entity_master: PiperJointEntityRef
    entity_slave: PiperJointEntityRef
    dof: Tuple[int, int, int, int, int, int]

