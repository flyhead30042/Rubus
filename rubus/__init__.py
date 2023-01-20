import os
from typing import AnyStr, Union, IO, Dict, Hashable, Any
from pandas import DataFrame
from tabulate import tabulate
from rubus.load_gpx import Geogpx
import yaml
from pathlib import Path

ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent.absolute()
TRACKLOGS_DIR = os.path.join(ROOT_DIR, "tracklogs")
CONFIGURATIONS_DIR = os.path.join(ROOT_DIR, "configurations")
IMAGES_DIR = os.path.join(ROOT_DIR, "images")
RUBUS_DIR = os.path.join(ROOT_DIR, "rubus")

def display_df(pd: DataFrame):
    print(tabulate(pd, headers='keys', tablefmt='psql'))


def load_gpx(xml_or_fileobj_or_filename: Union[AnyStr, IO[str]]) -> Geogpx:
    return Geogpx().load(xml_or_fileobj_or_filename)


def load_config(fileobj_or_filename: Union[AnyStr, IO[str]]) -> Dict[Hashable, Any]:
    if hasattr(fileobj_or_filename, 'read') or hasattr(fileobj_or_filename, 'getvalue'):
        stream = fileobj_or_filename
    else:
        stream = open(fileobj_or_filename, "r", encoding="UTF-8")

    config: Dict[Hashable, Any] = yaml.load(stream, Loader=yaml.CLoader)
    return config


if __name__ == "__main__":
    print(ROOT_DIR)
