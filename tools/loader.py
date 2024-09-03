import os
from unstructured.partition.md import optional_decode

def load_markdowns(dir, exclude_list=None):
    if exclude_list is None:
        exclude_list = ["README.md", "SECURITY.md", "index.md"]

    files = _list_files(dir, exclude_list)
    docs = []
    for md in files:
         with open(md, encoding="utf8") as f:
            text = optional_decode(f.read())
            docs.append(text)
        # TODO: need test, this will output plain text
        # elements = partition_md(filename=md)
        # text = "\n\n".join([str(el) for el in elements])

    return "\n\n".join(docs)


def _list_files(start_path, exclude_list, suffix=".md"):
    file_list = []
    for root, dirs, files in os.walk(start_path):
        dirs[:] = [d for d in dirs if not d == '.git']
        
        for f in files:
            if f.endswith(suffix) and f not in exclude_list:
                file_list.append(os.path.join(root, f))

    return file_list

