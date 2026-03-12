import sys
import time
import threading

from winrt.windows.devices.sensors import Inclinometer

from alarm_config import AlarmConfig, AlarmAxis
from audio_alarm import AudioAlarm


class LidAngleMonitor:
    def __init__(self, config: AlarmConfig):
        self._config = config
        self._audio = AudioAlarm()
        self._active_alarm = AlarmAxis.NONE
        self._running = False

        # Parse priority list from config strings to AlarmAxis enum
        axis_map = {"pitch": AlarmAxis.PITCH, "roll": AlarmAxis.ROLL, "yaw": AlarmAxis.YAW}
        self._priority_order = [
            axis_map[s.lower()] for s in config.priority if s.lower() in axis_map
        ]

        self._inclinometer = Inclinometer.get_default()

    def start_monitoring(self) -> None:
        if self._inclinometer is None:
            print("Inclinometer not found.")
            return

        print("Inclinometer detected successfully.")
        min_interval = self._inclinometer.minimum_report_interval
        self._inclinometer.report_interval = max(self._config.report_interval_ms, min_interval)

        self._running = True
        self._thread = threading.Thread(target=self._poll_loop, daemon=True)
        self._thread.start()

    def _poll_loop(self) -> None:
        interval = self._config.report_interval_ms / 1000.0
        while self._running:
            reading = self._inclinometer.get_current_reading()
            if reading is not None:
                self._process_reading(
                    reading.pitch_degrees,
                    reading.roll_degrees,
                    reading.yaw_degrees,
                )
            time.sleep(interval)

    def _process_reading(self, pitch: float, roll: float, yaw: float) -> None:
        # If an alarm is active, check if it resolved (below threshold - hysteresis)
        if self._active_alarm != AlarmAxis.NONE:
            value = self._get_axis_value(self._active_alarm, pitch, roll, yaw)
            resolve_at = (
                self._config.get_threshold(self._active_alarm)
                - self._config.hysteresis_buffer
            )
            if abs(value) < resolve_at:
                self._audio.stop()
                self._active_alarm = AlarmAxis.NONE

        # If no alarm active, check axes in priority order for a breach
        if self._active_alarm == AlarmAxis.NONE:
            for axis in self._priority_order:
                value = self._get_axis_value(axis, pitch, roll, yaw)
                threshold = self._config.get_threshold(axis)
                if abs(value) >= threshold:
                    self._active_alarm = axis
                    audio_file = self._config.get_audio_file(axis)
                    self._audio.play(audio_file)
                    break

        self._print_reading(pitch, roll, yaw)

    @staticmethod
    def _get_axis_value(axis: AlarmAxis, pitch: float, roll: float, yaw: float) -> float:
        return {
            AlarmAxis.PITCH: pitch,
            AlarmAxis.ROLL: roll,
            AlarmAxis.YAW: yaw,
        }.get(axis, 0.0)

    def _print_reading(self, pitch: float, roll: float, yaw: float) -> None:
        if self._active_alarm != AlarmAxis.NONE:
            status = f"ALARM: {self._active_alarm.value}"
        else:
            status = "OK"

        sys.stdout.write(
            f"\rPitch: {pitch:7.2f}\u00b0  |  Roll: {roll:7.2f}\u00b0  |  Yaw: {yaw:7.2f}\u00b0  |  [{status}]    "
        )
        sys.stdout.flush()

    def stop_monitoring(self) -> None:
        self._running = False
        self._audio.stop()

    def cleanup(self) -> None:
        self.stop_monitoring()
        self._audio.cleanup()
