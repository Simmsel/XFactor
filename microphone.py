## IMPORTS
import pyaudio
import wave
import numpy as np
import tensorflow as tf
from scipy.io import wavfile
from scipy.fft import fft
import os


##YAMNet for audio calssification? Make keyword checking instead of voice recognition?


Users = ["MoritzG", "MoritzR", "Jonathan", "Nico", "Simon", "Gabriel", "Sonstige"]


def init():
    print("Initializing audio connection")

    audio = pyaudio.PyAudio()
    device_count = audio.get_device_count()
    print(f"available audio-devices: {device_count}")

    mic_found = False
    for i in range(device_count):
        device_info = audio.get_device_info_by_index(i)
        if device_info['maxInputChannels'] > 0:
            mic_found = True
            print(f"Microphone detected: {device_info['name']} (Device {i})")
            break

    if not mic_found:
        print("No nicrophone detected. Please check the connection.")
    audio.terminate()
    return mic_found



## Funktion zum Aufnehmen von Audiospuren

def record_audio(filename='output.wav', duration=5, chunk=1024, channels=1, rate=44100):
    audio = pyaudio.PyAudio()

    stream = audio.open(format=pyaudio.paInt16,
                        channels=channels,
                        rate=rate,
                        input=True,
                        frames_per_buffer=chunk)

    print("Aufnahme gestartet...")
    frames = []

    for _ in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    print("Aufnahme beendet.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))

    print(f"Aufnahme gespeichert als {filename}")


def delete_audio(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


def verify():
    detected_user = ""

    ## do verification here
    #
    ## Load audio file
    # sample_rate, data = wavfile.read('audio_file.wav')

    # Perform FFT
    # fft_result = fft(data)
    #
    #
    #
    #
    #
    #
    #


    return detected_user
