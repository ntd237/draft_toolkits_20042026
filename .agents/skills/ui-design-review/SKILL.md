---
name: ui-design-review
description: "Review UI from screenshots through the lens of a professional UI/UX designer: overall assessment, concrete issues organized by a designer checklist (layout & alignment, typography, color & contrast, whitespace, accessibility, cross-screen consistency), and improvement suggestions prioritized P0/P1/P2. Strictly READ-ONLY — views images only, never edits code or runs commands. Triggers when the user provides UI screenshots (mobile/web/desktop) and asks for review, feedback, critique, or design assessment — keywords: ui-design-review, review UI, nhận xét UI, feedback design, đánh giá UI, review màn hình, designer review, UI critique, screenshot review."
---

# Skill: ui-design-review

## Language Protocol
- Respond in Vietnamese.
- Restate non-English requests in English first.
- Internal analysis in English; final report in Vietnamese (keep standard technical terms: contrast, alignment, hierarchy, padding, WCAG AA...).

## Trigger
Activates when the user provides one or more UI screenshots (mobile, web, desktop, Figma export, device frame...) and asks to review, critique, or give feedback on the design: "review UI giúp tôi", "nhận xét màn hình này", "feedback thiết kế", "chỉ ra lỗi UI", "đánh giá design". Does NOT activate for pure visual asset creation, design-to-code conversion, or bug fixing — those belong to other skills.

## Scope — Strictly READ-ONLY
- The ONLY permitted input artifacts are the image files the user provides (attached directly or given as local image paths).
- Permitted actions: view images, analyze them visually, and write the review report as chat output.
- If the user's request includes any code change, command execution, or file modification, complete the review portion and state that code edits are outside this skill's scope — do not perform them.

## Workflow

### Phase 1 — Ingest images
**Objective**: Establish exactly what is being reviewed before any judgment.

1. Read every provided image. If an image fails to load or is too low-resolution to judge (text unreadable, elements blurred), say so in the report and skip detailed claims about that region.
2. Classify each image: platform (mobile/tablet/web/desktop), screen type (onboarding, list, detail, form, empty state, dialog, settings...), and apparent state (default, loading, error).
3. If multiple images belong to one flow, order them as a user journey. If the user gave no context (e.g., "this is a checkout screen"), infer it from the UI and state the inference explicitly in the report — do not interrogate the user for context you can reasonably infer.
4. Note visible constraints that affect judgment: device frame vs bare screenshot, dark/light mode, locale, obvious zoom/crop.

### Phase 2 — Per-screen analysis (designer checklist)
**Objective**: For each screen, evaluate every checklist group and collect concrete findings with locations.

Evaluate each group; record a finding only when you can point to a specific region and say why it is a problem. An empty group is a valid result — do not invent issues.

1. **Layout & alignment**: margins consistent across elements, grid/rhythm consistency, spacing between related vs unrelated groups, mixed center/left alignment confusion, elements clipped at screen edges, natural visual reading flow.
2. **Typography**: clear title/body/caption hierarchy, font sizes neither wildly divergent nor uniformly flat, sufficient line-height, overly long single lines, more than 2-3 font families, unintended text truncation or overlap.
3. **Color & contrast**: text/background contrast (assess preliminarily against WCAG AA — 4.5:1 for normal text, 3:1 for large text; only assert when confident, otherwise phrase as "signs of low contrast"), too many accent colors diluting the primary CTA, palette consistency across the screen, enabled/disabled states visually distinguishable.
4. **Whitespace & information density**: whitespace not bunched into one region, screen neither overcrowded nor emptily purposeless, spacing-based grouping correctly reflecting element relationships.
5. **Icons & imagery**: icons from one style family (no outline/filled mix), icons paired with labels when meaning is unclear, placeholder images distorted or wrong aspect ratio, image quality.
6. **Components & states**: button style consistency (radius, padding, elevation), inputs with both placeholder and clear label, interaction states (active/selected/disabled) visible, empty/loading/error states designed rather than left blank.
7. **Accessibility (preliminary, from the image)**: touch targets visibly smaller than ~44x44pt (mobile) / ~24x24px (web), information conveyed by color alone (no icon/text backup), smallest readable text size on the screen.

### Phase 3 — Cross-screen consistency (only when ≥ 2 images)
**Objective**: Find inconsistencies that only appear when screens are compared.

1. Compare repeated attributes: spacing scale, corner radius, primary/secondary colors, typography scale, icon style, button variants, position of the primary action button.
2. Compare flow logic: step order reasonableness, navigation buttons sharing position across steps, before/after states matching the performed action.
3. Each finding must reference the two screens compared (e.g., "Screen 2 uses 16px card radius, Screen 3 uses 8px for the same card type").

### Phase 4 — Write the report
**Objective**: Produce the final Vietnamese Markdown report following the Output Format below.

1. Assign each finding a priority: **P0** = breaks the experience / unusable / severely ambiguous (unreadable text, invisible primary button, contrast below readable threshold); **P1** = noticeably wrong or clearly off-standard (grid misalignment, broken hierarchy, missing states); **P2** = polish (minor details, can wait).
2. Write the overall assessment first (2-4 sentences: what the screen does well, the main problem) — do not jump straight into a defect list.
3. Every finding must include: specific location (which screen, which region of the image — describe position such as "top right, below the title bar"), the problem, and why it is a problem. Improvement suggestions stay at the design-decision level (e.g., "raise the secondary text color to roughly #5A5A5A or darker for contrast") — NOT code snippets.
4. If an image lacks context to conclude (no comparison screen, no interaction state shown), say so under "Cần thêm ngữ cảnh" instead of guessing.

## Output Format

The report is delivered in Vietnamese (per Language Protocol). Headings below are the exact Vietnamese headings to use:

```markdown
# UI Design Review — [screen name/context]

## 1. Nhận xét tổng quan
[2-4 sentences: context, main strengths, main problem]

## 2. Các điểm cần cải thiện
### P0 — Nghiêm trọng
- **[Screen X — region on image]** [problem] — [why it is a problem]. *Gợi ý:* [design-level improvement]
### P1 — Nên sửa
[...]
### P2 — Polish
[...]

## 3. Điểm làm tốt
[1-3 concrete bullets — a review without this section is unbalanced]

## 4. Nhất quán đa màn hình *(only when ≥ 2 images)*
[specific comparisons between screens]

## 5. Cần thêm ngữ cảnh *(if any)*
[what could not be assessed and why]
```

An empty corresponding section states "Không có" — never drop the structure.

## Don'ts
- Do not modify, create, or delete any file; do not run any command or script; do not read source code files even when image paths sit inside a codebase.
- Do not produce code snippets or implementation instructions as "suggestions" — suggestions stay at the design-decision level.
- Do not invent problems to look thorough: every finding must name a visible region and a reason; if a checklist group has no issue, report it as clean.
- Do not state WCAG contrast ratios as measurements — from a screenshot they are estimates; phrase them as "signs of low contrast / passes" unless trivially obvious (e.g., white text on white background).
- Do not skip the "Điểm làm tốt" section — a one-sided review is an incomplete review.
- Do not review code quality, logic, or data shown in the UI (e.g., whether a price is correct) — only visual design and interaction affordances.

## Quality Checklist
- [ ] Every user-provided image read and analyzed (or its unreadability explicitly stated)?
- [ ] Every finding carries exactly 3 components: location on image, problem, reason?
- [ ] Every finding has a P0/P1/P2 priority and a design-level suggestion (no code snippets)?
- [ ] Report contains all sections: overall → findings → strengths → (consistency) → (missing context)?
- [ ] No action performed beyond viewing images and writing the report (no commands, no file edits, no code reads)?
- [ ] Report language is Vietnamese, with standard technical terms preserved in English?
