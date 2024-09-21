import os

from tools import *

import warnings

warnings.filterwarnings("ignore")

current_dir = os.path.dirname(os.path.realpath(__file__))
run_book_dir = os.path.join(current_dir, "..", "runbooks")


def list_files(path, file_extension):
    return [
        entry.path
        for entry in os.scandir(path)
        if entry.is_file() and entry.name.endswith(f".{file_extension}")
    ]


def embedding_files():
    all_files = list_files(run_book_dir, "md")
    documents = []
    i = 0
    for file in all_files:
        with open(file, "r") as f:
            content = f.read()
            title, desc = extract_title_and_description(content)
            documents.append((i, f"""Title: {title}\n Description: {desc}""", file))
            # documents.append((i, title, file))
            i = i + 1
    return documents


documents = embedding_files()

from txtai.embeddings import Embeddings

embeddings = Embeddings(
    path="sentence-transformers/all-MiniLM-L6-v2",
)
# export OMP_NUM_THREADS=1
embeddings.index(documents)

results = embeddings.search("why my cluster1's status is unknown", 5)
for item in results:
    file = documents[item[0]][2]
    print(item, file)
    # raw_content = ""
    # with open(file, "r") as f:
    #     raw_content = f.read()
    # print(raw_content)
