## main script to run on the raspi

## IMPORT Files

import audio
import camera
import fingerprint
import rfid
import helpers
import helpers

## IMPORT Libraries

import tensorflow as tf
import numpy as np

Users = ["MoritzG", "MoritzR", "Jonathan", "Nico", "Simon", "Gabriel", "Sonstige"]


## Variables

def main():

    ## Eingabezeile leeren
    helpers.clear_screen()


    ## Initialisierung der Komponenten
    print("Starting up...")
    audio.init()
    camera.init()
    fingerprint.init()
    rfid.init()



    ## cyclic programm
    while True:
        
        

if __name__ == "__main__":
    main()
