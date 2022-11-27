import sys
from pathlib import Path
from typing import Any, Dict

import nbformat as nbf

src_dir = Path(__file__).parent
sys.path.insert(0, str(src_dir))
sys.path.insert(0, str(src_dir / "nbpreview"))
from nbpreview.notebook import Notebook, _render_notebook  # type: ignore
from nbpreview.component.content.output.result.drawing import ImageDrawing

import cli


def write_output_nb(out_notebook: nbf.NotebookNode, out_path: Path) -> None:
    ext = out_path.name.split(".")[1]
    if ext == "ipynb":
        try:
            if len(out_notebook["cells"]) > 0:
                nbf.write(out_notebook, out_path)
        except Exception as e:
            raise RuntimeError(f"Error when writing to {out_path}") from e
    elif ext == "py":
        raise NotImplementedError("sry")
    else:
        raise AssertionError("This cannot happen.")


def main() -> int:
    input_notebooks, input_names, out_path = cli.main()

    n = len(input_notebooks)
    indices: Dict[str, int] = dict.fromkeys(input_names, 0)
    out_notebook = nbf.v4.new_notebook()
    while True:
        in_celdas: Dict[str, Any] = {}
        for nb, name in zip(input_notebooks, input_names):
            try:
                celda = nb.cells[indices[name]]
                in_celdas[name] = celda
            except Exception as e:
                # done_notebooks.add(nb)
                continue
        if len(in_celdas) == 0:
            break
        print("")
        for name, celda in in_celdas.items():
            cli.show_cell(celda, name)

        answer = cli.ask_for_cell(in_celdas)
        choose_nb = {f"Choose {name}": name for name in in_celdas.keys()}
        next_nb = {f"Next {name}": name for name in in_celdas.keys()}
        if choose_cell_name := choose_nb.get(answer, ""):
            new_cell = in_celdas[choose_cell_name]
            new_cell["id"] = f"{choose_cell_name}_{indices[choose_cell_name]}"
            out_notebook["cells"].append(new_cell)
            indices[choose_cell_name] += 1
        elif advance_cell_name := next_nb.get(answer, ""):
            indices[advance_cell_name] += 1
        elif answer == "Forward":
            for name in indices.keys():
                indices[name] += 1
        elif answer == "Backwards":
            for name in indices.keys():
                indices[name] = max(0, indices[name] - 1)
        elif answer == "Done":
            break
        else:
            raise KeyboardInterrupt("bye")

    cli.add_tags(out_notebook, out_path)
    out_notebook["metadata"] = input_notebooks[0].notebook_node["metadata"]
    write_output_nb(out_notebook, out_path)

    return 0


if __name__ == "__main__":
    sys.exit(main())
