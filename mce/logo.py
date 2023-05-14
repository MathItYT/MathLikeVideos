from manim import VGroup, Circle, MathTex, WHITE


LOGO_COLOR = "#2484e3"


class Logo(VGroup):
    def __init__(self):
        circ = Circle(color=WHITE).set_fill(LOGO_COLOR, opacity=1)
        sigma = MathTex(r"\sum", color=WHITE, background_stroke_width=0)
        super().__init__(circ, sigma)
