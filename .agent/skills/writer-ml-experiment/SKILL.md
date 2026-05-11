---
name: writer-ml-experiment
description: >
  Produces an ML experiment report with hypothesis, setup, metrics, results, analysis, and model card
  section. Use this skill whenever the user wants to document an ML experiment, write up model training
  results, create an experiment report, document a model evaluation, or asks to "write an ML experiment
  report", "document this training run", "write up my experiment results", "create an experiment log",
  "write a model card section", "document my model's performance", "compare these model runs", or
  "summarize this experiment". Also trigger for "hyperparameter search results", "ablation study",
  "model comparison report", and "training run documentation". Distinct from setup-eval-harness
  (which sets up the evaluation infrastructure) and writer-prompt (which designs prompts for LLMs).
author: Oleg Shulyakov
licence: MIT
version: 1.0.0
---

# writer-ml-experiment

Produce an **ML experiment report** with hypothesis, setup, results, analysis, and model card information.

## What makes a great experiment report

An experiment report should be reproducible and honest. Anyone should be able to read it and understand what was tested, under what conditions, and whether it worked — including experiments that failed. Negative results are as valuable as positive ones when documented well.

## Information gathering

From context, identify:
- **Experiment goal**: What question is being answered? What hypothesis is being tested?
- **Model/approach**: What model, architecture, or technique is being evaluated?
- **Dataset**: Training data, evaluation data, splits?
- **Metrics**: What was measured? Against what baselines?
- **Results**: Training curves, eval scores, errors?
- **Conclusion**: Did it work? What's the next step?

## Output format

```markdown
# ML Experiment Report: [Experiment Name / ID]

**Date:** [date]
**Author:** [name]
**Experiment ID:** [e.g., exp-2024-03-15-001 or MLflow/W&B run ID]
**Status:** [Running / Complete / Abandoned]

---

## 1. Hypothesis

**Question:** [What specific question are you trying to answer?]

**Hypothesis:** We believe that [approach / change] will [expected outcome] because [reasoning].

**Success criteria:**
- Primary: [e.g., "F1 score > 0.85 on the test set"]
- Secondary: [e.g., "Inference time < 100ms per sample"]
- Failure: [e.g., "Any improvement less than 2pp over baseline is not worth the added complexity"]

---

## 2. Background

[2–4 sentences: What was the motivation for this experiment? What prior work or baseline does it build on? What didn't work before?]

**Related experiments:**
- [Previous experiment ID and key finding]
- [Prior art / paper reference if applicable]

---

## 3. Experimental Setup

### Model / Approach

| Component | Details |
|-----------|---------|
| Model architecture | [e.g., BERT-base fine-tuned, ResNet-50, XGBoost] |
| Pre-trained checkpoint | [e.g., bert-base-uncased from HuggingFace] |
| Framework | [e.g., PyTorch 2.1, TensorFlow 2.14, scikit-learn 1.3] |
| Hardware | [e.g., 1× A100 80GB, 8-core CPU, training time: 3h] |

### Dataset

| Split | Size | Source | Notes |
|-------|------|--------|-------|
| Training | [N samples] | [source] | [any filtering or preprocessing] |
| Validation | [N samples] | [source] | [if different from training] |
| Test | [N samples] | [source] | **Held out; not used during development** |
| External test | [N samples] | [source] | [for distribution shift testing, optional] |

**Preprocessing:**
- [Step 1 — e.g., "Tokenization with max length 512; truncated from the right"]
- [Step 2 — e.g., "Class balancing via oversampling minority class (ratio 1:3)"]

### Hyperparameters

| Parameter | Value | Justification |
|-----------|-------|---------------|
| Learning rate | [e.g., 2e-5] | [e.g., From prior ablation; LR sweep range 1e-5 to 5e-5] |
| Batch size | [e.g., 32] | [Largest that fits in VRAM] |
| Epochs | [e.g., 5] | [Early stopping with patience=2] |
| Dropout | [e.g., 0.1] | [Default from architecture] |
| [Other key param] | [value] | [reason] |

### Baseline

[Describe the baseline this experiment is compared against — previous best model, simple heuristic, human performance, or zero-shot baseline.]

---

## 4. Results

### Primary Metrics

| Metric | This Experiment | Baseline | Delta | Statistical sig? |
|--------|----------------|----------|-------|-----------------|
| F1 (macro) | **[0.87]** | [0.84] | [+3pp] | p < 0.01 (n=5 seeds) |
| Accuracy | [0.91] | [0.89] | [+2pp] | p < 0.05 |
| Precision | [0.88] | [0.85] | [+3pp] | — |
| Recall | [0.86] | [0.83] | [+3pp] | — |
| Inference time | [87ms/sample] | [45ms/sample] | [+42ms] | — |

**Primary metric result:** [Primary metric met / not met] the success criterion of [criterion].

### Training curves

[Attach or reference: loss curves, validation metric over epochs, learning rate schedule]

```
Training loss:  [1.24 → 0.41 over 5 epochs]
Validation F1:  [0.71 → 0.87, peak at epoch 4]
Early stopped:  [At epoch 4 — no improvement for 2 epochs]
```

### Per-class / Per-segment Breakdown

| Class / Segment | Precision | Recall | F1 | Support |
|-----------------|-----------|--------|-----|---------|
| [Class A] | [0.92] | [0.88] | [0.90] | [N] |
| [Class B] | [0.78] | [0.84] | [0.81] | [N] |
| [Class C — low data] | [0.61] | [0.55] | [0.58] | [N] |

### Error Analysis

[Sample 20–50 errors; identify patterns. What does the model consistently get wrong?]

**Common failure modes:**
1. [e.g., "Misclassifies ambiguous cases where context is short (< 20 tokens)"] — [N] cases
2. [e.g., "Struggles with code-switching (mixed English/Spanish)"] — [N] cases
3. [e.g., "Overconfident on rare class C examples"] — [N] cases

**Example failures:**

| Input | Predicted | Actual | Confidence | Notes |
|-------|-----------|--------|-----------|-------|
| [Example] | [A] | [B] | [0.91] | [Why it might be wrong] |

---

## 5. Analysis

### What worked

- [Finding 1 — e.g., "Longer context window (512 vs 128) improved F1 by 5pp on documents > 100 words"]
- [Finding 2 — e.g., "Data augmentation with back-translation reduced overfitting on low-resource classes"]

### What didn't work

- [e.g., "Adding an auxiliary loss for entity detection did not improve performance (+0.2pp, within noise)"]
- [e.g., "Learning rate warmup made no difference at this scale"]

### Ablation results (if applicable)

| Ablation | F1 | vs Full | Takeaway |
|----------|-----|---------|----------|
| Without augmentation | 0.82 | -5pp | Augmentation is critical |
| With 128-token context | 0.83 | -4pp | Longer context matters |
| With auxiliary loss | 0.87 | +0pp | No benefit; remove |

---

## 6. Limitations

- [e.g., "Evaluated on English-only data; performance on multilingual inputs is unknown"]
- [e.g., "Test set may have distribution shift from production data (collected 6 months earlier)"]
- [e.g., "Class C had only 200 training examples; results there are high-variance"]
- [e.g., "Only tested 5 random seeds; confidence intervals are approximate"]

---

## 7. Conclusion & Next Steps

**Verdict:** [Go / No-go / Needs more work]

**Summary:** [2–3 sentences: Did it work? Is it worth shipping? What's the most important thing learned?]

**Recommended next steps:**
1. [e.g., "Deploy to 5% of traffic with A/B test"] — Owner: [Name] — By: [Date]
2. [e.g., "Collect more data for Class C; target 1000 examples"] — Owner: [Name]
3. [e.g., "Investigate inference speed — 87ms may be too slow for real-time use case"]

---

## 8. Reproducibility

**Code:** [Link to repo / branch / commit]
**Config:** [Link to config file or YAML]
**Artifacts:**
- Model checkpoint: [path or artifact link]
- Evaluation logs: [path or W&B/MLflow run link]
- Dataset version: [hash or DVC pointer]

**To reproduce:**
```bash
# Clone and set up
git clone [repo] && cd [repo]
git checkout [commit-hash]
pip install -r requirements.txt

# Run experiment
python train.py --config configs/[experiment-config].yaml

# Evaluate
python evaluate.py --model artifacts/[model-name] --split test
```

---

## 9. Model Card (if deploying)

**Model name:** [name]
**Version:** [version]
**Task:** [e.g., Text classification — 3 classes]
**Language(s):** [English]
**License:** [Apache 2.0 / MIT / proprietary]

**Intended use:**
- [Primary use case]
- [Out-of-scope uses: do not use for...]

**Performance:**
[Copy primary metrics table from above]

**Bias & fairness:**
[What groups may be under-represented in training data? Any known disparate performance?]

**Known limitations:**
[Copy limitations section from above]
```

## Calibration

- **In-progress experiment**: Focus on setup sections; leave results blank with `[pending]`
- **Negative result**: Emphasize the "What didn't work" and "Conclusion" sections; document clearly why it failed
- **Model card only**: Generate just section 9 with what's provided
- **Comparison of multiple runs**: Expand the primary metrics table to show all runs side by side
