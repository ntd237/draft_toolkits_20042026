---
name: convert-model
description: Model conversion planning and export guidance for machine learning and deep learning models across runtimes such as ONNX, TensorRT, OpenVINO, TFLite, Core ML, RKNN, Hailo, ncnn, and TorchScript. Use when Codex needs to convert or deploy a model artifact such as `.pt`, `.pth`, `.onnx`, `.h5`, SavedModel, or similar; handle direct conversion requests where the source format and target format are already specified; verify whether a requested output format is compatible with available hardware, libraries, drivers, and machine configuration; or rank the best N conversion paths when the preferred target is blocked or suboptimal.
---

# Model Conversion Strategy

## Overview

Use this skill to choose and explain the most suitable model conversion path for the user's deployment environment instead of blindly exporting to the first requested format. Focus on compatibility first, then performance, then portability, and always surface fallback paths when the preferred target is not feasible.

## High-Signal Trigger Examples

Use this skill when the request sounds like one of these:

- "Convert this PyTorch model to the best format for my NVIDIA GPU edge box."
- "I have a PyTorch model. Convert it to ONNX."
- "I already know the input and output formats. Convert this PyTorch model to TensorRT."
- "I want TensorRT output, but my current machine is CPU-only. What are the best alternatives?"
- "Which 3 export paths fit my Intel mini PC and current libraries?"
- "Can this ONNX model be turned into RKNN for my Rockchip board?"
- "My requested output format has too many dependencies. Give me the top 2 safer convert options."
- "Choose the best deployment artifact for this model based on my hardware and installed runtimes."

## Language Requirements

- Always respond in Vietnamese for all communications
- When receiving requests in non-English languages, first restate your understanding of the request in English before proceeding
- Internal thinking, analysis, and execution should be conducted in English, then translated to Vietnamese for the final response

## Primary Goal

Help the user answer four questions clearly:

- What is the source model and framework?
- What output format or deployment runtime is desired?
- Is that target actually compatible with the current hardware, libraries, drivers, and operating environment?
- If not, what are the best alternative conversion paths, ranked by suitability?

## Required Input Signals

Collect these inputs when available. Do not block on every item if a reasonable assumption is possible.

- Source framework and artifact type: PyTorch `.pt` or `.pth`, TensorFlow SavedModel, Keras `.h5`, ONNX `.onnx`, Paddle, Darknet, or another source.
- Model task and shape constraints: classification, detection, segmentation, pose, NLP, fixed shape or dynamic shape.
- Requested target runtime or file format, if any.
- Deployment hardware: CPU-only, NVIDIA GPU, Intel CPU or iGPU, Apple Silicon, Rockchip NPU, Hailo accelerator, Edge TPU, ARM SBC, x86 server.
- Memory constraints: RAM, VRAM, storage budget, batch size, latency target, throughput target.
- Installed or available software stack: CUDA, cuDNN, TensorRT, OpenVINO, ONNX Runtime, TFLite stack, Core ML tools, RKNN toolkit, Hailo SDK, compiler versions, Python version, OS.
- Precision tolerance: FP32, FP16, INT8, quantization allowed or forbidden.
- Deployment mode: offline batch, real-time edge inference, server inference, mobile app, camera device, embedded NPU.

Only ask follow-up questions that materially change the choice of runtime or export path.

## Direct Conversion Mode

When the user already specifies both the source format and the target format, treat the request as a direct conversion request first.

- Example: `PyTorch -> ONNX`
- Example: `PyTorch -> TensorRT`
- Example: `ONNX -> RKNN`

In this mode:

- Prioritize the requested conversion path before suggesting alternatives.
- Ask only the missing questions that affect whether the requested path can actually run.
- If the requested route is feasible, return that route first and give concrete conversion guidance.
- Suggest alternatives only when the requested route is blocked, fragile, or the user explicitly asks for options.

## Hardware-First Shortcuts

Use these shortcuts only as a starting point, then verify the actual toolchain and graph constraints:

- NVIDIA GPU with performance priority: prefer `TensorRT`, keep `ONNX` as fallback.
- Intel CPU or Intel iGPU deployment: prefer `OpenVINO`, keep `ONNX` as fallback.
- Apple device or Apple app deployment: prefer `Core ML`.
- Rockchip NPU deployment: prefer `RKNN`.
- Hailo accelerator deployment: prefer the `Hailo` toolchain flow.
- Lightweight mobile or embedded CPU deployment: consider `TFLite` or `ncnn`.
- Unknown or mixed deployment target: start with `ONNX`, then add one environment-specific option and one conservative fallback.

## Workflow

### Phase 1: Lock the real deployment target

**Objective**: Separate "requested file format" from "actual runtime target" so the recommendation matches the deployment environment.

**Execution**:

**Step 1.1 - Identify the true runtime**:
Determine whether the user actually needs an interchange format, a compiled runtime artifact, or a device-specific deployment package. For example, ONNX is often an interchange step, while TensorRT, RKNN, Core ML, or Hailo outputs are runtime-specific endpoints.

**Step 1.2 - Normalize the request**:
Translate vague requests such as "convert this for edge deployment" into a concrete target profile including hardware family, operating system, available libraries, and performance constraints.

If the user already provides a concrete source format and target format, preserve that exact pair as the primary route under evaluation instead of broadening the task into open-ended runtime exploration.

**Step 1.3 - Detect the requested option count**:
If the user asks for `n` options, return exactly `n` ranked conversion paths when feasible. If the user does not specify a number, default to `3` ranked paths: best fit, conservative fallback, and portable fallback.

If fewer than `n` credible options exist, return fewer and state why instead of inventing weak candidates.

If the user does not ask for options and has already specified both input and output formats, default to `direct conversion mode` rather than multi-option ranking.

**Deliverables must include**:
- A short statement of the real deployment target
- The requested target format or runtime
- The number of candidate conversion paths to present

### Phase 2: Check feasibility and blockers

**Objective**: Validate whether the requested output format is actually supported by the current machine and toolchain.

**Execution**:

**Step 2.1 - Validate hardware fit**:
Check whether the requested target depends on vendor-specific hardware. TensorRT requires NVIDIA GPUs. OpenVINO is strongest on Intel hardware. Core ML targets Apple platforms. RKNN targets Rockchip NPUs. Hailo deployment requires the Hailo toolchain and compatible accelerator hardware.

**Step 2.2 - Validate software stack fit**:
Check whether required libraries, compilers, and drivers are installed or realistically installable on the machine. If the stack is missing, distinguish between "easy to add" and "structurally incompatible".

**Step 2.3 - Validate model-graph fit**:
Check whether the source framework, opset, dynamic axes, custom operators, preprocessing pipeline, and precision requirements are likely to survive the conversion chain.

**Deliverables must include**:
- A feasibility verdict for the requested target: `feasible`, `feasible with setup`, or `not a good fit`
- The main blocker categories if anything is missing
- A short explanation of whether the blocker is hardware-bound, library-bound, config-bound, or model-graph-bound

### Phase 3: Generate ranked conversion paths

**Objective**: Recommend the most suitable conversion strategies, not just the requested one.

**Execution**:

**Step 3.1 - Build the candidate set**:
Start from the requested target if it is viable. Then add the strongest alternatives based on available hardware and libraries. Prefer paths the user can execute on the current machine before suggesting paths that require switching machines.

In direct conversion mode, the candidate set should contain only the requested route unless it is blocked, clearly fragile, or the user explicitly asks for alternatives.

**Step 3.2 - Rank candidates**:
Rank paths using this order of priority unless the user states otherwise:
1. Deployment compatibility
2. Execution feasibility on the current machine
3. Expected inference performance
4. Conversion reliability
5. Portability and maintainability

**Step 3.3 - Explain trade-offs**:
For each candidate, explain why it is a good fit, what the prerequisites are, and what compromises it introduces. If the requested output is not rank 1, say so directly and explain why.

**Deliverables must include**:
- Ranked options from best to worst
- A one-line reason for the ranking of each option
- Clear differentiation between "best overall" and "best portable fallback" when they differ

### Phase 4: Describe the conversion route

**Objective**: Turn each recommendation into an actionable conversion path.

**Execution**:

**Step 4.1 - Specify the route**:
Describe the conversion chain explicitly, for example `PyTorch -> ONNX -> TensorRT` or `PyTorch -> ONNX -> RKNN`.

**Step 4.2 - Specify dependencies**:
List the required hardware, libraries, drivers, compiler toolchain, and environment assumptions for each route.

**Step 4.3 - Specify key configuration choices**:
Call out important settings such as opset version, static versus dynamic shapes, input resolution, channel order, calibration dataset needs for INT8, and whether post-processing must remain outside the compiled graph.

If the user asks for actual conversion commands, generate commands only after the route is chosen. By default, provide concrete command guidance for the top-ranked option first, then summarize the rest more briefly unless the user requests full command coverage for every option.

**Deliverables must include**:
- The exact conversion chain for each option
- Required runtime stack
- Key config decisions that can break the conversion if chosen incorrectly

### Phase 5: Handle incompatibility honestly

**Objective**: Prevent the model from pretending a requested export target will work when it will not.

**Execution**:

**Step 5.1 - Reject impossible targets clearly**:
If the requested format is structurally mismatched with the user's hardware or software stack, say so directly.

**Step 5.2 - Replace with best-fit alternatives**:
Offer the best `n` alternatives that match the real environment, and explain why they are better aligned.

**Step 5.3 - Keep one portable fallback**:
Unless the user explicitly refuses portability, include one generic fallback such as ONNX or TorchScript when vendor-specific deployment looks fragile.

**Deliverables must include**:
- A direct incompatibility note when needed
- Best-fit replacement options
- One portable fallback unless explicitly unnecessary

## Runtime Selection Reference

Load `references/runtime-selection-matrix.md` when the user needs help mapping hardware and toolchain constraints to output formats, or when you need a quick shortlist of likely targets and blockers.

Load `references/quantization-and-shape-pitfalls.md` when the user asks about INT8 or FP16 conversion, calibration data, opset issues, unsupported operators, static versus dynamic shapes, preprocessing or post-processing mismatches, or when a conversion path fails even though the runtime choice itself seems reasonable.

## Output Format

Use this structure by default for open-ended recommendation requests:

1. Situation summary
2. Feasibility verdict for the requested target
3. Ranked conversion paths
4. Recommended next step

Template:

```markdown
## Situation Summary
- Source model: ...
- Requested target: ...
- Deployment environment: ...
- Assumptions: ...

## Feasibility Verdict
- Status: feasible / feasible with setup / not a good fit
- Why: ...
- Main blockers: ...

## Ranked Conversion Paths
### Option 1 - [Target format or runtime]
- Rank rationale: ...
- Conversion chain: ...
- Best for: ...
- Required hardware: ...
- Required libraries/toolchain: ...
- Key configuration points: ...
- Risks or caveats: ...

### Option 2 - [Target format or runtime]
- Rank rationale: ...
- Conversion chain: ...
- Best for: ...
- Required hardware: ...
- Required libraries/toolchain: ...
- Key configuration points: ...
- Risks or caveats: ...

### Option 3 - [Target format or runtime]
- Rank rationale: ...
- Conversion chain: ...
- Best for: ...
- Required hardware: ...
- Required libraries/toolchain: ...
- Key configuration points: ...
- Risks or caveats: ...

## Recommended Next Step
- Do this first: ...
```

If the user asks for implementation details, follow the ranked recommendation with concise export commands, environment notes, or a migration checklist.

If the user explicitly requests a short answer, compress the response but keep the feasibility verdict, ranked options, and the first recommended next step.

For direct conversion mode, use this shorter structure by default:

```markdown
## Conversion Request
- Source model: ...
- Requested conversion: `source -> target`
- Environment assumptions: ...

## Feasibility Verdict
- Status: feasible / feasible with setup / not a good fit
- Why: ...
- Main blockers: ...

## Conversion Path
- Route: `source -> intermediate if needed -> target`
- Required hardware: ...
- Required libraries/toolchain: ...
- Key configuration points: ...
- Main caveats: ...

## Recommended Next Step
- Do this first: ...
```

If the requested route is blocked, keep the direct-conversion verdict first, then add `Best Alternatives` as a separate section instead of replacing the requested route silently.

## Few-Shot Examples

Use these examples to copy the decision style, not to constrain the technical answer.

### Example 1: Requested TensorRT but no NVIDIA GPU

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

### Example 1B: Direct PyTorch to ONNX request

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

### Example 2: ONNX to RKNN for Rockchip deployment

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

### Example 3: INT8 edge deployment with calibration risk

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

## Quality Checklist

- [ ] The answer identifies the real deployment runtime, not just the requested file extension
- [ ] Hardware requirements are checked before recommending vendor-specific targets
- [ ] Library and driver prerequisites are called out explicitly
- [ ] The requested target receives a clear feasibility verdict
- [ ] Direct conversion requests keep the requested route as the primary answer unless it is blocked
- [ ] The answer provides ranked alternatives, not just one path
- [ ] At least one portable fallback is included when appropriate
- [ ] Important conversion settings are surfaced
- [ ] Quantization, calibration, and shape constraints are called out when relevant
- [ ] Assumptions are stated explicitly when user input is incomplete

## Important Rules

### Mandatory Practices

- Always distinguish between an interchange format and a deployable runtime artifact.
- Always evaluate the requested target against actual hardware, libraries, and machine configuration.
- Always provide the best `n` conversion paths when the user asks for multiple options.
- Always prioritize the explicitly requested `source -> target` route when the user has already specified both ends of the conversion.
- Always rank options and explain the ranking.
- Always say when a requested target is only possible after additional setup.
- Always mention calibration requirements when recommending INT8 or other aggressive quantization paths.

### Strictly Prohibited

- Do not recommend TensorRT, RKNN, Hailo, Core ML, or other vendor-specific outputs without checking hardware fit.
- Do not turn a direct conversion request into a generic multi-option recommendation unless the requested route is blocked or the user asks for alternatives.
- Do not assume that ONNX automatically solves deployment compatibility.
- Do not treat export success as deployment success.
- Do not hide missing dependencies, unsupported operators, or calibration requirements.
- Do not invent exact compatibility claims when the installed toolchain version is unknown.
- Do not return a single preferred path when the user explicitly asked for `n` alternatives.

## Best Practices Summary

Choose the deployment runtime from the environment backward, not from the file extension forward. The strongest answer is the one that tells the user which conversion path will work on the actual machine today, which one will work after extra setup, and which portable fallback remains available if the ideal vendor-specific route fails.
