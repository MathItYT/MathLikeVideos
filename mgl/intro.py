from manimlib import *
from mgl.logo import Logo


class Intro(InteractiveScene):
    def construct(self):
        logo = Logo().as_vgroup()
        txt = TexText("MathLike")
        VGroup(logo, txt).arrange(DOWN)
        self.play(LaggedStart(
            GrowFromCenter(logo, path_arc=PI / 2),
            Write(txt)
        ))
        self.wait()


class IntroWithoutText(InteractiveScene):
    def construct(self):
        logo = Logo()
        self.play(GrowFromCenter(logo, path_arc=PI / 2))
        self.wait()
