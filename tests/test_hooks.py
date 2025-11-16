Unit tests for OS hooks.
Checks if hooks are properly installed and events are captured.
"""
import unittest
from src.sensor.windows_hook import WindowsAPIHook


class TestWindowsHook(unittest.TestCase):
    def test_createprocess_hook(self):
        hook = WindowsAPIHook()
