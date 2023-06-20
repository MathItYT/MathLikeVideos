from manim_voiceover import VoiceoverScene
from manim_voiceover.services.azure import AzureService


__all__ = ["AzureSpeechScene", "express_as"]


class AzureSpeechScene(VoiceoverScene):
    """A scene that uses Azure's speech service to generate audio."""
    def setup(self):
        self.express_as(None)
    
    def express_as(self, style):
        self.set_speech_service(AzureService(voice="es-ES-AlvaroNeural", style=style))
