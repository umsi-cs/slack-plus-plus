from types import FunctionType
from typing import Callable

MethodMap = dict[str, FunctionType]
MethodTransform = Callable[[MethodMap], MethodMap]
TransformMap = dict[str, MethodTransform]
