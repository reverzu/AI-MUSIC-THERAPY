import streamlit as st
import mediapipe as mp
import numpy as np
from keras.models import load_model
import cv2

# Loading Model
try:
    model = load_model("./Models/model.h5")
    # Loading Labels
    label = np.load("./Models/labels.npy")
    pred = np.load("./Models/emotion.npy")[0]
except:
    pass


if 'emotion' not in st.session_state:
    st.session_state['emotion'] = None
if 'play_something_else' not in st.session_state:
    st.session_state['play_something_else'] = None


def startFacialEmotionRecognition():
    # Holistics pipeline generates seperate models for pose, face and hand components
    holistic = mp.solutions.holistic
    # Hands Data
    hands = mp.solutions.hands
    # Holistics pipeline calling
    holis = holistic.Holistic()
    # Drawing holistics on window
    drawing = mp.solutions.drawing_utils

    # Starting video camera capture
    camera = cv2.VideoCapture(0)
    # Frame Window Initialiazation
    FRAME_WINDOW = st.image([])
    # Capture Button
    capture_button = st.button("Capture 📷", key='capture')
    # Reading video camera frames
    while True:
        frames_list = []
        # Frames capture
        _, frame = camera.read()

        # Frames flipping to mirror
        frame = cv2.flip(frame, 1)

        # Holistics Result
        res = holis.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Reading Facial Landmarks
        if res.face_landmarks:
            for i in res.face_landmarks.landmark:
                frames_list.append(i.x - res.face_landmarks.landmark[1].x)
                frames_list.append(i.y - res.face_landmarks.landmark[1].y)
            # Left Hand
            if res.left_hand_landmarks:
                for i in res.left_hand_landmarks.landmark:
                    frames_list.append(
                        i.x - res.left_hand_landmarks.landmark[8].x)
                    frames_list.append(
                        i.y - res.left_hand_landmarks.landmark[8].y)
            else:
                for i in range(42):
                    frames_list.append(0.0)

            # Right Hand
            if res.right_hand_landmarks:
                for i in res.right_hand_landmarks.landmark:
                    frames_list.append(
                        i.x - res.right_hand_landmarks.landmark[8].x)
                    frames_list.append(
                        i.y - res.right_hand_landmarks.landmark[8].y)
            else:
                for i in range(42):
                    frames_list.append(0.0)

            # Reshaping the Numpy Array
            frames_list = np.array(frames_list).reshape(1, -1)
            # Predicting facial emotional data
            pred = label[np.argmax(model.predict(frames_list))]

            # Printing Results
            if pred is not None:
                st.session_state['emotion'] = pred
                st.session_state['play_something_else'] = pred
                print(pred)
            # Putting predicted data on window
            cv2.putText(frame, pred, (50, 50),
                        cv2.FONT_ITALIC, 1, (255, 0, 0), 2)

        # Applying FaceMesh
        drawing.draw_landmarks(frame, res.face_landmarks,
                               holistic.FACEMESH_CONTOURS, landmark_drawing_spec=drawing.DrawingSpec(
                                   color=(255, 0, 0), thickness=-1, circle_radius=1),)
        # Left hand Skeleton
        drawing.draw_landmarks(
            frame, res.left_hand_landmarks, hands.HAND_CONNECTIONS)
        # Right hand Skeleton
        drawing.draw_landmarks(
            frame, res.right_hand_landmarks, hands.HAND_CONNECTIONS)

        # Showing Camera Frames Window
        FRAME_WINDOW.image(frame, use_column_width=True)

        np.save("./Models/emotion.npy", np.array([pred]))
        # Loop out from the Process
        if cv2.waitKey(1) == 27 or capture_button:
            cv2.destroyAllWindows()
            camera.release()
            break
    return
