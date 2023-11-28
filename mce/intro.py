from manim import *
from logo import Logo


__all__ = ["Intro"]


class Intro(Scene):
    logo = Logo()

    def construct(self):
        logo = self.logo
        txt = Tex("MathLike")
        VGroup(logo, txt).arrange(DOWN)
        self.play(LaggedStart(SpinInFromNothing(
            logo, angle=PI), Write(txt), lag_ratio=0.5))
        self.wait()


class IntroWithoutText(Scene):
    logo = Logo()

    def construct(self):
        logo = self.logo
        self.play(SpinInFromNothing(logo, angle=PI))
        self.wait()
