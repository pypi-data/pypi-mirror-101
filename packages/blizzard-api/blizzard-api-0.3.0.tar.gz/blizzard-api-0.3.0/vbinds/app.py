
"""
vbinds - This package's command-line entry-point application.
"""

# built-in
import argparse
import os
import json

# internal
from vbinds.classes.icon_cache import IconCache
from vbinds.classes.engine import engine_from_output_root
from vbinds.classes.playable_class import get_classes


def entry(args: argparse.Namespace) -> int:
    """ Execute the requested task. """

    args.out_dir = os.path.abspath(args.out_dir)

    # initialize an icon cache and query engine
    icon_cache = IconCache(os.path.join(args.out_dir, "icons"))
    engine = engine_from_output_root(args.out_dir)

    icon_cache.get("spell_frost_frostshock")
    icon_cache.get("spell_nature_lightning")

    classes = get_classes(engine)
    for class_name, data in classes.items():
        filename = os.path.join(args.out_dir,
                                (class_name + ".json").replace(" ", "_"))
        with open(filename, "w") as outfile:
            indent = None if not args.indent else args.indent
            outfile.write(json.dumps(data.to_serialize, indent=indent))
        print(data)

    engine.save()
    return 0


def add_app_args(parser: argparse.ArgumentParser) -> None:
    """ Add application-specific arguments to the command-line parser. """

    parser.add_argument("-o", "--out-dir", default=os.getcwd(),
                        help="root directory for program outputs")
    parser.add_argument("-i", "--indent", default=0, type=int,
                        help="indent argument for json serialization")
