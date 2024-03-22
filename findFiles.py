import os
import random
import streamlit as st
import base64

def findFiles(fileName, searchPath):
    result = []

    # Wlaking top-down from the root
    for root, dir, files in os.walk(searchPath):
        if fileName in files:
            result.append(os.path.join(root, fileName))

    return True if len(result)>0 else False


def songOnEmotion(emotion):
    if emotion == 'Happy':
        song = random.choice(os.listdir("./music/happy/"))
        return ("./music/happy/"+song)
    elif emotion == 'Neutral':
        directories = ["./music/neutral/",
                    "./music/happy/", "./music/sad/"]
        random_dir_index = random.randint(0, len(directories) - 1)
        chosen_directory = directories[random_dir_index]
        song = random.choice(os.listdir(chosen_directory))
        return (chosen_directory+song)
    elif emotion == 'Sad':
        song = random.choice(os.listdir("./music/sad/"))
        return ("./music/sad/"+song)
    

def autoplay_audio(emotion):
    audio_player = st.empty()
    file_path = songOnEmotion(emotion)
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true" style="width:100%">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        audio_player.markdown(md, unsafe_allow_html=True,)


def imageOnEmotion(emotion):
    if emotion == 'Happy':
        song = random.choice(os.listdir("./images/happy/"))
        return ("./images/happy/"+song)
    elif emotion == 'Neutral':
        directories = ["./images/neutral/",
                    "./images/happy/", "./images/sad/"]
        random_dir_index = random.randint(0, len(directories) - 1)
        chosen_directory = directories[random_dir_index]
        song = random.choice(os.listdir(chosen_directory))
        return (chosen_directory+song)
    elif emotion == 'Sad':
        song = random.choice(os.listdir("./images/sad/"))
        return ("./images/sad/"+song)



