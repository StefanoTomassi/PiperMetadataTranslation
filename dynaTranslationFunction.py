import re
from dataClasses import DynaPartSet, DynaCoordinateSys
def read_keywords(dir_file: str) -> dict:
    """Reads an LS-DYNA keyword file and returns a dictionary of keywords and their associated lines.
    Args:
        dir_file (str): Path to the LS-DYNA keyword file.
    Returns:
        dict: A dictionary where keys are keywords (without the leading '*') and values are lists of lines associated with each keyword."""

    file = open(dir_file, 'r')
    cards = {}
    counters = {}
    current_keyword = None
    for line in file:
        line = line.rstrip('\n\r')
        if line.startswith('*'):
            keyword_base = line
            counters[keyword_base] = counters.get(keyword_base, 0) + 1
            current_keyword = f"{keyword_base}_{counters[keyword_base]}"
            cards[current_keyword] = []
            continue
        if line.startswith('$'):
            continue
        if current_keyword is not None:
            cards[current_keyword].append(line)
    file.close()
    return cards

def get_dyna_set_part_list(cards):
    """
    Starting from the dyna card *SET_PART_LIST_TITLE, it provides a new 'PiperEntity' object
    with the following attribute:
    -PiperEntity.name: title of *SET_PART_LIST_TITLE
    -PiperEntity.id: ID of *SET_PART_LIST_TITLE
    -PiperEntity.keyword: *SET_PART_LIST_TITLE
    
    """
    PartSets = []
    for card in cards:
        if 'SET_PART_LIST_TITLE' in card:
            name = cards[card][0]
            id = cards[card][1].split()[0]
            part_ids = []
            for line in cards[card][2:]:
                part_ids.extend([id for id in re.findall(r'\d+', line)])
            PartSets.append(DynaPartSet(
                name = name,
                id = id,
                parts = part_ids)
            )

    return PartSets

def get_dyna_coordinates_list(cards):
    """
    From the cards, it pulls out the same structure of the function above...
    TO FINISH WITH THE DATABASE NODE ID
    """
    Frames = []
    History_ids = []
    for card in cards:
        if 'DEFINE_COORDINATE_NODES_TITLE' in card:
            name = cards[card][0]
            id = cards[card][1].split()[0]
            node = cards[card][1].split()[1]
            Frames.append(DynaCoordinateSys(
                name = name,
                id = id,
                node = node)
            )
        if 'DATABASE_HISTORY_NODE_ID' in card:
            m = re.match(r"\s*(\d+)(.*)", cards[card][0])
            id = int(m.group(1))
            name = m.group(2).strip()
            History_ids.append(DynaCoordinateSys(
                name = name,
                id = id,
                node = id)
            )
    return Frames, History_ids