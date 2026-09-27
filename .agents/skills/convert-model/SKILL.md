---
name: convert-model
description: Model conversion planning and export guidance for ML/DL models across runtimes — ONNX, TensorRT, OpenVINO, TFLite, Core ML, RKNN, Hailo, ncnn, TorchScript. Use when converting or deploying a model artifact (.pt, .pth, .onnx, .h5, SavedModel); when the user specifies a source and target format; when verifying if a target is compatible with available hardware, libraries, and machine config; or when ranking the best N conversion paths after the preferred target is blocked or suboptimal.
---

# Skill: convert-model

## Language Protocol
- Respond in Vietnamese. Restate non-English requests in English before proceeding.
- Internal analysis in English; final response in Vietnamese.

## Trigger
User asks to convert, export, or deploy a model — specifies source and/or target format, asks which conversion path fits their hardware, or wants ranked alternatives when a preferred target is blocked.

## Workflow

### Phase 1: Lock the Real Deployment Target
- Separate "requested file format" from "actual runtime target": interchange format (ONNX), compiled runtime artifact (TensorRT, RKNN, Core ML, Hailo), or device-specific deployment package.
- Normalize vague requests ("convert for edge deployment") into a concrete profile: hardware family, OS, available libraries, performance constraints.
- **Direct Conversion Mode**: if the user provides both source and target formats, preserve that exact pair as the primary route instead of broadening into open-ended exploration.
- Option count: if the user asks for `n` options, return exactly `n` ranked paths. If unspecified, default to 3 (best fit, conservative fallback, portable fallback). If fewer than `n` credible options exist, return fewer and state why.

### Phase 2: Check Feasibility & Blockers
- Verify three fits: **hardware** (vendor targets need matching hardware), **software stack** (libraries, compilers, drivers installed or realistically installable — distinguish "easy to add" from "structurally incompatible"), and **model graph** (opset, dynamic axes, custom operators, preprocessing, precision survive the conversion chain).
- Deliver a verdict: `feasible`, `feasible with setup`, or `not a good fit`, with blocker categories: hardware-bound, library-bound, config-bound, graph-bound.
- Hardware-to-format mapping and typical chains: see `references/runtime-selection-matrix.md`.

### Phase 3: Generate Ranked Conversion Paths
- Build the candidate set from the requested target if viable, then the strongest alternatives for the actual environment. In Direct Conversion Mode, keep only the requested route unless it is blocked, fragile, or the user asks for alternatives.
- Rank by: deployment compatibility → feasibility on current machine → expected inference performance → conversion reliability → portability/maintainability.
- Give each option a one-line reason. If the requested target is not rank 1, say so directly. Keep one portable fallback (ONNX or TorchScript) unless the user explicitly refuses portability.

### Phase 4: Describe the Conversion Route
- State the chain explicitly (e.g. `PyTorch -> ONNX -> TensorRT`) with required hardware, libraries, drivers, and environment assumptions.
- Call out key configuration: opset version, static vs dynamic shapes, input resolution, channel order, INT8 calibration dataset, whether post-processing stays outside the compiled graph.
- Generate commands only after the route is chosen: full commands for the top-ranked option, summarize the rest unless the user asks for full coverage.

### Phase 5: Handle Incompatibility Honestly
- Reject impossible targets clearly; replace with best-fit alternatives matching the real environment.
- For INT8/FP16, calibration, opset, shape, and pre/post-processing pitfalls: see `references/quantization-and-shape-pitfalls.md`.

## Reference Files
- `references/runtime-selection-matrix.md` — hardware-to-format mapping, conversion chains by source, blocker categories, default ranking heuristic, minimal question set.
- `references/quantization-and-shape-pitfalls.md` — precision guidance (FP32/FP16/INT8), calibration rules, shape rules, graph warnings, failure pattern guide.
- `references/examples.md` — few-shot examples: requested TensorRT with no NVIDIA GPU, direct PyTorch→ONNX, ONNX→RKNN for Rockchip, INT8 edge deployment with calibration risk.

## Output Format

Open-ended recommendation requests:

```markdown
## Situation Summary
- Source model / Requested target / Deployment environment / Assumptions

## Feasibility Verdict
- Status: feasible / feasible with setup / not a good fit
- Why / Main blockers

## Ranked Conversion Paths
### Option N - [Target]
- Rank rationale / Conversion chain / Best for / Required hardware / Libraries / Key config / Risks

## Recommended Next Step
- Do this first: ...
```

Direct Conversion Mode (user specified both source and target):

```markdown
## Conversion Request
- Source model / Requested conversion: `source -> target` / Environment assumptions

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
- Do not assume ONNX alone solves deployment compatibility, or treat export success as deployment success.
- Do not hide missing dependencies, unsupported operators, or calibration requirements; do not invent compatibility claims when the installed toolchain version is unknown.
- Do not return a single path when the user explicitly asked for `n` alternatives.

## Quality Checklist
- [ ] Real deployment runtime identified, not just the requested file extension?
- [ ] Hardware fit checked and prerequisites called out before recommending vendor-specific targets?
- [ ] Requested target received a clear feasibility verdict?
- [ ] Direct conversion requests keep the requested route as primary unless blocked?
- [ ] Option count honored, with a portable fallback included when appropriate?
- [ ] Key settings (opset, shapes, precision, calibration) and assumptions surfaced explicitly?
