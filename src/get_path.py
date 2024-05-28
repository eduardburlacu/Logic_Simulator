"""Locate Definition Files in the Folder."""
import os
path = os.listdir(os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "def_files")))
print(path)
