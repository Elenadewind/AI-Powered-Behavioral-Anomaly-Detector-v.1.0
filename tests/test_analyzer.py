import unittest
from src.analyzer.behavioral_analyzer import BehavioralAnalyzer

class TestBehavioralAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = BehavioralAnalyzer(model_path="../models/dummy_model.onnx")

    def test_anomaly_score(self):
        events = [
            {"process": "python.exe", "action": "create_file", "target": "malware.py"},
            {"process": "python.exe", "action": "network_connect", "target": "evil.com"}
        ]
        score = self.analyzer.analyze(events)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)

if __name__ == '__main__':
    unittest.main()
