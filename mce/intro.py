from manim import *
from mce.logo import Logo


__all__ = ["Intro"]


class Intro(Scene):
    def construct(self):
        logo = Logo()
        txt = Tex("MathLike")
        VGroup(logo, txt).arrange(DOWN)
        self.play(LaggedStart(SpinInFromNothing(logo, angle=PI), Write(txt), lag_ratio=0.5))
        self.wait()
