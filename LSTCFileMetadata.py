from dataclasses import dataclass
from typing import Tuple, List, Dict
from collections import defaultdict
from dataClasses import DynaPartSet, PiperJointRecord, PiperEntity, LSTCLimb, LSTCChildrenEntity, LSTCCoordinatePointSystem, LSTCParentEntity
def create_limbs(PiperJoints):
    limbs = []
    for Joint in PiperJoints:
        limbs.append(Joint.name) 
    return limbs

def build_lstc_limb_from_piper_joint(
    joint: PiperJointRecord,
    part: DynaPartSet = None
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
        name=part.name,
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

def build_parent_children_dict(
    entities: List[PiperEntity],
    joints: List[PiperJointRecord],
) -> Dict[str, List[str]]:
    """
    Build a dictionary:
        key   -> parent entity name (joint master)
        value -> list of child entity names (joint slaves)
    """

    entity_names = {entity.name for entity in entities}
    parent_children = defaultdict(list)
    for joint in joints:
        parent_name = joint.entity_master.name
        child_name = joint.entity_slave.name

        if parent_name not in entity_names:
            raise ValueError(
                f"Master entity '{parent_name}' from joint '{joint.name}' "
                f"is not present in entities list."
            )

        if child_name not in entity_names:
            raise ValueError(
                f"Slave entity '{child_name}' from joint '{joint.name}' "
                f"is not present in entities list."
            )

        if child_name not in parent_children[parent_name]:
            parent_children[parent_name].append(child_name)


    children_parent = defaultdict(list)
    for joint in joints:
        parent_name = joint.entity_master.name
        child_name = joint.entity_slave.name

        if parent_name not in entity_names:
            raise ValueError(
                f"Master entity '{parent_name}' from joint '{joint.name}' "
                f"is not present in entities list."
            )

        if child_name not in entity_names:
            raise ValueError(
                f"Slave entity '{child_name}' from joint '{joint.name}' "
                f"is not present in entities list."
            )

        if parent_name not in children_parent[child_name]:
            children_parent[child_name].append(parent_name)
            
    return dict(parent_children), dict(children_parent)

