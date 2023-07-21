from manimlib import *


class RightTriangle(Polygon):
    def __init__(self, a, b, angle=None, flip_axis=None, **kwargs):
        vertices = np.array([
            [0, 0, 0],
            [a, 0, 0],
            [a, b, 0]
        ])
        super().__init__(*vertices, **kwargs)
        if angle is not None:
            self.rotate(angle)
        if flip_axis is not None:
            self.flip(flip_axis)
        self.center()


class Angle(Arc):
    def __init__(self, A, O, B, radius=0.5, other_angle=False, other_start_angle=False, **kwargs):
        A = np.array(A)
        O = np.array(O)
        B = np.array(B)
        angle = angle_between_vectors(
            A - O,
            B - O
        )
        start_angle = angle_between_vectors(
            A - O,
            RIGHT
        )
        if other_start_angle:
            start_angle = TAU - start_angle
        if other_angle:
            angle = TAU - angle
        super().__init__(start_angle=start_angle, angle=angle, radius=radius, arc_center=O, **kwargs)


class RightAngle(Square):
    def __init__(self, A, O, size=0.5, **kwargs):
        A = np.array(A)
        O = np.array(O)
        start_angle = angle_between_vectors(
            A - O,
            RIGHT
        )
        super().__init__(side_length=size, **kwargs)
        self.move_to(O, aligned_edge=DL)
        self.rotate(start_angle, about_point=O)


# class VisualizacionTriangulo(InteractiveScene):
#     drag_to_pan = False

#     def setup(self):
#         super().setup()
#         self.a_text = TexText("Ajusta el valor de $a$").to_corner(UL)
#         self.a_slider = LinearNumberSlider(
#             3,
#             min_value=0.5,
#             max_value=FRAME_WIDTH - 1,
#             step=0.01
#         ).next_to(self.a_text, DOWN).to_edge(LEFT)
#         self.b_text = TexText("Ajusta el valor de $b$").next_to(self.a_slider, DOWN).to_edge(LEFT)
#         self.b_slider = LinearNumberSlider(
#             4,
#             min_value=0.5,
#             max_value=FRAME_HEIGHT - 1,
#             step=0.01
#         ).next_to(self.b_text, DOWN).to_edge(LEFT)
#         self.in_simulation = False
#         self.add(self.a_text, self.a_slider, self.b_text, self.b_slider)
    
#     def construct(self) -> None:
#         self.camera.use_window_fbo(False)
#         self.file_writer.begin_insert()

#         def update_tri():
#             mob = RightTriangle(
#                 a=self.a_slider.get_value(),
#                 b=self.b_slider.get_value(),
#                 color=RED
#             )
#             if self.in_simulation:
#                 self.states_to_save.append(self.get_state())
#             return mob

#         self.tri = always_redraw(update_tri)
#         A, B, C = self.tri.get_vertices()
#         angle = always_redraw(lambda: Angle(B, A, C, radius=0.5))
#         angle_label = always_redraw(lambda: TexText("$\\theta$").move_to(
#             Angle(B, A, C, radius=0.8).point_from_proportion(0.5)
#         ))
#         def var_func():
#             var = Tex("\\theta", "=", "0.00", "^\\circ").next_to(self.b_slider, DOWN).to_edge(LEFT)
#             dec = var.make_number_changable("0.00")
#             A, B, C = self.tri.get_vertices()
#             angle = angle_between_vectors(
#                 B - A,
#                 C - A
#             )
#             degrees = var[-1]
#             dec.set_value(angle * 180 / PI)
#             y = degrees.align_to(dec, UP).get_y()
#             degrees.next_to(dec, RIGHT, buff=0.05).set_y(y)
#             return var
#         self.var = always_redraw(var_func)
#         def sine_func():
#             sine = Tex("\\sen", "\\theta", "=", "0.00").next_to(self.var, DOWN).to_edge(LEFT)
#             dec = sine.make_number_changable("0.00")
#             A, B, C = self.tri.get_vertices()
#             angle = angle_between_vectors(
#                 B - A,
#                 C - A
#             )
#             dec.set_value(np.sin(angle))
#             return sine
#         self.sine = always_redraw(sine_func)
#         def cosine_func():
#             cosine = Tex("\\cos", "\\theta", "=", "0.00").next_to(self.sine, DOWN).to_edge(LEFT)
#             dec = cosine.make_number_changable("0.00")
#             A, B, C = self.tri.get_vertices()
#             angle = angle_between_vectors(
#                 B - A,
#                 C - A
#             )
#             dec.set_value(np.cos(angle))
#             return cosine
#         self.cosine = always_redraw(cosine_func)
#         def tangent_func():
#             tangent = Tex("\\tan", "\\theta", "=", "0.00").next_to(self.cosine, DOWN).to_edge(LEFT)
#             dec = tangent.make_number_changable("0.00")
#             A, B, C = self.tri.get_vertices()
#             angle = angle_between_vectors(
#                 B - A,
#                 C - A
#             )
#             dec.set_value(np.tan(angle))
#             return tangent
#         self.tangent = always_redraw(tangent_func)
        
#         self.play(ShowCreation(self.tri))
#         self.play(ShowCreation(angle), Write(angle_label))
#         self.play(FadeIn(VGroup(self.var, self.sine, self.cosine, self.tangent)))

#         self.states_to_save = []
#         self.in_simulation = True
#         self.embed(False)
#         self.in_simulation = False
#         self.get_final_part()
#         self.file_writer.end_insert()
#         self.camera.use_window_fbo(True)
#         raise EndScene()
    
#     def get_final_part(self):
#         for state in self.states_to_save:
#             self.restore_state(state)
#             self.wait(1 / self.camera.fps)


class VisualizacionCirculo(InteractiveScene):
    drag_to_pan = False

    def setup(self):
        self.states_to_save = []
        super().setup()
        self.theta_text = TexText("Ajusta el valor de $\\theta$").to_corner(UP, buff=0.1).to_edge(LEFT, buff=0.15)
        self.theta_slider = LinearNumberSlider(
            PI / 3,
            min_value=0,
            max_value=TAU,
            step=0.01
        ).next_to(self.theta_text, DOWN).to_edge(LEFT, buff=0.15)
        self.theta_var = Tex("\\theta", "=", "0.00").next_to(self.theta_slider, DOWN).to_edge(LEFT, buff=0.15)
        dec = self.theta_var.make_number_changable("0.00")
        dec.set_value(self.theta_slider.get_value())
        dec.add_updater(lambda m: m.set_value(self.theta_slider.get_value()))
        self.in_simulation = False
        self.panel = Group(self.theta_text, self.theta_slider, self.theta_var)
        self.panel.add_to_back(SurroundingRectangle(self.panel, color=WHITE).set_fill(BLACK, opacity=1) \
                               .round_corners(0.1))
        self.add(self.panel)
    
    def construct(self) -> None:
        def scene_updater(mob, dt):
            if self.in_simulation:
                self.states_to_save.append(self.get_state())
        
        self.in_simulation = True

        self.add(Mobject().add_updater(scene_updater))
        self.number_plane = NumberPlane(
            x_range=[-32, 32, 1],
            y_range=[-16, 16, 1],
            width=64,
            height=32,
            background_line_style={
                "stroke_color": GREY,
                "stroke_width": 2,
                "stroke_opacity": 0.5
            }
        )
        self.circle = ImplicitFunction(lambda x, y: x ** 2 + y ** 2 - 1).scale(2)
        self.circle.set_color(RED)
        self.circle_label = Tex("x^2 + y^2 = 1", font_size=60).to_edge(UP, buff=0.15)
        self.circle_label_rect = SurroundingRectangle(self.circle_label, color=WHITE).set_fill(BLACK, opacity=1) \
                                    .round_corners(0.1)
        self.circle_label_g = VGroup(self.circle_label_rect, self.circle_label).fix_in_frame()
        self.dot = always_redraw(lambda: Dot(2 * RIGHT).rotate(self.theta_slider.get_value(), about_point=ORIGIN))
        self.angle = always_redraw(lambda: Angle(
            RIGHT,
            ORIGIN,
            self.dot.get_center(),
            other_angle=self.theta_slider.get_value() > PI,
            radius=0.5
        ))
        self.angle_label = always_redraw(lambda: TexText("$\\theta$").move_to(
            Angle(
                RIGHT,
                ORIGIN,
                self.dot.get_center(),
                other_angle=self.theta_slider.get_value() > PI,
                radius=0.8
            ).point_from_proportion(0.5)
        ))
        self.line = always_redraw(lambda: Line(
            self.number_plane.get_origin(),
            self.dot.get_center()
        ))
        self.circle_g = VGroup(self.circle, self.angle, self.line, self.dot, self.angle_label)
        self.bring_to_back(self.number_plane, self.circle_label_g, self.panel)
        self.play(Write(self.circle_label_g))
        self.bring_to_back(self.number_plane, self.circle_g, self.circle_label_g, self.panel)
        self.play(Write(self.circle_g))
        self.embed(False)
        self.in_simulation = False
        self.camera.use_window_fbo(False)
        self.file_writer.begin_insert()
        self.get_final_part()
        self.file_writer.end_insert()
        self.camera.use_window_fbo(True)
        raise EndScene()

    def get_final_part(self):
        for state in self.states_to_save:
            self.restore_state(state)
            self.wait(1 / self.camera.fps)
    
    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if chr(symbol) == "1":
            self.draw_sine()
        elif chr(symbol) == "2":
            self.draw_cosine()
        elif chr(symbol) == "3":
            self.draw_sine_and_cosine()
        super().on_key_press(symbol, modifiers)
    
    def draw_sine(self):
        self.play(self.theta_slider.animate.set_value(0))
        self.sine = VMobject(color=YELLOW).set_points(ORIGIN)
        self.line = always_redraw(lambda: DashedLine(
            self.dot.get_center(),
            self.sine.get_end()
        ))
        def draw_sine(m):
            m.add_points_as_corners([
                2 * self.theta_slider.get_value() * RIGHT + self.dot.get_y() * UP
            ])
        self.bring_to_back(self.number_plane, self.circle_g, self.sine, self.line, self.circle_label_g, self.panel)
        self.sine.add_updater(draw_sine)
        self.camera.frame.save_state()
        self.play(
            self.theta_slider.animate(run_time=7).set_value(TAU),
            self.camera.frame.animate(run_time=7).scale(2).move_to(2 * PI * RIGHT) # The scale is 2 and we want to move to the middle
        )
        self.play(Restore(self.camera.frame))
        self.sine.clear_updaters()
        self.play(FadeOut(self.sine), FadeOut(self.line))
    
    def draw_cosine(self):
        self.play(self.theta_slider.animate.set_value(0))
        self.cosine = VMobject(color=BLUE).set_points(2 * RIGHT)
        self.line = always_redraw(lambda: DashedLine(
            self.dot.get_center(),
            self.cosine.get_end()
        ))
        def draw_cosine(m):
            m.add_points_as_corners([
                2 * self.theta_slider.get_value() * DOWN + self.dot.get_x() * RIGHT
            ])
        self.cosine.add_updater(draw_cosine)
        self.bring_to_back(self.number_plane, self.circle_g, self.cosine, self.line, self.circle_label_g, self.panel)
        self.camera.frame.save_state()
        self.play(
            self.theta_slider.animate(run_time=7).set_value(TAU),
            self.camera.frame.animate(run_time=7).scale(2).move_to(2 * PI * DOWN) # The scale is 2 and we want to move to the middle
        )
        self.play(Restore(self.camera.frame))
        self.cosine.clear_updaters()
        self.play(FadeOut(self.cosine), FadeOut(self.line))
    
    def draw_sine_and_cosine(self):
        self.play(self.theta_slider.animate.set_value(0))
        self.sine = VMobject(color=YELLOW).set_points(ORIGIN)
        self.cosine = VMobject(color=BLUE).set_points(2 * RIGHT)
        self.sine_line = always_redraw(lambda: DashedLine(
            self.dot.get_center(),
            self.sine.get_end()
        ))
        self.cosine_line = always_redraw(lambda: DashedLine(
            self.dot.get_center(),
            self.cosine.get_end()
        ))
        def draw_sine(m):
            m.add_points_as_corners([
                2 * self.theta_slider.get_value() * RIGHT + self.dot.get_y() * UP
            ])
        def draw_cosine(m):
            m.add_points_as_corners([
                2 * self.theta_slider.get_value() * DOWN + self.dot.get_x() * RIGHT
            ])
        self.sine.add_updater(draw_sine)
        self.cosine.add_updater(draw_cosine)
        self.bring_to_back(
            self.number_plane,
            self.circle_g,
            self.sine,
            self.cosine,
            self.sine_line,
            self.cosine_line,
            self.circle_label_g,
            self.panel
        )
        self.camera.frame.save_state()
        self.play(
            self.theta_slider.animate(run_time=7).set_value(TAU),
            self.camera.frame.animate(run_time=7).scale(2).move_to(2 * PI * DR) # The scale is 2 and we want to move to the middle
        )
        self.play(Restore(self.camera.frame))
        self.sine.clear_updaters()
        self.cosine.clear_updaters()
        self.play(FadeOut(self.sine), FadeOut(self.cosine), FadeOut(self.sine_line), FadeOut(self.cosine_line))
