import re

def clean_string(text: str) ->str:
    return re.sub(r'[^a-zA-Z0-9.]', '_', text)

# r'[^a-zA-Z0-9.]'  # Keeps letters, numbers, and dots (.)
# r'[^a-zA-Z0-9]'   # remove all nonAlphanumeric chuchu