from manim import *
from manim_studio import *
from logo import Logo, YouTubeLogo


template = TexTemplate(preamble=r"""
\usepackage[spanish]{babel}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{mlmodern}""".strip())
config.tex_template = template
Text.set_default(font="Roboto", weight=BOLD)
config.background_color = "#111111"


class SlideMaker(LiveScene):
    pass


class FirstSlide(Scene):
    def construct(self):
        slide = load_mobject("first_slide.pkl")
        self.add(slide)
