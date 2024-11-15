import cv2
import torch
import numpy as np
from facenet_pytorch import InceptionResnetV1, MTCNN
from torchvision import transforms
from PIL import Image
from scipy.spatial.distance import cosine
from picamera2 import Picamera2  # Importiere Picamera2

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
train_embeddings = np.load("train_embeddings.npy")
train_labels = np.load("train_labels.npy")

# Zähler für erkannte Personen, speichert auch die letzte Übereinstimmung
recognition_count = {label: {"count": 0, "last_prob": 0} for label in train_labels}

# Kosinus-Ähnlichkeitsmaß zur Identifizierung der Person
def identify_person(embedding, train_embeddings, train_labels, threshold=0.25):
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

# Initialisiere die Kamera mit Picamera2
picam2 = Picamera2()  # Instanziiere Picamera2
config = picam2.create_still_configuration(
    #main={"size": (1920, 1080)}  # Setze die Auflösung auf 640x480 (ändern nach Bedarf)
    main={"size": (640, 480)}
)
picam2.configure(config)  # Konfiguriere die Kamera im "Still"-Modus (für Fotos)
picam2.start()  # Starte die Kamera

i = 0

#while True:
for i in range(50):
    i = i+1
    print(i)
    # Nimm ein Bild von der Kamera
    frame = picam2.capture_array()  # Capture frame als NumPy Array
    
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
picam2.stop()
cv2.destroyAllWindows()
