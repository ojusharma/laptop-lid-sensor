from alarm_config import AlarmConfig
from lid_angle_monitor import LidAngleMonitor


def main():
    config = AlarmConfig.load("config.json")

    print("=== Laptop Tilt Alarm (Python) ===")
    print(f"Thresholds  ->  Pitch: {config.pitch_threshold}\u00b0  Roll: {config.roll_threshold}\u00b0  Yaw: {config.yaw_threshold}\u00b0")
    print(f"Hysteresis  ->  {config.hysteresis_buffer}\u00b0 buffer")
    print(f"Priority    ->  {' > '.join(config.priority)}")
    print(f"Audio files ->  Pitch: {config.pitch_audio_file}  Roll: {config.roll_audio_file}  Yaw: {config.yaw_audio_file}")
    print()
    print("Place your MP3 files in the audio/ folder.")
    print("Press Enter to stop monitoring.")
    print()

    monitor = LidAngleMonitor(config)
    monitor.start_monitoring()

    try:
        input()
    except KeyboardInterrupt:
        pass

    monitor.cleanup()
    print()
    print("Monitoring stopped!")


if __name__ == "__main__":
    main()
