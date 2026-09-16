# Mode A: Direct Single-Block Prompt Optimization

Comprehensive guide on processing workflow and enrichment techniques for **Mode A (Default)**, inherited and extended from the `optimize-input` command standard.

---

## 1. Core Principles

0. **Execution Directives & Constraints**:
   - **Rewrite Only**: Do NOT execute the prompt. Do NOT answer the prompt. Only rewrite it.
   - **Protected Mentions Preservation**: If the prompt contains tokens of the form `⟦PLH:N⟧` (protected @-mentions), copy each token unchanged into the rewritten prompt at the same relative position. Do not delete, translate, or reformat them.

1. **Strict Language Preservation**:
   - The language of the final optimized prompt **MUST** strictly match 100% of the user's input language.
   - Vietnamese input &rarr; Vietnamese output.
   - English input &rarr; English output.
   - Do not translate the request into another language unless explicitly instructed by the user.
   - Technical identifiers (filenames, functions, libraries, CLI tools, API routes) must remain standard and uncorrupted.

2. **Single-Block Cohesion**:
   - The enriched prompt is synthesized into a single cohesive, natural, and fluid text block.
   - Avoid dissecting the prompt into complex, multi-section boilerplate headings (Role, Task, Input, Output...).
   - The output is immediately ready to copy-paste directly into an AI assistant without formatting adjustments.

3. **Fidelity to Core Intent**:
   - Clarify, specify, and elevate requirements without introducing unrequested scope creep or speculative side features.

---

## 2. The 5 Optimization Dimensions

When analyzing raw prompts, scan and enrich across 5 core dimensions:

| Dimension | Objective | Enrichment Strategy |
|---|---|---|
| **1. Clarity & Actionability** | Replace vague verbs with precise, unambiguous technical action statements. | Replace *"fix"*, *"check"*, *"make"* with *"isolate root cause and implement robust fix"*, *"inspect execution flow and verify integrity"*. |
| **2. Context & Scope Boundary** | Explicitly define target artifacts, files, modules, or directories. | Convert *"readme file"* &rarr; "`README.md` in the project root directory"; *"auth feature"* &rarr; *"authentication and role-based access control module"*. |
| **3. Structured Deliverables** | Explicitly enumerate components expected in the response. | Detail requirements: root-cause explanation, contextual code diffs, testing steps, and edge-case handling. |
| **4. Output Format & Standards** | Establish clear visual and architectural presentation guidelines. | Specify: structured Markdown, syntax-highlighted code blocks, comparison tables, or execution plans. |
| **5. Constraints & Guardrails** | Embed practical technical guardrails and safety standards. | Enforce: backward compatibility (non-breaking), robust error handling, minimal external dependencies. |

---

## 3. Action Verb Mapping

| Raw / Vague Verb | Precise Technical Action Verb (English) | Vietnamese Equivalent |
|---|---|---|
| inspect / check / read | inspect, analyze the structure, and trace data flow | đọc, phân tích cấu trúc và đánh giá luồng dữ liệu |
| fix / patch | isolate root cause, implement robust fix, and verify | cô lập nguyên nhân gốc, sửa đổi triệt để và kiểm chứng |
| make / create / write | architect, implement complete source code with robust error handling | thiết kế kiến trúc, triển khai mã nguồn hoàn chỉnh kèm xử lý lỗi |
| optimize | profile bottlenecks, optimize algorithm/memory usage while preserving correctness | đo đạc điểm nghẽn, tối ưu hóa thuật toán/bộ nhớ, giữ vững tính đúng đắn |
| review / look at | audit for logic flaws, security vulnerabilities, performance, and conventions | rà soát logic, lỗ hổng bảo mật, hiệu năng và chuẩn convention |

---

## 4. Single-Block Synthesis Technique

To craft a unified, cohesive single block containing all 5 dimensions:
- **Opening Sentence**: State the primary action and pinpoint the concrete target scope/artifact.
- **Body Sentences (Steps & Deliverables)**: Connect specific technical actions with concrete deliverables using smooth, natural transitional phrasing.
- **Closing Sentence (Constraints & Validation)**: State non-functional constraints, error handling expectations, and explicit verification criteria.

---

## 5. Real-World Transformation Examples

### Example 1: Bug Fixing (Vietnamese Input &rarr; Vietnamese Output)
- **Raw Input**: `Sửa lỗi crash khi upload ảnh lớn giúp tôi.`
- **Enriched Prompt (Mode A)**:
> Hãy kiểm tra và xử lý triệt để lỗi ứng dụng bị crash khi người dùng tải lên hình ảnh dung lượng lớn trong module xử lý tập tin (upload). Trước hết, phân tích mã nguồn và log lỗi để xác định nguyên nhân gốc rễ (như tràn bộ nhớ heap, timeout xử lý, hoặc thiếu giới hạn kích thước file). Tiếp đó, triển khai giải pháp khắc phục bằng cách bổ sung cơ chế stream/chunking, kiểm tra dung lượng và định dạng file từ sớm (early validation), đồng thời bắt ngoại lệ an toàn và trả về thông báo lỗi thân thiện cho client mà không làm sập server. Cuối cùng, cung cấp mã nguồn hoàn chỉnh kèm hướng dẫn kiểm thử với các kích thước file biên để xác minh tính ổn định.

### Example 2: Feature Implementation (English Input &rarr; English Output)
- **Raw Input**: `Add JWT authentication to my Express API.`
- **Enriched Prompt (Mode A)**:
> Please design and implement a secure JWT-based authentication system for the existing Express.js API. Create dedicated endpoints for user registration, login, and token refresh, incorporating bcrypt for password hashing and standard token expiration policies. Implement reusable Express middleware to protect private routes by extracting and validating Bearer tokens from incoming HTTP headers. Ensure the solution adheres to security best practices by preventing timing attacks, securing secret keys via environment variables, handling expired or malformed tokens gracefully with appropriate HTTP status codes, and providing concise code snippets with step-by-step testing instructions using curl or Postman.

### Example 3: Documentation & Code Exploration (Vietnamese Input &rarr; Vietnamese Output)
- **Raw Input**: `Đọc file readme và tóm tắt dự án này.`
- **Enriched Prompt (Mode A)**:
> Vui lòng đọc kỹ tệp tin `README.md` tại thư mục gốc của dự án và cung cấp bản tóm lược toàn diện về hệ thống. Nội dung phản hồi cần làm rõ: mục tiêu cốt lõi của dự án, kiến trúc tổng quan và công nghệ sử dụng, các tính năng chính, hướng dẫn cài đặt từng bước cùng cấu hình môi trường, cũng như hướng dẫn vận hành cơ bản kèm theo ví dụ minh họa trực quan.

### Example 4: Performance Optimization (English Input &rarr; English Output)
- **Raw Input**: `Optimize slow database query for order history.`
- **Enriched Prompt (Mode A)**:
> Please analyze and optimize the slow database query retrieving customer order history. Inspect the query structure, table schemas, existing indexes, and execution plan (EXPLAIN ANALYZE) to pinpoint bottlenecks such as full table scans, redundant joins, or N+1 queries. Propose and write the refactored, high-performance query utilizing proper indexing, selective column projections, and efficient pagination. Additionally, provide the necessary DDL index statements and performance benchmark estimates comparing before and after the optimization.
