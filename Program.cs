using System;

public class Program
{
    public static void Main()
    {
        var monitor = new LidAngleMonitor();

        monitor.StartMonitoring();
        Console.ReadLine();
        monitor.StopMonitoring();
        Console.WriteLine("Monitoring stopped!");
    }
}
