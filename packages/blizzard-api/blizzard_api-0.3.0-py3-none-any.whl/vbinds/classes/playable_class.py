
"""
vbinds - An interface for working with a playable class.
"""

# built-in
import os
from typing import List, Dict

# internal
from .engine import Engine
from .specialization import Specialization


class PlayableClass:
    """ An interface for working with class data. """

    def __init__(self, engine: Engine, class_id: int):
        """ Initialize a class from its numeric identity. """

        self.engine = engine

        # initialize base-class data
        self.data = engine.get_class(class_id)
        self.media = engine.get_class_media(class_id)
        assert self.data is not None
        assert self.media is not None
        self.icon = self.media["assets"][0]["value"]

        self.name = self.data["name"]
        self.to_serialize = {"name": self.name, "icon": self.icon}

        # initialize specialization data
        self.specs = {}
        for spec_idx_data in self.data["specializations"]:
            spec = Specialization(self.engine, spec_idx_data["id"])
            self.specs[spec_idx_data["name"].lower()] = spec

        self.to_serialize["specs"] = []
        for spec in self.specs.values():
            self.to_serialize["specs"].append(spec.to_serialize)

    def roles(self) -> List[str]:
        """ Get the list of roles this class can fulfill. """

        role_list = []
        for spec in self.specs.values():
            role = spec.role()
            if role not in role_list:
                role_list.append(role)
        return role_list

    def macros(self) -> Dict[str, List[str]]:
        """ Collect all of the talent macros for this class. """

        result: Dict[str, List[str]] = {}
        for spec in self.specs.values():
            result[spec.name] = []
            for macro in spec.macros.values():
                result[spec.name].append(macro)
        return result

    def __str__(self) -> str:
        """ Turn the class into a String for debugging. """

        assert self.data is not None
        border = "****************************************"
        name_border = "=" * len(self.name)
        lines = [border, name_border, self.name, name_border]
        for spec in self.specs.values():
            lines.append(str(spec))
        lines.append(border)
        return os.linesep.join(lines)


def get_classes(engine: Engine) -> Dict[str, PlayableClass]:
    """ Using the query engine, get a list of all playable-class objects. """

    classes = engine.get_classes()
    assert classes is not None

    class_objs = {}
    for class_idx_data in classes:
        class_data = PlayableClass(engine, class_idx_data["id"])
        class_objs[class_data.name.lower()] = class_data
    return class_objs
