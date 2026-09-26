# Usability Heuristics & Edge-Case Audit Matrix

Evaluation criteria based on the Nielsen Norman Group's 10 Usability Heuristics paired with Vietnamese typography stress testing and issue severity tiers.

---

## 1. Nielsen's 10 Usability Heuristics

| Heuristic | Audit Focus | Common Failure Signature |
| :--- | :--- | :--- |
| **1. Visibility of system status** | Immediate, unambiguous feedback within reasonable time (spinners, progress bars, saved toast). | Button clicked with zero feedback, inducing repeated accidental clicks. |
| **2. Match between system & real world** | Use familiar words, phrases, and metaphors instead of internal system jargon. | Displaying raw database error codes (`ERR_500_NULL`) instead of plain explanation. |
| **3. User control & freedom** | Provide a clear "emergency exit" (Cancel, Back, Close, Undo) for mistaken actions. | Modal without an 'X' button; non-recoverable deletion without confirmation. |
| **4. Consistency & standards** | Identical visual treatment, terminology, and location for equivalent actions across screens. | Primary action button colored green in one view and gray in another. |
| **5. Error prevention** | Design interfaces to eliminate error-prone conditions before submission occurs. | Permitting submission of incomplete forms only to flash multiple error banners. |
| **6. Recognition rather than recall** | Minimize cognitive load: Make options, filters, and actions visible rather than remembered. | Requiring users to remember a reference ID across different screens. |
| **7. Flexibility & efficiency of use** | Accommodate both novices and power users (shortcuts, advanced filters, bulk actions). | Absence of keyboard shortcuts in dense admin data management screens. |
| **8. Aesthetic & minimalist design** | Remove extraneous or rarely needed elements that compete with relevant information. | Cluttered interfaces loaded with excessive decorative visual noise. |
| **9. Help users recognize & recover** | Error messages must clearly state: (1) what happened, (2) why, (3) how to fix it immediately. | Generic messaging like "An error has occurred. Please try again." |
| **10. Help & documentation** | Searchable, concise, task-focused assistance delivered in context. | 100-page unindexed documentation PDF without contextual tooltips. |

---

## 2. Vietnamese Typography & Layout Stress Testing

1. **Diacritics Clipping Stress Test**:
   - Test high-density tone strings: `"Cộng hòa Xã hội Chủ nghĩa Việt Nam"`, `"Trường THPT Chuyên Lương Thế Vinh"`, `"Đề xuất chỉnh sửa dữ liệu"`.
   - Verify on iOS Safari, Android Chrome, and desktop browsers that accent glyphs (`?`, `~`, `.`) and circumflexes (`^`, `ă`) are not clipped vertically.
2. **Button Label Expansion Stress Test**:
   - Check translated action labels (`Cancel` → `Hủy bỏ thao tác`, `Submit request` → `Gửi yêu cầu phê duyệt`).
   - Confirm labels do not overflow button boundaries or trigger unwanted ellipsis truncation (`...`).

---

## 3. Issue Severity Matrix

- **P0 - Blocker (Critical WCAG / Functionality Failure)**:
  - Critical barrier preventing users from completing primary tasks (e.g., checkout button inaccessible via keyboard, keyboard trap in modal, text contrast < 2:1, missing network failure recovery).
  - *Action*: Mandatory resolution before design release.
- **P1 - Major (High Friction / Visual Integrity Failure)**:
  - Significant usability friction or visual defect (e.g., clipped Vietnamese tone marks, absence of loading state for actions > 2s, mobile touch targets < 40px, deceptive dark pattern).
  - *Action*: Resolve within current release cycle.
- **P2 - Minor (Cosmetic Polish)**:
  - Slight spacing inconsistency, abrupt animation easing, minor microcopy refinement.
  - *Action*: Record in design debt backlog.
