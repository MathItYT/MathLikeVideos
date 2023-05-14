from manim import *
from logo import Logo
from manim_course_utils import *
from intro import Intro


config.background_color = "#ece6e2"
Text.set_default(color=BLACK)
MathTex.set_default(color=BLACK)



class Thumbnail(Scene):
    def construct(self):
        title = Tex(r"\textbf{Curso de Manim}").scale(3).to_edge(UP)
        banner = ManimBanner(dark_theme=False)
        number = Tex(r"\textbf{0}").scale(3).to_corner(DL)
        logo = Logo().to_corner(DR)
        subtitulo = Tex(r"\textbf{La bienvenida}").scale(2).to_edge(DOWN)
        self.add(title, banner, number, subtitulo, logo)



class Introduction(Intro):
    def construct(self):
        banner = ManimBanner(dark_theme=False)
        self.play(banner.create())
        self.play(banner.expand())
        self.wait()
        self.play(FadeOut(banner, scale=2))
        super().construct()


class Requisitos(Scene):
    def construct(self):
        requisitos = Tex("\\textbf{Requisitos}").scale(2).to_edge(UP)
        self.play(DrawBorderThenFill(requisitos))
        self.wait()
        table = Table(
            [
                ["Programación", BulletedList(
                    "Python (intermedio, si es avanzado mejor)",
                    "Numpy (básico)",
                    "Manejo de librerías (intermedio si integrarás librerías externas, básico en general)",
                    "Manejo de clases (intermedio)",
                    "Manejo de funciones (avanzado)",
                    "Recursividad (opcional, pero recomendado)",
                    "Manejo de archivos (opcional, pero recomendado)",
                    "Manejo de excepciones (opcional, pero recomendado)",
                    "Manejo de decoradores (opcional, pero recomendado)",
                    "Lo requerido para tus proyectos"
                )],
                ["Matemáticas", BulletedList(
                    "Nociones de cálculo",
                    "Interpolación",
                    "Contenidos escolares",
                    "Matemáticas del diseño (opcional, pero recomendado)",
                    "Matemáticas de la animación (opcional, pero recomendado)",
                    "Lo requerido para tus proyectos"
                )],
                ["Otras áreas", BulletedList(
                    "Creatividad",
                    "Dibujo (opcional, pero recomendado)",
                    "Animación (opcional, pero recomendado)",
                    "Software de posproducción (opcional, pero recomendado)",
                    "Lo requerido para tus proyectos"
                )],
            ],
            element_to_mobject=lambda el: Tex(el) if isinstance(el, str) else el,
            arrange_in_grid_config={"cell_alignment": LEFT},
            line_config={"color": BLACK, "stroke_width": 1},
            h_buff=0.5,
            v_buff=0.5,
        ).scale(0.275).to_edge(DOWN, buff=0.2)
        for cell in table.get_columns()[1]:
            for item in cell.get_parts_by_tex("opcional, pero recomendado"):
                item.set_color_by_gradient(BLUE_E, GREEN_E)
        self.play(table.create())
        self.wait()


class Metodo(Scene):
    def construct(self):
        title = Tex("\\textbf{El método}").scale(2).to_edge(UP)
        self.play(LaggedStartMap(FadeIn, title[0], scale=2))
        self.wait()
        items = ["Proyectos", "Ejercicios", "Videos", "Documentación", "Comunidad"]
        items = [Tex(
            rf"\textbf{{{item}}}",
            background_stroke_color=BLACK,
            background_stroke_width=4,
            background_stroke_opacity=1
        ) for item in items]
        for item in items:
            item.scale(7)
            item.set_color_by_gradient(BLUE, GREEN)
            self.play(ChangeSpeed(
                Succession(
                    FadeIn(item, scale=5, rate_func=linear),
                    ScaleInPlace(item, 0.5, run_time=2, rate_func=linear),
                    FadeOut(item, scale=0.1, rate_func=linear)
                ),
                speedinfo={
                    0.3: 1,
                    0.2: 0.1,
                    0.8: 0.1,
                    1: 1
                },
                rate_func=linear
            ), run_time=2)
        self.wait()


class Proyecto(Scene):
    start: bool = False

    def construct(self):
        self.title = Tex("\\textbf{Proyectos}").scale(2).to_edge(UP)
        if self.start:
            self.play(Write(self.title))
        else:
            self.add(self.title)
        self.wait()


class GridAxes(Axes):
    def __init__(
        self,
        x_range=(-10, 10, 1),
        y_range=(-10, 10, 1),
        x_length=5,
        y_length=5,
        dashed_grid=False,
        grid_kw = None,
        tips=False,
        **kwargs
    ):
        super().__init__(x_range=x_range, y_range=y_range, x_length=x_length,  y_length=y_length, tips=tips, **kwargs)
        if grid_kw is None:
            grid_kw = dict()
        self.add(self.get_grid(dashed=dashed_grid, **grid_kw))

    def get_grid(self, dashed=False, **grid_kw):
        x_range, y_range = self.x_range, self.y_range
        x_min, x_max, x_step = x_range[0], x_range[1], x_range[2]
        y_min, y_max, y_step = y_range[0], y_range[1], y_range[2]
        x_ticks = np.arange(x_min, x_max + x_step, x_step)
        y_ticks = np.arange(y_min, y_max + y_step, y_step)

        grid = self.get_axes()
        line_class = {False: Line, True: DashedLine}[dashed]
        for x in x_ticks:
            grid.add(line_class(
                self.coords_to_point(x, y_min),
                self.coords_to_point(x, y_max),
                stroke_width=1,
                stroke_opacity=0.5,
                **grid_kw
            ))
        for y in y_ticks:
            grid.add(line_class(
                self.coords_to_point(x_min, y),
                self.coords_to_point(x_max, y),
                stroke_width=1,
                stroke_opacity=0.5,
                **grid_kw
            ))
        return grid


class Proyecto1(Proyecto, MovingCameraScene):
    start = True

    def construct(self):
        super().construct()
        ax = GridAxes().set_color(BLACK)
        ax.add_coordinates(font_size=14, color=BLACK, buff=0.125)
        self.play(Create(ax, run_time=2))
        self.wait()
        graph = ax.plot(lambda x: (1 / 2) ** x, x_range=(-np.log(10) / np.log(2), 10, 0.01), color=PURE_RED)
        self.play(Create(graph, run_time=2))
        dot = Dot(ax.i2gp(-3, graph), color=BLACK)
        self.play(Create(dot))
        self.wait()
        f_x = MathTex("f", "(", "x", ")", "=", "a^", "x").set_color_by_tex_to_color_map({"x": BLUE_E, "a": YELLOW_E}) \
            .to_corner(UL)
        a_question = MathTex("\\text{¿}", "a", "\\text{?}").set_color_by_tex_to_color_map({"a": YELLOW_E}) \
            .next_to(f_x, DOWN)
        rec = SurroundingRectangle(VGroup(f_x, a_question), color=BLACK, stroke_width=2, fill_opacity=0.5, corner_radius=0.2)
        self.play(DrawBorderThenFill(f_x))
        self.wait()
        self.play(Write(a_question))
        self.bring_to_back(rec)
        self.play(Write(rec))
        self.wait()
        self.play(Wiggle(VGroup(rec, f_x, a_question)))
        self.wait()

        h_line = ax.get_horizontal_line(dot.get_center(), color=BLACK, stroke_width=2)
        v_line = ax.get_vertical_line(dot.get_center(), color=BLACK, stroke_width=2)
        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.scale(0.75).move_to(dot.get_center()))
        self.bring_to_back(ax, graph, h_line, v_line)
        self.play(Create(h_line), Create(v_line))
        self.wait()
        point_tex = MathTex("(", "-3", ",", "8", ")", font_size=20, color=BLACK).set_background_stroke(color=BLACK, width=1)
        point_tex.next_to(dot, UP, buff=0.05)
        self.play(Write(point_tex))
        self.wait()

        f_minus_3 = MathTex("f", "(", "-3", ")", "=", "8")
        minus_3_f = f_minus_3[2]
        eight_f = f_minus_3[5]
        f_minus_3.next_to(self.title, UP)
        f_minus_3.remove(minus_3_f, eight_f)
        minus_3 = point_tex[1].copy()
        eight = point_tex[3].copy()
        self.play(minus_3.animate.replace(minus_3_f), eight.animate.replace(eight_f), FadeIn(f_minus_3))
        self.wait()
        a_to_the_minus_3 = MathTex("a^", "{-3}", "=", "8").next_to(self.title, UP)
        minus_3_a = a_to_the_minus_3[1]
        eight_a = a_to_the_minus_3[3]
        a_to_the_minus_3.remove(minus_3_a, eight_a)
        self.play(
            minus_3.animate.replace(minus_3_a),
            eight.animate.replace(eight_a),
            ReplacementTransform(f_minus_3, a_to_the_minus_3)
        )
        self.wait()
        a_to_the_3 = MathTex("a^", "3", "=", "{1", "\\over", "8}").next_to(self.title, UP)
        minus_3_a = a_to_the_3[1]
        eight_a = a_to_the_3[-1]
        a_to_the_3.remove(minus_3_a, eight_a)
        self.play(
            FadeOut(minus_3[0]),
            minus_3[1].animate.replace(minus_3_a),
            eight.animate.replace(eight_a),
            ReplacementTransform(a_to_the_minus_3, a_to_the_3)
        )
        minus_3.remove(minus_3[0])
        self.wait()
        a = MathTex("a", "=", "{1", "\\over", "2}").next_to(self.title, UP)
        eight_a = a[-1]
        a.remove(eight_a)
        self.play(
            FadeOut(minus_3),
            ReplacementTransform(eight, eight_a),
            ReplacementTransform(a_to_the_3, a)
        )
        a.add(eight_a)
        self.wait()
        self.play(Restore(self.camera.frame), a.animate.to_edge(DOWN, buff=0.15))
        self.play(Circumscribe(a, color=YELLOW_E))
        self.wait()


class YMuchoMas(Scene):
    def construct(self):
        y_mucho_mas = Tex("¡Y mucho más!").scale(3)
        self.play(Succession(
            FadeIn(y_mucho_mas, shift=3 * RIGHT, rate_func=linear),
            Wait(2),
            FadeOut(y_mucho_mas, shift=3 * RIGHT, rate_func=linear)
        ))
