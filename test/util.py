from pathlib import Path
import os

def get_test_path(path):
    curdir = Path(__file__)
    resdir = os.path.join(curdir.parent, path)
    return resdir
