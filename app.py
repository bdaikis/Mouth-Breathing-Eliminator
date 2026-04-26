import cv2
import mediapipe as mp
import time

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

UPPER_LIP = 13
LOWER_LIP = 14
LEFT_CORNER = 78
RIGHT_CORNER = 308
OPEN_RATIO_THRESHOLD = 0.3
MOUTH_OPEN_DURATION = 5  # seconds (use 30 later, 5 for testing)

mouth_open_since = None
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0].landmark
        h, w = frame.shape[:2]

        # Get coordinates
        upper = landmarks[UPPER_LIP]
        lower = landmarks[LOWER_LIP]
        left  = landmarks[LEFT_CORNER]
        right = landmarks[RIGHT_CORNER]

        gap   = abs(upper.y - lower.y) * h
        width = abs(left.x - right.x) * w
        ratio = gap / width if width > 0 else 0

        is_open = ratio > OPEN_RATIO_THRESHOLD

        # Timer logic
        if is_open:
            if mouth_open_since is None:
                mouth_open_since = time.time()
            elapsed = time.time() - mouth_open_since
        else:
            mouth_open_since = None
            elapsed = 0

        # Debug display
        color = (0, 0, 255) if is_open else (0, 255, 0)
        status = f"OPEN ({elapsed:.1f}s)" if is_open else "CLOSED"
        cv2.putText(frame, f"Mouth: {status}", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        cv2.putText(frame, f"Ratio: {ratio:.3f}", (30, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 1)

        if elapsed >= MOUTH_OPEN_DURATION:
            cv2.putText(frame, "STOP MOUTH BREATHING", (30, 140),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

    cv2.imshow("Mouth Breathing Detector", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()