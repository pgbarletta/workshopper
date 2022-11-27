"""Jupyter notebook output data."""
from typing import Union

from component.content.output.error import Error
from component.content.output.result.result import Result
from component.content.output.stream import Stream

Output = Union[Result, Error, Stream]
