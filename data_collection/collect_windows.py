Data collection script for Windows.
Logs API calls from monitored processes.
"""
from src.sensor.windows_hook import WindowsAPIHook
import time

def collect_windows_data(output_path: str):
    hook = WindowsAPIHook()
    # TODO: Запуск мониторинга и запись в output_path
    print(f"Collecting data on Windows. Saving to {output_path}")
    time.sleep(10)  # Пример
    print("Data collection completed")

if __name__ == "__main__":
    collect_windows_data("dataset/windows_data.jsonl")
