import streamlit as st
import findFiles

def generateMusic(music_generator_prompt, music_duration, sample_rate_different):
    from audiocraft.models import musicgen
    import torchaudio
    import os
    import random
    st.text("Resources loaded successfully")
    output_directory = r"./aiGeneratedMusic/"

    model = musicgen.MusicGen.get_pretrained(
        'medium', device='cuda')
    model.set_generation_params(duration=int(
        music_duration) if music_duration else 10)
    prompted_list = [music_generator_prompt]
    res = model.generate(prompted_list)
    num = int(random.random()*10**10)
    for i, audio in enumerate(res):
        audio_cpu = audio.cpu()
        file_path = os.path.join(
            output_directory, f'{prompted_list[i].split(" ")[0]}_audio-{num}.wav')
        torchaudio.save(file_path, audio_cpu, sample_rate=int(
            sample_rate_different) if sample_rate_different else 32000)
    for i in range(len(res)):
        file_path = os.path.join(
            output_directory, f'{prompted_list[i].split(" ")[0]}_audio-{num}.wav')
        st.image(findFiles.imageOnEmotion('Neutral'))
        st.audio(file_path)