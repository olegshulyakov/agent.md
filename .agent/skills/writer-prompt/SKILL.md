---
name: writer-prompt
description: >
  Produces optimized prompts for LLMs with system instructions, few-shot examples, output format
  specification, and evaluation criteria. Use this skill whenever the user wants to write an LLM
  prompt, improve an existing prompt, design a system prompt, add few-shot examples, optimize prompt
  performance, or asks to "write a system prompt", "help me write a better prompt", "design a prompt
  for this task", "add few-shot examples", "improve this prompt", "why isn't my prompt working",
  "write a prompt for my chatbot", or "design a prompt for this classification task". Also trigger
  for "prompt engineering", "system message design", "chain of thought prompting", "prompt templates",
  "structured output prompts", and "prompt optimization". Distinct from setup-eval-harness (which
  evaluates prompt performance) and setup-rag (which retrieves context for prompts).
---

# writer-prompt

Produce **optimized LLM prompts** with system instructions, few-shot examples, output format, and evaluation criteria.

## Prompt engineering principles

1. **Be specific about the task**: Vague instructions produce vague results. "Summarize this" is worse than "Write a 3-sentence summary for a non-technical executive."
2. **Specify the output format**: If you need JSON, say so. If you need markdown, say so. LLMs format output to match expectations.
3. **Use few-shot examples**: 2–3 good examples are often more effective than elaborate instructions.
4. **Assign a role/persona**: "You are an expert [X]" primes the model to use domain-appropriate reasoning.
5. **Chain of thought**: Ask the model to "think step by step" for reasoning tasks; it genuinely helps.
6. **Constrain output**: Shorter, constrained outputs are usually better than open-ended ones for structured tasks.

## Information gathering

From context, identify:
- **Task**: What should the prompt accomplish? Classification, generation, extraction, reasoning, summarization?
- **Target model**: GPT-4, Claude, Gemini, Llama? (affects formatting preferences)
- **Input format**: What does the user (or application) send as input?
- **Output format**: What should come back? Free text, JSON, markdown, structured list?
- **Constraints**: Length limits, tone, what to avoid?
- **Examples**: Does the user have examples of good input/output pairs?

## Output format

Produce all prompt components as separate, usable blocks:

```markdown
# Prompt: [Task Name]

**Task:** [What this prompt accomplishes]
**Model:** [GPT-4o / Claude 3.5 / Generic]
**Version:** v1.0
**Last updated:** [date]

---

## System Prompt

```
You are [role / persona description].

[Core instructions — what to do, what to produce]

## Rules
- [Rule 1 — be specific about what to do]
- [Rule 2 — be specific about what to avoid]
- [Rule 3]

## Output format
[Exact description of expected output — or example structure]

If you're unsure about anything, ask for clarification rather than guessing.
```

---

## User Message Template

```
[Context or preamble if needed]

[Input variable — e.g., {{user_query}}, {{document}}, {{code}}]

[Closing instruction if needed — e.g., "Please respond in JSON."]
```

---

## Few-shot Examples

### Example 1
**Input:**
```
[realistic example input]
```
**Output:**
```
[ideal output for that input]
```

### Example 2
**Input:**
```
[different example — ideally a harder or edge case]
```
**Output:**
```
[ideal output]
```

---

## Evaluation Criteria

What does a good response look like? Use these to assess prompt quality:

| Criterion | How to check | Weight |
|-----------|-------------|--------|
| [Criterion 1 — e.g., "Output is valid JSON"] | Parse with `json.loads()` | High |
| [Criterion 2 — e.g., "Summary is < 100 words"] | Word count check | Medium |
| [Criterion 3 — e.g., "All required fields present"] | Check for keys: [...] | High |
| [Criterion 4 — e.g., "Tone is professional"] | Human review | Low |

---

## Known Failure Modes

[What does this prompt do badly? Under what conditions does it fail?]

- [e.g., "Outputs invalid JSON when the input contains quotes or newlines — wrap in triple quotes"]
- [e.g., "Over-explains reasoning when told to be brief — add 'Be concise. Do not explain your reasoning.'"]

---

## Iteration Log

| Version | Change | Result |
|---------|--------|--------|
| v1.0 | Initial version | Baseline |
| v1.1 | Added few-shot examples | +15% accuracy on test set |
```

## Prompt patterns for common tasks

### Classification prompt

```
You are a content moderation specialist.

Classify the following text into exactly one category:
- SAFE: Content is appropriate for all audiences
- MILD: Content may be inappropriate for children but is not harmful
- HARMFUL: Content contains violence, hate speech, or other harmful material

Rules:
- Respond with ONLY the category label — no explanation
- When in doubt, classify as MILD
- Consider context; satire or news about harmful events is not itself harmful

Text to classify:
{{text}}
```

### Extraction prompt (JSON output)

```
You are a data extraction assistant.

Extract the following information from the text and return it as valid JSON.
If a field is not present in the text, use null.

Required fields:
- company_name: string
- headquarters: string  
- founded_year: integer or null
- ceo: string or null
- employee_count: integer or null

Return ONLY valid JSON. No explanation, no markdown code blocks.

Text:
{{text}}
```

### Summarization prompt

```
You are a professional summarizer.

Write a summary of the following [document type] for [target audience].

Requirements:
- Length: [2–3 sentences / 1 paragraph / bullet points]
- Tone: [professional / casual / neutral]
- Include: [key decisions / main arguments / action items]
- Exclude: [background context / examples / technical details]

Document:
{{document}}
```

### Chain-of-thought reasoning prompt

```
You are an expert [domain] analyst.

Analyze the following problem. Think step by step before giving your final answer.

Problem: {{problem}}

Format your response as:
<thinking>
[Your step-by-step reasoning]
</thinking>
<answer>
[Your final answer — clear and actionable]
</answer>
```

### Structured generation prompt

```
You are a [role].

Generate a [document type] based on the information provided.

Output the result as a JSON object with this exact structure:
{
  "title": "string",
  "sections": [
    {
      "heading": "string",
      "content": "string",
      "priority": "high" | "medium" | "low"
    }
  ],
  "metadata": {
    "word_count": number,
    "reading_time_minutes": number
  }
}

Do not include any text before or after the JSON object.

Input information:
{{input}}
```

## Anti-patterns to avoid

| Anti-pattern | Why it fails | Fix |
|-------------|-------------|-----|
| "Do X, but don't do Y, but if Z then Y is okay, but..." | Contradictory instructions confuse the model | Simplify; use examples instead |
| "Be helpful, accurate, and thorough" | Generic instructions add noise, not signal | Describe the specific task and output format |
| No output format specified | Model invents its own format | Always specify exactly what you want back |
| System prompt + user prompt with conflicting instructions | Model will follow one or average them | Keep system prompt stable; vary only user message |
| Very long prompt for simple task | Dilutes important instructions | Shorter prompts are often more reliable for simple tasks |

## Temperature guidance

| Task | Temperature | Reason |
|------|------------|--------|
| Classification / extraction | 0 | Deterministic; same input → same output |
| Summarization | 0–0.3 | Mostly deterministic; slight variation OK |
| Creative writing / brainstorming | 0.7–1.0 | Diversity of output is desired |
| Code generation | 0–0.2 | Correctness matters; low variance |
| Chatbot responses | 0.5–0.7 | Natural variation without incoherence |

## Calibration

- **Fix a broken prompt**: Diagnose what's failing (format? reasoning? scope?); apply targeted fixes
- **New prompt from scratch**: Draft system prompt + 2 examples; suggest evaluation criteria
- **Complex multi-step task**: Consider breaking into multiple prompts / chains
- **JSON output**: Always add "Return ONLY valid JSON" + a few-shot example with the exact schema
