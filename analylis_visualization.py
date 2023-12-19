# analysis_and_visualization.py
import cv2
import numpy as np
import mediapipe as mp
from tensorflow.keras.models import load_model
from utils import mediapipe_detection, draw_styled_landmarks, extract_keypoints


from spoty_main import spotify_search

client_id = "b3a47786876e4b3caf05c32b0bf2feea"
client_secret = "f7021e75f1144c0fa6ccade8bfbf8ce8"
query_limit = 10
path = "selectedSong"

# Carica il modello addestrato
model = load_model('action.h5')

mp_holistic = mp.solutions.holistic

# Configurazione
actions = np.array(['hello', 'thanks', 'I love you'])
colors = [(245, 117, 16), (117, 245, 16), (16, 117, 245)]

# Variabili di rilevamento
sequence = []
sentence = ""
predictions = []
threshold = 0.5

# Configurazione della webcam
cap = cv2.VideoCapture(0)

# Set mediapipe model 
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
        # Leggi il frame dalla webcam
        ret, frame = cap.read()

        # Effettua la rilevazione con Mediapipe
        image, results = mediapipe_detection(frame, holistic)

        # Disegna i landmarks
        draw_styled_landmarks(image, results)

        # Logica di previsione
        keypoints = extract_keypoints(results)
        sequence.append(keypoints)
        sequence = sequence[-30:]

        if len(sequence) == 30:
            res = model.predict(np.expand_dims(sequence, axis=0))[0]
            predictions.append(np.argmax(res))

            # Logica di visualizzazione
            if np.unique(predictions[-10:])[0] == np.argmax(res):
                if res[np.argmax(res)] > threshold:
                    sentence = actions[np.argmax(res)]
                    spotify_search(sentence, client_id, client_secret, query_limit, path)
                    cap.release()
                    cv2.destroyAllWindows()
        #cv2.rectangle(image, (0, 0), (640, 40), (245, 117, 16), -1)
       # cv2.putText(image, sentence, (3, 30),
         #   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # Visualizza il frame
        cv2.imshow('Live Video', image)

        # Interrompi il loop alla pressione del tasto 'q'
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    # Rilascia la webcam e chiudi le finestre
    cap.release()
    cv2.destroyAllWindows()





