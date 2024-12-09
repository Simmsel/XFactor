from picamera2 import Picamera2
from datetime import datetime
import os
import cv2
import torch
import numpy as np
import time
from facenet_pytorch import InceptionResnetV1, MTCNN
from torchvision import transforms
from PIL import Image
from scipy.spatial.distance import cosine


Users = ["Jonathan", "MoritzG", "MoritzR", "Nico", "Simon", "Gabriel", "Sonstige"]
PIC_COUNT = 5

camera = Picamera2()


def init():
    
    global camera

    
    if camera is None:
        raise RuntimeError("Camera not available")
    try:
        config = camera.create_still_configuration(
        #main={"size": (1920, 1080)}  # Setze die Auflösung auf 640x480 (ändern nach Bedarf)
        main={"size": (640, 480)}
        )
        camera.configure(config)  # Konfiguriere die Kamera im "Still"-Modus (für Fotos)
        #camera.start()  # Starte die Kamera
        print("camera initialization successfull")
    except:
        print("Error during Initilization of camera")
        

def take_picture(save_path="/home/pi/XFactor/data/Pictures/"):
    
    global camera

    camera.start()


    if save_path.endswith(".jpg"):
        file_path = save_path
    else:
        # create filename with timestamp and ending
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(save_path, f"Pic_{timestamp}.jpg")

    # take picture and save
    camera.capture_file(file_path)
    # print(f"Picture saved under: {file_path}")
    
    # stop camera
    return file_path


def delete_picture(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


def make_dataset(path, set_size = 20):
    
    # required LED imports
    from main import LEDs
    import RPi.GPIO as GPIO
    import led
    import time
    
    # led setup
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    for l in LEDs:
            led.init_gpio(l)
    
    if path == None:
        print("please specify a path!")
        return
               
    if not os.path.exists(path):
        os.makedirs(path)
    
    print("collection of dataset begins shortly")
    time.sleep(3)
    
    for i in range(1, set_size):
        
        # make all lights off
        for l in LEDs:
            led.led_control(l)
        
        # count down for lights on
        for l in LEDs:
            time.sleep(0.5)
            led.led_control(l, GPIO.HIGH)
            
        time.sleep(0.6)
        
        file_path = os.path.join(path, f"Pic_{i}.jpg")
        take_picture(file_path)
        
        # make all lights off
        for l in LEDs:
            led.led_control(l)
        time.sleep(0.3)
        
        # make all lights on
        for l in LEDs:
            led.led_control(l, GPIO.HIGH)
        time.sleep(0.3)
        
        # make all lights off
        for l in LEDs:
            led.led_control(l)
        time.sleep(0.3)
            
        # make all lights on
        for l in LEDs:
            led.led_control(l, GPIO.HIGH)
        time.sleep(0.3)
        
        print(f"Progress: {i} / {set_size}")


def identify_person(embedding, train_embeddings, train_labels, threshold=0.30):
    min_distance = float('inf')
    label = "Unbekannt"
    probability = 0

    for i, train_embedding in enumerate(train_embeddings):
        distance = cosine(embedding, train_embedding)
        if distance < min_distance and distance < threshold:
            min_distance = distance
            label = train_labels[i]
            probability = 1 - distance  # Höhere Wahrscheinlichkeit bei kleinerem Abstand
    return label, probability


def verify():
    camera.start()
    print("Model is being imported...")
    # Initialisiere das FaceNet-Modell und den MTCNN-Detektor
    model = InceptionResnetV1(pretrained='vggface2').eval()
    mtcnn = MTCNN(keep_all=True)  # Aktiviert die Erkennung aller Gesichter im Bild
    
    # Transformation für Bildvorverarbeitung
    transform = transforms.Compose([
    transforms.Resize((160, 160)),
    transforms.ToTensor(),
    transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
    ])
    
    # Lade die trainierten Embeddings und Labels
    train_embeddings = np.load("/home/pi/XFactor/data/updated_train_embeddings.npy")
    train_labels = np.load("/home/pi/XFactor/data/updated_labels.npy")

    # Zähler für erkannte Personen, speichert auch die letzte Übereinstimmung
    recognition_count = {label: {"count": 0, "last_prob": 0} for label in train_labels}
    
    detected_user = ""
        
    print("Taking pictures...")
        
    #while True:
    for i in range(PIC_COUNT):
        print(f"Iteration {i+1} von {PIC_COUNT}")
        print(i)
        # Nimm ein Bild von der Kamera
        
        frame = camera.capture_array()  # Capture frame als NumPy Array
        if frame is None:
            break
        # Konvertiere das Bild von RGB (von Picamera2) nach BGR (für OpenCV)
        rgb_frame = frame  # Picamera2 gibt bereits ein RGB-Bild zurück
        bgr_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)
        # cv2.imshow("Display1", frame)
        # Erkenne Gesichter im Bild
        boxes, probs = mtcnn.detect(rgb_frame)  # Gibt Bounding Boxen und Wahrscheinlichkeiten zurück
        if boxes is not None:
            for box in boxes:
                # Überprüfe, ob die Bounding Box innerhalb der Bildgrenzen liegt
                x1, y1, x2, y2 = [int(coord) for coord in box]
                if x1 < 0 or y1 < 0 or x2 > bgr_frame.shape[1] or y2 > bgr_frame.shape[0]:
                    continue  # Überspringe diese Box, wenn sie ungültig ist
                    
                box_width = x2 - x1
                if box_width < 100:
                    print(f"Gesicht zu weit entfernt, Breite {box_width}")
                    time.sleep(1)
                    continue

                # Schneide das Gesicht aus
                face = bgr_frame[y1:y2, x1:x2]  # Das Gesicht ausschneiden
                if face.size == 0:
                    continue  # Überspringe, falls das Gesicht leer ist

                # Konvertiere das ausgeschnittene Gesicht in ein PIL-Bild für die Transformation
                face_pil = Image.fromarray(cv2.cvtColor(face, cv2.COLOR_BGR2RGB))
                image_tensor = transform(face_pil).unsqueeze(0)

                # Berechne das Embedding für das ausgeschnittene Gesicht
                with torch.no_grad():
                    embedding = model(image_tensor).numpy().flatten()

                # Identifiziere die Person und berechne die Wahrscheinlichkeit
                person_label, probability = identify_person(embedding, train_embeddings, train_labels)
                # Wenn eine bekannte Person erkannt wird, aktualisiere den Zähler und die Übereinstimmung
                if person_label != "Unbekannt":
                    recognition_count[person_label]["count"] += 1
                    recognition_count[person_label]["last_prob"] = probability
                print(person_label, probability) # new
                
                # Zeige das Gesicht und den Namen sowie die Wahrscheinlichkeit
                cv2.putText(bgr_frame, f"Person: {person_label}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(bgr_frame, f"Probability: {probability:.2f}", (x1, y1 + 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Zeige den Zähler für die Erkennungen am oberen Rand, inkl. Übereinstimmung
        y_offset = 30  # Startposition für den Zähler
        for label, data in recognition_count.items():
            count = data["count"]
            last_prob = data["last_prob"]
            cv2.putText(bgr_frame, f"{label}: {count} (Accuracy: {last_prob:.2f})", (50, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            y_offset += 20  # Abstand zwischen den Zählern

        # Zeige den Videoframe
        # cv2.imshow("Face Recognition", bgr_frame)
        # Beende den Stream mit der 'q'-Taste
        
        #pil_image = Image.fromarray(bgr_frame)  # NumPy Array in PIL Image konvertieren

        # Zeige das Bild mit PIL (Pillow)
        #pil_image.show()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    # Stoppe die Kamera und schließe das Fenster
    camera.stop()
    
    print(recognition_count)
    max_count = -1
    max_label = None

    # Durchlaufe das Dictionary
    for label, values in recognition_count.items():
        count = values["count"]
        
        # Überprüfe, ob der count größer als 3 ist und ob es der höchste ist
        if count > 2 and count > max_count:
            max_count = count
            max_label = label

    # Gib das Label mit dem höchsten count aus
    if max_label:
        print(f"Das Label mit dem höchsten count über 3 ist: {max_label} mit count {max_count}")
        return max_label
    else:
        print("Kein Label hat einen count größer als 3.")
        
    
    
if __name__ == "__main__":
    init()


