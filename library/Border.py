from library.PriceMovementEnum import PriceMovement
from typing import List


class Border:


    def __init__(self, left_border: List[PriceMovement], right_border: List[PriceMovement]) -> None:
        self._left_border = left_border
        self._right_border = right_border

    def compare_borders(self, border) -> bool:
        if (border._left_border == self._left_border) &\
            (border._right_border == self._right_border):
            return True
        
        return False

