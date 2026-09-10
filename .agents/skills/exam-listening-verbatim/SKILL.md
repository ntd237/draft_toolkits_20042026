---
name: exam-listening-verbatim
description: "Exact verbatim transcription for IELTS, TOEIC, TOEFL, and similar listening-exam audio. Use when the user provides an audio file or asks to write out the full spoken content with maximum fidelity, preserving original wording, repetitions, fillers, numbers, spelled letters, and speaker turns without summarizing, translating, correcting, or inventing missing words."
---

# Skill: exam-listening-verbatim

## Language Protocol
- Respond in Vietnamese when communicating with the user.
- Keep the transcript in the original audio language.
- Default to short responses: transcript first, explanation after only if truly needed.
- If the user asks only to "chép lại", default to verbatim transcript, no answers or glosses.

## Trigger
User sends an audio file from a listening exam (IELTS, TOEIC, TOEFL, or similar) or asks to transcribe the full spoken content with maximum fidelity — no summarizing, translating, correcting grammar, or inventing missing words.

## Workflow

### Phase 1: Confirm Audio Access & Lock Output Scope
**Objective**: Ensure processing only on real, accessible audio and lock the output to verbatim transcript.

- Verify the audio file is actually accessible in the current context. If it cannot be accessed, the format is unsupported, or there is no audio, state the limitation and ask for a suitable file. Never pretend to have heard content when the audio is inaccessible.
- Lock the default output mode as verbatim transcription. Do not pivot to summarizing, translating, explaining, grammar-correcting, or "smoothing" unless the user explicitly requests it.
- Establish the uncertainty policy: any segment that cannot be verified after re-listening must be marked transparently at its exact location, never guessed from exam context, templates, or language probability.

### Phase 2: Rough Verbatim Pass (Full File Coverage)
**Objective**: Produce a complete rough transcript covering the entire file before refining difficult segments.

- Listen through the entire audio once to capture the structure: number of speakers, fast/slow regions, noisy sections, spelling, number dictation, addresses, proper nouns, or exam instructions.
- Transcribe speech exactly as heard — preserve repetitions, self-corrections, filler words ("uh", "um", "well"), spelled-out letters, phone numbers, dates, times, and short error-prone facts. Do not clean up spoken style.
- Use minimal, cautious punctuation. Punctuation must not change the meaning, order, or original wording.

### Phase 3: Targeted Re-Listening & Verification
**Objective**: Minimize errors in difficult regions and ensure nothing was added or omitted.

- Re-listen carefully to high-risk segments: noise, fast speech, heavy accent, overlapping speakers, and segments containing numbers, letters, proper nouns, emails, addresses, prices, dates, times. These are the highest error-probability regions in IELTS, TOEIC, and similar audio.
- Check file boundaries (start and end) and speaker-turn transitions to avoid missing opening lines, closing lines, or short dialogue turns. If speaker changes need representation, prefer line breaks; only label `Speaker 1` / `Speaker 2` when the user requests it or the audio clearly self-identifies.
- If a segment remains unverifiable after multiple listens, insert a minimal marker at that exact position: `[không nghe rõ]` or `[không chắc]`. Do not fill gaps with contextual inference, exam templates, collocations, or plausible answers.

### Phase 4: Final Transcript Output
**Objective**: Deliver the final transcript in a minimal format, with no content mixed in outside the transcript.

- **If audio is clear and verifiable**: output only the verbatim transcript. No long preamble, no method explanation, no content summary.
- **If unverifiable regions remain**: still output the verbatim transcript with uncertainty markers in place. After the transcript, add one short note stating some segments could not be verified 100% and offer to re-transcribe if the user sends a clearer version or a shorter clip.
- **If the user requests additional tasks** (translate, summarize, solve): complete the verbatim transcript first or place the additional work in a separate section. Never mix it into the transcript itself.

## Output Format

Default order:
1. Verbatim transcript
2. Short note on unverifiable segments (only if any remain)

Template:

```text
[Verbatim transcript from start to finish]

[Only if needed]
Ghi chú: Một số đoạn còn chưa thể xác minh 100%. Nếu bạn muốn, hãy gửi bản audio rõ hơn hoặc cắt riêng đoạn đó để mình chép lại chính xác hơn.
```

If the user requests timestamps or speaker separation, apply those while keeping the spoken content verbatim.

## Don'ts
- Do not summarize in place of a transcript.
- Do not translate or interpret when the user only asked to transcribe.
- Do not correct grammar, clean spoken English, or remove repetitions/fillers for "polish".
- Do not guess missing words from exam templates, question context, or plausible-sounding answers.
- Do not add speaker names, titles, long annotations, or unrequested metadata.
- Do not pretend to have heard the file when the audio was not actually accessible or processed.

## Quality Checklist
- [ ] Audio confirmed accessible before transcribing?
- [ ] Transcript covers the entire file from start to finish?
- [ ] No summary, translation, or interpretation mixed into the transcript?
- [ ] Error-prone details (numbers, spelled letters, proper nouns, dates/times) re-checked?
- [ ] Repetitions, filler words, and false starts preserved, not silently removed?
- [ ] No guessed words filling gaps?
- [ ] All unverifiable regions marked transparently at their exact positions?
