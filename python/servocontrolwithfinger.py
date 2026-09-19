import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import serial

esp32 = serial.Serial("COM5", 115200)

MODEL_PATH = "hand_landmarker.task"
base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=2,
    min_hand_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

detector = vision.HandLandmarker.create_from_options(options)  

cap = cv2.VideoCapture(0)
print("Apasă tasta 'q' pentru a închide fereastra.")

# Definim coordonatele pentru slider
slider_x_min = 100
slider_x_max = 540
slider_y = 420
while True:
    ret, frame = cap.read()
    if not ret:
        print("Nu pot accesa camera!")
        break

    frame = cv2.flip(frame, 1)

    # Toată logica trebuie să fie în interiorul buclei while (indentată la dreapta)
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_image
    )

    result = detector.detect(mp_image)

    if result.hand_landmarks:
        for hand_index, hand in enumerate(result.hand_landmarks):
            coordonate_puncte = {}
            h, w, c = frame.shape
            #print(f"Rezoluție: {w} x {h}")
            
            for landmark_id, point in enumerate(hand):
                x = int(point.x * w)
                y = int(point.y * h)
                
                coordonate_puncte[landmark_id] = (x, y)

                cv2.circle(
                    frame,                     
                    (x, y),                    
                    5,                         
                    (0, 255, 0),                 
                    cv2.FILLED                       
                )
            if 8 in coordonate_puncte:
                x8, y8 = coordonate_puncte[8]
                #Tranformam pozitia lui 8 in unghiul de rotatie al servomotorului, care are o valoare intre 0 si 180 grade

                angle=int(x8/w*180)
                angle = max(0, min(180, angle))  # Asigură că unghiul este între 0 și 180
                esp32.write(angle.to_bytes(1, 'little'))  # Trimite unghiul la ESP32
                cv2.circle(
                    frame,                     
                    (x8, y8),                    
                    10,                         
                    (0, 0, 255),                 
                    cv2.FILLED                       
                )
                cv2.putText(
                    frame,
                    f"X={x8}",
                    (20,40), #coordonatele textului
                    cv2.FONT_HERSHEY_SIMPLEX, #fontul textului
                    1,
                    (255, 255, 255), #culoarea textului
                    2 #grosimea textului
                    )
                cv2.putText(
                    frame,
                    f"Y={y8}",
                    (20,80), #coordonatele textului
                    cv2.FONT_HERSHEY_SIMPLEX, #fontul textului
                    1,
                    (255, 255, 255), #culoarea textului
                    2 #grosimea textului
                    )
                cv2.putText(
                    frame,
                    f"Unghi={angle}",
                    (20,120), #coordonatele textului
                    cv2.FONT_HERSHEY_SIMPLEX, #fontul textului
                    1,
                    (255, 255, 255), #culoarea textului
                    2 #grosimea textului
                    )
                cv2.line(
                    frame,
                    (slider_x_min, slider_y),
                    (slider_x_max, slider_y),
                    (255, 0, 0),
                    5
                )
            
                slider_position = int(slider_x_min + (slider_x_max - slider_x_min) * (angle / 180))
                cv2.circle(
                    frame,
                    (slider_position, slider_y),
                    12,
                    (0, 255, 0),
                    cv2.FILLED
                )
                cv2.putText(
                    frame,
                    "0°",
                    (slider_x_min - 10, slider_y + 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 255),
                    2
                )

                cv2.putText(
                    frame,
                    "90°",
                    (slider_x_min + 205, slider_y + 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 255),
                    2
                )

                cv2.putText(
                    frame,
                    "180°",
                    (slider_x_max - 20, slider_y + 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 255),
                    2
                )       

                
                    
            

    # Afișarea imaginii trebuie să se facă la fiecare iterație (cadru)
    cv2.imshow("Imaginea", frame)
    
    # waitKey(1) permite afișarea video-ului fluent (așteaptă 1 ms)
    # Ieșim din buclă dacă apăsăm tasta 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Eliberăm camera la final
cap.release()
esp32.close()
cv2.destroyAllWindows()
