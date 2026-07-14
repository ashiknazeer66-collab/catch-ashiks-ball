# 🎮 Gesture Ball Sort AI

A gesture-controlled Ball Sort Puzzle game built using **Python**, **Pygame**, **OpenCV**, and **MediaPipe**.

Instead of using a mouse or keyboard, players control the game with **hand gestures**. The webcam tracks the user's hand in real time, allowing them to pick and move colored balls using a simple pinch gesture.

This project demonstrates the combination of **computer vision**, **gesture recognition**, and **game development** to create a touchless gaming experience.

## Features

- Hand tracking using MediaPipe
- Finger cursor control
- Pinch gesture detection
- Pick and drop balls
- Ball Sort game rules
- Real-time gameplay

- ## Technologies Used

- Python
- Pygame
- OpenCV
- MediaPipe

- ## Screenshot

![Game Screenshot](assets/screenshot1.png)

## Gameplay

![Gameplay](assets/gameplay.gif)




## Project Workflow

1. The webcam captures the user's hand.
2. MediaPipe detects the hand landmarks.
3. The index finger controls the cursor.
4. A pinch gesture is detected when the thumb and index finger come close together.
5. The player picks the top ball from the selected tube.
6. Moving the hand changes the selected tube.
7. Releasing the pinch drops the ball into the selected tube if the move is valid.
8. The game follows Ball Sort Puzzle rules and updates the screen in real time.
