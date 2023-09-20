from manim import *
from creature import CharCreature, RoundBubble, ShowBubble, Bubble, DestroyBubble
from logo import Logo


__all__ = ["MathCreature", "RoundBubble", "ShowBubble", "Bubble"]


class MathCreature(CharCreature):
    def __init__(self, body=None, eyes_scale=2, eyes_prop=[0.5, 0], **kwargs):
        if body is None:
            body = Logo()
        super().__init__(body, eyes_scale, eyes_prop, **kwargs)
