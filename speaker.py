import pygame


# play an audio sound
def play_sound(file_path):

    # initialize pygame
    pygame.mixer.init()
    
    # load and play sound file
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
