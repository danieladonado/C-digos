import cv2 as cv
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import serial as sr

Puerto_serial=sr.Serial('COM5',9600)
# CONFIGURAR MEDIAPIPE

base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=2
)
detector = vision.HandLandmarker.create_from_options(options)

mp_hands = mp.tasks.vision.HandLandmarksConnections
mp_drawing = mp.tasks.vision.drawing_utils
mp_drawing_styles = mp.tasks.vision.drawing_styles

base_keypoints=[2,5,9,13,17]
puntas_keypoints=[4,8,12,16,20]
ancho = [5,17]


def draw_landmarks_on_image(rgb_image, detection_result):
    hand_landmarks_list = detection_result.hand_landmarks 
    modified_image = np.copy(rgb_image)    
    
    for i in range(len(hand_landmarks_list)):   
        hand_landmarks = hand_landmarks_list[i]  # 21 landmarks de la mano

        mp_drawing.draw_landmarks(
            modified_image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style()
        )
        
        height, width, _ = modified_image.shape 
        
        coordenadas_BD=[]
        coordenadas_PD=[]
        coordenadas_Ancho=[]

        for i in base_keypoints:
            x= int(hand_landmarks[i].x*width) #list comprehension
            y= int(hand_landmarks[i].y*height)
            coordenadas_BD.append((x, y))

        for i in puntas_keypoints:
            x= int(hand_landmarks[i].x*width)
            y= int(hand_landmarks[i].y*height)
            coordenadas_PD.append((x, y))
        for i in ancho:
            x= int(hand_landmarks[i].x*width)
            y= int(hand_landmarks[i].y*height)
            coordenadas_Ancho.append((x, y))
            
        coordenadas_BD=np.array(coordenadas_BD)
        coordenadas_PD=np.array(coordenadas_PD)
        coordenadas_Ancho=np.array(coordenadas_Ancho)
        
        Distancia_marcadores= np.linalg.norm(coordenadas_BD-coordenadas_PD, axis=1)  
        Ancho_mano= np.linalg.norm(coordenadas_Ancho[0]-coordenadas_Ancho[1])

        umbral = 0.6 * Ancho_mano
        # Si está cerca a la base del dedo o si la punta del dedo está por abajo de la base del dedo.
        Estado_dedos = ((Distancia_marcadores<umbral) | (coordenadas_PD[:,1]>coordenadas_BD[:,1]))

        # Para el pulgar que necesita un umbral más grande
        Estado_dedos[0] = Distancia_marcadores[0] < (0.7 * Ancho_mano)
        
        cadena_datos=[]
        for i in Estado_dedos:
            if i==False:
                cadena_datos.append(1)
            else:
                cadena_datos.append(0)
                

        comando=""
        for index in range(5):
            comando=comando+str(cadena_datos[index])
        
        comando=comando+"\n"
        Puerto_serial.write(comando.encode('UTF-8'))

    
    return modified_image

source = cv.VideoCapture(0)
nombre_ventana = 'Hand Landmark Detection'
cv.namedWindow(nombre_ventana, cv.WINDOW_NORMAL)

while cv.waitKey(1) != 27:
    has_frame, frame = source.read()
    if not has_frame:
        break

    # BGR (OpenCV) → RGB (MediaPipe)
    rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    # Convertir a formato MediaPipe Image
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    # Detectar manos
    detection_result = detector.detect(mp_image)

    # Dibujar keypoints
    annotated_frame = draw_landmarks_on_image(rgb_frame, detection_result)

    # Convertir de vuelta a BGR para mostrar
    annotated_frame = cv.cvtColor(annotated_frame, cv.COLOR_RGB2BGR)

    cv.imshow(nombre_ventana, annotated_frame)

source.release()
cv.destroyAllWindows()