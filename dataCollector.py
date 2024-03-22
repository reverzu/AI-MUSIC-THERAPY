import cv2
import streamlit as st
import mediapipe as mp
import numpy as np


def startCollectingData(emotion):

    FRAME_WINDOW = st.image([])
    camera = cv2.VideoCapture(0)

    # Naming the Emotion data
    name = emotion

    # Holistics pipeline generates seperate models for pose, face and hand components
    holistic = mp.solutions.holistic
    # Hands Data
    hands = mp.solutions.hands
    # Holistics pipeline calling
    holis = holistic.Holistic()
    # Drawing holistics on window
    drawing = mp.solutions.drawing_utils

    # Emotions List
    X = []
    # Data Size
    data_size = 0

    while True:
        # Frame List
        frames_list = []

        # Frames capture
        _, frame = camera.read()

        # Frames flipping to mirror
        frame = cv2.flip(frame, 1)

        # Holistics Result
        result = holis.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Reading Facial Landmarks
        if result.face_landmarks:
            for i in result.face_landmarks.landmark:
                frames_list.append(
                    i.x - result.face_landmarks.landmark[1].x)
                frames_list.append(
                    i.y - result.face_landmarks.landmark[1].y)

            # Left Hand
            if result.left_hand_landmarks:
                for i in result.left_hand_landmarks.landmark:
                    frames_list.append(
                        i.x - result.left_hand_landmarks.landmark[8].x)
                    frames_list.append(
                        i.y - result.left_hand_landmarks.landmark[8].y)
            else:
                for i in range(42):
                    frames_list.append(0.0)

            # Right Hand
            if result.right_hand_landmarks:
                for i in result.right_hand_landmarks.landmark:
                    frames_list.append(
                        i.x - result.right_hand_landmarks.landmark[8].x)
                    frames_list.append(
                        i.y - result.right_hand_landmarks.landmark[8].y)
            else:
                for i in range(42):
                    frames_list.append(0.0)

            # Appending list and increasing the size
            X.append(frames_list)
            data_size = data_size+1

        # Applying FaceMesh
        drawing.draw_landmarks(
            frame, result.face_landmarks, holistic.FACEMESH_CONTOURS)
        # Left hand Skeleton
        drawing.draw_landmarks(frame, result.left_hand_landmarks,
                                hands.HAND_CONNECTIONS)
        # Right hand Skeleton
        drawing.draw_landmarks(frame, result.right_hand_landmarks,
                                hands.HAND_CONNECTIONS)

        # Putting predicted data on window
        cv2.putText(frame, str(data_size), (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # Showing Camera Frames Window
        # cv2.imshow("window", frame)
        FRAME_WINDOW.image(frame, use_column_width=True)
        # Loop out from the Process
        if cv2.waitKey(1) == 27 or data_size > 255:
            cv2.destroyAllWindows()
            camera.release()
            break

    if X !=[]:
        saveEmotions(name, X)
        return True
    return True


def saveEmotions(name, X):
    # Saving emotions as a Numpy Array
    np.save(f"Models/{name}.npy", np.array(X))
    # Printing the Array Shape
    print(np.array(X).shape)
    st.markdown(f'''<h4 style='text-align: center;'>Done 👍🏼</h4>''',
                unsafe_allow_html=True)
