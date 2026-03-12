import json
import os
from enum import Enum


class AlarmAxis(Enum):
    NONE = "None"
    PITCH = "Pitch"
    ROLL = "Roll"
    YAW = "Yaw"


class AlarmConfig:
    def __init__(self):
        self.pitch_threshold: float = 30.0
        self.roll_threshold: float = 30.0
        self.yaw_threshold: float = 30.0
        self.hysteresis_buffer: float = 5.0
        self.priority: list[str] = ["Pitch"]
        self.pitch_audio_file: str = "audio/pitch.mp3"
        self.roll_audio_file: str = "audio/roll.mp3"
        self.yaw_audio_file: str = "audio/yaw.mp3"
        self.report_interval_ms: int = 50

    @staticmethod
    def load(path: str) -> "AlarmConfig":
        config = AlarmConfig()
        if not os.path.exists(path):
            print(f"Config file not found at '{path}', using defaults.")
            return config

        with open(path, "r") as f:
            data = json.load(f)

        config.pitch_threshold = float(data.get("pitchThreshold", 30.0))
        config.roll_threshold = float(data.get("rollThreshold", 30.0))
        config.yaw_threshold = float(data.get("yawThreshold", 30.0))
        config.hysteresis_buffer = float(data.get("hysteresisBuffer", 5.0))
        config.priority = data.get("priority", ["Pitch"])
        config.pitch_audio_file = data.get("pitchAudioFile", "audio/pitch.mp3")
        config.roll_audio_file = data.get("rollAudioFile", "audio/roll.mp3")
        config.yaw_audio_file = data.get("yawAudioFile", "audio/yaw.mp3")
        config.report_interval_ms = int(data.get("reportIntervalMs", 50))

        return config

    def get_threshold(self, axis: AlarmAxis) -> float:
        return {
            AlarmAxis.PITCH: self.pitch_threshold,
            AlarmAxis.ROLL: self.roll_threshold,
            AlarmAxis.YAW: self.yaw_threshold,
        }.get(axis, float("inf"))

    def get_audio_file(self, axis: AlarmAxis) -> str:
        return {
            AlarmAxis.PITCH: self.pitch_audio_file,
            AlarmAxis.ROLL: self.roll_audio_file,
            AlarmAxis.YAW: self.yaw_audio_file,
        }.get(axis, "")
