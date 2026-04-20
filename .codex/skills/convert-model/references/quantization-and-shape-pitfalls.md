# Quantization And Shape Pitfalls

Use this reference when a conversion path looks correct at the runtime-selection level but may still fail because of graph details, precision choices, or deployment assumptions.

## When To Load This Reference

Load this file when the user mentions any of these:

- `INT8`, `FP16`, quantization, calibration, representative dataset
- dynamic shape, static shape, fixed input size, variable batch size
- opset mismatch, unsupported operators, custom layers, graph simplification
- preprocessing mismatch, channel order, normalization, resize behavior
- post-processing inside or outside the graph
- "conversion succeeded but inference output is wrong"

## Precision Guidance

### FP32

- Safest default when conversion reliability matters more than runtime speed.
- Best starting point for debugging graph correctness before trying lower precision.

### FP16

- Usually lower risk than INT8 when the target runtime supports it well.
- Good compromise when the hardware benefits from reduced precision but calibration complexity is undesirable.
- Still verify numerical drift for sensitive models.

### INT8

- Recommend only when the runtime and hardware actually benefit from it.
- Usually needs representative calibration data that reflects real deployment inputs.
- Gains can be substantial, but poor calibration can damage accuracy badly.
- Call this out explicitly when the user wants aggressive optimization without a calibration dataset.

## Calibration Rules

- Ask whether a representative dataset exists before recommending INT8 as the primary path.
- Prefer real deployment-like samples over synthetic or random data.
- If the user lacks calibration data, downgrade INT8 in the ranking unless the target workflow absolutely requires it.
- Mention that calibration quality affects accuracy more than the export command itself.

## Shape Rules

### Dynamic Shapes

- Useful when the runtime truly needs variable input sizes or batch sizes.
- More fragile during export and downstream compilation.
- Some vendor-specific compilers or deployment stacks prefer or require static shapes.

### Static Shapes

- Usually safer for embedded deployment and vendor-specific compilers.
- Prefer static shapes when the target pipeline is latency-sensitive and input dimensions are known ahead of time.
- If the user already knows the exact deployment resolution, bias toward static export unless there is a clear reason not to.

## Opset And Graph Warnings

- Do not assume the newest opset is always the best choice.
- If the downstream runtime is version-sensitive, recommend an opset that is conservative and widely supported by the full conversion chain.
- Unsupported operators, custom layers, control flow, and dynamic post-processing logic are common reasons an export path fails after looking valid on paper.
- If the graph contains custom operations, mention that vendor-specific runtimes may be harder to support than a conservative fallback such as ONNX or TorchScript.

## Preprocessing And Post-Processing Pitfalls

- Call out input layout assumptions such as `NCHW` versus `NHWC`.
- Call out channel order assumptions such as `RGB` versus `BGR`.
- Mention resize method, normalization constants, and letterboxing policy when they affect runtime parity.
- Say explicitly whether post-processing like NMS is expected to stay outside the graph or be embedded into the exported artifact.

## Failure Pattern Guide

### Export succeeds, runtime compile fails

- Likely causes: unsupported operators, wrong opset, dynamic shape incompatibility, vendor-toolchain limitation.
- Usual response: keep the runtime choice if it still matches the hardware, but recommend graph simplification, opset adjustment, or a more conservative fallback path.

### Export and compile succeed, predictions are wrong

- Likely causes: preprocessing mismatch, layout mismatch, quantization drift, post-processing mismatch.
- Usual response: compare preprocessing and post-processing behavior before blaming the runtime choice.

### INT8 path is fast but accuracy collapses

- Likely causes: poor calibration data, overly aggressive quantization, sensitive layers.
- Usual response: downgrade INT8, test FP16 or FP32, or improve the calibration dataset.

### Dynamic model converts poorly to embedded runtime

- Likely causes: embedded compiler prefers fixed dimensions or limited shape profiles.
- Usual response: recommend static shapes if deployment dimensions are known.

## Ranking Adjustments

- Rank FP16 above INT8 when calibration data is missing or the user mainly wants a reliable deployment path.
- Rank a static-shape export above a dynamic-shape export for embedded deployment when the input size is known.
- Rank a portable fallback above a fragile vendor-specific path if the graph includes unsupported operators or unverified custom layers.

## Minimal Questions For Pitfall Diagnosis

Ask only these if needed:

1. Is INT8 required or just optional?
2. Do you have a representative calibration dataset?
3. Is the deployment input size fixed?
4. Are there custom operators or post-processing layers inside the graph?
5. Did the failure happen during export, compilation, or runtime inference?
