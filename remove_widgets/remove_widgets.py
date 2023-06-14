from pathlib import Path
from glob import glob

import nbformat as nbf

for archivo in glob("**/*.ipynb", recursive=True):
    file_path = Path(archivo)
    print(file_path.name)
    with open(file_path, 'r') as f:
        nb = nbf.read(f, as_version=4)
    try:
        del nb['metadata']["widgets"]
    except KeyError:
        print(f"\t{file_path.name} does not have metadata")
        continue
    with open(file_path, 'w') as f:
        nbf.write(nb, f)
