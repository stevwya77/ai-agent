import os

def list_files(path):
    for root, _, files in os.walk(path):
        for file in files:
            print(os.path.join(root, file))

list_files(".")