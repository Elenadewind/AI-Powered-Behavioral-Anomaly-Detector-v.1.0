Quantizes ONNX model to 4-bit.
Reduces size and inference latency.
"""
from onnxruntime.quantization import quantize_dynamic

def quantize_model(input_model: str, output_model: str):
    quantize_dynamic(input_model, output_model, weight_type=3)  # 4-bit
    print(f!Quantized model saved to {output_model}")


if __name__ == "__main__":
    quantize_model("models/behavioral_model.onnx", "models/quantized_model.onnx")
