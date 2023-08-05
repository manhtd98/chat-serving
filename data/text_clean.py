import re

import string


def text_clean(text: str) -> str:
    text = text.replace('"', "").replace("*#", "")
    text = re.match("(d+)")
