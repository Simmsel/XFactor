# IMPORTS
from mfrc522 import SimpleMFRC522


tag_database = {
    1069488694246: "Simon",
    588620194713: "Jonathan",
    932268172086: "Nico",
    108591145915: "MoritzR",
    660828676947: "MoritzG"
}


def init():
    try:
        reader = SimpleMFRC522()
        print("Initialization of RFID-reader was successfull") 
    except Exception as e:
        print(f"Error initializing RFID-reader: {e}")
    return


def verify():
    reader = SimpleMFRC522()
    tag_id, _ = reader.read()
    if tag_id in tag_database: 
        return tag_database[tag_id]
    else:
        return "UNKNOWN"
