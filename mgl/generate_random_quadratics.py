from manimlib import *
from mgl.azure_speech_scene import AzureSpeechScene
from mgl.logo import Logo, YouTubeLogo


class Fraction:
    def __init__(self, a, b, positive_wo_sign=False):
        assert b != 0, "Denominator cannot be zero"
        self.a = a
        self.b = b
        self.positive_wo_sign = positive_wo_sign
    
    @classmethod
    def from_float(cls, n: float, positive_wo_sign=False):
        if n == int(n):
            return cls(int(n), 1, positive_wo_sign=positive_wo_sign)
        return cls(*n.as_integer_ratio(), positive_wo_sign=positive_wo_sign)
    
    def __str__(self):
        if self.b == 1:
            if self.a >= 0 and self.positive_wo_sign:
                return f"{self.a}"
            if self.a >= 0:
                return f"+ {self.a}"
            return f"- {-self.a}"
        if self.a < 0 and self.b < 0:
            return "- {%d\\over %d}" % (-self.a, -self.b)
        if self.a < 0 or self.b < 0:
            return "- {%d\\over %d}" % (abs(self.a), abs(self.b))
        return "+ {%d\\over %d}" % (self.a, self.b)


def convert_number_to_fraction(n: float, positive_wo_sign=False):
    return str(Fraction.from_float(n, positive_wo_sign=positive_wo_sign))


def get_tex_string(a, b, c):
    a = convert_number_to_fraction(a, positive_wo_sign=True)
    b = convert_number_to_fraction(b)
    c = convert_number_to_fraction(c)
    if a == "1":
        a = ""
    elif a == "- 1":
        a = "-"
    if b == "+ 1":
        b = "+"
    elif b == "- 1":
        b = "-"
    elif b == "+ 0" and c != "+ 0":
        return f"{a}x^2{c}=0"
    elif b == "+ 0" and c == "+ 0":
        return f"{a}x^2=0"
    if c == "+ 0":
        return f"{a}x^2{b}x=0"
    return f"{a} x^2 {b} x {c} = 0"


def read_equation_espanol(tex_str: str):
    tex_str = tex_str.replace("=", "igual")
    tex_str = tex_str.replace("+", "más")
    tex_str = tex_str.replace("-", "menos")
    tex_str = tex_str.replace("x", "equis")
    tex_str = tex_str.replace("^2", "al cuadrado")
    return tex_str


class RandomScene(AzureSpeechScene):
    voice = "es-ES-DarioNeural"

    def construct(self) -> None:    
        self.mob_to_render = input()
        self.coefficients = map(int, input().split(","))
        self.ejercicio = TexText("\\textsc{Ejercicio}", font_size=192).to_edge(UP)
        titulo = Tex("\\text{¡Encuentra las soluciones}")
        titulo2 = Tex("x\\text{ de la siguiente ecuación!}", t2c={"x": YELLOW})
        self.titulo = VGroup(titulo, titulo2)
        self.titulo.arrange(DOWN)
        self.titulo.set_width(FRAME_WIDTH - 2 * MED_SMALL_BUFF)
        self.titulo.to_edge(DOWN)
        self.titulo = VGroup(*[sm for mob in self.titulo for sm in mob.submobjects])

        a, b, c = self.coefficients
        eq = get_tex_string(a, b, c)
        self.ecuacion = Tex(eq, font_size=96, t2c={"x": YELLOW})
        logo = Logo().as_vgroup().to_edge(RIGHT)
        yt_logo = YouTubeLogo().as_vgroup().to_edge(LEFT)
        self.logos = VGroup(logo, yt_logo)

        subtitulos = [
            ("Te propongo un reto", {"reto": YELLOW}),
            ("Resuelve esta ecuación", {"ecuación": YELLOW}),
            (self.ecuacion.tex_string, {"x": YELLOW}),
            ("¡Buena suerte!", {"suerte": YELLOW})
        ]

        to_speak = []
        subtitulos_mobs = []

        for subtitulo in subtitulos:
            if subtitulo[0] == self.ecuacion.tex_string:
                to_speak.append(read_equation_espanol(subtitulo[0]))
                subtitulos_mobs.append(self.ecuacion.copy())
                continue
            subtitulo_mob = TexText(subtitulo[0], font_size=96, t2c=subtitulo[1])
            to_speak.append(subtitulo[0])
            subtitulos_mobs.append(subtitulo_mob)

        self.subtitulos_group = VGroup(*subtitulos_mobs)

        mob_to_render = getattr(self, self.mob_to_render)

        if mob_to_render == self.titulo:
            self.play(Write(self.ejercicio))
            self.play(LaggedStartMap(FadeIn, self.titulo, scale=0.5))
            self.wait()
        elif mob_to_render == self.subtitulos_group:
            self.logos.to_edge(DOWN)
            self.play(GrowFromCenter(logo, path_arc=PI / 2), GrowFromCenter(yt_logo, path_arc=PI / 2))
            self.wait()
            for subtitulo_mob, subtitulo in zip(subtitulos_mobs, to_speak):
                self.speak(subtitulo)
                subtitulo_mob.set_width(min(
                    subtitulo_mob.get_width(),
                    logo.get_left()[0] - yt_logo.get_right()[0] - 2 * MED_SMALL_BUFF
                ))
                subtitulo_mob.to_edge(UP)
                self.add(subtitulo_mob)
                self.wait_until_current_audio_finished()
                self.remove(subtitulo_mob)
        elif mob_to_render == self.ecuacion:
            self.ecuacion.set_width(FRAME_WIDTH - 2 * MED_SMALL_BUFF)
            self.play(DrawBorderThenFill(self.ecuacion))
            self.wait()
    
    def interact(self):
        pass


print(get_tex_string(-7, -1, 5))
