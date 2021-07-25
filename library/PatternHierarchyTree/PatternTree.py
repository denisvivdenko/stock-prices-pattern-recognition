from library.PatternHierarchyTree.Pattern import Pattern
from typing import List
import pandas as pd


class PatternTree(Pattern):


    def __init__(self, moving_average_pattern: pd.DataFrame, subpatterns: List[Pattern]=[]) -> None:
        self.moving_average_pattern: pd.DataFrame = moving_average_pattern
        self.pattern_length: int = self.moving_average_pattern
        self._subpatterns: List[Pattern] = subpatterns
        self.subpatterns_count: int = len(subpatterns)

    def __init__(self) -> None:
        self._subpatterns: List[Pattern] = []

    def add(self, component: Pattern) -> None:
        self._subpatterns.append(component)
        component.parent = self
        self.subpatterns_count += 1

    def remove(self, component: Pattern) -> None:
        self._subpatterns.remove(component)
        component.parent = None
        self.subpatterns_count -= 1

    def is_composite(self) -> bool:
        return True

    def get_subpatterns(self) -> List[Pattern]:
        return self._subpatterns