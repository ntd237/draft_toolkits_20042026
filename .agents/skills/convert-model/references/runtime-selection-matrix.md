# Runtime Selection Matrix

Use this reference when mapping deployment constraints to likely output formats and conversion chains.

## Hardware-to-Format Mapping

One line per runtime: what it is best for, typical chain, and the main caveat.

- `ONNX`: best generic interchange and fallback when the final runtime is undecided. Preserves optionality; watch for custom operators and dynamic shape issues.
- `TensorRT`: best for NVIDIA GPU when speed matters. Chain `PyTorch -> ONNX -> TensorRT`. Needs matching CUDA/cuDNN/TensorRT and careful shape handling; poor fit for CPU-only.
- `OpenVINO`: best for Intel CPU/iGPU and Intel-centric edge or server. Chain `PyTorch -> ONNX -> OpenVINO IR`. Less compelling for non-Intel targets.
- `TFLite`: best for mobile and lightweight edge CPU, especially TensorFlow-family stacks. Chain `SavedModel -> TFLite` (or via ONNX from PyTorch). Quantization often required for real gains; operator coverage can be weaker for complex models.
- `Core ML`: best for Apple deployment (iPhone, iPad, macOS). Chain `PyTorch -> ONNX or direct tooling -> Core ML`. Poor fit outside the Apple ecosystem.
- `RKNN`: best for Rockchip NPU boards. Chain `PyTorch -> ONNX -> RKNN`. Requires Rockchip toolkit matching the target chip; pointless without Rockchip hardware.
- `Hailo`: best for Hailo accelerators via the Hailo SDK compiler flow (parse, optimize, quantize, compile). Poor fit without Hailo hardware.
- `ncnn`: lightweight mobile/embedded CPU when a small runtime matters more than broad operator support. Verify operator support and simplification steps early.
- `TorchScript`: conservative fallback close to PyTorch when vendor acceleration is unavailable or ONNX export is fragile.

Decision shortcut: NVIDIA GPU → TensorRT; Intel → OpenVINO; Apple → Core ML; Rockchip → RKNN; Hailo → Hailo flow; generic ARM/mobile → TFLite or ncnn; unknown future deployment → ONNX first.

## Common Conversion Chains By Source

- `PyTorch`: usually `PyTorch -> ONNX -> target runtime`, or `PyTorch -> TorchScript` as a conservative fallback.
- `TensorFlow or Keras`: often `SavedModel -> TFLite`, `SavedModel -> ONNX`, or `SavedModel -> Core ML` depending on deployment.
- `ONNX source already available`: go straight `ONNX -> TensorRT`, `ONNX -> OpenVINO`, or `ONNX -> RKNN` if the graph is compatible.
- `Vendor-neutral planning stage`: export `ONNX` first, validate graph health, then branch into vendor-specific compilers.

## Blocker Categories

- `Hardware-bound`: the requested target depends on hardware the user does not have.
- `Library-bound`: required SDKs, runtimes, or converters are missing.
- `Config-bound`: wrong opset, shape mode, precision mode, or preprocessing assumptions.
- `Graph-bound`: unsupported operators, custom layers, control flow, or fragile export graph.

## Default Ranking Heuristic

When the user does not specify ranking criteria, prefer:

1. The path that fits the actual deployment hardware today
2. The path the current machine can build with the fewest missing dependencies
3. The path with the strongest deployment portability as fallback

Avoid ranking a vendor-specific path above a portable fallback when the vendor stack is still missing and the user needs something runnable immediately.

## Minimal Question Set

Ask only these if the user did not provide enough context:

1. What is the source model format and framework?
2. What hardware will run inference in production?
3. Which libraries or runtimes are already available on that machine?
4. Is quantization allowed?
5. How many candidate conversion paths do you want?

For quantization, shape, opset, or graph-failure analysis, also load `quantization-and-shape-pitfalls.md`.
