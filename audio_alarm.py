import os

import pygame


class AudioAlarm:
    def __init__(self):
        pygame.mixer.init()
        self._is_playing = False

    @property
    def is_playing(self) -> bool:
        return self._is_playing

    def play(self, file_path: str) -> None:
        self.stop()

        full_path = os.path.abspath(file_path)
        if not os.path.exists(full_path):
            print(f"[AudioAlarm] File not found: {full_path}")
            return

        pygame.mixer.music.load(full_path)
        pygame.mixer.music.play(loops=-1)  # -1 = loop forever
        self._is_playing = True

    def stop(self) -> None:
        if self._is_playing:
            pygame.mixer.music.stop()
        self._is_playing = False

    def cleanup(self) -> None:
        self.stop()
        pygame.mixer.quit()
