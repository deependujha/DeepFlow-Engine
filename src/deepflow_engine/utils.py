# credits: https://github.com/deependujha

import json
from typing import Any


def write_log(log_data: dict[str, Any], filename: str = "collisions_log.json") -> None:
    json_data = json.dumps(log_data, indent=4)
    with open(filename, "w") as f:
        f.write(json_data)
