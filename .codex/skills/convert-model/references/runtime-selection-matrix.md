# Runtime Selection Matrix

Use this reference when mapping deployment constraints to likely output formats and conversion chains.

## Quick Routing

- `ONNX`: Best generic interchange format and common fallback when the final runtime is still undecided.
- `TensorRT engine` or TensorRT-compatible ONNX: Best fit for NVIDIA GPU deployment when CUDA and TensorRT are available.
- `OpenVINO IR`: Best fit for Intel CPU, Intel iGPU, and Intel-centric edge or server deployment.
- `TFLite`: Best fit for mobile, lightweight edge CPU deployment, and some accelerator workflows.
- `Core ML`: Best fit for Apple deployment targets such as iPhone, iPad, and macOS apps.
- `RKNN`: Best fit for Rockchip NPU devices and SBCs that use the RKNN toolkit.
- `Hailo archive or HEF flow`: Best fit for Hailo accelerator deployments with the Hailo SDK and compiler flow.
- `ncnn`: Strong lightweight option for mobile or edge CPU deployments when a small, portable inference stack matters.
- `TorchScript`: Good fallback when staying close to the PyTorch ecosystem is more important than vendor-specific acceleration.

## Hardware-First Mapping

- `NVIDIA GPU available now`: prioritize `TensorRT`, keep `ONNX` as portability fallback.
- `Intel CPU or Intel iGPU`: prioritize `OpenVINO`, keep `ONNX` or plain ONNX Runtime as fallback.
- `Apple device deployment`: prioritize `Core ML`.
- `Rockchip NPU device`: prioritize `RKNN`.
- `Hailo accelerator deployment`: prioritize the `Hailo` compiler flow.
- `Generic ARM or mobile CPU`: consider `TFLite` or `ncnn`.
- `Unknown future deployment`: prioritize `ONNX` first because it preserves optionality.

## Common Conversion Chains By Source

- `PyTorch`: usually `PyTorch -> ONNX -> target runtime`, or `PyTorch -> TorchScript` as a conservative PyTorch-centered fallback.
- `TensorFlow or Keras`: often `SavedModel -> TFLite`, `SavedModel -> ONNX`, or `SavedModel -> Core ML` depending on deployment.
- `ONNX source already available`: often go straight from `ONNX -> TensorRT`, `ONNX -> OpenVINO`, or `ONNX -> RKNN` if the graph is compatible.
- `Vendor-neutral planning stage`: often export `ONNX` first, validate graph health, then branch into vendor-specific compilers.

## Common Fit Rules

### ONNX

- Best when the user needs portability, debugging flexibility, or an intermediate export step.
- Good fallback when vendor-specific toolchains are not yet installed.
- Watch for unsupported custom operators, dynamic shape issues, and preprocessing or post-processing logic that lives outside the graph.

### TensorRT

- Choose when the target machine has an NVIDIA GPU and inference speed matters.
- Typical chain: `PyTorch -> ONNX -> TensorRT`.
- Requires matching CUDA, cuDNN, TensorRT, GPU architecture, and often careful shape handling.
- Poor fit for CPU-only systems or mixed environments that need strong portability.

### OpenVINO

- Choose when deployment is centered on Intel CPUs, Intel iGPUs, or Intel edge hardware.
- Typical chain: `PyTorch -> ONNX -> OpenVINO IR`.
- Strong option when the user wants efficient CPU inference without NVIDIA dependencies.
- Less compelling when the deployment target is Apple, Rockchip, Hailo, or a generic mobile app stack.

### TFLite

- Choose for lightweight edge or mobile deployment, especially when the target prefers TensorFlow-family tooling.
- Typical chain may be `TensorFlow SavedModel -> TFLite`, or a more indirect route from PyTorch through ONNX and TensorFlow conversion tooling if the graph supports it.
- Quantization often matters for real edge gains, so calibration data may be required.
- Operator coverage and graph conversion reliability can be weaker for complex models.

### Core ML

- Choose when the real target is Apple hardware and app integration matters.
- Typical chain: `PyTorch -> ONNX or direct tooling -> Core ML`.
- Best when deployment will stay inside the Apple ecosystem.
- Poor fit for non-Apple deployment environments.

### RKNN

- Choose when the target device is a Rockchip NPU board or appliance.
- Typical chain: `PyTorch -> ONNX -> RKNN`.
- Requires Rockchip-specific toolkit versions, target chip compatibility, and deployment-side runtime alignment.
- Not a good recommendation unless Rockchip hardware is actually present in the target plan.

### Hailo

- Choose when the target includes a Hailo accelerator and the user can run the Hailo SDK flow.
- Often requires graph preparation, model parsing, optimization, quantization, and compilation into a deployment artifact.
- Not a good fit unless the user is explicitly deploying to Hailo hardware.

### ncnn

- Choose when lightweight mobile or embedded CPU deployment matters more than broad operator support.
- Often used for compact edge apps that need a lean inference runtime.
- Verify operator support and any model simplification steps early.

### TorchScript

- Choose when staying close to PyTorch is valuable and the user does not need a vendor-specific compiler immediately.
- Useful as a conservative fallback when ONNX conversion is fragile or custom ops are tightly coupled to PyTorch.

## Blocker Categories

- `Hardware-bound`: The requested target depends on hardware the user does not have.
- `Library-bound`: Required SDKs, runtimes, or converters are missing.
- `Config-bound`: Wrong opset, shape mode, precision mode, or preprocessing assumptions.
- `Graph-bound`: Unsupported operators, custom layers, control flow, or fragile export graph.

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
