from pydub import AudioSegment
from pydub.effects import normalize
import os

pause_same_speaker = 300
pause_diff_speaker = 600
background_volume = -18
fade_duration = 3000


def load_audio(path: str) -> AudioSegment:
    return AudioSegment.from_wav(path)


def stitch_dialogue(audio_paths: list[str], script: list[dict]) -> AudioSegment:
    combined = AudioSegment.empty()

    for i, path in enumerate(audio_paths):
        segment = load_audio(path)
        segment = normalize(segment)

        if i == 0:
            combined += segment
        else:
            prev_speaker = script[i - 1]["speaker"]
            curr_speaker = script[i]["speaker"]

            if prev_speaker == curr_speaker:
                pause = AudioSegment.silent(duration=pause_same_speaker)
            else:
                pause = AudioSegment.silent(duration=pause_diff_speaker)

            combined += pause + segment

    return combined


def overlay_background(dialogue: AudioSegment, music_path: str = None) -> AudioSegment:
    if not music_path or not os.path.exists(music_path):
        print("no background music")
        return dialogue

    music = AudioSegment.from_file(music_path)
    while len(music) < len(dialogue):
        music += music

    music = music + background_volume
    music = music.fade_in(fade_duration).fade_out(fade_duration)

    final = dialogue.overlay(music)
    return final


def export_podcast(audio: AudioSegment, job_id: str) -> str:
    output_dir = os.path.join("podcast_app", "outputs", job_id)
    os.makedirs("output_dir", exist_ok=True)

    output_path = os.path.join(output_dir, "podcast.mp3")
    audio.export(
        output_path,
        format="mp3",
        bitrate="192k",
        tags={
            "artist": "AI Podcast Generator",
            "title": f"Podcast {job_id}",
            "genre": "Podcast",
        },
    )
    return output_path


def mix_podcast(
    audio_paths: list[str], script: list[dict], job_id: str, music_path: str = None
) -> str:
    dialogue = stitch_dialogue(audio_paths, script)

    final_audio = overlay_background(dialogue, music_path)

    podcast_path = export_podcast(final_audio, job_id)

    return podcast_path
