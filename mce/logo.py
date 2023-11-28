from manim import VGroup, Circle, MathTex, SVGMobject, WHITE, PURE_RED


LOGO_COLOR = "#2484e3"


class Logo(VGroup):
    def __init__(self, logo_color=None, white=None, icon=None):
        if logo_color is None:
            logo_color = LOGO_COLOR
        if white is None:
            white = WHITE
        if icon is None:
            icon = MathTex("\\sum", color=white)
        circ = Circle(color=white).set_fill(logo_color, opacity=1)
        super().__init__(circ, icon)


class YouTubeLogo(Logo):
    def __init__(self, white=None):
        if white is None:
            white = WHITE
        youtube = SVGMobject("youtube.svg").scale(0.5)
        youtube[0].set_color(white)
        youtube[1].set_color(PURE_RED)
        super().__init__(PURE_RED, white, youtube)
