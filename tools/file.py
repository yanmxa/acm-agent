import os


def list_files(path, file_extension):
    return [
        entry.path
        for entry in os.scandir(path)
        if entry.is_file() and entry.name.endswith(f".{file_extension}")
    ]
