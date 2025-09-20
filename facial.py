import cv2
import time
import requests

# Haar Cascades
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade  = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')  # mais robusto

# Configurações
video_path = "video.mp4"
both_time = 2.0
node_red_url = "http://localhost:1880/both_eyes_closed"
notify_cooldown = 10.0

both_closed_since = None
last_notify = 0

cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("Erro ao abrir vídeo:", video_path)
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        # Foco na parte superior do rosto (onde estão os olhos)
        upper_face_gray = gray[y:y + h//2, x:x + w]
        upper_face_color = frame[y:y + h//2, x:x + w]

        eyes = eye_cascade.detectMultiScale(upper_face_gray, scaleFactor=1.1, minNeighbors=5)

        # Lógica de olhos fechados
        left_eye_closed = False
        right_eye_closed = False

        if len(eyes) == 0:
            left_eye_closed = True
            right_eye_closed = True
        elif len(eyes) == 1:
            left_eye_closed = True  # simplificação
        else:
            left_eye_closed = False
            right_eye_closed = False

        # Desenhar landmarks amarelos e texto
        if left_eye_closed or right_eye_closed:
            cv2.putText(frame, "Olho Fechado", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h//2), (0, 255, 255), 2)

        # Temporizador para ambos olhos fechados
        if left_eye_closed and right_eye_closed:
            if both_closed_since is None:
                both_closed_since = time.time()
            elapsed = time.time() - both_closed_since
            cv2.putText(frame, f"Ambos fechados: {elapsed:.2f}s", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 200, 255), 2)
            if elapsed >= both_time and (time.time() - last_notify) > notify_cooldown:
                try:
                    requests.post(node_red_url, json={"event": "both_eyes_closed", "duration": elapsed})
                    print("[Node-RED] Notificado!")
                    last_notify = time.time()
                except:
                    print("[Node-RED] Erro ao notificar")
        else:
            both_closed_since = None

    cv2.imshow("Deteccao de Piscadas", frame)
    if cv2.waitKey(30) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
