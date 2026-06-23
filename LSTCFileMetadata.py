from dataclasses import dataclass
from typing import Tuple, List
from dataClasses import PiperJointRecord, LSTCLimb, LSTCChildrenEntity, LSTCCoordinatePointSystem, LSTCParentEntity
def create_limbs(PiperJoints):
    limbs = []
    for Joint in PiperJoints:
        limbs.append(Joint.name) 
    return limbs

def build_lstc_limb_from_piper_joint(
    joint: PiperJointRecord,
    part: List = None
) -> LSTCLimb:
    """
    Create an LSTCLimb from a PiperJointRecord.

    Rules applied:
    - name: same as limb_name if provided, otherwise joint.name
    - cps.node1: parent entity frame keyword id
    - cps.node2: children entity frame keyword id
    - lock: last 3 values of joint.dof
    - lcid: always (0, 0, 0)
    - part: provided part list, default empty list
    - children.name: slave entity name
    - parent.name: provided parent_name if given, otherwise master entity name
    - parent.node: same as cps.node1
    """

    node1 = joint.entity_master.frame.keyword.id
    node2 = joint.entity_slave.frame.keyword.id

    cps = LSTCCoordinatePointSystem(
        node1=node1,
        node2=node2,
    )

    children = LSTCChildrenEntity(
        name=joint.entity_slave.name
    )

    parent = LSTCParentEntity(
        name=joint.entity_master.name,
        node=node1,
    )

    limb = LSTCLimb(
        name=joint.name,
        cps=cps,
        lock=tuple(int(not x) for x in joint.dof[3:6]),
        lcid=(0, 0, 0),
        part=part.parts,
        children=children,
        parent=parent,
    )

    return limb

def extract_parts_for_current_joint(PiperJoint, parts):
    for part in parts:
        if part.name == PiperJoint.entity_master.name:
            current_part = part
            return current_part
        else:
            continue
    return 0
    