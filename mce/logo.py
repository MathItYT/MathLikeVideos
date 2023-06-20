from manim import VGroup, Circle, MathTex, WHITE


LOGO_COLOR = "#2484e3"


class Logo(VGroup):
    def __init__(self, color=LOGO_COLOR, icon=None):
        if icon is None:
            icon = MathTex("\\sum")
        circ = Circle(color=WHITE).set_fill(color, opacity=1)
        super().__init__(circ, icon)
