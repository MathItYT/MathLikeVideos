from manim import *
from logo import Logo
from intro import Intro


config.background_color = "#ece6e2"
Text.set_default(color=BLACK)
MathTex.set_default(color=BLACK)


class Thumbnail(Scene):
    def construct(self):
        title = Tex(r"\textbf{Curso de Manim}").scale(3).to_edge(UP)
        banner = ManimBanner(dark_theme=False)
        number = Tex(r"\textbf{1}").scale(3).to_corner(DL)
        logo = Logo().to_corner(DR)
        subtitulo = Tex(r"\textbf{Configuración del curso}").scale(1.25).to_edge(DOWN)
        self.add(title, banner, number, subtitulo, logo)


class Configuracion(Scene):
    def construct(self):
        title = Tex("\\textbf{¿Qué necesito para hacer el curso?}").scale(1.25)
        title.to_edge(UP)
        self.play(LaggedStartMap(FadeIn, title[0], shift=UP))
        b_lst = BulletedList(
            "Tener en cuenta los requisitos.",
            "Tener instalado Manim.",
            "Tener instalado VSCode.",
            "Tener instalado Git.",
            "Tener una cuenta en GitHub.",
            "Tener una cuenta en YouTube.",
            "Tener una cuenta en Discord.",
            "Unirse al server de Discord."
        )
        b_lst.scale(0.8)

        for item in b_lst:
            item[1:].set_color_by_gradient(BLUE_E, GREEN_E)
            self.play(Create(item[0]))
            self.play(Write(item[1:]))
            self.wait()
        
        self.play(FadeOut(b_lst, shift=DOWN))


class Introduction(Intro):
    def construct(self):
        banner = ManimBanner(dark_theme=False)
        self.play(banner.create())
        self.play(banner.expand())
        self.wait()
        self.play(FadeOut(banner, scale=2))
        super().construct()
