from manimlib import *
from mgl.intro import Intro
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, SpeechSynthesisOutputFormat, ResultReason
from azure.cognitiveservices.speech.audio import AudioOutputConfig
from dotenv import load_dotenv
import json
import audioread


load_dotenv()


def serialize_word_boundary(wb):
    return {
        "audio_offset": wb["audio_offset"],
        "duration_milliseconds": int(wb["duration_milliseconds"].microseconds / 1000),
        "text_offset": wb["text_offset"],
        "word_length": wb["word_length"],
        "text": wb["text"],
        "boundary_type": wb["boundary_type"],
    }


def is_json_cached(text, voice):
    with open(f"{voice}.json", "r+") as f:
        return text in json.load(f)


def get_cached_file(text, voice):
    with open(f"{voice}.json", "r+") as f:
        return json.load(f)[text]


def create_json_file(voice):
    with open(f"{voice}.json", "w+") as f:
        f.write("{}")


def speak(text, voice = "en-US-GuyNeural"):
    if not Path(f"{voice}.json").exists():
        create_json_file(voice)
    if is_json_cached(text, voice):
        print("Using cached file")
        return get_cached_file(text, voice)
    print("Generating new voiceover")
    speech_config = SpeechConfig(
        subscription=os.getenv("AZURE_SUBSCRIPTION_KEY"),
        region=os.getenv("AZURE_SERVICE_REGION")
    )
    speech_config.set_speech_synthesis_output_format(
        SpeechSynthesisOutputFormat["Audio48Khz192KBitRateMonoMp3"],
    )
    i = 0
    while (filename := Path("audio") / f"azure{i}.mp3").exists():
        i += 1
    audio_config = AudioOutputConfig(filename=str(filename))
    speech_service = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    word_boundaries = []
    ssml_beginning = r"""<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"
    xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">
    <voice name="%s">
        """ % (
            voice
        )
    ssml_end = r"""
    </voice>
</speak>
        """
    initial_offset = len(ssml_beginning)
    def process_event(evt):
            # print(f'{type(evt)=}')
            result = {label[1:]: val for label, val in evt.__dict__.items()}
            result["boundary_type"] = result["boundary_type"].name
            result["text_offset"] = result["text_offset"] - initial_offset
            return result
    speech_service.synthesis_word_boundary.connect(
        lambda evt: word_boundaries.append(process_event(evt))
    )
    ssml = ssml_beginning + text + ssml_end
    result = speech_service.speak_ssml_async(ssml).get()
    with open(f"{voice}.json", "r+") as f:
        data = json.load(f)
        data[text] = str(filename)
        f.seek(0)
        json.dump(data, f)
    if result.reason == ResultReason.SynthesizingAudioCompleted:
        return filename
    raise RuntimeError(f"Something went wrong with the Azure speech synthesis: {result.reason}")


class Cancel(Cross):
    def __init__(self, mobject: Mobject, color=RED, **kwargs):
        super().__init__(mobject, stroke_color=color, **kwargs)
        self.remove(self.submobjects[-1])


class AzureSpeechScene(InteractiveScene):
    voice: str = "en-US-GuyNeural"
    add_audio: bool = True

    def speak(self, text):
        if self.current_audio_duration is not None:
            self.wait_until_current_audio_finished()
        filename = speak(text, self.voice)
        self.current_audio_duration = self.get_current_audio_duration(filename)
        self.start_audio_time = self.time
        self.add_sound(str(filename))
    
    def wait_until_current_audio_finished(self):
        if self.time - self.start_audio_time >= self.current_audio_duration:
            self.current_audio_duration = None
            self.start_audio_time = None
            return
        self.wait(self.current_audio_duration - (self.time - self.start_audio_time))
        self.current_audio_duration = None
        self.start_audio_time = None
    
    def get_current_audio_duration(self, filename):
        with audioread.audio_open(filename) as f:
            return f.duration
    
    def setup(self):
        super().setup()
        self.states_to_save = []
        # self.recording = False
        self.current_audio_duration = None
        self.start_audio_time = None
        self.record()
    
    def record(self):
        # self.recording = True
        self.camera.use_window_fbo(False)
        self.file_writer.begin_insert()
    
    def stop_recording(self):
        self.file_writer.end_insert()
        self.camera.use_window_fbo(True)
        self.file_writer.movie_file_path = self.file_writer.inserted_file_path
        if self.add_audio:
            self.file_writer.add_sound_to_video()
    
    def tear_down(self) -> None:
        self.stop_recording()
        super().tear_down()
    
    def get_image(self):
        self.camera.capture(*self.render_groups)
        return self.camera.get_image()
    
    # def get_recording(self):
    #     for state in self.states_to_save:
    #         self.restore_state(state)
    #         self.wait(1 / self.camera.fps)


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


class Introduction(Intro, AzureSpeechScene):
    def construct(self):
        f_x = Tex("f(x)=ax^2+bx+c", isolate=["f", "x", "a", "b", "c"])
        equals_0 = Tex("f(x)=0", isolate=["f", "x"])
        quad_formula = Tex("x={-b\\pm\\sqrt{b^2-4ac}\\over 2a}", isolate=["x", "a", "b", "c"])
        all_g = VGroup(f_x, equals_0, quad_formula).arrange(DOWN)
        self.speak("We have a quadratic function.")
        self.play(Write(f_x))
        self.speak("You want to solve the equation f of x equals 0.")
        self.play(TransformMatchingTex(f_x.copy(), equals_0))
        self.speak("In school, you probably would have used the quadratic formula.")
        self.play(TransformMatchingTex(equals_0.copy(), quad_formula))
        self.speak("But let's see an interesting way to solve this kind of equations.")
        self.play(FadeOut(all_g, scale=10))
        Intro.construct(self)


class Warning(AzureSpeechScene):
    def construct(self) -> None:
        strings = [
            "Warning: This video is absolutely useless for everyday",
            "life unless you're a mathematician or something else.",
            "But it's fun!"
        ]
        warning = Text(
            "\n".join(strings),
            text2weight={"Warning": BOLD},
            text2color={"Warning": YELLOW},
            font_size=40
        )
        self.speak(" ".join(strings))
        self.play(FadeIn(warning, scale=0.5))
        self.wait_until_current_audio_finished()
        self.play(DrawBorderThenFill(warning, remover=True, final_alpha_value=0, rate_func=lambda t: smooth(1 - t)))


class EmbedCallbacksScene(AzureSpeechScene):
    callbacks: list[str]

    def setup(self):
        super().setup()
        self.current_callback = 0
    
    def construct(self):
        self.embed()
    
    def update_embed(self):
        self.dont_break = True
        while self.dont_break:
            self.wait(1 / self.camera.fps)
    
    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if chr(symbol) == "0":
            getattr(self, self.callbacks[self.current_callback])()
            self.current_callback += 1
        elif chr(symbol) == "1":
            self.update_embed()
        elif chr(symbol) == "2":
            self.dont_break = False
        super().on_key_press(symbol, modifiers)
