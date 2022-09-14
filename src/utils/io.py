import json

def read_josn(file_path: str) -> dict:
    """Reads a josn file and returns the dictionary
    """
    with open(file_path) as f:
        return json.load(f)

def read_file(file_path: str) -> str:
    """Reads a file and returns the content
    """
    with open(file_path) as f:
        return f.read()