import os


# clear the terminal
def clear_screen():
    # Check for the OS
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Linux und macOS
        os.system('clear')