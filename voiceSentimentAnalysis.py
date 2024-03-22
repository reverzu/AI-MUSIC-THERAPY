import streamlit as st
import speech_recognition as sr
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


if 'sentiment' not in st.session_state:
    st.session_state['sentiment'] = None
if 'play_something_else_voice' not in st.session_state:
    st.session_state['play_something_else_voice'] = None


def AnalyzeVoiceSentiment():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.text("Clearing Background Noises...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        st.text("Waiting for you message...")
        recordedAudio = recognizer.listen(source)
        st.text("Recording Done")
    try:
        text = recognizer.recognize_google(recordedAudio, language='en-US')
    except Exception as ex:
        st.error(ex)
    sentence = [str(text)]
    analyzer = SentimentIntensityAnalyzer()

    for i in sentence:  
        ps = analyzer.polarity_scores(i)
    if ps:
        compound = float(ps.get('compound'))
        if float(compound)>=-0.35 and float(compound)<=0.35:
            st.session_state['sentiment'] = 'Neutral'
            st.session_state['play_something_else_voice'] = 'Neutral'
            np.save("sentiment.npy", np.array(['Neutral']))
        elif float(compound) < -0.35:
            st.session_state['sentiment'] = 'Sad'
            st.session_state['play_something_else_voice'] = 'Sad'
            np.save("sentiment.npy", np.array(['Sad']))
        elif float(compound) > 0.35:
            st.session_state['sentiment'] = 'Happy'
            st.session_state['play_something_else_voice'] = 'Happy'
            np.save("sentiment.npy", np.array(['Happy']))