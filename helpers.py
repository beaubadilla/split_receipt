import re

# Matches "100%", "0%", "99%", "51%", "51.5%", "18%", "18.213%", "0.5%", "1%"
PERCENTAGE_REGEX = re.compile(r"^[0-9]+\.?[0-9]+%$")

DECIMAL_REGEX = re.compile(r"^[0-9]+\.[0-9]+$")
DOLLAR_REGEX = re.compile(r"^\$[0-9]+\.?[0-9]*$")


def prompt_d(prompt: str) -> float:
    """Prompt for an input representing a decimal, but allow both decimal or percentage form

    0.18    => 0.18
    18%     => 0.18
    """
    accepted: bool = False
    val: float = None
    while not accepted:
        response = input(prompt)
        if DECIMAL_REGEX.match(response):
            val = float(response)
            accepted = True
        elif PERCENTAGE_REGEX.match(response):
            val, _ = response.split("%")
            val = float(val)
            accepted = True
        else:
            print(f"Invalid input. Acceptable formats: 18%, 18.0%, 0.18")

    return val
