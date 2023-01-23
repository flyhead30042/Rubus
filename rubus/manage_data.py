import os
from datetime import datetime
from typing import Dict
import pandas as pd

DTFORMAT = '%Y/%m/%d %H:%M'


def dir_all(p) -> pd.DataFrame:
    def extract(type: str, dirpath: str, name: str) -> Dict:
        fullname = os.path.join(dirpath, name)
        state = os.stat(fullname)
        return {"type": type,
                "path": dirpath,
                "name": name,
                "full_name": fullname,
                "size": state.st_size,
                "last_updated": datetime.fromtimestamp(state.st_mtime).strftime(DTFORMAT)}

    data = list()
    for dirpath, dirnames, filenames in os.walk(p):
        for filename in filenames:
            data.append(extract("file", dirpath, filename))
        for dirname in dirnames:
            data.append(extract("dir", dirpath, dirname))

    df = pd.DataFrame(data, columns=["type", "path", "name", "full_name", "size", "last_updated"])
    return df