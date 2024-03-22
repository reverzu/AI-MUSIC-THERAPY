import cv2
import streamlit as st
import mediapipe as mp
import numpy as np
import staticData
import random
import os
import base64
import pandas as pd
import findFiles
import dataCollector
import facialEmotion
import chatCompanion
import aiMusicGen
import voiceSentimentAnalysis
import polarplot
import songrecommendations
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from keras.models import load_model


SPOTIPY_CLIENT_ID = 'e8b2cad659b24dc1ab06ae8b35982f54'
SPOTIPY_CLIENT_SECRET = 'feeed209c813439ea8d649e017ce222b'

auth_manager = SpotifyClientCredentials(
    client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)


if 'emotion' not in st.session_state:
    st.session_state['emotion'] = None
if 'sentiment' not in st.session_state:
    st.session_state['sentiment'] = None
if 'play_something_else' not in st.session_state:
    st.session_state['play_something_else'] = None
if 'play_something_else_voice' not in st.session_state:
    st.session_state['play_something_else_voice'] = None


try:
    # Loading Model
    model = load_model("Models/model.h5")
    # Loading Labels
    labels = np.load("Models/labels.npy")
except:
    model = None

st.set_page_config(page_title="🎶 AI Music Therapy", layout='wide')
st.markdown(""" <style>
                .block-container{
                padding-top:1.5rem;
                }
            
                .container {
                display: inline-block;
                }
            
                div.stButton > button:first-child {
                height:2.5em;
                width:100%;
                }
            
                div.stButton > button:first-child:hover{
                border:1 px solid gray;
                }
            
                .typed-out{
                overflow: hidden;
                border-right: .15em solid orange;
                white-space: nowrap;
                font-size: 1.1rem;
                margin: 0 auto; /* Gives that scrolling effect as the typing happens */
                letter-spacing: .15em; /* Adjust as needed */
                width: 0;
                animation: typing 1s forwards,
                blink-caret .75s step-end infinite;
                font-weight: 550;
                }		
            
                .typewriter{
                overflow: hidden; /* Ensures the content is not revealed until the animation */
                border-right: .12em solid orange; /* The typwriter cursor */
                white-space: nowrap; /* Keeps the content on a single line */
                font-size: 1.6rem;
                margin: 0 auto; /* Gives that scrolling effect as the typing happens */
                letter-spacing: .15em; /* Adjust as needed */
                animation: 
                typing 3.5s forwards,
                blink-caret .75s step-end infinite;
                font-size:1rem;
                display: inline-block;
                width: 0;
                }

                /* The typing effect */
                @keyframes typing {
                from { width: 0 }
                to { width: 100% }
                }

                /* The typewriter cursor effect */
                @keyframes blink-caret {
                from, to { border-color: transparent }
                50% { border-color: orange; }
                }
                </style>""",
            unsafe_allow_html=True)


st.title("🎶 AI Music Therapy")
st.markdown(
    f'<div class="container"><div class="typed-out">"{staticData.music_quotes[random.randint(0, len(staticData.music_quotes) - 1)]}</div></div><br><br>', unsafe_allow_html=True)


st.sidebar.header("🎶 AI Music Therapy")
st.sidebar.title("Main Menu")
search_choices = ['Home', 'Song/Track', 'Artist', 'Album', 'Research']
search_selected = st.sidebar.selectbox(
    "Your search choice please: ", search_choices)
search_results = []
tracks = []
artists = []
albums = []

if search_selected == "Home":
    if model is None:
        spacel, middle, spacer = st.columns([2, 8, 2])
        with middle:
            st.markdown("<h2 style='text-align: center;'>Train the Model to your Facial Expressions</h2>",
                        unsafe_allow_html=True)
            st.markdown(
                f'''<h4 style='text-align: center;'>Show different Faces for the Emotions</h4>''', unsafe_allow_html=True)

            col1, col2, col3 = st.columns([1, 1, 1])
            col11, col12 = st.columns([1, 1])

            with col1:
                happy_collect = st.button("Happy 😊", use_container_width=True)
            with col2:
                neutral_collect = st.button(
                    "Netural 😐", use_container_width=True)
            with col3:
                sad_collect = st.button("Sad 😢", use_container_width=True)

            if happy_collect:
                st.markdown(
                    "<h4 style='text-align: center;'>Show us your Happy 😊 Face</h4>", unsafe_allow_html=True)
                dataCollector.startCollectingData('Happy')
            if neutral_collect:
                st.markdown(
                    "<h4 style='text-align: center;'>Show us your Neutral 😐 Face</h4>", unsafe_allow_html=True)
                dataCollector.startCollectingData('Neutral')
            if sad_collect:
                st.markdown(
                    "<h4 style='text-align: center;'>Show us your Sad 😢 Face</h4>", unsafe_allow_html=True)
                dataCollector.startCollectingData('Sad')

            with col12:
                happy_file = findFiles.findFiles('Happy.npy', './Models/')
                sad_file = findFiles.findFiles('Sad.npy', './Models/')
                neutral_file = findFiles.findFiles('Neutral.npy', './Models/')
                if happy_file and neutral_file and sad_file:
                    train_model_button = st.button(
                        label="Train the Model ➡", type="primary", use_container_width=True)
                    if train_model_button:
                        with col11:
                            creating_progress = st.spinner(
                                "Training the Model... (Please be patient, it may take a few minutes)")
                            with creating_progress:
                                import modelTrainer
                                modelTrainer.train()
                else:
                    st.markdown(
                        "<h4 style='text-align: center;'>Emotion Values are Missing...</h4>", unsafe_allow_html=True)

    else:
        tab1, tab2, tab3 = st.tabs(
            ['Home', 'Chat Companion', "AI Music Generator"])

        with tab1:
            col_main1, col_main2 = st.columns([8, 4])
            with col_main1:
                key, value = random.choice(
                    list(staticData.articles_dict.items()))
                st.subheader(key)
                st.image("./images/slides/" +
                         random.choice(os.listdir("./images/slides/")))
                st.markdown(value[0])
                st.markdown(value[1])
                st.markdown('---')
                mainHeaderPlaceholder = st.empty()
                mainHeader = mainHeaderPlaceholder.markdown(
                    "<h1 style='text-align: center;'>Hello there, How are we feeling today?</h1><br>", unsafe_allow_html=True)

                col1, col2, col3 = st.columns([1, 1, 1])

                with col1:
                    happy = st.button("Play Something Happy 😊",
                                      use_container_width=True)
                with col2:
                    neutral = st.button(
                        "Play Something Netural 😐", use_container_width=True)
                with col3:
                    sad = st.button("Play Something Sad 😢",
                                    use_container_width=True)

                st.markdown("<br>", unsafe_allow_html=True)

                if happy:
                    st.image(findFiles.imageOnEmotion('Happy'))
                    findFiles.autoplay_audio('Happy')
                elif sad:
                    st.image(findFiles.imageOnEmotion('Sad'))
                    findFiles.autoplay_audio('Sad')
                elif neutral:
                    st.image(findFiles.imageOnEmotion('Neutral'))
                    findFiles.autoplay_audio('Neutral')

                st.markdown('<hr>', unsafe_allow_html=True)
                st.markdown(
                    "<h1 style='text-align: center;'>Capture Emotion from your webcam?</h1><br>", unsafe_allow_html=True)

                colb1, colb2 = st.columns([1, 1])
                with colb1:
                    emotion_capture_button = st.button(
                        "Capture My Facial Emotion 📷", use_container_width=True)
                with colb2:
                    Play_something_else_button = st.button(
                        "Play Something Else 🎵", use_container_width=True)

                if emotion_capture_button:
                    facialEmotion.startFacialEmotionRecognition()
                if st.session_state['emotion'] is not None:
                    emotion_capture_result = st.empty()
                    emotion_capture_result.markdown(
                        f"<h2 style='text-align: center;'>It Looks like you're {st.session_state['emotion']}</h2><p>Let me Play some {st.session_state['emotion']} Music for you...</p>", unsafe_allow_html=True)
                    st.image(findFiles.imageOnEmotion(
                        st.session_state['emotion']))
                    findFiles.autoplay_audio(st.session_state['emotion'])
                    st.session_state['emotion'] = None
                else:
                    pass

                if Play_something_else_button and st.session_state['play_something_else'] is not None:
                    emotion_capture_play_something_else_result = st.empty()
                    emotion_capture_play_something_else_result.markdown(
                        f"<h2 style='text-align: center;'>It Looks like you're {st.session_state['play_something_else']}</h2><p>Let me Play some {st.session_state['play_something_else']} Music for you...</p>", unsafe_allow_html=True)
                    st.image(findFiles.imageOnEmotion(
                        st.session_state['play_something_else']))
                    findFiles.autoplay_audio(
                        st.session_state['play_something_else'])
                else:
                    pass

                st.markdown('<br><hr>', unsafe_allow_html=True)
                st.markdown(
                    "<h1 style='text-align: center;'>Analyze Sentiment from your Voice?</h1><br>", unsafe_allow_html=True)

                colc1, colc2 = st.columns([1, 1])
                with colc1:
                    voice_analyzer_button = st.button(
                        "Analyze My Voice 🗣🎙", use_container_width=True)
                with colc2:
                    Play_something_else_voice_button = st.button(
                        "Play Something Else 🎵 ", use_container_width=True)

                if voice_analyzer_button:
                    voiceSentimentAnalysis.AnalyzeVoiceSentiment()
                if st.session_state['sentiment'] is not None:
                    sentiment_analysis_result = st.empty()
                    sentiment_analysis_result.markdown(
                        f"<h2 style='text-align: center;'>It Looks like you're {st.session_state['sentiment']}</h2><p>Let me Play some {st.session_state['sentiment']} Music for you...</p>", unsafe_allow_html=True)
                    st.image(findFiles.imageOnEmotion(
                        st.session_state['sentiment']))
                    findFiles.autoplay_audio(st.session_state['sentiment'])
                    st.session_state['sentiment'] = None
                else:
                    pass

                if Play_something_else_voice_button and st.session_state['play_something_else_voice'] is not None:
                    emotion_capture_play_something_else_voice_result = st.empty()
                    emotion_capture_play_something_else_voice_result.markdown(
                        f"<h2 style='text-align: center;'>It Looks like you're {st.session_state['play_something_else_voice']}</h2><p>Let me Play some {st.session_state['play_something_else_voice']} Music for you...</p>", unsafe_allow_html=True)
                    st.image(findFiles.imageOnEmotion(
                        st.session_state['play_something_else_voice']))
                    findFiles.autoplay_audio(
                        st.session_state['play_something_else_voice'])
                else:
                    pass

            with col_main2:
                st.video('./videos/Steve Parker Artist Talk _ FIGHT SONG.mp4')
                st.video('./videos/Song of the Ambassadors at Lincoln Center.mp4')
                st.video(
                    './videos/Marconi Union - Weightless (Official Video).mp4')
                st.video('./videos/Digitonal - Mirtazapine (The Ambient Zone).mp4')
                st.video('./videos/Chris Coco - Waterfall (The Ambient Zone).mp4')

        with tab2:
            cold1, cold2, cold3 = st.columns([8, 0.1, 4])
            with cold1:
                output = ''
                st.subheader("🎶 AI Music Therapy Chat Companion")
                chatCompanion.chat()
                with cold3:
                    st.markdown(
                        f'<h4 style="padding-bottom:0;">Frequently Asked Questions</h4>', unsafe_allow_html=True)
                    st.markdown('---')
                    for key, value in staticData.chats_dict.items():
                        with st.expander(key):
                            st.markdown(f'{value}')
            pass

        with tab3:
            tab3_col1, tab3_col2 = st.columns([8, 4])
            with tab3_col2:
                st.subheader("Additional Details")
                music_duration = st.slider("Music Duration", 1, 30, 10)
                sample_rate_different = st.text_input(
                    "Enter Sample Rate(in Hz, only int)", placeholder="Default 32000Hz")

                st.markdown('__Some previously generated__')
                for i in os.listdir(r"./aiGeneratedMusic/"):
                    audio_file = "./aiGeneratedMusic/" + i
                    st.audio(audio_file)

            with tab3_col1:
                music_generator_prompt = st.text_input(
                    "What type of Music do you want to listen?", placeholder="Enter some prompt to generate Music, For ex. Happy, with Earthly feel and Summer Breeze")
                generate_music_button = st.button("Generate 🎶", type='primary')
                if music_generator_prompt and generate_music_button:
                    # loading = st.empty()
                    loading_progress = st.spinner(
                        "Generating Music... (Please be patient, it may take a few minutes)")
                    with loading_progress:
                        aiMusicGen.generateMusic(
                            music_generator_prompt, music_duration, sample_rate_different)
            pass


elif search_selected == "Song/Track":
    st.title("🎶 Search any Song/Track")
    search_keyword = st.text_input(search_selected + " (Keyword Search)")
    button_clicked = st.button("Search")
    st.subheader("Start song/track search")
    tracks = sp.search(q='track:' + search_keyword, type='track', limit=20)
    tracks_list = tracks['tracks']['items']
    if len(tracks_list) > 0:
        for track in tracks_list:
            # st.write(track['name'] + " - By - " + track['artists'][0]['name'])
            search_results.append(
                track['name'] + " - By - " + track['artists'][0]['name'])
elif search_selected == "Artist":
    st.title("🎶 Search any Artist")
    search_keyword = st.text_input(search_selected + " (Keyword Search)")
    button_clicked = st.button("Search")
    st.subheader("Start artist search")
    artists = sp.search(q='artist:' + search_keyword, type='artist', limit=20)
    artists_list = artists['artists']['items']
    if len(artists_list) > 0:
        for artist in artists_list:
            # st.write(artist['name'])
            search_results.append(artist['name'])
elif search_selected == "Album":
    st.title("🎶 Search any Album")
    search_keyword = st.text_input(search_selected + " (Keyword Search)")
    button_clicked = st.button("Search")
    st.subheader("Start album search")
    albums = sp.search(q='album:' + search_keyword, type='album', limit=20)
    albums_list = albums['albums']['items']
    if len(albums_list) > 0:
        for album in albums_list:
            # st.write(album['name'] + " - By - " + album['artists'][0]['name'])
            # print("Album ID: " + album['id'] + " / Artist ID - " + album['artists'][0]['id'])
            search_results.append(
                album['name'] + " - By - " + album['artists'][0]['name'])
elif search_selected == "Research":
    def displayPDF(file):
        # Opening file from file path
        with open(file, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    # Embedding PDF in HTML
        pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="1000" type="application/pdf"></iframe>'

    # Displaying File
        st.markdown(pdf_display, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(
        ['Industrial Designers Society of America', 'World Federation of Music Therapy'])
    with tab1:
        displayPDF(
            "./pdf/Artificial-Intelligence-Music-Therapy-and-the-Fight-Against-Mental-Illness.pdf")
    with tab2:
        displayPDF(
            "./pdf/World Federation of Music Therapy.pdf")


selected_album = None
selected_artist = None
selected_track = None
if search_selected == 'Song/Track':
    selected_track = st.selectbox("Select your song/track: ", search_results)
elif search_selected == 'Artist':
    selected_artist = st.selectbox("Select your artist: ", search_results)
elif search_selected == 'Album':
    selected_album = st.selectbox("Select your album: ", search_results)

if selected_track is not None and len(tracks) > 0:
    tracks_list = tracks['tracks']['items']
    track_id = None
    if len(tracks_list) > 0:
        for track in tracks_list:
            str_temp = track['name'] + " - By - " + track['artists'][0]['name']
            if str_temp == selected_track:
                track_id = track['id']
                track_album = track['album']['name']
                img_album = track['album']['images'][0]['url']
                # st.write(track_id, track_album)
                # st.image(img_album)
                songrecommendations.save_album_image(img_album, track_id)
    selected_track_choice = None
    if track_id is not None:
        image = songrecommendations.get_album_mage(track_id)
        st.image(image)
        track_choices = ['Song Features', 'Similar Songs Recommendation']
        selected_track_choice = st.sidebar.selectbox(
            'Please select track choice: ', track_choices)
        if selected_track_choice == 'Song Features':
            track_features = sp.audio_features(track_id)
            df = pd.DataFrame(track_features, index=[0])
            df_features = df.loc[:, ['acousticness', 'danceability', 'energy',
                                     'instrumentalness', 'liveness', 'speechiness', 'valence']]
            st.dataframe(df_features)
            polarplot.feature_plot(df_features)
        elif selected_track_choice == 'Similar Songs Recommendation':
            token = songrecommendations.get_token(
                SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET)
            similar_songs_json = songrecommendations.get_track_recommendations(
                track_id, token)
            recommendation_list = similar_songs_json['tracks']
            recommendation_list_df = pd.DataFrame(recommendation_list)
            # st.dataframe(recommendation_list_df)
            recommendation_df = recommendation_list_df[[
                'name', 'explicit', 'duration_ms', 'popularity']]
            st.dataframe(recommendation_df)
            # st.write("Recommendations....")
            songrecommendations.song_recommendation_vis(recommendation_df)

    else:
        st.write("Please select a track from the list")

elif selected_album is not None and len(albums) > 0:
    albums_list = albums['albums']['items']
    album_id = None
    album_uri = None
    album_name = None
    if len(albums_list) > 0:
        for album in albums_list:
            str_temp = album['name'] + " - By - " + album['artists'][0]['name']
            if selected_album == str_temp:
                album_id = album['id']
                album_uri = album['uri']
                album_name = album['name']
    if album_id is not None and album_uri is not None:
        st.markdown(f"**All tracks for the album : {album_name}**")
        # st.markdown(album_name)
        album_tracks = sp.album_tracks(album_id)
        df_album_tracks = pd.DataFrame(album_tracks['items'])
        # st.dataframe(df_album_tracks)
        df_tracks_min = df_album_tracks.loc[:,
                                            ['id', 'name', 'duration_ms', 'explicit', 'preview_url']]
        # st.dataframe(df_tracks_min)
        for idx in df_tracks_min.index:
            with st.container():
                col1, col2, col3, col4 = st.columns((4, 4, 1, 1))
                col11, col12 = st.columns((8, 2))
                col1.write(df_tracks_min['id'][idx])
                col2.write(df_tracks_min['name'][idx])
                col3.write(df_tracks_min['duration_ms'][idx])
                col4.write(df_tracks_min['explicit'][idx])
                if df_tracks_min['preview_url'][idx] is not None:
                    col11.write(df_tracks_min['preview_url'][idx])
                    # with col12:
                    st.audio(df_tracks_min['preview_url']
                             [idx], format="audio/mp3")


if selected_artist is not None and len(artists) > 0:
    artists_list = artists['artists']['items']
    artist_id = None
    artist_uri = None
    selected_artist_choice = None
    if len(artists_list) > 0:
        for artist in artists_list:
            if selected_artist == artist['name']:
                artist_id = artist['id']
                artist_uri = artist['uri']

    if artist_id is not None:
        artist_choice = ['Albums', 'Top Songs']
        selected_artist_choice = st.sidebar.selectbox(
            'Select artist choice', artist_choice)

    if selected_artist_choice is not None:
        if selected_artist_choice == 'Albums':
            artist_uri = 'spotify:artist:' + artist_id
            album_result = sp.artist_albums(artist_uri, album_type='album')
            all_albums = album_result['items']
            col1, col2, col3 = st.columns((6, 4, 2))
            for album in all_albums:
                col1.write(album['name'])
                col2.write(album['release_date'])
                col3.write(album['total_tracks'])
        elif selected_artist_choice == 'Top Songs':
            artist_uri = 'spotify:artist:' + artist_id
            top_songs_result = sp.artist_top_tracks(artist_uri)
            for track in top_songs_result['tracks']:
                with st.container():
                    col1, col2, col3, col4 = st.columns((4, 4, 2, 2))
                    col11, col12 = st.columns((10, 2))
                    col21, col22 = st.columns((11, 1))
                    col31, col32 = st.columns((11, 1))
                    col1.write(track['id'])
                    col2.write(track['name'])
                    if track['preview_url'] is not None:
                        col11.write(track['preview_url'])
                        with col12:
                            st.audio(track['preview_url'], format="audio/mp3")
                    with col3:
                        def feature_requested():
                            track_features = sp.audio_features(track['id'])
                            df = pd.DataFrame(track_features, index=[0])
                            df_features = df.loc[:, [
                                'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness', 'valence']]
                            with col21:
                                st.dataframe(df_features)
                            with col31:
                                polarplot.feature_plot(df_features)

                        feature_button_state = st.button(
                            'Track Audio Features', key=track['id'], on_click=feature_requested)
                    with col4:
                        def similar_songs_requested():
                            token = songrecommendations.get_token(
                                SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET)
                            similar_songs_json = songrecommendations.get_track_recommendations(
                                track['id'], token)
                            recommendation_list = similar_songs_json['tracks']
                            recommendation_list_df = pd.DataFrame(
                                recommendation_list)
                            recommendation_df = recommendation_list_df[[
                                'name', 'explicit', 'duration_ms', 'popularity']]
                            with col21:
                                st.dataframe(recommendation_df)
                            with col31:
                                songrecommendations.song_recommendation_vis(
                                    recommendation_df)

                        similar_songs_state = st.button(
                            'Similar Songs', key=track['id']+track['name'], on_click=similar_songs_requested)
                    st.write('----')
