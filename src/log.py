from datetime import datetime
from typing import List, Dict, Any, Tuple
import os

def write_file(account: str, content: str, day: datetime = datetime.today().date()):

    file_name = f"logs/{account}_{day}.txt"
    with open(file_name, 'a') as f:
        f.write(f"{content}\n")

def read_file(account: str, day: datetime = datetime.today().date()) -> Tuple[int, List[str]]:

    file_name: str = f"logs/{account}_{day}.txt"
    print(file_name)
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            data: str = f.read()
            # print(data)
        return _parse_data(data)
    else:
        return 0, []

def _parse_data(data: str) -> Tuple[int, List[str]]:
    items: list[str] = [item for item in data.split("\n") if len(item.strip()) > 0 ]
    items_listing: list[str] = []
    for item in items:
        part: list[str] = [i.strip() for i in item.split("##")]
        if len(part) > 2:
            items_listing.append(part[1])
    last_no: int = int(items[-1].split("##")[0].strip())

    return last_no, items_listing



