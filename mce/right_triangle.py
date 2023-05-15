from manim import Polygon, ORIGIN, RIGHT, UP


__all__ = ["RightTriangle"]


class RightTriangle(Polygon):
    def __init__(self, a, b, **kwargs):
        v1 = ORIGIN
        v2 = RIGHT * a
        v3 = UP * b
        super().__init__(v1, v2, v3, **kwargs)
        self.center()