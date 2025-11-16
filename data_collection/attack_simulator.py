Simulates malicious API call sequences.
Runs in isolated environment.
"""
import json

def simulate_promptflux_attack():
    """Simulates PROMPTFLUX-style attack via LLM."""
    attack_sequence = [
        {"api": "CreateProcess", "args": ["cmd.exe", "/c", "echo malicious"]},
        {"api": "WriteProcessMemory", "args": ["inject.dll"]}
    ]
    return attack_sequence

def save_attack_sample(output_path: str):
    sample = {
        "process": "python.exe",
        "api_sequence": simulatepromptflux_attack(),
        "label": "malicious",
        "context": "LLM-generated code injection"
    }
    with open(output_path, 'a') as f:
        f.write(json.dumps(sample) + '\n')

if __name__ == "__main__":
    save_attack_sample("dataset/attack_sample.jsonl")
