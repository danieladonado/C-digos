import cv2 as cv
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# CONFIGURAR MEDIAPIPE

base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=2
)
detector = vision.HandLandmarker.create_from_options(options)

# FUNCION PARA DIBUJAR
mp_hands = mp.tasks.vision.HandLandmarksConnections
mp_drawing = mp.tasks.vision.drawing_utils
mp_drawing_styles = mp.tasks.vision.drawing_styles

# Texto Derecha - Izquierda
MARGIN = 10
FONT_SIZE = 1
FONT_THICKNESS = 2
HANDEDNESS_TEXT_COLOR = (0,0,0)
#(88, 205, 54)

def draw_landmarks_on_image(rgb_image, detection_result):
    hand_landmarks_list = detection_result.hand_landmarks #[mano 1, mano 2]
    detectionID_list = detection_result.handedness  #[izq, der]
    modified_image = np.copy(rgb_image)

    for i in range(len(hand_landmarks_list)):    #Si i es 0 -> mano 1 e izq
        hand_landmarks = hand_landmarks_list[i]  # 21 landmarks de la mano
        detectionID = detectionID_list[i]

        mp_drawing.draw_landmarks(
            modified_image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style()
        )
        
        height, width, _ = modified_image.shape 
        x_coords = [lm.x for lm in hand_landmarks]
        y_coords = [lm.y for lm in hand_landmarks]
        
        x1=int(hand_landmarks[0].x*width)
        y1=int(hand_landmarks[0].y*height)
        
        cv.circle(modified_image, (x1, y1), 6, (255, 255, 255), 4)  
        
        

        text_x = int(min(x_coords) * width)
        text_y = int(min(y_coords) * height) - MARGIN

        cv.putText(
            modified_image,
            detectionID[0].category_name,
            (text_x, text_y),
            cv.FONT_HERSHEY_DUPLEX,
            FONT_SIZE,
            HANDEDNESS_TEXT_COLOR,
            FONT_THICKNESS,
            cv.LINE_AA
        )

    return modified_image

# ABRIR CAMARA
source = cv.VideoCapture(0)
nombre_ventana = 'Hand Tracking'
cv.namedWindow(nombre_ventana, cv.WINDOW_NORMAL)


# LOOP PRINCIPAL
while cv.waitKey(1) != 27:
    has_frame, frame = source.read()

    if not has_frame:
        break

    frame = cv.flip(frame, 1)
    
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

    # Mostrar
    cv.imshow(nombre_ventana, annotated_frame)


source.release()
cv.destroyAllWindows()


