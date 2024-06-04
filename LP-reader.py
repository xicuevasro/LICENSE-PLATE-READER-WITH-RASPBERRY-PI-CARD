import cv2
import openalpr
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

# Initialiser la caméra et capturer une référence brute de l'image
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(640, 480))

# Autoriser la caméra à démarrer
time.sleep(0.1)

# Initialiser l'instance OpenALPR
alpr = openalpr.Alpr("us", "/etc/openalpr/openalpr.conf", "/usr/share/openalpr/runtime_data")
if not alpr.is_loaded():
    print("Erreur de chargement OpenALPR")
    exit()

alpr.set_top_n(20)

# Capture de l'image
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array

    # Convertir l'image en image OpenALPR
    results = alpr.recognize_array(image)

    # Afficher les résultats
    for plate in results['results']:
        print(f"Plaque détectée: {plate['plate']}")
        print(f"Confiance: {plate['confidence']}")
        print("")

    # Afficher l'image
    cv2.imshow("Image", image)
    
    # Si 'q' est pressé, quitter la boucle
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

    # Effacer le flux pour la prochaine image
    rawCapture.truncate(0)

# Libérer les ressources
camera.close()
alpr.unload()
cv2.destroyAllWindows()
