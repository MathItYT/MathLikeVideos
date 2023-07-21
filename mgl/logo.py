from manimlib import *


__all__ = ["Logo", "YouTubeLogo", "LOGO_COLOR", "PURE_RED"]


LOGO_COLOR = "#2484e3"
PURE_RED = "#ff0000"


class Logo(Group):
    def __init__(self, color=LOGO_COLOR, icon=None):
        if icon is None:
            icon = Tex("\\sum")
        circ = Circle(stroke_color=WHITE).set_fill(color, opacity=1)
        super().__init__(circ, icon)
    
    def as_vgroup(self):
        return VGroup(*self.submobjects)


class YouTubeLogo(Logo):
    def __init__(self):
        youtube = SVGMobject("youtube.svg").scale(0.5)
        youtube[0].set_color(WHITE)
        youtube[1].set_color(PURE_RED)
        super().__init__(PURE_RED, youtube)


class IMOLogo(Logo):
    def __init__(self):
        imo = ImageMobject("imo.png").scale(0.25)
        super().__init__("#333333", imo)
    
    def as_vgroup(self):
        raise TypeError("IMOLogo can't be converted to VGroup")

