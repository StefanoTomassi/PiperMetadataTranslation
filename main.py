from parseXMLPiperData import parse_joints, parse_landmarks_lxml, parse_entities
import chooseYourFolderAndFile as chooser
import dataClasses

file_path = chooser.choose_file("Select the Piper XML file to parse", [("XML files", "*.xml"), ("All files", "*.*")])
output_folder = chooser.choose_folder("Select the output folder for the parsed file")
landmarks = parse_landmarks_lxml(file_path)
joints = parse_joints(file_path)
entities = parse_entities(file_path)
print(entities)