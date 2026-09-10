---
name: convert-model
description: Model conversion planning and export guidance for ML/DL models across runtimes — ONNX, TensorRT, OpenVINO, TFLite, Core ML, RKNN, Hailo, ncnn, TorchScript. Use when converting or deploying a model artifact (.pt, .pth, .onnx, .h5, SavedModel); when the user specifies a source and target format; when verifying if a target is compatible with available hardware, libraries, and machine config; or when ranking the best N conversion paths after the preferred target is blocked or suboptimal.
---

# Skill: convert-model

## Language Protocol
- Respond in Vietnamese. Restate non-English requests in English before proceeding.
- Internal analysis in English; final response in Vietnamese.

## Trigger
User asks to convert, export, or deploy a model — specifies source format and/or target format, asks which conversion path fits their hardware, or wants ranked alternatives when a preferred target is blocked.

## Workflow

### Phase 1: Lock the Real Deployment Target
**Objective**: Separate "requested file format" from "actual runtime target" so the recommendation matches the deployment environment.

- Identify the true runtime: does the user need an interchange format (ONNX), a compiled runtime artifact (TensorRT, RKNN, Core ML, Hailo), or a device-specific deployment package?
- Normalize vague requests ("convert for edge deployment") into a concrete target profile: hardware family, OS, available libraries, performance constraints.
- If the user already provides both source and target formats, preserve that exact pair as the primary route (Direct Conversion Mode) instead of broadening into open-ended exploration.
- Detect the requested option count: if the user asks for `n` options, return exactly `n` ranked paths. If unspecified, default to 3 (best fit, conservative fallback, portable fallback). If fewer than `n` credible options exist, return fewer and state why.

### Phase 2: Check Feasibility & Blockers
**Objective**: Validate whether the requested output format is supported by the current machine and toolchain.

- **Hardware fit**: Does the target require vendor-specific hardware? TensorRT → NVIDIA GPU. OpenVINO → Intel. Core ML → Apple. RKNN → Rockchip NPU. Hailo → Hailo accelerator.
- **Software stack fit**: Are required libraries, compilers, and drivers installed or realistically installable? Distinguish "easy to add" from "structurally incompatible."
- **Model-graph fit**: Will the source framework, opset, dynamic axes, custom operators, preprocessing pipeline, and precision requirements survive the conversion chain?
- Deliver a feasibility verdict: `feasible`, `feasible with setup`, or `not a good fit` — with blocker categories (hardware-bound, library-bound, config-bound, graph-bound).

### Phase 3: Generate Ranked Conversion Paths
**Objective**: Recommend the most suitable conversion strategies, not just the requested one.

- Build the candidate set: start from the requested target if viable, then add strongest alternatives based on available hardware and libraries. In Direct Conversion Mode, keep only the requested route unless it is blocked, fragile, or the user asks for alternatives.
- Rank by: deployment compatibility → execution feasibility on current machine → expected inference performance → conversion reliability → portability/maintainability.
- Explain trade-offs for each candidate: why it fits, prerequisites, compromises. If the requested output is not rank 1, say so directly.
- Deliver: ranked options best-to-worst, one-line reason per option, clear differentiation between "best overall" and "best portable fallback."

### Phase 4: Describe the Conversion Route
**Objective**: Turn each recommendation into an actionable path.

- Specify the conversion chain explicitly (e.g. `PyTorch -> ONNX -> TensorRT`).
- List required hardware, libraries, drivers, compiler toolchain, environment assumptions.
- Call out key configuration choices: opset version, static vs dynamic shapes, input resolution, channel order, calibration dataset for INT8, whether post-processing stays outside the compiled graph.
- Generate commands only after the route is chosen. Provide full commands for the top-ranked option first; summarize the rest unless the user requests full coverage.

### Phase 5: Handle Incompatibility Honestly
**Objective**: Prevent pretending a requested export target will work when it will not.

- Reject impossible targets clearly. Replace with best-fit alternatives matching the real environment. Keep one portable fallback (ONNX or TorchScript) unless the user explicitly refuses portability.
- See `references/quantization-and-shape-pitfalls.md` for INT8/FP16, calibration, opset, unsupported operators, static/dynamic shapes, and preprocessing/post-processing mismatches.

## Reference Files
- `references/runtime-selection-matrix.md` — hardware-to-format mapping, common conversion chains by source, blocker categories, default ranking heuristic, minimal question set.
- `references/quantization-and-shape-pitfalls.md` — precision guidance (FP32/FP16/INT8), calibration rules, shape rules, opset/graph warnings, preprocessing/post-processing pitfalls, failure pattern guide, ranking adjustments.
- `references/examples.md` — few-shot examples: requested TensorRT with no NVIDIA GPU, direct PyTorch→ONNX, ONNX→RKNN for Rockchip, INT8 edge deployment with calibration risk.

## Output Format

For open-ended recommendation requests:

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
### Option 1 - [Target]
- Rank rationale / Conversion chain / Best for / Required hardware / Libraries / Key config / Risks

### Option 2 - [Target]
- ...

## Recommended Next Step
- Do this first: ...
```

For Direct Conversion Mode (user specified both source and target):

```markdown
## Conversion Request
- Source model: ...
- Requested conversion: `source -> target`
- Environment assumptions: ...

## Feasibility Verdict
- Status / Why / Main blockers

## Conversion Path
- Route: `source -> intermediate if needed -> target`
- Required hardware / Libraries / Key config / Main caveats

## Recommended Next Step
- Do this first: ...
```

If the requested route is blocked, keep the direct-conversion verdict first, then add `Best Alternatives` as a separate section.

## Don'ts
- Do not recommend vendor-specific outputs (TensorRT, RKNN, Hailo, Core ML) without checking hardware fit.
- Do not turn a direct conversion request into a generic multi-option recommendation unless the route is blocked or the user asks for alternatives.
- Do not assume ONNX automatically solves deployment compatibility.
- Do not treat export success as deployment success.
- Do not hide missing dependencies, unsupported operators, or calibration requirements.
- Do not invent compatibility claims when the installed toolchain version is unknown.
- Do not return a single path when the user explicitly asked for `n` alternatives.

## Quality Checklist
- [ ] Real deployment runtime identified, not just the requested file extension?
- [ ] Hardware requirements checked before recommending vendor-specific targets?
- [ ] Library and driver prerequisites called out explicitly?
- [ ] Requested target received a clear feasibility verdict?
- [ ] Direct conversion requests keep the requested route as primary unless blocked?
- [ ] Ranked alternatives provided (not just one path)?
- [ ] At least one portable fallback included when appropriate?
- [ ] Important conversion settings surfaced (opset, shapes, precision, calibration)?
- [ ] Assumptions stated explicitly when user input is incomplete?
