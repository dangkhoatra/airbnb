import json
from typing import List, Dict, Any
import re
from typing import Tuple


def get_users_info() -> List[Dict[str, Any]]:
    with open('users.json', 'r') as f:
        data = json.load(f)
        return data
    

def parse_text_get_numbers(text: str) -> Tuple[int, int, int]:
    # Use regular expressions to extract numbers
    numbers = re.findall(r'\d+', text)
    
    # Convert the numbers to integers
    first_number = int(numbers[0])
    second_number = int(numbers[1])
    third_number = int(numbers[2])
    
    return first_number, second_number, third_number

def modify_text(text: str):
    text = text.strip()
    if text[-1] == '.':
        new_text = text[:-1]
    else:
        new_text = text + '.'
    return new_text

def parse_href_to_get_listingid(href: str) -> str:
    # url = "https://www.airbnb.com/hosting/listings/40362152/details"
    pattern = r"/(\d+)/details"
    match = re.search(pattern, href)

    if match:
        listing_id = match.group(1)
        return listing_id
    else:
        raise ValueError(f"This href can't contain any ListingID. Href: {href}")