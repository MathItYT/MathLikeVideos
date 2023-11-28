from manim import VGroup, Circle, MathTex, SVGMobject, WHITE, PURE_RED


LOGO_COLOR = "#2484e3"


class Logo(VGroup):
    def __init__(self, color=LOGO_COLOR, icon=None):
        if icon is None:
            icon = MathTex("\\sum", color=WHITE)
        circ = Circle(color=WHITE).set_fill(color, opacity=1)
        super().__init__(circ, icon)


class YouTubeLogo(Logo):
    def __init__(self):
        youtube = SVGMobject("youtube.svg").scale(0.5)
        youtube[0].set_color(WHITE)
        youtube[1].set_color(PURE_RED)
        super().__init__(PURE_RED, youtube)
