import re
from typing import List

def parse_names(names_str) -> List[str]:
    # Multiple names
    if "," in names_str:
        # remove ","
        names_tokens: List[str] = names_str.split(",")
        
        # remove "and"
        names = [re.sub(r"\band\b", "", token) for token in names_tokens]

        names = [name.strip() for name in names]
    # Two names
    elif "and" in names_str and "," not in names_str:
        # remove "and"
        names: List[str] = names_str.split("and")
        names = [word.strip() for word in names]
    # One name
    else:
        names = [names_str]

    return names
