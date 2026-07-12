import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0)


def get_finger_position():

    success, frame = cap.read()

    if not success:
        return None

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    x = None
    y = None

    if results.multi_hand_landmarks:

        for hand in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

            index_tip = hand.landmark[8]
            thumb_tip = hand.landmark[4]

            h, w, _ = frame.shape
            thumb_x = int(thumb_tip.x * w)
            thumb_y = int(thumb_tip.y * h)

            x = int(index_tip.x * w)
            y = int(index_tip.y * h)
            # Distance between thumb and index finger
            distance = ((thumb_x - x) ** 2 + (thumb_y - y) ** 2) ** 0.5

            cv2.circle(frame, (x, y), 12, (0, 0, 255), -1)
            # Show pinch status
            if distance < 40:
                cv2.putText(
                    frame,
                    "PINCH!",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2,
                )
            cv2.circle(frame, (thumb_x, thumb_y), 12, (0, 255, 0), -1)

    cv2.imshow("Hand Tracker", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        return None

    pinching = False

    if x is not None and y is not None:
        if distance < 40:
            pinching = True

    return x, y, pinching


if __name__ == "__main__":

    while True:

        position = get_finger_position()

        print(position)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
