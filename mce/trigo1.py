from manim import *
from logo import Logo


MathTex.set_default(background_stroke_color=BLACK, background_stroke_width=4, background_stroke_opacity=1)
Brace.set_default(background_stroke_color=BLACK, background_stroke_width=4, background_stroke_opacity=1)


titulos = [
    "Semejanza de triángulos",
    "Primer Teorema de Tales",
    "Triángulos rectángulos",
    "Teorema de Pitágoras",
    "Razones trigonométricas",
    "Resolviendo el problema inicial"
]


class RightTriangle(Polygon):
    def __init__(self, a, b, **kwargs):
        v1 = ORIGIN
        v2 = RIGHT * a
        v3 = UP * b
        super().__init__(v1, v2, v3, **kwargs)
        self.center()


class HLine(Line):
    def __init__(self, length, **kwargs):
        super().__init__(LEFT * length / 2, RIGHT * length / 2, **kwargs)
        self.set_stroke(width=2, color=BLACK)


def get_label_for_side(poly: Polygon, idx1, idx2, label, direction, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER):
    p1 = poly.get_vertices()[idx1]
    p2 = poly.get_vertices()[idx2]
    mid = (p1 + p2) / 2
    return MathTex(label).next_to(mid, direction, buff=buff)


def get_angle(poly: Polygon, idx1, idx2, idx3, **kwargs):
    p1 = poly.get_vertices()[idx1]
    p2 = poly.get_vertices()[idx2]
    p3 = poly.get_vertices()[idx3]
    for p in (p1, p2, p3):
        p[-1] = 0
    line1, line2 = Line(p2, p1), Line(p2, p3)
    if kwargs.get("angle_class") is None:
        angle_class = Angle
    angle = angle_class(line1, line2, **kwargs)
    return angle


def get_right_angle(poly: Polygon, idx1, idx2, idx3, **kwargs):
    return get_angle(poly, idx1, idx2, idx3, angle_class=RightAngle, **kwargs)


def get_angle_label(angle: Angle, label):
    line1, line2 = angle.lines
    radius = angle.radius * 0.75
    point = Angle(line1, line2, radius=radius).get_midpoint()
    return MathTex(label).move_to(point)


class OneHundredSubs(Scene):
    def construct(self):
        thanks = Tex("¡Gracias por los", "100+ suscriptores!", "Se vienen cositas...")
        thanks[:2].scale(2)
        thanks[-1].scale(1.5)
        thanks.arrange(DOWN)
        thanks[1].set_color(YELLOW)
        thanks[2].set_color(PURE_RED)
        logo = Logo().to_corner(DR)
        self.add(thanks, logo)


class GrowHeight(Animation):
    def __init__(self, mobject: Mobject, rate_func=smooth, **kwargs):
        self.original_height = mobject.height
        super().__init__(mobject, rate_func=rate_func, **kwargs)
    
    def interpolate_mobject(self, alpha):
        if alpha < 0.01:
            alpha = 0.01
        self.mobject.set(height=self.original_height * self.rate_func(alpha))


class TituloProblemaInicial(Scene):
    def construct(self):
        problema, inicial = titulo = Tex("Problema", "Inicial", font_size=96).arrange(DOWN)
        copy = titulo.copy()
        problema.shift(10 * LEFT)
        inicial.shift(10 * RIGHT)
        self.play(
            ChangeSpeed(
                AnimationGroup(
                    problema.animate.shift(20 * RIGHT),
                    inicial.animate.shift(20 * LEFT)
                ),
                speedinfo={0.3: 1, 0.4: 0.1, 0.6: 0.1, 0.7: 1},
                rate_func=linear
            ),
            Succession(Wait(89 / 60), Circumscribe(copy, run_time=0.2))
        )


class ProblemaInicial(Scene):
    def construct(self):
        building = SVGMobject("building.svg").set_stroke(width=2, color=BLACK)
        building.set(height=6)
        building.to_edge(RIGHT)
        self.play(DrawBorderThenFill(building[0]))
        self.play(LaggedStartMap(FadeIn, building[1:], scale=2))
        self.wait()
        br = Brace(building, LEFT)
        br_text = br.get_tex("h")
        self.play(GrowHeight(br))
        self.play(Write(br_text))
        self.wait()
        person = SVGMobject("person.svg")
        person.set(height=1)
        person.align_to(building, DOWN).to_edge(LEFT)
        self.play(*[Create(mob) for mob in person])
        self.wait()
        person_height = MathTex(r"1.7\text{ m}").next_to(person, RIGHT)
        self.play(Write(person_height))
        self.wait()
        self.play(FadeOut(br, br_text))
        altura = Tex("Altura: $h$").next_to(building, UP)
        tri = RightTriangle(
            (building.get_left()[0] * RIGHT + person.get_top()[1] * UP - person.get_top())[0],
            (building.get_corner(UL) - (building.get_left()[0] * RIGHT + person.get_top()[1] * UP))[1],
            color=WHITE
        ).flip(UP).next_to(person.get_top(), UR, buff=0)
        dashed = DashedVMobject(tri, num_dashes=100, color=WHITE)
        label = get_label_for_side(tri, 0, 1, "x", DOWN)
        self.play(Write(altura), Create(dashed))
        self.wait()
        self.play(GrowFromEdge(label, UP))
        angle = get_angle(tri, 0, 1, 2, radius=2)
        angle_label = get_angle_label(angle, "30^{\\circ}}")
        self.play(Create(VGroup(angle, angle_label)))
        self.wait()


class Pregunta(Scene):
    def construct(self):
        pregunta = Tex("¿Cuánto mide $h$?").scale(2)
        self.play(ChangeSpeed(
            Succession(FadeIn(pregunta, scale=0.01), ScaleInPlace(pregunta, 1.5), FadeOut(pregunta, scale=10)),
            speedinfo={
                0.3: 1,
                0.4: 0.1,
                0.6: 0.1,
                0.7: 1
            },
            rate_func=linear
        ))


class TituloScene(Scene):
    n: int

    def construct(self):
        titulo = Tex(titulos[self.n], font_size=96).shift(UP)
        titulo = titulo[::-1]
        circs = VGroup(*[Circle(radius=0.1, color=BLUE_E, fill_opacity=0.5) for _ in range(len(titulos))])
        circs.arrange(RIGHT, buff=1)
        lines = VGroup(*[Line(0.4 * LEFT, 0.4 * RIGHT).move_to(circs[i:i+2]) for i in range(len(circs) - 1)])
        lines.set_stroke(width=2, color=BLUE_E)
        VGroup(circs, lines).to_edge(DOWN, buff=1)
        anims = []
        for i, circ in enumerate(circs):
            anims.append(Create(circ))
            if i < len(circs) - 1:
                anims.append(Create(lines[i]))
        self.play(
            LaggedStartMap(FadeIn, titulo[0], shift=RIGHT),
            LaggedStart(*anims, lag_ratio=0.5),
            run_time=2
        )
        self.play(circs[self.n].animate.set_color(YELLOW))
        self.wait()


class TituloSemejanza(TituloScene):
    n = 0
