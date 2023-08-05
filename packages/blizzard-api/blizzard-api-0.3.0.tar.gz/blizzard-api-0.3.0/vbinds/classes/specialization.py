
"""
vbinds - An interface for working with a playable specializations.
"""

# built-in
import os
from typing import Optional

# internal
from .engine import Engine
from .talent import Talent


def level_to_index(level: int) -> int:
    """ From a talen row's 'level', get the one-indexed translation. """

    level_data = {
        15: 1,
        25: 2,
        30: 3,
        35: 4,
        40: 5,
        45: 6,
        50: 7,
    }
    return level_data[level]


def is_talent_active(talent_data: dict) -> bool:
    """ Determine if a talent is active or passive, based on the API data. """

    return talent_data["spell_tooltip"]["cast_time"].lower() != "passive"


def build_row_macro(row_idx: int, row_data: dict) -> Optional[str]:
    """
    For a given talent row, build a macro to arbitrate non-passive abilities
    if applicable.
    """

    val = None
    non_passives = []

    for idx, data in row_data.items():
        if is_talent_active(data["raw"]):
            non_passives.append((data["raw"]["talent"]["name"], idx))

    if len(non_passives) > 1:
        val = "#showtooltip{}/cast ".format(os.linesep)
        for ability in non_passives:
            val += "[talent:{}/{}] {}; ".format(row_idx, ability[1],
                                                ability[0])
        val = val.rstrip()

    return val


# pylint: disable=too-many-locals
class Specialization:
    """ An interface for working with spec data. """

    def __init__(self, engine: Engine, spec_id: int):
        """ Initialize spec data from its numeric identity. """

        self.engine = engine
        self.data = engine.get_spec(spec_id)
        assert self.data is not None

        # build the talent rows
        self.talent_rows = {}
        self.levels = {}
        for tier_data in self.data["talent_tiers"]:
            # store talents as one-indexed
            talent_row = {}
            for talent_data in tier_data["talents"]:
                ttip = talent_data["spell_tooltip"]
                f_str = "({}, {}) {}".format(talent_data["talent"]["name"],
                                             ttip["cast_time"],
                                             ttip["description"])
                talent_row[talent_data["column_index"] + 1] = {
                    "text": f_str,
                    "raw": talent_data
                }

            # save tiers as one-indexed
            index = level_to_index(tier_data["level"])
            self.talent_rows[index] = talent_row
            self.levels[index] = tier_data["level"]

        # store this spec's talent macros
        self.macros = {}
        for row_idx, row_data in self.talent_rows.items():
            macro = build_row_macro(row_idx, row_data)
            if macro is not None:
                self.macros[row_idx] = macro

        self.name = self.data["name"]

        # build a data structure for serialization
        media = engine.get_spec_media(spec_id)
        assert media is not None
        self.to_serialize = {
            "icon": media["assets"][0]["value"],
            "name": self.name,
            "role": self.data["role"]["name"],
        }
        self.to_serialize["talent_rows"] = []
        for row, data in self.talent_rows.items():
            rdata: dict = {
                "index": row,
                "level": self.levels[row],
                "macro": None,
            }
            if row in self.macros:
                rdata["macro"] = self.macros[row]
            rdata["talents"] = {}
            for talent_idx, talent_data in data.items():
                tdata = Talent(self.engine,
                               talent_data["raw"]["talent"]["id"]).to_serialize
                tdata["active"] = is_talent_active(talent_data["raw"])
                rdata["talents"][talent_idx] = tdata
            self.to_serialize["talent_rows"].append(rdata)

    def role(self) -> str:
        """
        Determine the role (i.e. 'Damage', 'Tank', 'Healer') for this spec.
        """

        assert self.data is not None
        return self.data["role"]["name"]

    def __str__(self) -> str:
        """ Turn the spec into a String for debugging. """

        assert self.data is not None
        title = "{} ({})".format(self.name, self.data["role"]["name"])
        name_border = "-" * len(title)
        lines = [name_border, title, name_border]

        # build the talent-tree "table"
        for row_idx, row_data in self.talent_rows.items():
            lines.append("{}:".format(row_idx))
            for talent_idx, talent_data in row_data.items():
                lines.append("    {}: {}".format(talent_idx,
                                                 talent_data["text"]))
            macro = build_row_macro(row_idx, row_data)
            if macro is not None:
                lines.append("macro:")
                lines.append(macro)

        return os.linesep.join(lines)
