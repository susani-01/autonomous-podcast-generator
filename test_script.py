from podcast_app.script_generator import generate_script
from podcast_app.tts_engine import synthesize_script
from podcast_app.audio_mixer import mix_podcast

# sample = """
# Artificial intelligence is transforming healthcare.
# Doctors now use AI to detect cancer earlier than ever before.
# Machine learning models analyze thousands of medical images per second.
# This technology is saving lives and reducing costs across hospitals worldwide.
# """

sample = """
How to synergize the relationship between boyfriend and a girl friend in the current society
"""

script = generate_script(sample)
# for line in script:
#     print(f"{line['speaker']}:{line['text']}")

audio_files = synthesize_script(script, job_id="test_job_001")
# for f in audio_files:
#     print(f"{f}")

podcast_path = mix_podcast(
    audio_paths=audio_files,
    script=script,
    job_id="test_job_001",
    music_path="podcast_app/music/background.mp3",
)
