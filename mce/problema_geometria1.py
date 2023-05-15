from manim import *
from logo import Logo
from right_triangle import RightTriangle
from equal_sides import EqualSidesMark


MathTex.set_default(background_stroke_width=1, background_stroke_opacity=1, background_stroke_color=WHITE)


class Figure(VGroup):
    def __init__(self):
        eq_tri = Triangle(color=WHITE).scale_to_fit_width(2)
        tuples = ((0, 1), (1, 2), (0, 2))
        eq_tri_sides = VGroup(*[EqualSidesMark.from_polygon(2, eq_tri, i, j) for i, j in tuples])
        l1 = Line(ORIGIN, 2 * RIGHT).rotate(120 * DEGREES)
        l1.next_to(eq_tri.get_vertices()[2], DR, buff=0)
        l2 = Line(ORIGIN, RIGHT).rotate(np.arctan(3 / 5))
        l2.scale_to_fit_height(l1.height)
        l2.next_to(l1.get_start(), UR, buff=0)
        l3 = Line(l1.get_end(), l2.get_end())
        rt = RightTriangle(5, 3, color=WHITE).scale_to_fit_height(eq_tri.height)
        rt.rotate(-angle_of_vector(rt.get_vertices()[2] - rt.get_vertices()[1]))
        rt.next_to(l2.get_end(), UR, buff=0)
        right_ang = RightAngle(
            Line(rt.get_vertices()[0], rt.get_vertices()[1]),
            Line(rt.get_vertices()[0], rt.get_vertices()[2]),
            length=0.2
        )
        gamma = Angle(l1, l2, other_angle=True, radius=0.3)
        gamma_tex = MathTex("\\gamma", font_size=30).move_to(
            Angle(l1, l2, other_angle=True, radius=0.5).get_midpoint()
        )
        length_5_midpoint = (rt.get_vertices()[0] + rt.get_vertices()[1]) / 2
        length_5 = Tex("5", font_size=30).next_to(length_5_midpoint, UL, buff=0.1)
        length_3_midpoint = (rt.get_vertices()[0] + rt.get_vertices()[2]) / 2
        length_3 = Tex("3", font_size=30).next_to(length_3_midpoint, UR, buff=0.1)
        super().__init__(eq_tri, eq_tri_sides, l1, l2, l3, rt, right_ang, length_5, length_3, gamma, gamma_tex)
        self.gamma_tex = gamma_tex
        self.center()


class ElEnunciado(Scene):
    def construct(self):
        titulo = Tex("Considere la siguiente figura:", font_size=60)
        self.play(Write(titulo))
        self.wait(2)

        fig = Figure()
        self.play(titulo.animate.scale(0.7).next_to(fig, UP))
        self.play(Write(fig))
        self.wait()

        tex = MathTex("\\text{Encuentre }\\tan", "\\gamma", font_size=60).next_to(fig, DOWN)
        self.play(LaggedStart(
            LaggedStartMap(FadeIn, tex[0], shift=UP),
            ReplacementTransform(fig.gamma_tex.copy(), tex[1], path_arc=-PI / 2),
            lag_ratio=0.5
        ))
        self.wait()


class Solucion(MovingCameraScene):
    def construct(self):
        enunciado = VGroup(
            Tex("Considere la siguiente figura:", font_size=60),
            Figure(),
            MathTex("\\text{Encuentre }\\tan", "\\gamma", font_size=60)
        ).arrange(DOWN)
        self.add(enunciado)
        titulo_enun, fig, encuentre = enunciado
        eq_tri, eq_tri_sides, l1, l2, l3, rt, right_ang, length_5, length_3, gamma, gamma_tex = fig
        solucion = Tex("Solución", font_size=96).to_edge(UP)
        self.play(DrawBorderThenFill(solucion))
        self.wait()

        # Sabemos que los ángulos internos de un triángulo equilátero miden 60°
        angles = VGroup(
            Angle(
                Line(eq_tri.get_vertices()[0], eq_tri.get_vertices()[1]),
                Line(eq_tri.get_vertices()[0], eq_tri.get_vertices()[2]),
                radius=0.5
            ),
            Angle(
                Line(eq_tri.get_vertices()[1], eq_tri.get_vertices()[2]),
                Line(eq_tri.get_vertices()[1], eq_tri.get_vertices()[0]),
                radius=0.5
            ),
            Angle(
                Line(eq_tri.get_vertices()[2], eq_tri.get_vertices()[0]),
                Line(eq_tri.get_vertices()[2], eq_tri.get_vertices()[1]),
                radius=0.5
            )
        )
        angle60_1, angle60_2, angle60_3 = angles
        angle60_1_tex = MathTex("60^\\circ", font_size=30).move_to(
            Angle(
                Line(eq_tri.get_vertices()[0], eq_tri.get_vertices()[1]),
                Line(eq_tri.get_vertices()[0], eq_tri.get_vertices()[2]),
                radius=0.7
            ).get_midpoint()
        )
        angle60_2_tex = angle60_1_tex.copy().move_to(
            Angle(
                Line(eq_tri.get_vertices()[1], eq_tri.get_vertices()[2]),
                Line(eq_tri.get_vertices()[1], eq_tri.get_vertices()[0]),
                radius=0.8
            ).get_midpoint()
        )
        angle60_3_tex = angle60_1_tex.copy().move_to(
            Angle(
                Line(eq_tri.get_vertices()[2], eq_tri.get_vertices()[0]),
                Line(eq_tri.get_vertices()[2], eq_tri.get_vertices()[1]),
                radius=0.7
            ).get_midpoint()
        )
        self.play(
            LaggedStart(
                LaggedStartMap(Create, angles, lag_ratio=0.3),
                Write(VGroup(angle60_1_tex, angle60_2_tex, angle60_3_tex)),
                lag_ratio=0.5
            )
        )
        self.wait()
        self.play(Uncreate(eq_tri_sides))
        self.wait()

        angle60_op = Angle(
            Line(l1.get_end(), l2.get_start()),
            Line(l1.get_end(), l3.get_end()),
            radius=0.5
        )
        angle60_op_tex = MathTex("60^\\circ", font_size=30).move_to(
            Angle(
                Line(l1.get_end(), l2.get_start()),
                Line(l1.get_end(), l3.get_end()),
                radius=0.8
            ).get_midpoint()
        )
        self.play(LaggedStart(Create(angle60_op), Write(angle60_op_tex), lag_ratio=0.5))
        self.wait()

        angle_theta = Angle(
            Line(rt.get_vertices()[1], rt.get_vertices()[2]),
            Line(rt.get_vertices()[1], rt.get_vertices()[0]),
            radius=0.5
        )
        theta = MathTex("\\theta", font_size=30).move_to(
            Angle(
                Line(rt.get_vertices()[1], rt.get_vertices()[2]),
                Line(rt.get_vertices()[1], rt.get_vertices()[0]),
                radius=0.7
            ).get_midpoint()
        )
        self.play(LaggedStart(Create(angle_theta), Write(theta), lag_ratio=0.5))
        self.wait()

        angle_theta_op = Angle(
            Line(l2.get_end(), l1.get_end()),
            Line(l2.get_end(), l2.get_start()),
            radius=0.5
        )
        theta_op = MathTex("\\theta", font_size=30).move_to(
            Angle(
                Line(l2.get_end(), l1.get_end()),
                Line(l2.get_end(), l2.get_start()),
                radius=0.7
            ).get_midpoint()
        )
        self.play(LaggedStart(Create(angle_theta_op), Write(theta_op), lag_ratio=0.5))
        self.wait()

        ang_ninety_minus_theta = Angle(
            Line(rt.get_vertices()[2], rt.get_vertices()[0]),
            Line(rt.get_vertices()[2], rt.get_vertices()[1]),
            radius=0.5
        )

        self.play(self.camera.frame.animate.shift(2 * DOWN))
        eq = MathTex("\\gamma", "+", "60^\\circ", "+", "\\theta", "=", "180^\\circ")
        eq.to_edge(DOWN, buff=0)
        eq.shift(0.5 * DOWN)
        self.play(TransformMatchingTex(
            VGroup(gamma_tex, angle60_op_tex, theta_op).copy(),
            eq,
            path_arc=-PI / 2
        ))
        self.wait()

        eq2 = MathTex("\\gamma", "=", "180^\\circ", "-", "60^\\circ", "-", "\\theta")
        eq2.move_to(eq)
        self.play(TransformMatchingTex(eq, eq2, key_map={"+": "-"}))
        self.wait()

        eq3 = MathTex("\\gamma", "=", "120^\\circ", "-", "\\theta")
        eq3.move_to(eq2)
        one_hundred_80 = eq2[2]
        minus = eq2[3]
        sixty = eq2[4]
        one_hundred_20 = eq3[2]
        eq2.remove(one_hundred_80, minus, sixty)
        eq3.remove(one_hundred_20)
        self.play(*[item.animate.replace(item2) for item, item2 in zip(eq2, eq3)], ReplacementTransform(VGroup(one_hundred_80, minus, sixty), one_hundred_20))
        self.wait()
        eq3.remove(*eq3.submobjects)
        eq3.add(*eq2.submobjects[:-2], one_hundred_20, *eq2.submobjects[-2:])
        self.play(eq3.animate.next_to(encuentre, DOWN))
        self.wait()

        rt_copy = rt.copy()
        rt_measures = VGroup(length_5, length_3, theta, angle_theta, right_ang).copy()
        vg = VGroup(rt_copy, rt_measures)
        self.play(vg.animate(path_arc=-PI).next_to(eq3, DOWN))
        self.wait()

        right_arrow = MathTex("\\Rightarrow").set_y(vg.get_y())
        self.play(vg.animate.next_to(right_arrow, LEFT))
        self.play(FadeIn(right_arrow, scale=2))
        tan_theta = MathTex("\\tan", "\\theta", "=", "{3", "\\over", "5}").next_to(right_arrow, RIGHT)
        self.play(Write(tan_theta))
        self.wait()

        self.play(
            FadeOut(vg),
            FadeOut(right_arrow),
            tan_theta.animate.set_x(0)
        )
        self.wait()

        tan_gamma = MathTex("\\tan", "\\gamma", "=", "\\tan", "(", "120^\\circ", "-", "\\theta", ")")
        tan_gamma.move_to(eq3)
        self.play(TransformMatchingTex(eq3, tan_gamma))
        self.wait()

        apply_difference_identity = MathTex(
            "\\tan", "\\gamma", "=", "{\\tan", "120^\\circ", "-",
            "\\tan", "\\theta", "\\over", "1", "+", "\\tan", "120^\\circ",
            "\\tan", "\\theta}"
        )
        apply_difference_identity.move_to(tan_gamma)
        self.play(TransformMatchingTex(tan_gamma, apply_difference_identity, transform_mismatches=True))
        self.wait()

        replace_values = MathTex(
            "\\tan", "\\gamma", "=", "{-", "\\sqrt{3}", "-", "{3", "\\over", "5}", "\\over",
            "1", "-", "\\sqrt{3}", "\\cdot", "{3", "\\over", "5}}"
        )
        self.play(VGroup(apply_difference_identity, tan_theta).animate.shift(0.5 * DOWN))
        replace_values.move_to(apply_difference_identity)
        self.play(TransformMatchingTex(
            apply_difference_identity,
            replace_values,
            transform_mismatches=True
        ))
        self.wait()
        
        amplify_by_minus_5 = MathTex(
            "\\tan", "\\gamma", "=", "{5\\sqrt{3}", "+", "3", "\\over", "3", "\\sqrt{3}", "-", "5}"
        )
        amplify_by_minus_5.move_to(replace_values)
        self.play(TransformMatchingTex(
            replace_values,
            amplify_by_minus_5,
            transform_mismatches=True
        ))
        self.wait()

        rationalize = MathTex(
            "\\tan", "\\gamma", "=", "{(", "5", "\\sqrt{3}", "+", "3", ")", "(", "3", "\\sqrt{3}", "+", "5)",
            "\\over", "(", "3", "\\sqrt{3}", "-", "5", ")", "(", "3", "\\sqrt{3}", "+", "5", ")}"
        )
        rationalize.move_to(amplify_by_minus_5)
        self.play(TransformMatchingTex(
            amplify_by_minus_5,
            rationalize,
            transform_mismatches=True
        ))
        self.wait()

        distributed = MathTex(
            "\\tan", "\\gamma", "=", "{60", "+", "34", "\\sqrt{3}", "\\over", "2}"
        )
        distributed.move_to(rationalize)
        self.play(TransformMatchingTex(
            rationalize,
            distributed,
            transform_mismatches=True
        ))
        self.wait()

        final_result = MathTex(
            "\\tan", "\\gamma", "=", "30", "+", "17", "\\sqrt{3}"
        )
        final_result.move_to(distributed)
        self.play(TransformMatchingTex(
            distributed,
            final_result,
            transform_mismatches=True
        ))
        self.wait()

        self.play(Circumscribe(final_result))
        self.wait()

        self.play(self.camera.frame.animate.shift(2 * UP))
        self.wait()


class TangentOfDifference(Scene):
    def construct(self):
        tan_of_difference = MathTex(
            "\\tan", "(", "\\alpha", "-", "\\beta", ")",
            "=", "{\\tan", "\\alpha", "-", "\\tan", "\\beta", "\\over", "1", "+", "\\tan", "\\alpha", "\\tan", "\\beta}"
        ).set_color_by_gradient(BLUE, GREEN)
        self.play(LaggedStartMap(FadeIn, tan_of_difference, shift=UP))
        self.wait()
        self.play(LaggedStartMap(FadeOut, tan_of_difference, shift=DOWN))


class TangentOf120Degrees(Scene):
    def construct(self):
        tan_of_120 = MathTex("\\tan", "120^\\circ", "=", "-\\sqrt{3}").set_color_by_gradient(BLUE, GREEN)
        self.play(LaggedStartMap(FadeIn, tan_of_120, shift=UP))
        self.wait()
        self.play(LaggedStartMap(FadeOut, tan_of_120, shift=DOWN))


class ArrowAnimation(Scene):
    def construct(self):
        arr = CurvedArrow(ORIGIN, 2 * RIGHT, angle=PI / 4)
        self.play(Create(arr))
        self.wait()
        self.play(FadeOut(arr))


class Thumbnail(Scene):
    def construct(self):
        geometria = Tex("\\textbf{Geometría}", font_size=96).to_edge(UP)
        fig = Figure()
        tan_gamma_question = MathTex("\\text{¿}", "\\tan", "\\gamma", "\\text{?}").scale(2).to_edge(DOWN)
        tan_gamma_question.set_color_by_gradient(BLUE, GREEN)
        logo = Logo().to_corner(DR)
        self.add(geometria, fig, tan_gamma_question, logo)
