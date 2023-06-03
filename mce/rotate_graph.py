from manim import *
from grid_axes import GridAxes


config.frame_width, config.frame_height = config.frame_height, config.frame_width
config.pixel_width, config.pixel_height = config.pixel_height, config.pixel_width
config.background_color = "#333333"


class HowToRotateShort(MovingCameraScene):
    def construct(self):
        ax = GridAxes(grid_kw={"stroke_opacity": 0.2})
        titulo = Tex("¿Cómo rotar una gráfica?").to_edge(UP)
        self.play(Create(ax, run_time=2), LaggedStartMap(FadeIn, titulo[0], shift=0.5*UP))
        self.wait()
        graph1 = ax.plot(lambda x: 1 / 10 * x**2, x_range=[-10, 0], color=RED).reverse_points()
        graph2 = ax.plot(lambda x: 1 / 10 * x**2, x_range=[0, 10], color=RED)
        self.play(Create(graph1), Create(graph2), run_time=1.5)
        self.wait()
        graph = VGroup(graph1, graph2)

        self.play(FadeOut(graph))
        dot = Dot(ax.c2p(4, 7), color=RED)
        self.play(Create(dot))
        frame: ScreenRectangle = self.camera.frame
        frame.save_state()
        self.play(frame.animate.scale(0.7))
        self.wait()
        line = Line(ax.c2p(0, 0), dot.get_center(), color=RED)
        l = Line(ORIGIN, RIGHT)
        ang = Angle(l, line, radius=0.7, other_angle=False, color=WHITE, stroke_width=2)
        measure = angle_between_vectors(l.get_end() - l.get_start(), line.get_end() - line.get_start())
        fill_mob = Sector(stroke_width=0, fill_opacity=1, fill_color=BLACK, inner_radius=0, outer_radius=0.7, angle=measure)
        theta = MathTex(r"\theta").scale(0.7).move_to(
            Angle(l, line, radius=0.5, other_angle=False).get_midpoint()
        )
        self.bring_to_back(ax, line)
        self.play(Create(line))
        self.wait()
        self.bring_to_back(ax, fill_mob, ang, line)
        self.play(Create(ang), FadeIn(fill_mob))
        self.play(Write(theta))
        self.wait()
        line_and_point = VGroup(line, dot)

        line_and_point2 = line_and_point.copy()
        self.play(Rotate(line_and_point2, angle=PI / 3, about_point=ax.c2p(0, 0)))
        self.wait()
        ang2 = Angle(line, line_and_point2[0], radius=0.7, other_angle=False, color=WHITE, stroke_width=2)
        alpha = MathTex(r"\alpha").scale(0.7).move_to(
            Angle(line, line_and_point2[0], radius=0.5, other_angle=False).get_midpoint()
        )
        measure2 = angle_between_vectors(line.get_end() - line.get_start(), line_and_point2[0].get_end() - line_and_point2[0].get_start())
        start_angle2 = angle_between_vectors(RIGHT, line.get_end() - line.get_start())
        fill_mob2 = Sector(stroke_width=0, fill_opacity=1, fill_color=BLACK, inner_radius=0, outer_radius=0.7, start_angle=start_angle2, angle=measure2)
        self.bring_to_back(ax, fill_mob, fill_mob2, ang, ang2, line, line_and_point2[0])
        self.play(FadeIn(fill_mob2), Create(ang2), Write(alpha))
        self.wait()

        p = MathTex("P(x,y)", color=RED, font_size=36).next_to(dot, UR, buff=0.1)
        q = MathTex("Q(x',y')", color=BLUE, font_size=36).next_to(line_and_point2[1], UL, buff=0.1)
        self.play(line_and_point2.animate.set_color(BLUE))
        self.play(Write(p), Write(q))
        self.wait()
        r = Tex(r"Longitud de $OP$ y $OQ$: $r$", font_size=36).next_to(ax, DOWN, buff=0.5)
        self.play(ReplacementTransform(VGroup(line_and_point, line_and_point2).copy(), r, path_arc=3 * PI / 4))
        self.wait()

        sys_of_eqs = VGroup(MathTex(
            r"x = r\cos\theta \\",
            r"y = r\sin\theta",
            font_size=36
        ))
        sys_of_eqs.add(Brace(sys_of_eqs, LEFT)).next_to(frame.get_top(), DOWN, buff=0.1)
        sys_of_eqs2 = VGroup(MathTex(
            r"""x' = r\cos(\theta+\alpha) \\
            y' = r\sin(\theta+\alpha)""",
            font_size=36
        ))
        sys_of_eqs2.add(Brace(sys_of_eqs2, LEFT)).next_to(sys_of_eqs, DOWN, buff=0.1)
        self.play(Write(sys_of_eqs))
        self.wait()
        self.play(Write(sys_of_eqs2))
        self.wait()
        sys_of_eqs2_solving = VGroup(MathTex(
            r"x' = ", r"r\cos\theta", r"\cos\alpha - ", r"r\sin\theta", r"\sin\alpha \\",
            r"y' = ", r"r\sin\theta", r"\cos\alpha+", r"r\cos\theta", r"\sin\alpha",
            font_size=36
        ))
        sys_of_eqs2_solving.add(Brace(sys_of_eqs2_solving, LEFT)).next_to(sys_of_eqs, DOWN, buff=0.1)
        self.play(FadeTransform(sys_of_eqs2, sys_of_eqs2_solving))
        self.wait()
        tex_to_color_map = {
            r"r\cos\theta": YELLOW,
            r"r\sin\theta": BLUE,
        }
        sys_of_eqs.save_state()
        self.play(sys_of_eqs[0].animate.set_color_by_tex_to_color_map(tex_to_color_map))
        self.play(sys_of_eqs2_solving[0].animate.set_color_by_tex_to_color_map(tex_to_color_map))
        self.wait()
        sys_of_eqs2_solving2 = VGroup(MathTex(
            r"x' = ", r"x", r"\cos\alpha - ", r"y", r"\sin\alpha \\",
            r"y' = ", r"y", r"\cos\alpha+", r"x", r"\sin\alpha",
            font_size=36
        ))
        sys_of_eqs2_solving2.add(Brace(sys_of_eqs2_solving2, LEFT)).next_to(sys_of_eqs, DOWN, buff=0.1)
        self.play(FadeTransform(sys_of_eqs2_solving, sys_of_eqs2_solving2), Restore(sys_of_eqs))
        self.wait()

        self.play(Circumscribe(sys_of_eqs2_solving2))
        self.wait()
        self.play(FadeOut(sys_of_eqs), Uncreate(VGroup(line_and_point, line_and_point2, ang, ang2, fill_mob, fill_mob2, alpha, theta, p, q)))
        self.play(Restore(frame))
        self.wait()

        self.play(Create(graph1), Create(graph2))
        self.wait()
        self.bring_to_back(ax, graph)
        self.play(graph.animate.apply_matrix([[np.cos(PI / 3), -np.sin(PI / 3)], [np.sin(PI / 3), np.cos(PI / 3)]]))
        self.wait(2)
