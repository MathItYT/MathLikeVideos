from manim import *


class ManimStudioLogo(VGroup):
    def __init__(self):
        self.banner = ManimBanner(dark_theme=False)
        self.studio = Tex("Studio")
        self.studio.scale(4)
        super().__init__(self.banner, self.studio)
        self.arrange(RIGHT, buff=0.5)
        self.studio.set_y(self.banner.M.get_bottom()[
                          1] + self.studio.get_height() / 2)

    @override_animation(Create)
    def create(self):
        return AnimationGroup(Create(self.banner), LaggedStartMap(FadeIn, self.studio, scale=2))

    @override_animate(Uncreate)
    def uncreate(self):
        return FadeOut(self, scale=5)
