from manim_voiceover import VoiceoverScene
from manim_voiceover.services.recorder import RecorderService


__all__ = ["RecorderScene"]


class RecorderScene(VoiceoverScene):
    def setup(self):
        self.set_speech_service(RecorderService(transcription_model="large"))
