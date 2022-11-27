import sys
from pathlib import Path
import argparse
from typing import Tuple, List, Any, Dict

import nbformat as nbf
import questionary
from rich.console import Console


src_dir = Path(__file__).parent
sys.path.insert(0, str(src_dir))
sys.path.insert(0, str(src_dir / "nbpreview"))
from nbpreview.notebook import Notebook, _render_notebook  # type: ignore


def main() -> Tuple[Tuple[Notebook, ...], Tuple[str, ...], Path]:
    parsero = argparse.ArgumentParser()
    parsero.add_argument(
        "-f",
        "--infiles",
        help="Input notebooks",
        # type=str,
        nargs="*",
        required=True,
    )
    parsero.add_argument(
        "-o",
        "--outfile",
        help="Output notebook or python script template",
        type=str,
        required=True,
    )
    args = parsero.parse_args()
    if isinstance(args.infiles, str):
        input_list = [args.infiles]
    else:
        input_list = args.infiles

    input_nb_nodes: List[nbf.NotebookNode] = []
    input_nb_names: List[str] = []
    for in_fn in input_list:
        try:
            in_path = Path(in_fn)
            input_nb_nodes.append(nbf.read(in_path, as_version=4))
            input_nb_names.append(in_path.name.split(".")[0])
        except Exception as e:
            raise FileNotFoundError(f"Cannot read notebook: {in_fn}") from e

    for in_nb in input_nb_nodes:
        try:
            nbf.validate(in_nb)
        except Exception as e:
            raise ValueError("Invalid notebook: {in_nb}") from e

    input_notebooks: Tuple[Notebook, ...] = tuple(
        [Notebook(nb_node) for nb_node in input_nb_nodes]
    )
    input_names: Tuple[str, ...] = tuple(input_nb_names)

    out_path = Path(args.outfile)
    assert (
        out_path.parent.is_dir()
    ), f"Invalid location for output file: {out_path.parent}."
    ext = out_path.name.split(".")[1]
    assert ext in {
        "py",
        "ipynb",
    }, f"{ext} is in invalid extension. Choose either '.py' or '.ipynb'."

    return input_notebooks, input_names, out_path


def ask_for_cell(celdas: Dict[str, Any]) -> str:
    choose_nb = [f"Choose {nb}" for nb in celdas.keys()]
    next_nb = [f"Next {nb}" for nb in celdas.keys()]
    choices = ["Forward", "Backwards"] + next_nb + choose_nb + ["Done"]
    return questionary.select(
        "Select cell from notebook or move forward", choices=choices
    ).ask()


def show_cell(celda: nbf.NotebookNode, name: str) -> None:
    print("")
    print("========= ", end="\t")
    print(name, end="\t")
    print(" =========")
    tabla = _render_notebook(
        [celda],
        plain=False,
        unicode=True,
        hyperlinks=True,
        nerd_font=True,
        files=False,
        hide_hyperlink_hints=True,
        hide_output=False,
        theme="ansi_dark",
        language="python",
        images=True,
        image_drawing="braille",
        color=True,
        negative_space=True,
        relative_dir=None,
        characters=None,
    )

    console = Console()
    console.print(tabla)


def add_tags(notebook: nbf.NotebookNode, out_path: Path) -> None:

    start_tagging = questionary.select(
        "Do you want to add tags?", choices=["Yes", "No"]
    ).ask()
    if start_tagging == "Yes":
        answer = "core"
        for cell in notebook["cells"]:
            show_cell(cell, out_path.name)
            answer = questionary.text("tag for this cells", default=answer).ask()
            if "tags" in cell["metadata"]:
                cell["metadata"]["tags"] += [answer]
            else:
                cell["metadata"]["tags"] = [answer]
    else:
        return
