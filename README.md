# XFactor

## Projektdescription

### fingerprint.py

This file includes functions to read a fingerprint into the database, and to verify a user and check whether his fingerprint is in the database

### camera.py

This file performs the face detection by loading a pretrained net and performing the face detection, returning the name of a detected user

### led.py

This file is used to control the LEDs

### microphone.py

This file is performs the passphrase detection by loading a pretrained model and checking whos passphrase was spoken

### rfid.py

This file is used to verify a user by reading his RFID Tag and checking the database for matches

### speaker.py

This face is used to output sound

### motor.py

This file is used to control the servo motor with a PWM signal

### helpers.py

This file contains helping functions such as a function to clear the screen

### main.py

This file contains the main script
