from lxml import etree
import xml.etree.ElementTree as ET
from dataclasses import dataclass
import dataClasses

def parse_landmarks_lxml(xml_file):
    tree = etree.parse(xml_file)
    records = []

    for elem in tree.xpath("//landmarks"):
        name = elem.get("name")
        landmark_type = elem.get("type")

        keyword = elem.xpath("./keyword/@kw")
        node_id = elem.xpath("./keyword/id/text()")

        fe_keyword = keyword[0] if keyword else None
        fe_id = int(node_id[0]) if node_id else None

        records.append(dataClasses.PiperLandmarks(
            name=name,
            keyword=fe_keyword,
            id=fe_id
        ))

    return records

def parse_joint_entity(elem: ET.Element) -> dataClasses.PiperJointEntityRef:
    name = elem.get("name")

    keyword_elem = elem.find("./setFrame/keyword")
    if keyword_elem is None:
        raise ValueError(f"Missing <keyword> in entity '{name}'")

    kw = keyword_elem.get("kw")
    id_text = keyword_elem.findtext("id")

    if kw is None or id_text is None:
        raise ValueError(f"Incomplete frame definition in entity '{name}'")

    return dataClasses.PiperJointEntityRef(
        name=name,
        frame=dataClasses.FrameRef(
            keyword=dataClasses.PiperKeywordRef(
                kw=kw,
                id=int(id_text.strip())
            )
        )
    )


def parse_joints(xml_file: str) -> list:
    tree = ET.parse(xml_file)
    root = tree.getroot()

    joints = []

    for joint_elem in root.iter("joint"):
        joint_name = joint_elem.get("name")
        if joint_name is None:
            raise ValueError("A <joint> element is missing its 'name' attribute")

        master_elem = joint_elem.find("entity_master")
        slave_elem = joint_elem.find("entity_slave")
        dof_text = joint_elem.findtext("setDof")

        if master_elem is None or slave_elem is None:
            raise ValueError(f"Joint '{joint_name}' is missing master/slave entity")

        if dof_text is None:
            raise ValueError(f"Joint '{joint_name}' is missing <setDof>")

        dof = tuple(int(x) for x in dof_text.split())
        if len(dof) != 6:
            raise ValueError(f"Joint '{joint_name}' has invalid DOF vector: {dof_text}")

        joints.append(
            dataClasses.PiperJointRecord(
                name=joint_name,
                entity_master=parse_joint_entity(master_elem),
                entity_slave=parse_joint_entity(slave_elem),
                dof=dof
            )
        )

    return joints

def parse_entities(xml_file: str) -> list:
    tree = ET.parse(xml_file)
    root = tree.getroot()

    entities = []

    for entity_elem in root.iter("entity"):
        name = entity_elem.get("name")
        if name is None:
            raise ValueError("An <entity> element is missing its 'name' attribute")

        keyword_elem = entity_elem.find("keyword")
        if keyword_elem is None:
            raise ValueError(f"Entity '{name}' is missing <keyword>")

        kw = keyword_elem.get("kw")
        id_text = keyword_elem.findtext("id")

        if kw is None or id_text is None:
            raise ValueError(f"Entity '{name}' has incomplete keyword definition")

        entities.append(
            dataClasses.PiperEntity(
                name=name,
                keyword=kw,
                    id=id_text
                )
            )

    return entities

def store_autoSet_ids(entities):
    """
    Once the entity with name Auto is found, the ids of the set present in auto are stored in a list.
    Input: list containing PiperEntity objects
    Output: list object containing the ids

    """
    for entity in entities:
        if entity.name == 'Auto':
            IDS = entity.id
            IDS = IDS.split()
    return IDS

def create_PiperEntities_from_autoSet(AutoIDS, PartSets):
    piper_entities = []

    # Create a dictionary for fast lookup: {set_id: PartSets_object}
    partsets_by_id = {partset.id: partset for partset in PartSets}

    for auto_id in AutoIDS:
        if auto_id in partsets_by_id:
            matched_partset = partsets_by_id[auto_id]

            entity = dataClasses.PiperEntity(
                name=matched_partset.name,
                keyword='*SET_PART_LIST_TITLE',
                id=auto_id
            )
            piper_entities.append(entity)

    return piper_entities

def substitute_AutoEntities_with_singleEntity(old_entities, new_entities):
    EntitiesForJoints = []
    SkinEntities = []
    for old_entity in old_entities:
        if old_entity.name == 'Auto':
            EntitiesForJoints.extend(new_entities)
        else:
            SkinEntities.append(old_entity)

    return SkinEntities, EntitiesForJoints

def create_joints_for_hypermesh(Frames, Joints, PiperJointEntities):
    return 0 