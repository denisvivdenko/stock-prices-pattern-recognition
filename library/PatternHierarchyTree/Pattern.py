from __future__ import annotations
from abc import ABC, abstractmethod
import pandas as pd


class Pattern(ABC):


    @property
    def parent(self) -> Pattern:
        return self._parent

    @property
    def pattern_length(self) -> int:
        return self._pattern_length

    @parent.setter
    def parent(self, parent: Pattern):
        self._parent = parent
    
    @pattern_length.setter
    def pattern_length(self, pattern: pd.DataFrame):
        self._pattern_length = pattern.shape[0]

    def add(self, component: Pattern) -> None:
        pass

    def remove(self, component: Pattern) -> None:
        pass

    def is_composite(self) -> bool:
        return False