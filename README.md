## Motion-switch
Motion-switch is a project built to support individuals with speech impairments or disabilities that make it difficult to use voice-based virtual assistants like Alexa or Siri.
Instead of relying on vocal commands, this system uses hand gestures to perform simple actions, making technology more inclusive and accessible :D

**What it does**
Right now, the project is able to:
Detect and track both hands, but prioritize the right hand when both are visible (this can be adjusted as per user preference).
Read basic hand gestures, aka open and closed fists as ON and OFF signals.
Use an Arduino Uno R3 to move a servo based on those commands.
Run a separate test script that simply detects and labels fingers on both hands.

**⚙ Technologies used**
Python for hand gesture recognition and communication logic
Arduino Uno R3 for hardware control (servo)
Planning to move to Raspberry Pi soon to make the system more portable and remove reliance on a laptop.

**Testing & Development**
Currently, there are a few different parts of the project:

hand_tracking_basic.py:
Handles initial testing, detects hands and labels fingers without connecting to any hardware. Further works on right hand priority. 

hand_tracking_arduino.py:
Connects with Arduino to send commands to a servo motor based on gestures.

arduino.ino:
Arduino code that listens for serial input and controls the servo accordingly.

requirements.txt:
Lists the Python libraries used in this project.

**Future Features (WIP)**
I'm working on adding a sound sensor to detect double claps. The idea is:
Clap twice to activate gesture mode
Once in gesture mode, the system responds to hand gestures
Clap again to turn gesture mode off

However, the Arduino currently struggles with handling both the mic and servo together, the mic’s signal interferes with the servo. I might solve this by using an extra Arduino Nano before fully shifting to Raspberry Pi.

**Help Needed**
The sound sensor part isn’t working well right now. If you know how to cleanly separate mic and servo signals on Arduino, feel free to reach out!

**Contributions**
This project is open for suggestions, improvements, or feedback, especially from those working in accessibility tech or embedded systems.


