import os


def find(name, path, ext='.txt'):
    for root, dirs, files in os.walk(path):
        if name+ext in files:
            return os.path.join(root, name+ext)
