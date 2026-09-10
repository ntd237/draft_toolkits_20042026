# Few-Shot Examples

Use these examples to copy the decision style, not to constrain the technical answer.

## Example 1: Requested TensorRT but no NVIDIA GPU

**User request**:
`I have a PyTorch .pt model and want TensorRT output, but my current machine is CPU-only. Give me the best 3 conversion options.`

**Good answer pattern**:

```markdown
## Situation Summary
- Source model: PyTorch `.pt`
- Requested target: TensorRT
- Deployment environment: current machine is CPU-only
- Assumptions: no remote NVIDIA build machine is available

## Feasibility Verdict
- Status: not a good fit
- Why: TensorRT depends on NVIDIA GPU tooling and is not a natural fit for a CPU-only environment
- Main blockers: hardware-bound, library-bound

## Ranked Conversion Paths
### Option 1 - ONNX
- Rank rationale: best portable option that the current machine can produce and validate now
- Conversion chain: `PyTorch -> ONNX`
- Best for: neutral export and later branching into another runtime
- Required hardware: CPU-only is fine
- Required libraries/toolchain: PyTorch export stack, ONNX tooling
- Key configuration points: opset choice, input shape handling
- Risks or caveats: export success does not guarantee every downstream runtime will accept the graph

### Option 2 - OpenVINO IR
- Rank rationale: stronger immediate runtime path than TensorRT for CPU-centric deployment
- Conversion chain: `PyTorch -> ONNX -> OpenVINO IR`
- Best for: Intel-oriented CPU deployment
- Required hardware: CPU is fine, especially Intel
- Required libraries/toolchain: OpenVINO conversion stack
- Key configuration points: static versus dynamic shape expectations, preprocessing alignment
- Risks or caveats: less compelling if the actual production machine is not Intel-centric

### Option 3 - TorchScript
- Rank rationale: conservative fallback close to PyTorch
- Conversion chain: `PyTorch -> TorchScript`
- Best for: keeping deployment simple when vendor-specific acceleration is unavailable
- Required hardware: CPU-only is fine
- Required libraries/toolchain: PyTorch runtime
- Key configuration points: tracing versus scripting behavior
- Risks or caveats: less portable than ONNX across heterogeneous runtimes

## Recommended Next Step
- Do this first: export to ONNX, validate graph integrity, then choose OpenVINO or another runtime based on the real production hardware.
```

## Example 1B: Direct PyTorch to ONNX request

**User request**:
`I have a PyTorch model. Convert it to ONNX.`

**Good answer pattern**:

```markdown
## Conversion Request
- Source model: PyTorch
- Requested conversion: `PyTorch -> ONNX`
- Environment assumptions: standard PyTorch export environment is available

## Feasibility Verdict
- Status: feasible
- Why: ONNX is a standard and portable export target for PyTorch models
- Main blockers: config-bound or graph-bound only if unsupported operators or shape issues appear

## Conversion Path
- Route: `PyTorch -> ONNX`
- Required hardware: generic CPU is sufficient for export
- Required libraries/toolchain: PyTorch export stack, ONNX tooling
- Key configuration points: opset version, input shapes, dynamic axes only if truly needed
- Main caveats: custom operators or embedded post-processing can still cause export issues

## Recommended Next Step
- Do this first: export the model to ONNX and validate the graph with ONNX tooling before planning downstream deployment.
```

## Example 2: ONNX to RKNN for Rockchip deployment

**User request**:
`I already have an ONNX model and need the best 2 convert paths for a Rockchip NPU board.`

**Good answer pattern**:

```markdown
## Situation Summary
- Source model: ONNX
- Requested target: best 2 paths for Rockchip deployment
- Deployment environment: Rockchip NPU board
- Assumptions: RKNN toolkit can be installed or is already available

## Feasibility Verdict
- Status: feasible with setup
- Why: RKNN is the strongest match for Rockchip NPU deployment, but exact toolkit and chip compatibility must be checked
- Main blockers: library-bound, config-bound

## Ranked Conversion Paths
### Option 1 - RKNN
- Rank rationale: native fit for the target hardware
- Conversion chain: `ONNX -> RKNN`
- Best for: Rockchip NPU inference
- Required hardware: Rockchip target device
- Required libraries/toolchain: RKNN toolkit matching the target chip
- Key configuration points: input layout, quantization mode, target platform selection
- Risks or caveats: unsupported ops or wrong toolkit version can break conversion

### Option 2 - ONNX Runtime fallback
- Rank rationale: portable fallback when RKNN conversion is blocked or still under investigation
- Conversion chain: `ONNX -> ONNX Runtime deployment`
- Best for: validating the graph before vendor-specific compilation
- Required hardware: generic CPU
- Required libraries/toolchain: ONNX Runtime
- Key configuration points: shape sanity, preprocessing consistency
- Risks or caveats: will not use the Rockchip NPU

## Recommended Next Step
- Do this first: verify the exact Rockchip chip family and RKNN toolkit version before attempting RKNN conversion.
```

## Example 3: INT8 edge deployment with calibration risk

**User request**:
`Give me the best 3 conversion routes for edge deployment. INT8 is allowed if it really helps.`

**Good answer pattern**:

```markdown
## Situation Summary
- Source model: not fully specified
- Requested target: top 3 edge deployment routes
- Deployment environment: edge device, exact hardware not yet fixed
- Assumptions: portability matters and INT8 is allowed but not mandatory

## Feasibility Verdict
- Status: feasible with setup
- Why: multiple edge runtimes are plausible, but the best choice depends on hardware family and calibration readiness
- Main blockers: hardware-bound, config-bound

## Ranked Conversion Paths
### Option 1 - ONNX
- Rank rationale: best first export when hardware is still undecided
- Conversion chain: `source framework -> ONNX`
- Best for: preserving optionality before branching to a hardware-specific compiler
- Required hardware: generic
- Required libraries/toolchain: ONNX export stack
- Key configuration points: opset, dynamic axes, graph validation
- Risks or caveats: not itself the fastest final runtime

### Option 2 - TFLite INT8
- Rank rationale: strong edge candidate when the deployment stack favors lightweight CPU inference and a calibration dataset exists
- Conversion chain: `source framework -> SavedModel or compatible graph -> TFLite INT8`
- Best for: mobile or lightweight edge CPU deployment
- Required hardware: generic ARM or mobile-class CPU
- Required libraries/toolchain: TFLite conversion stack
- Key configuration points: representative calibration data, supported ops, static shape expectations
- Risks or caveats: quantization can reduce accuracy if calibration is poor

### Option 3 - ncnn
- Rank rationale: lean fallback for embedded CPU deployment
- Conversion chain: `source framework -> ONNX -> ncnn`
- Best for: compact inference stacks
- Required hardware: embedded CPU
- Required libraries/toolchain: ncnn conversion tooling
- Key configuration points: operator support, model simplification steps
- Risks or caveats: not every graph converts cleanly

## Recommended Next Step
- Do this first: lock the actual hardware family before committing to INT8-specific optimization work.
```
