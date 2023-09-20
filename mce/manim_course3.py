from manim import *
from logo import Logo
from intro import Intro


config.background_color = "#ece6e2"
VMobject.set_default(color=BLACK)


class Thumbnail(Scene):
    def construct(self):
        title = Tex(r"\textbf{Curso de Manim}").scale(3).to_edge(UP)
        banner = ManimBanner(dark_theme=False)
        number = Tex(r"\textbf{2}").scale(3).to_corner(DL)
        logo = Logo().to_corner(DR)
        subtitulo = Tex(r"\textbf{Estructura y\\funcionamiento}").scale(
            1.25).to_edge(DOWN)
        self.add(title, banner, number, subtitulo, logo)


class Introduction(Intro):
    def construct(self):
        banner = ManimBanner(dark_theme=False)
        self.play(banner.create())
        self.play(banner.expand())
        self.wait()
        self.play(FadeOut(banner, scale=2))
        super().construct()
