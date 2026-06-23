from parseXMLPiperData import parse_joints, parse_landmarks_lxml, parse_entities
from parseXMLPiperData import substitute_AutoEntities_with_singleEntity, create_PiperEntities_from_autoSet, store_autoSet_ids
import dynaTranslationFunction as dynaTrasl
import chooseYourFolderAndFile as chooser
import dataClasses
import LSTCFileMetadata as LSTC

#Selection of the files
file_path = chooser.choose_file("Select the Piper XML file to parse", [("XML files", "*.xml"), ("All files", "*.*")])
output_folder = chooser.choose_folder("Select the output folder for the parsed file")
keyword_part_set_file = chooser.choose_file("Select the keyword file containing the set of parts:",[("keyword files", "*.k*"), ("All files", "*.*")])
keyword_coordinate_sys_file = chooser.choose_file("Select the keyword file containing the coordinate systems:",[("keyword files", "*.k*"), ("All files", "*.*")])
# Collecting the set of parts in LS-Dyna keyword file
PartSetsCards = dynaTrasl.read_keywords(keyword_part_set_file)
CoordsCards = dynaTrasl.read_keywords(keyword_coordinate_sys_file)
PartSets = dynaTrasl.get_dyna_set_part_list(PartSetsCards)
frames, history_ids = dynaTrasl.get_dyna_coordinates_list(CoordsCards)

# Collect the Piper entities
landmarks = parse_landmarks_lxml(file_path)
joints = parse_joints(file_path)
entitiesFromPiper = parse_entities(file_path)

#Elaboration of Piper entities
AutoIDs = store_autoSet_ids(entitiesFromPiper)
PiperEntitiesAuto = create_PiperEntities_from_autoSet(AutoIDs, PartSets)
SkinEntities, EntitiesForJoints = substitute_AutoEntities_with_singleEntity(entitiesFromPiper, PiperEntitiesAuto)

limbs = LSTC.create_limbs(joints)
limbs = []
for joint in joints:
    actual_part = LSTC.extract_parts_for_current_joint(joint,PartSets)
    actual_limb = LSTC.build_lstc_limb_from_piper_joint(joint, actual_part)
    limbs.append(actual_limb)
print(limbs)