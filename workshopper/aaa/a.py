from pathlib import Path
from typing import List, Literal, Any, Union
import questionary
import nbpreview as nbp
import nbformat as nbf
from rich.console import Console
from rich.table import Table
from notebook import Notebook, _render_notebook

import enum
class LowerNameEnum(enum.Enum):
    """Enum base class that sets value to lowercase version of name."""

    def _generate_next_value_(  # type: ignore[override,misc]
        name: str,  # noqa: B902,N805
        start: int,
        count: int,
        last_values: List[Any],
    ) -> str:
        """Set member's values as their lowercase name."""
        return name.lower()
@enum.unique
class ImageDrawingEnum(str, LowerNameEnum):
    """Image drawing types."""

    BLOCK = enum.auto()
    CHARACTER = enum.auto()
    BRAILLE = enum.auto()
ImageDrawing = Union[ImageDrawingEnum, Literal["block", "character", "braille"]]


notebook_node = nbf.read(Path("/home/pbarletta/labo/22/workshopper/notebook_templates", "Lecture1_MDAnalysisBasics.ipynb"), as_version=4)
nbf.validate(notebook_node)

nba = Notebook(notebook_node)


tabla = _render_notebook([nba.cells[0]], plain=False, unicode=True, hyperlinks=True, nerd_font=True, files=False,
    hide_hyperlink_hints=True, hide_output=False, theme="ansi_dark", language="python", 
    images=False, image_drawing=ImageDrawing, color=True, negative_space=False,
    relative_dir=None, characters=None)

console = Console()
console.print(tabla)