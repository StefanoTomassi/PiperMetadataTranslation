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
class LSTCCoordinatePointSystem:
    node1: int
    node2: int

@dataclass
class LSTCChildrenEntity:
    name: str

@dataclass
class LSTCParentEntity:
    name: str
    node: int

@dataclass
class LSTCLimb:
    name: str
    cps: LSTCCoordinatePointSystem
    lock: Tuple[int, int, int]
    lcid: Tuple[int, int, int]
    part: list
    children: LSTCChildrenEntity
    parent: LSTCParentEntity

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
class PiperFrameRef:
    keyword: PiperKeywordRef

@dataclass
class PiperJointEntityRef:
    name: str
    frame: PiperFrameRef

@dataclass
class PiperJointRecord:
    name: str
    entity_master: PiperJointEntityRef
    entity_slave: PiperJointEntityRef
    dof: Tuple[int, int, int, int, int, int]