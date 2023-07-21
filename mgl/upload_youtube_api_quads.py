import json
import random
import subprocess
from pathlib import Path


def get_i():
    with open("many_exercises.json", "r") as f:
        return len(json.load(f)) + 1


def exercise_in_json(a, b, c):
    with open("many_exercises.json", "r") as f:
        return [a, b, c] in json.load(f).values()


def save_parameters(a, b, c):
    with open("many_exercises.json", "r+") as f:
        data = json.load(f)
        data[str(get_i())] = [a, b, c]
        f.seek(0)
        json.dump(data, f)


def get_random_coefficients():
    a = random.randint(-10, 10)
    b = random.randint(-10, 10)
    c = random.randint(-10, 10)
    if a == 0 or exercise_in_json(a, b, c):
        return get_random_coefficients()
    return a, b, c


def get_title():
    return f"Reto {get_i()}: ¡Resuelve esta ecuación cuadrática!"


def get_file():
    i = 0
    while (Path("out") / f"RandomScene_insert_{i}.mp4").exists():
        i += 1
    return Path("out") / f"RandomScene_insert_{i}.mp4"


def get_final_file_wo_music():
    i = 0
    while (Path("out") / f"final_wo_audio_{i}.mp4").exists():
        i += 1
    return Path("out") / f"final_wo_audio_{i}.mp4"


def get_final_file():
    i = 0
    while (Path("out") / f"final_{i}.mp4").exists():
        i += 1
    return Path("out") / f"final_{i}.mp4"


def get_ffmpeg_command_wo_music(file1, file2, file3):
    return f'ffmpeg -i "{file1}" -i "{file2}" -i "{file3}" -filter_complex vstack=3 -vsync 2 -map 2:a "{get_final_file_wo_music()}"'


def get_ffmpeg_command(video, audio):
    return f'ffmpeg -i "{video}" -i "{audio}" -filter_complex "[1:a]volume=0.05,apad[A];[0:a][A]amerge[out]" -c:v copy -map 0:v -map [out] {get_final_file()}'


def get_manimgl_command():
    return "manimgl generate_random_quadratics.py"


video_description = """¡Hola! En este video, te reto a resolver una ecuación cuadrática. ¡Buena suerte!

Este video ha sido generado automáticamente por Python con ManimGL, Azure Speech y YouTube Data API v3. ¡Suscríbete para más videos como este!"""


def render_video():
    coefficients = get_random_coefficients()
    generated_videos = []
    for part in ("titulo", "ecuacion", "subtitulos_group"):
        generated_videos.append(get_file())
        subprocess.run(
            get_manimgl_command(),
            input="\n".join([part, ",".join(map(str, coefficients))]).encode()
        )
    final_file_wo_audio = get_final_file_wo_music()
    subprocess.run(
        get_ffmpeg_command_wo_music(*generated_videos)
    )
    final_file = get_final_file()
    subprocess.run(
        get_ffmpeg_command(final_file_wo_audio, "Inkling - Slenderbeats.mp3")
    )
    return final_file, coefficients


def upload_to_youtube(file):
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    import pickle
    import os

    SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
    API_SERVICE_NAME = "youtube"
    API_VERSION = "v3"

    def get_authenticated_service():
        credentials = None
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                credentials = pickle.load(token)
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "client_secret.json", SCOPES
                )
                credentials = flow.run_local_server()
            with open("token.pickle", "wb") as token:
                pickle.dump(credentials, token)
        return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

    service = get_authenticated_service()

    request_body = {
        "snippet": {
            "title": get_title(),
            "description": video_description,
            "tags": ["quadratics", "functions", "equations", "math", "manim", "python", "youtube"],
            "categoryId": "27"
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        }
    }

    mediaFile = MediaFileUpload(file)

    response_upload = (
        service.videos()
        .insert(
            part="snippet,status",
            body=request_body,
            media_body=mediaFile
        )
        .execute()
    )

    print(response_upload)


def generate_and_upload_many_videos(n: int):
    for _ in range(n):
        video, parameters = render_video()
        upload_to_youtube(video)
        save_parameters(*parameters)


generate_and_upload_many_videos(20)

