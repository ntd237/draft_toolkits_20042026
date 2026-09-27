# Few-Shot Examples

Use these examples to copy the decision style, not to constrain the technical answer. Field templates live in SKILL.md; answers below are condensed to the decisions that matter.

## Example 1: Requested TensorRT but no NVIDIA GPU

**User request**: `I have a PyTorch .pt model and want TensorRT output, but my current machine is CPU-only. Give me the best 3 conversion options.`

**Good answer pattern** (open-ended template):

- Verdict: `not a good fit` — TensorRT depends on NVIDIA GPU tooling; blockers: hardware-bound, library-bound.
- Option 1 - ONNX: `PyTorch -> ONNX`; best portable option the current machine can produce and validate now. Caveat: export success does not guarantee every downstream runtime accepts the graph.
- Option 2 - OpenVINO IR: `PyTorch -> ONNX -> OpenVINO IR`; stronger runtime path for CPU-centric deployment. Caveat: less compelling if production is not Intel-centric.
- Option 3 - TorchScript: `PyTorch -> TorchScript`; conservative fallback close to PyTorch. Caveat: less portable than ONNX across heterogeneous runtimes.
- Next step: export to ONNX, validate graph integrity, then choose the runtime based on real production hardware.

## Example 1B: Direct PyTorch to ONNX request

**User request**: `I have a PyTorch model. Convert it to ONNX.`

**Good answer pattern** (Direct Conversion Mode template):

- Verdict: `feasible` — ONNX is a standard, portable export target for PyTorch.
- Route: `PyTorch -> ONNX`; generic CPU suffices for export; key config: opset version, input shapes, dynamic axes only if truly needed.
- Caveat: custom operators or embedded post-processing can still cause export issues.
- Next step: export and validate the graph with ONNX tooling before planning downstream deployment.

## Example 2: ONNX to RKNN for Rockchip deployment

**User request**: `I already have an ONNX model and need the best 2 convert paths for a Rockchip NPU board.`

**Good answer pattern** (exactly 2 options, as requested):

- Verdict: `feasible with setup` — RKNN is the strongest match, but exact toolkit and chip compatibility must be checked; blockers: library-bound, config-bound.
- Option 1 - RKNN: `ONNX -> RKNN`; native fit for the target hardware; key config: input layout, quantization mode, target platform. Caveat: unsupported ops or wrong toolkit version can break conversion.
- Option 2 - ONNX Runtime: portable fallback when RKNN conversion is blocked or under investigation. Caveat: will not use the Rockchip NPU.
- Next step: verify the exact Rockchip chip family and RKNN toolkit version before attempting conversion.

## Example 3: INT8 edge deployment with calibration risk

**User request**: `Give me the best 3 conversion routes for edge deployment. INT8 is allowed if it really helps.`

**Good answer pattern** (hardware not yet fixed):

- Verdict: `feasible with setup` — multiple edge runtimes are plausible; best choice depends on hardware family and calibration readiness; blockers: hardware-bound, config-bound.
- Option 1 - ONNX: best first export when hardware is undecided; preserves optionality before branching to a hardware-specific compiler.
- Option 2 - TFLite INT8: strong candidate for lightweight CPU edge deployment if a representative calibration dataset exists. Caveat: poor calibration can damage accuracy.
- Option 3 - ncnn: lean fallback for embedded CPU. Caveat: not every graph converts cleanly.
- Next step: lock the actual hardware family before committing to INT8-specific optimization work.
