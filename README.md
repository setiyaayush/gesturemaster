1. Neutral Mode (N)
   State: Default state when no specific action is being performed.
   Finger Gesture: No fingers are raised ([0, 0, 0, 0, 0]).
   Usage:
   Acts as a resting mode.
   Resets any active mode when a neutral gesture is detected.
2. Scroll Mode (Scroll)
   Gesture to Enter:

Index finger raised alone ([0, 1, 0, 0, 0]), or
Index and middle fingers raised ([0, 1, 1, 0, 0]).
Actions:

Scroll Up: Keep only the index finger raised ([0, 1, 0, 0, 0]).
Moves the screen upward.
Scroll Down: Raise both the index and middle fingers ([0, 1, 1, 0, 0]).
Moves the screen downward.
Exit Scroll Mode: Close your hand ([0, 0, 0, 0, 0]). 3. Volume Control Mode (Volume)
Gesture to Enter:

Raise the thumb and index finger ([1, 1, 0, 0, 0]).
Actions:

Control Volume:
Use your thumb and index finger to make a pinch gesture.
The distance between the two fingers adjusts the volume:
Closer fingers = Lower volume.
Further apart fingers = Higher volume.
The volume bar and percentage will update on the screen.
Exit Volume Mode: Raise the pinky finger (fingers[-1] == 1). 4. Cursor Mode (Cursor)
Gesture to Enter:

Raise all fingers ([1, 1, 1, 1, 1]).
Actions:

Control the Cursor:
Use the tip of your index finger (lmList[8]) to control the cursor.
Move your hand to guide the cursor's position on the screen.
Click:
Lower your thumb (fingers[0] == 0).
Exit Cursor Mode: Lower all fingers except the thumb ([0, 0, 0, 0, 0]).
Switching Between Modes
To switch between modes, use the gestures specified for entering each mode.
For example: From Scroll mode, make the Volume gesture ([1, 1, 0, 0, 0]) to switch directly to Volume mode.


To install dependencies :
pip install -r requirements.txt
