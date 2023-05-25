from manim import Polygon, MathTex, DEFAULT_MOBJECT_TO_MOBJECT_BUFFER, ORIGIN, RIGHT, UP


__all__ = ["RightTriangle", "get_label_for_side"]


class RightTriangle(Polygon):
    def __init__(self, a, b, **kwargs):
        v1 = ORIGIN
        v2 = RIGHT * a
        v3 = UP * b
        super().__init__(v1, v2, v3, **kwargs)
        self.center()


def get_label_for_side(poly: Polygon, idx1, idx2, label, direction, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER):
    p1 = poly.get_vertices()[idx1]
    p2 = poly.get_vertices()[idx2]
    mid = (p1 + p2) / 2
    return MathTex(label).next_to(mid, direction, buff=buff)
