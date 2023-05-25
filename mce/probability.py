from manim import *
from colour import Color
import random


config.background_color = "#333333"


class BlazeCard(VGroup):
    def __init__(self, n: int):
        assert n in range(15)
        if n == 0:
            color = WHITE
        elif n in range(1, 8):
            color = "#f9305b"
        else:
            color = "#252f38"
        sq = Square(fill_opacity=1, color=color).round_corners(0.2)
        txt = Text(str(n), color=BLACK if n == 0 else WHITE, font="Roboto", weight=BOLD, font_size=24)
        circ = Circle(radius=0.5, color=BLACK if n == 0 else WHITE, stroke_width=8)
        super().__init__(sq, circ, txt)


class BlazeScene(MovingCameraScene):
    def construct(self):
        self.camera: MovingCamera
        columns = 4
        rows = 10
        cards = VGroup()
        for _ in range(rows * columns):
            cards.add(BlazeCard(random.randint(0, 14)))
        cards.arrange_in_grid(rows, columns, buff=1)
        cards.to_edge(UP, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER)
        frame = self.camera.frame
        frame.save_state()
        frame.next_to(cards, DOWN).shift(config.frame_height * UP)
        cards.submobjects = cards.submobjects[::-1]
        self.play(
            LaggedStartMap(FadeIn, cards[:-1], scale=2, run_time=2, lag_ratio=0.05),
            Succession(Wait(0.6), Restore(frame, run_time=1.4))
        )
        self.wait()
        self.play(FadeIn(cards[-1], scale=2))
        self.wait()


class Ruleta(VGroup):
    def __init__(self, times: int = 3, saldo: float = 5000):
        super().__init__(
            *[BlazeCard(random.randint(0, 14)) for _ in range(times * 100)]
        )
        self[4].center()
        self[:3].arrange(RIGHT, buff=0.5).next_to(self[4], LEFT, buff=0.5)
        self[5:].arrange(RIGHT, buff=0.5).next_to(self[4], RIGHT, buff=0.5)
        self.saldo = saldo
        self.n = 4
    
    def apostar(self, scene: Scene, color: str, monto: float = 250):
        assert color in (WHITE, "#f9305b", "#252f38")
        assert monto <= self.saldo and monto >= 9.6
        color = Color(color).hex
        self.saldo -= monto
        giros = random.randint(20, 80)
        self.n += giros
        real_color = self[self.n][0].get_color().hex
        scene.play(self.animate.shift(giros * 2.5 * LEFT), run_time=7, rate_func=rush_from)
        scene.wait()
        if real_color == color:
            if color != WHITE:
                self.saldo += monto * 2
            else:
                self.saldo += monto * 14
        return self[self.n]


class Apostando(Scene):
    def construct(self):
        ruleta = Ruleta(3)
        saldo_txt = Text(f"Saldo: ${ruleta.saldo}", font="Roboto", font_size=24, color=WHITE)
        options = VGroup(BlazeCard(0), BlazeCard(5), BlazeCard(10))
        options.scale(0.5).arrange(RIGHT, buff=0.5).to_edge(DOWN)
        saldo_txt.to_corner(UR)
        self.add(ruleta, line := Line(2 * DOWN, 2 * UP, stroke_width=6))
        self.play(DrawBorderThenFill(saldo_txt), LaggedStartMap(FadeIn, options, scale=2, lag_ratio=0.2))
        colors = (WHITE, "#f9305b", "#252f38")
        montos = (250, 500, 500)
        for color, monto in zip(colors, montos):
            self.play(Transform(saldo_txt, Text(f"Saldo: ${ruleta.saldo - monto}", font="Roboto", font_size=24, color=WHITE).to_corner(UR)))
            self.play(options[colors.index(color)].animate(rate_func=there_and_back).scale(1.2))
            blaze_card = ruleta.apostar(self, color, monto)
            txt = Text(f"Blaze rodó {blaze_card[-1].text}", font="Roboto", font_size=24, color=WHITE, weight=BOLD)
            txt.next_to(line, UP)
            self.play(FadeIn(txt, scale=2))
            self.wait(0.5)
            self.play(FadeOut(txt, scale=0.5))
            self.play(Transform(saldo_txt, Text(f"Saldo: ${ruleta.saldo}", font="Roboto", font_size=24, color=WHITE).to_corner(UR)))
            self.wait()
