from picamera2 import Picamera2
import cv2
import torch
import numpy as np
import time
from facenet_pytorch import InceptionResnetV1, MTCNN
from torchvision import transforms
from PIL import Image
from scipy.spatial.distance import cosine

PIC_COUNT = 5

camera = Picamera2()


# Initialize camera and check if it is detected
def init():
    
    global camera
    
    if camera is None:
        raise RuntimeError("Camera not available")
    try:
        config = camera.create_still_configuration(
        main={"size": (640, 480)}
        )
        camera.configure(config)
        print("camera initialization successfull")
    except:
        print("Error during Initilization of camera")
        

# return the detected user
def identify_person(embedding, train_embeddings, train_labels, threshold=0.30):
    min_distance = float('inf')
    label = "Unknown"
    probability = 0

    for i, train_embedding in enumerate(train_embeddings):
        distance = cosine(embedding, train_embedding)
        if distance < min_distance and distance < threshold:
            min_distance = distance
            label = train_labels[i]
            probability = 1 - distance  # Higher probability with bigger distance
    return label, probability


# camera setup, loading of the model and evaluating
def verify():
    camera.start()
    print("Model is being imported...")
    # Initialize the FaceNet-Modell and the MTCNN-Detector
    model = InceptionResnetV1(pretrained='vggface2').eval()
    mtcnn = MTCNN(keep_all=True)  # Activate recognition of all faces in the picture
    
    # transformation for image recognition
    transform = transforms.Compose([
    transforms.Resize((160, 160)),
    transforms.ToTensor(),
    transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
    ])
    
    # Load trained embeddings and labels
    train_embeddings = np.load("/home/pi/XFactor/data/updated_train_embeddings.npy")
    train_labels = np.load("/home/pi/XFactor/data/updated_labels.npy")

    # Counter for detected persons, also saves last match
    recognition_count = {label: {"count": 0, "last_prob": 0} for label in train_labels}
    
    detected_user = ""
        
    print("Taking pictures...")
        
    for i in range(PIC_COUNT):
        print(f"Iteration {i+1} von {PIC_COUNT}")
        print(i)

        
        frame = camera.capture_array()  # Capture frame als NumPy Array
        if frame is None:
            break
        # Convert picture from RGB (Picamera2) to BGR (OpenCV)
        rgb_frame = frame
        bgr_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)
        # Detect faces in the picture
        boxes, probs = mtcnn.detect(rgb_frame)  # Returns bounding box and probabilitiy
        if boxes is not None:
            for box in boxes:
                # Check if bounding box is within the picture borders
                x1, y1, x2, y2 = [int(coord) for coord in box]
                if x1 < 0 or y1 < 0 or x2 > bgr_frame.shape[1] or y2 > bgr_frame.shape[0]:
                    continue  # Skip if picture is unvalid
                    
                box_width = x2 - x1
                if box_width < 100:
                    print(f"Face too far away, width: {box_width}")
                    time.sleep(1)
                    continue

                # Cut the face
                face = bgr_frame[y1:y2, x1:x2]
                if face.size == 0:
                    continue  # skip if face is empty
                
                # Convert the cut face to PIL-Picture for transformation
                face_pil = Image.fromarray(cv2.cvtColor(face, cv2.COLOR_BGR2RGB))
                image_tensor = transform(face_pil).unsqueeze(0)

                # calculate embedding for the cut face
                with torch.no_grad():
                    embedding = model(image_tensor).numpy().flatten()

                # identify person and calculate probability
                person_label, probability = identify_person(embedding, train_embeddings, train_labels)
                # if person detected refresh counter and probability
                if person_label != "Unbekannt":
                    recognition_count[person_label]["count"] += 1
                    recognition_count[person_label]["last_prob"] = probability
                print(person_label, probability) # new
                
                # Show face, name and probabiliy
                cv2.putText(bgr_frame, f"Person: {person_label}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(bgr_frame, f"Probability: {probability:.2f}", (x1, y1 + 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Show counter
        y_offset = 30  # Startposition for counter
        for label, data in recognition_count.items():
            count = data["count"]
            last_prob = data["last_prob"]
            cv2.putText(bgr_frame, f"{label}: {count} (Accuracy: {last_prob:.2f})", (50, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            y_offset += 20  # Distance between counter

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Stop camera and close window
    camera.stop()
    
    print(recognition_count)
    max_count = -1
    max_label = None

    # walk through the dictionary
    for label, values in recognition_count.items():
        count = values["count"]
        
        # Check if counter is bigger than 3 and if it is the biggest one
        if count > 2 and count > max_count:
            max_count = count
            max_label = label

    # return label with highest count
    if max_label:
        print(f"The label with the highest count above 3 is: {max_label} with count {max_count}")
        return max_label
    else:
        print("There is no label with a count higher than 3.")
