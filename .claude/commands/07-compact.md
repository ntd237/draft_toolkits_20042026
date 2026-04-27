---
description: "Generate structured conversation summary with analysis-first approach. Captures requests, concepts, files, problems, and tasks."
type: auto
---

Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previous actions.
Your summary must cover the entire timeline from the first user request in the conversation up to the current moment.
You must always write the summary in Vietnamese.
This summary should be thorough in capturing technical details, code patterns, and architectural decisions that would be essential for continuing development work without losing context.

**Estimated Time**: 3-5 minutes (depending on conversation length)

---

## When to Use This Command

**When to use:**
- **Conversation is long** and complex (>10 exchanges)
- **Need to preserve context** for future work
- **Switching tasks** or taking a break
- **User explicitly requests** summary

**Don't use for:**
- Short conversations (<5 exchanges)
- Simple Q&A without code changes

---

## Summarization Tiers

Choose the appropriate level of detail based on the conversation complexity:
1. **Quick Compact (5-10 exchanges):** Focus on the File Status Table and Pending Tasks. Skip long descriptions.
2. **Deep Compact (>10 exchanges or complex architectural changes):** Full 8-section summary including technical analysis and optional diagrams.

---

Before providing your final summary, write an **Analysis** section to organize your thoughts and ensure you've covered all necessary points. In your analysis process:

1. Chronologically analyze each message and section of the conversation. For each section thoroughly identify:
   - The user's explicit requests and intents
   - Your approach to addressing the user's requests
   - Key decisions, technical concepts and code patterns
   - Specific details like file names, function signatures, file edits, etc.
   - **Performance Note:** Avoid including "full code snippets" unless absolutely critical. Use concise diffs or reference line numbers/function names to save context tokens.
2. Double-check for technical accuracy and completeness, addressing each required element thoroughly.

Your summary should include the following sections:

1. **Primary Request and Intent:** Capture all of the user's explicit requests and intents in detail.
2. **Key Technical Concepts:** List all important technical concepts, technologies, and frameworks discussed.
3. **File Status Table:** A concise table showing files created, modified, or deleted.
   | File Name | Status | Key Changes |
   | :--- | :--- | :--- |
   | [Name] | [Created/Modified/Deleted] | [Brief summary] |
4. **Project Architecture (Optional):** Use **Mermaid** syntax if the conversation involved complex data flows or structure changes.
5. **Detailed Changes:** Enumerate specific files and code sections examined or modified. Use concise diffs or focused snippets. Include a summary of why each change is important.
6. **Problem Solving:** Document problems solved and any ongoing troubleshooting efforts.
7. **Pending Tasks & Next Steps:** Outline pending tasks and the immediate next step (with direct quotes from the conversation to ensure interpretation consistency).
8. **Handover Summary:** A single paragraph summarizing the "State of the Project" for a fresh start.

---

Please provide your summary based on the conversation so far, following this structure and ensuring precision and thoroughness in your response.
