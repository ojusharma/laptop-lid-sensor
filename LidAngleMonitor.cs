using System;
using Windows.Devices.Sensors;

public class LidAngleMonitor
{
    private Inclinometer _inclinometer;

    public void StartMonitoring()
    {
        _inclinometer = Inclinometer.GetDefault();

        if (_inclinometer != null)
        {
            Console.WriteLine("Inclinometer detected successfully.");
            _inclinometer.ReportInterval = Math.Max(50, _inclinometer.MinimumReportInterval);

            var reading = _inclinometer.GetCurrentReading();
            if (reading != null)
            {
                PrintReading(reading.PitchDegrees, reading.RollDegrees, reading.YawDegrees);
            }

            _inclinometer.ReadingChanged += Inclinometer_ReadingChanged;
        }
        else
        {
            Console.WriteLine("Inclinometer not found.");
        }
    }

    private void Inclinometer_ReadingChanged(Inclinometer sender, InclinometerReadingChangedEventArgs args)
    {
        var r = args.Reading;
        PrintReading(r.PitchDegrees, r.RollDegrees, r.YawDegrees);
    }

    private static void PrintReading(float pitch, float roll, float yaw)
    {
        Console.WriteLine($"Pitch: {pitch,7:F2}°  |  Roll: {roll,7:F2}°  |  Yaw: {yaw,7:F2}°");
    }

    public void StopMonitoring()
    {
        if (_inclinometer != null)
        {
            _inclinometer.ReadingChanged -= Inclinometer_ReadingChanged;
        }
    }
}
