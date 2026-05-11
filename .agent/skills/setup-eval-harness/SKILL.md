---
name: setup-eval-harness
description: >
  Generates an evaluation harness for machine learning models with metrics definitions, dataset
  management, scoring rubrics, and benchmark runner configuration. Use this skill whenever the user
  wants to set up an ML evaluation framework, define model evaluation metrics, create an eval dataset,
  build a benchmark runner, evaluate LLM outputs, score model performance, or asks to "set up an eval
  harness", "create evaluation metrics for my model", "build a benchmark for this LLM", "define how to
  measure model quality", "create an eval dataset", "automate model evaluation", or "set up evals for
  my AI system". Also trigger for "LLM evaluation", "model scoring", "RAGAS setup", "evals pipeline",
  "automated testing for AI", and "ground truth dataset creation". Distinct from setup-rag (which sets
  up the retrieval pipeline) and writer-ml-experiment (which documents experiment results).
---

# setup-eval-harness

Generate an **evaluation harness** for ML/AI models with metrics, dataset management, scoring, and a benchmark runner.

## Eval harness components

1. **Dataset** — evaluation examples with inputs and expected outputs (ground truth)
2. **Metrics** — how to measure quality (exact match, semantic similarity, task-specific)
3. **Scorer** — automated scoring per metric
4. **Runner** — orchestrates running all examples through the model
5. **Reporter** — aggregates results into a benchmark report

## Information gathering

From context, identify:
- **Model type**: LLM (text generation), classifier, retrieval, regression, image?
- **Task**: Question answering, summarization, code generation, classification, RAG?
- **Metric preferences**: Exact match, BLEU/ROUGE, embedding similarity, LLM-as-judge?
- **Dataset**: Existing dataset or needs to be created?
- **Language/framework**: Python? What libraries available (transformers, langchain, etc.)?

Default to Python with a modular, framework-agnostic structure.

## Output structure

```
eval-harness/
├── README.md
├── pyproject.toml (or requirements.txt)
├── data/
│   ├── eval_dataset.jsonl      # Evaluation examples
│   └── README.md               # Dataset documentation
├── evals/
│   ├── __init__.py
│   ├── runner.py               # Main entry point
│   ├── metrics/
│   │   ├── __init__.py
│   │   ├── exact_match.py
│   │   ├── semantic_similarity.py
│   │   ├── llm_judge.py        # LLM-as-judge scorer
│   │   └── task_specific.py    # Your custom metrics
│   ├── dataset.py              # Dataset loading and validation
│   └── reporter.py             # Results aggregation and output
└── results/
    └── .gitkeep
```

## Dataset format (`eval_dataset.jsonl`)

```jsonl
{"id": "001", "input": "What is the capital of France?", "expected": "Paris", "metadata": {"category": "geography", "difficulty": "easy"}}
{"id": "002", "input": "Summarize: [long text]", "expected": "The text discusses...", "metadata": {"category": "summarization"}}
{"id": "003", "input": {"context": "...", "question": "..."}, "expected": {"answer": "...", "sources": ["doc1"]}, "metadata": {"category": "rag-qa"}}
```

## Runner (`evals/runner.py`)

```python
import asyncio
import json
from pathlib import Path
from datetime import datetime
from typing import Callable, Any

from .dataset import load_dataset
from .metrics import METRICS_REGISTRY
from .reporter import generate_report


async def run_eval(
    model_fn: Callable[[Any], Any],  # Your model/LLM call function
    dataset_path: str = "data/eval_dataset.jsonl",
    metrics: list[str] = None,
    output_dir: str = "results",
    run_name: str = None,
    max_concurrent: int = 5,
) -> dict:
    """
    Run evaluation harness.
    
    Args:
        model_fn: Async function taking input, returning output
        dataset_path: Path to .jsonl eval dataset
        metrics: List of metric names to compute (default: all registered)
        output_dir: Where to save results
        run_name: Human-readable name for this run
        max_concurrent: Max parallel model calls
    """
    examples = load_dataset(dataset_path)
    metrics = metrics or list(METRICS_REGISTRY.keys())
    run_name = run_name or f"eval_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    print(f"Running eval '{run_name}': {len(examples)} examples, metrics: {metrics}")
    
    # Run model on all examples (with concurrency limit)
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def run_one(example):
        async with semaphore:
            try:
                actual = await model_fn(example["input"])
                return {**example, "actual": actual, "error": None}
            except Exception as e:
                return {**example, "actual": None, "error": str(e)}
    
    results = await asyncio.gather(*[run_one(ex) for ex in examples])
    
    # Score each result
    scored_results = []
    for result in results:
        scores = {}
        if result["error"] is None:
            for metric_name in metrics:
                metric_fn = METRICS_REGISTRY.get(metric_name)
                if metric_fn:
                    scores[metric_name] = metric_fn(
                        predicted=result["actual"],
                        expected=result["expected"],
                        input=result["input"],
                    )
        scored_results.append({**result, "scores": scores})
    
    # Generate report
    report = generate_report(scored_results, run_name, metrics)
    
    # Save results
    out_path = Path(output_dir) / run_name
    out_path.mkdir(parents=True, exist_ok=True)
    (out_path / "results.jsonl").write_text(
        "\n".join(json.dumps(r) for r in scored_results)
    )
    (out_path / "summary.json").write_text(json.dumps(report, indent=2))
    
    print(f"Results saved to {out_path}/")
    print_summary(report)
    
    return report
```

## Metrics (`evals/metrics/`)

### Exact match

```python
# metrics/exact_match.py
import re

def exact_match(predicted: str, expected: str, **_) -> dict:
    pred = predicted.strip().lower()
    exp = expected.strip().lower()
    return {
        "score": 1.0 if pred == exp else 0.0,
        "details": {"predicted": predicted, "expected": expected}
    }

def normalized_exact_match(predicted: str, expected: str, **_) -> dict:
    """Normalize whitespace, punctuation, and case."""
    def normalize(text: str) -> str:
        text = text.lower()
        text = re.sub(r"[^\w\s]", "", text)
        text = " ".join(text.split())
        return text
    
    return {
        "score": 1.0 if normalize(predicted) == normalize(expected) else 0.0,
    }
```

### Semantic similarity

```python
# metrics/semantic_similarity.py
from sentence_transformers import SentenceTransformer, util

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def semantic_similarity(predicted: str, expected: str, threshold: float = 0.7, **_) -> dict:
    model = get_model()
    emb_pred = model.encode(predicted, convert_to_tensor=True)
    emb_exp = model.encode(expected, convert_to_tensor=True)
    score = float(util.cos_sim(emb_pred, emb_exp))
    
    return {
        "score": score,
        "passed": score >= threshold,
        "details": {"similarity": score, "threshold": threshold}
    }
```

### LLM-as-judge

```python
# metrics/llm_judge.py
import json
from openai import AsyncOpenAI

client = AsyncOpenAI()

JUDGE_SYSTEM_PROMPT = """You are an expert evaluator. Given a question, a correct answer, and a model's response,
rate the model's response quality on a scale of 1-5 and explain your reasoning.

Respond in JSON:
{
    "score": <1-5>,
    "reasoning": "<brief explanation>",
    "correct": <true/false>
}"""

async def llm_judge(predicted: str, expected: str, input: str, **_) -> dict:
    prompt = f"""Question: {input}
Correct Answer: {expected}
Model's Response: {predicted}

Rate the model's response."""
    
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": JUDGE_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0,
    )
    
    result = json.loads(response.choices[0].message.content)
    return {
        "score": result["score"] / 5.0,  # Normalize to 0-1
        "raw_score": result["score"],
        "correct": result["correct"],
        "reasoning": result["reasoning"],
    }
```

### Metrics registry

```python
# metrics/__init__.py
from .exact_match import exact_match, normalized_exact_match
from .semantic_similarity import semantic_similarity
from .llm_judge import llm_judge

METRICS_REGISTRY = {
    "exact_match": exact_match,
    "normalized_exact_match": normalized_exact_match,
    "semantic_similarity": semantic_similarity,
    "llm_judge": llm_judge,
}
```

## Reporter (`evals/reporter.py`)

```python
import statistics
from collections import defaultdict

def generate_report(results: list[dict], run_name: str, metrics: list[str]) -> dict:
    total = len(results)
    errors = sum(1 for r in results if r.get("error"))
    
    # Aggregate scores per metric
    metric_scores = defaultdict(list)
    for result in results:
        for metric, score_data in result.get("scores", {}).items():
            score = score_data["score"] if isinstance(score_data, dict) else score_data
            metric_scores[metric].append(score)
    
    metric_summary = {}
    for metric, scores in metric_scores.items():
        metric_summary[metric] = {
            "mean": statistics.mean(scores),
            "median": statistics.median(scores),
            "stdev": statistics.stdev(scores) if len(scores) > 1 else 0,
            "min": min(scores),
            "max": max(scores),
            "pass_rate": sum(1 for s in scores if s >= 0.7) / len(scores),
        }
    
    return {
        "run_name": run_name,
        "total_examples": total,
        "errors": errors,
        "success_rate": (total - errors) / total,
        "metrics": metric_summary,
    }

def print_summary(report: dict):
    print(f"\n{'='*50}")
    print(f"Eval: {report['run_name']}")
    print(f"Examples: {report['total_examples']} | Errors: {report['errors']}")
    print(f"\nMetrics:")
    for metric, stats in report["metrics"].items():
        print(f"  {metric}: mean={stats['mean']:.3f} | pass_rate={stats['pass_rate']:.1%}")
    print('='*50)
```

## CLI entry point

```python
# run_eval.py — example usage
import asyncio
import sys

from evals.runner import run_eval
from openai import AsyncOpenAI

client = AsyncOpenAI()

async def my_model(input_data) -> str:
    """Replace with your actual model call."""
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": str(input_data)}],
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    report = asyncio.run(run_eval(
        model_fn=my_model,
        dataset_path="data/eval_dataset.jsonl",
        metrics=["exact_match", "semantic_similarity"],
        run_name=sys.argv[1] if len(sys.argv) > 1 else None,
    ))
    
    # Exit with failure if quality threshold not met
    if report["metrics"]["semantic_similarity"]["mean"] < 0.7:
        sys.exit(1)
```

## Calibration

- **LLM/chat evaluation**: Use `llm_judge` + `semantic_similarity`; exact match rarely appropriate
- **RAG evaluation**: Add retrieval metrics (precision/recall on sources); use RAGAS if available
- **Classification**: Accuracy, F1, confusion matrix — add to metrics registry
- **Code generation**: Execution-based eval — run the code and check test pass rate
- **Simple/quick setup**: Just the runner + JSONL dataset + one metric; no async needed
