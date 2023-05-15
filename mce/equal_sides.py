from manim import Polygon, VGroup, Line, LEFT, RIGHT, DOWN, PI, angle_of_vector
import numpy as np


__all__ = ["EqualSidesMark"]

class EqualSidesMark(VGroup):
    def __init__(self, n: int, v1: np.ndarray, v2: np.ndarray, length: float = 0.3, buff: float = 0.1, **kwargs):
        super().__init__()
        for _ in range(n):
            self.add(Line(length * LEFT / 2, length * RIGHT / 2, **kwargs))
        self.arrange(DOWN, buff)
        self.rotate(angle_of_vector(v2 - v1) - PI / 2)
        self.move_to((v1 + v2) / 2)
    
    @staticmethod
    def from_polygon(n: int, polygon: Polygon, idx1: int, idx2: int, **kwargs) -> "EqualSidesMark":
        v1, v2 = polygon.get_vertices()[idx1], polygon.get_vertices()[idx2]
        return EqualSidesMark(n, v1, v2, **kwargs)
