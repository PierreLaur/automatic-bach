import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from pygame import mixer
import time


class Player:
    def __init__(self) -> None:
        self.notes = []
        pygame.init()
        pygame.mixer.set_num_channels(50)
        for n in range(1, 26):
            self.notes.append(mixer.Sound(f'notes/Piano1{n}.mp3'))

    def play_chord(self, chord):
        for note in chord:
            self.notes[note].set_volume(0.5)
            self.notes[note].play(0, 2000)

    def play_note(self, note):
        self.notes[note].set_volume(1.0)
        self.notes[note].play(0, 2000)

    def stop_playing(self):
        time.sleep(1)
