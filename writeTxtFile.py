from dataclasses import dataclass
from typing import Tuple, List, Dict, Optional
from dataClasses import LSTCLimb


def _fmt_children_from_dict(
    limb_name: str,
    parent_children_dict: Dict[str, List[str]]
) -> str:
    children = parent_children_dict.get(limb_name, [])
    if not children:
        return "0"
    return ",\n      ".join(str(child) for child in children)


def _fmt_parent_from_dict(
    limb: LSTCLimb,
    children_parent_dict: Dict[str, List[str]]
) -> str:
    parents = children_parent_dict.get(limb.name, [])
    if not parents:
        return "0, 0"

    parent_name = parents[0]
    return f"{parent_name}, {limb.cps.node1}"


def _fmt_part(part_list: list) -> str:
    if not part_list:
        return "0"
    return ",\n".join(f"      {pid}" for pid in part_list)


def _unique_limbs_by_name(limbs: List[LSTCLimb]) -> List[LSTCLimb]:
    unique = {}
    for limb in limbs:
        if limb.name not in unique:
            unique[limb.name] = limb
    return list(unique.values())


def limb_to_tree_block(
    limb: LSTCLimb,
    parent_children_dict: Dict[str, List[str]],
    children_parent_dict: Dict[str, List[str]]
) -> str:
    children_str = _fmt_children_from_dict(limb.name, parent_children_dict)
    parent_str = _fmt_parent_from_dict(limb, children_parent_dict)

    return (
        f"  %{limb.name} {{\n"
        f"    %cps {{\n"
        f"      {limb.cps.node1}, 0, 1\n"
        f"    }}\n"
        f"    %lock {{ {limb.lock[0]}, {limb.lock[1]}, {limb.lock[2]} }}\n"
        f"    %lcid {{ {limb.lcid[0]}, {limb.lcid[1]}, {limb.lcid[2]} }}\n"
        f"    %part {{\n"
        f"      {_fmt_part(limb.part)}\n"
        f"    }}\n"
        f"    %children {{\n"
        f"      {children_str}\n"
        f"    }}\n"
        f"    %parent {{\n"
        f"      {parent_str}\n"
        f"    }}\n"
        f"  }}"
    )


def occupant_to_tree_text(
    occupant_name: str,
    limbs: List[LSTCLimb],
    parent_children_dict: Dict[str, List[str]],
    children_parent_dict: Dict[str, List[str]],
    h_point: Tuple[float, float, float] = (0.0, 0.0, 0.0),
    rotation: Tuple[float, float, float] = (0.0, 1.0, 0.0),
    vertical: Tuple[float, float, float] = (0.0, 0.0, 1.0),
) -> str:
    unique_limbs = _unique_limbs_by_name(limbs)

    limb_names = ",\n".join(f"    {limb.name}" for limb in unique_limbs)
    limb_blocks = "\n".join(
        limb_to_tree_block(limb, parent_children_dict, children_parent_dict)
        for limb in unique_limbs
    )

    return (
        "%occinfo\n"
        "%occupant {\n"
        f"  %name {occupant_name}\n"
        "  %limbs {\n"
        f"{limb_names}\n"
        "  }\n"
        "  %globals {\n"
        f"    %h_point {{ {h_point[0]}, {h_point[1]}, {h_point[2]} }}\n"
        f"    %rotation {{ {rotation[0]}, {rotation[1]}, {rotation[2]} }}\n"
        f"    %vertical {{ {vertical[0]}, {vertical[1]}, {vertical[2]} }}\n"
        "  }\n"
        f"{limb_blocks}\n"
        "}\n"
        "%endoccinfo\n"
    )


def write_tree_file(
    output_path: str,
    occupant_name: str,
    limbs: List[LSTCLimb],
    parent_children_dict: Dict[str, List[str]],
    children_parent_dict: Dict[str, List[str]],
    h_point: Tuple[float, float, float] = (0.0, 0.0, 0.0),
    rotation: Tuple[float, float, float] = (0.0, 1.0, 0.0),
    vertical: Tuple[float, float, float] = (0.0, 0.0, 1.0),
) -> None:
    text = occupant_to_tree_text(
        occupant_name=occupant_name,
        limbs=limbs,
        parent_children_dict=parent_children_dict,
        children_parent_dict=children_parent_dict,
        h_point=h_point,
        rotation=rotation,
        vertical=vertical,
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)