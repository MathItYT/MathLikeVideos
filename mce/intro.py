from manim import *
from logo import Logo


__all__ = ["Intro"]


class Intro(Scene):
    def construct(self):
        logo = Logo()
        txt = Tex("MathLike")
        VGroup(logo, txt).arrange(DOWN)
        self.play(LaggedStart(SpinInFromNothing(logo, angle=PI), Write(txt), lag_ratio=0.5))
        self.wait()


class IntroWithoutText(Scene):
    def construct(self):
        logo = Logo()
        self.play(SpinInFromNothing(logo, angle=PI))
        self.wait()
