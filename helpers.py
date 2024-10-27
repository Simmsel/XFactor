import os

def clear_screen():
    # Prüfen, welches Betriebssystem verwendet wird
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Linux und macOS
        os.system('clear')