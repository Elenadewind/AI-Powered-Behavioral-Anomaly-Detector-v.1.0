Dataset Builder for Behavioral Anomaly Detection

Usage:
    builder = DatasetBuilder('dataset.jsonl')
    builder.add_sample('chrome.exe', [...], 'legitimate')
"""
import json
import os

class DatasetBuilder:
    def __init__(self, output_path: str):
        self.output_path = output_path
        # Ensure file exists
        if not os.path.exists(self.output_path):
            with open(self.output_path, 'w') as f:
                f.write("")  # Create empty file

    def add_sample(self, process_name: str, api_calls: list, label: str):
        """
        Add a sample to the dataset.

        Args:
            process_name: Name of the process (e.g., 'chrome.exe')
            api_calls: List of API call dicts [{'api': '...', 'args': [...]}]
            label: 'legitimate' or 'malicious'
        """
        sample = {
            "process": process_name,
            "api_sequence": api_calls,
            "label": label
        }
        with open(self.output_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(sample) + '\n')

    def clear(self):
        """Clear the dataset file."""
        with open(self.output_path, 'w') as f:
            pass
