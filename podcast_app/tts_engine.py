import numpy as np
import soundfile as sf
import os
from kokoro import KPipeline

v_map = {
    "HOST1":"af_heart",
    "HOST2":"am_michael"
}

ppls = {
   "HOST1":KPipeline(lang_code="a"),
   "HOST2":KPipeline(lang_code='a')
}

def synthesize_line(speaker: str,text: str,line_index: int,output_dir:str) -> str:
    voice = v_map[speaker]
    ppl=ppls[speaker]

    gen = ppl(text,voice=voice,speed=1.0)
    chunks = [audio for _, _,audio in gen]
    full_audio = np.concatenate(chunks)

    path = os.path.join(output_dir,f"line_{line_index:03d}_{speaker}.wav")
    sf.write(path,full_audio,24000)

    return path

def synthesize_script(script: list[dict],job_id:str) ->list[str]:
    output_dir = os.path.join("podcast_app","outputs",job_id,"lines")
    os.makedirs(output_dir,exist_ok=True)

    audio_paths = []
    for i,line in enumerate(script):
        path = synthesize_line(
            speaker=line["speaker"],
            text=line["text"],
            line_index=i,
            output_dir=output_dir
        )

        audio_paths.append(path)
    return audio_paths
