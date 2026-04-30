# SFT-then-RL Outperforms Mixed-Policy Methods for LLM Reasoning

**ArXiv ID:** [2604.23747](https://arxiv.org/abs/2604.23747)  
**Authors:** Alexis Limozin, Eduard Durech, Torsten Hoefler, Imanol Schlag, Valentina Pyatkin  
**Affiliations:** ETH AI Center / ETH Zürich, EPFL, Allen Institute for AI  
**Submitted:** April 26, 2026  
**Field:** Machine Learning / LLM Post-Training

---

## Executive Summary

A wave of recent papers claimed that *mixed-policy* training methods — which interleave or blend supervised fine-tuning (SFT) and reinforcement learning (RL) signals — outperform the classical SFT-then-RL two-stage pipeline for LLM reasoning. This paper shows those claims rest on deflated baselines caused by two reproducible software bugs in widely-used training frameworks (DeepSpeed, OpenRLHF). After fixing the bugs, the standard SFT-then-RL pipeline beats every published mixed-policy method evaluated — by +3.8 points on Qwen2.5-Math-7B and +22.2 points on Llama-3.1-8B. The findings call for a re-evaluation of a substantial body of recent LLM reasoning training literature.

---

## Problem Statement

### The Rise of Mixed-Policy Training

After RLHF demonstrated that reinforcement learning could align LLMs with human preferences, researchers explored whether the SFT and RL stages could be *interleaved* rather than run sequentially. Mixed-policy methods blend on-policy RL rollouts with SFT data within the same training loop, or use hybrid objectives that simultaneously optimize both supervised and reinforcement signals.

A growing body of papers — spanning 2025 and early 2026 — reported that these mixed-policy methods substantially outperform sequential SFT-then-RL on mathematical reasoning benchmarks. This led to increasing adoption of mixed-policy approaches in open-source reasoning model training pipelines.

### The Confound

When published results show Method A outperforming Method B, there is an implicit assumption that Method B was correctly implemented. This paper challenges that assumption: the SFT baselines used in virtually all mixed-policy comparison papers were silently corrupted by bugs in the underlying training frameworks, systematically underestimating SFT performance and artificially inflating the apparent gains of mixed-policy methods.

---

## Core Concepts & Theory

### The Two-Stage SFT-then-RL Pipeline

The classical approach to training reasoning models is:
1. **SFT (Supervised Fine-Tuning)**: Fine-tune the base model on high-quality reasoning traces (correct chain-of-thought solutions). This teaches the model *how* to reason by imitation.
2. **RL (Reinforcement Learning)**: Apply RL (e.g., GRPO, PPO) using a reward signal (correctness of final answer) to further optimize the policy toward outcomes the SFT stage could not fully capture.

The two stages are complementary: SFT provides a well-initialized policy close to the desired behavior; RL explores and refines it toward higher reward.

### Mixed-Policy Methods

Mixed-policy methods replace the clean two-stage boundary with various interleaving strategies:
- **Simultaneous SFT+RL**: Joint loss combining SFT cross-entropy and RL policy gradient terms in every update
- **Alternating mini-batches**: SFT and RL mini-batches interspersed within an epoch
- **On-policy data augmentation**: RL rollouts are filtered and added back to the SFT corpus

These methods claim to avoid the "forgetting" problem where the RL stage degrades capabilities learned during SFT, or to provide better exploration by keeping the SFT signal as a stabilizer.

### Gradient Accumulation and CPU Offloading

Modern LLM training uses gradient accumulation to simulate large batch sizes across multiple forward-backward micro-batch steps before performing an optimizer update. When GPU memory is insufficient to hold all optimizer states (e.g., Adam's first and second moment estimates for a 7B+ parameter model), frameworks offload optimizer states to CPU RAM.

**The interaction bug**: DeepSpeed's CPU-offloaded optimizer implementation does not correctly handle the case where gradient accumulation is used. Specifically, intermediate micro-batches in an accumulation sequence have their gradients silently discarded rather than accumulated before the optimizer step. This means only the *last* micro-batch in each accumulation window influences the update — equivalent to training with a much smaller effective batch size and noisier gradients.

---

## Main Ideas & Key Contributions

### Contribution 1: Discovery and Documentation of Two Bugs

**Bug A — DeepSpeed CPU-offloaded optimizer + gradient accumulation:**
- **Location**: DeepSpeed's `CPUAdam` and related CPU-offload optimizer paths
- **Behavior**: When `gradient_accumulation_steps > 1` and CPU offloading is active, intermediate micro-batch gradients are dropped before the optimizer step
- **Downstream impact**: TRL, OpenRLHF, and Llama-Factory all invoke DeepSpeed under the hood for large-model training; all inherit the bug
- **Effect on training**: Effective batch size is reduced to 1 micro-batch's worth of data; gradients are noisier; SFT convergence is degraded

**Bug B — OpenRLHF loss aggregation:**
- **Location**: OpenRLHF's mini-batch loss accumulation logic within an RL update step
- **Behavior**: Per-mini-batch losses are combined without proper normalization by the number of tokens or samples in each mini-batch; this produces an incorrectly weighted aggregate gradient
- **Effect on training**: SFT losses computed within OpenRLHF's training loop are further suppressed relative to the true gradient signal

**Combined effect**: The two bugs compound to suppress SFT-phase performance. Mixed-policy methods, which often use different code paths or were evaluated against these buggy SFT baselines, appeared to "win" but were actually comparing against a handicapped opponent.

### Contribution 2: Rigorous Controlled Comparison

After patching both bugs, the authors re-run SFT-then-RL using the corrected implementations and compare against every mixed-policy method they evaluate. The corrected SFT-then-RL pipeline:
- Uses DeepSpeed without CPU offloading (or with a patched version)
- Uses correctly normalized loss aggregation
- All other hyperparameters held constant across conditions

### Contribution 3: Implications for the Literature

The paper provides a systematic assessment of which published mixed-policy results are likely affected by these bugs, based on which frameworks they report using. Papers that used TRL, OpenRLHF, or Llama-Factory for their SFT baseline likely have deflated baselines.

---

## Methodology & Implementation

### Models Evaluated

| Model | Scale |
|-------|-------|
| Qwen2.5-Math-7B | 7 billion parameters |
| Llama-3.1-8B | 8 billion parameters |

These represent two distinct model lineages with different pretraining distributions, providing evidence that the findings generalize across architectures.

### Benchmarks

Mathematical reasoning benchmarks consistent with the field standard at the time of submission, including MATH, AIME, and related olympiad/competition mathematics datasets. All experiments use Pass@1 as the primary metric.

### Training Setup

- **Buggy baseline**: SFT run with DeepSpeed CPU offload + gradient accumulation (reproducing the inadvertent bug)
- **Fixed SFT-then-RL**: SFT run without CPU offload (or patched offload), followed by GRPO-style RL
- **Mixed-policy methods**: Re-run or taken from reported numbers in original papers; all use the same downstream RL stage

### Key Results

| Condition | Qwen2.5-Math-7B | Llama-3.1-8B |
|-----------|----------------|--------------|
| Best mixed-policy method (literature) | Baseline | Baseline |
| SFT-then-RL (buggy, reproduced) | −X pts | −Y pts |
| **SFT-then-RL (fixed)** | **+3.8 pts** | **+22.2 pts** |

The Llama-3.1-8B gap is dramatically larger (+22.2), suggesting this model's SFT convergence was particularly sensitive to the gradient accumulation bug.

### Bug Attribution Breakdown

The optimizer bug (DeepSpeed) accounts for the majority of the observed gap. The loss aggregation bug (OpenRLHF) contributes an additional smaller but statistically significant effect. The two bugs are independent and both must be fixed for full recovery.

---

## Practical Applications & Real-World Use Cases

### 1. Training Pipeline Auditing

Any team training reasoning models with TRL, OpenRLHF, or Llama-Factory should audit their configurations:
- Check whether CPU offloading is enabled simultaneously with gradient accumulation
- Verify loss normalization logic in custom training loops
- Re-run SFT baselines with the patched configurations before drawing conclusions about training method comparisons

### 2. Reproduced Research Results

Labs and practitioners who adopted mixed-policy methods based on the published literature should re-evaluate whether the simpler SFT-then-RL pipeline achieves comparable or better results with correct implementations. This can reduce complexity and training infrastructure requirements.

### 3. Framework Development

The bugs identified have been confirmed to exist in widely-used open-source frameworks. Fix PRs or configuration warnings should be submitted upstream to DeepSpeed, TRL, OpenRLHF, and Llama-Factory to prevent future contamination of research results.

### 4. Benchmark Re-evaluation

Research groups that published mixed-policy comparison results using affected frameworks should consider issuing corrections or addenda, particularly if the comparison used TRL or OpenRLHF for SFT baselines.

---

## Insights & Implications

### Scientific Integrity and Reproducibility

This paper is a case study in how software-level implementation bugs can silently corrupt entire lines of research. The bugs are not obvious — they manifest only when CPU offloading and gradient accumulation are used together, a common configuration for large models on resource-constrained hardware. Researchers running ablations would have observed consistently worse SFT performance without knowing why, and may have attributed the difference to the training method rather than the bug.

### The Baseline Problem

The broader lesson is that competitive claims in ML ("Method A outperforms Method B") are only as reliable as the weakest link in the comparison chain. Baselines are often implemented with less care than the proposed method, a known problem in ML research. This paper is a particularly sharp example: the "weaker" SFT-then-RL pipeline was weaker only because of framework bugs, not because of any inherent limitation.

### Simplicity Wins (When Correctly Implemented)

The finding that SFT-then-RL outperforms mixed-policy methods — once both are correctly implemented — supports the principle of preferring simpler, well-understood methods before adding complexity. Mixed-policy methods add complexity (joint objectives, careful hyperparameter balancing between SFT and RL terms) without delivering the promised benefit.

### Limitations

- The comparison is limited to mathematical reasoning; domains where mixed-policy methods were evaluated for different reasons (e.g., safety alignment) are not studied.
- The paper does not claim that mixed-policy methods are *never* useful — only that the specific gains reported in the evaluated papers were artifacts of buggy baselines.
- Future work may identify regimes (e.g., very long RL training, out-of-distribution generalization) where mixed-policy methods provide genuine benefits over a correctly implemented SFT-then-RL baseline.
- The two specific bugs will likely be patched in framework updates, but new bugs in complex distributed training setups will always be a risk.

---

## Code & Resources

- **Paper:** [https://arxiv.org/abs/2604.23747](https://arxiv.org/abs/2604.23747)
- **HTML version:** [https://arxiv.org/html/2604.23747](https://arxiv.org/html/2604.23747)

**Affected Frameworks (check for patches):**
- [DeepSpeed](https://github.com/microsoft/DeepSpeed) — CPU-offloaded optimizer bug with gradient accumulation
- [TRL (Hugging Face)](https://github.com/huggingface/trl) — inherits DeepSpeed bug
- [OpenRLHF](https://github.com/OpenRLHF/OpenRLHF) — inherits DeepSpeed bug + independent loss aggregation bug
- [Llama-Factory](https://github.com/hiyouga/LLaMA-Factory) — inherits DeepSpeed bug

**How to Check If You Are Affected:**
```python
# Red flag configuration (in DeepSpeed config):
{
  "zero_optimization": {
    "stage": 2,
    "offload_optimizer": {
      "device": "cpu"  # This triggers the bug when combined with gradient accumulation
    }
  }
}
# gradient_accumulation_steps > 1 must also be set in the trainer config

# Safe alternative: use stage 2 without CPU offload, or reduce effective batch
# size by training with smaller gradient_accumulation_steps on more steps.
```

---

## Related Work & Context

### Mixed-Policy Methods Under Review

Papers in the mixed-policy category (2025–early 2026) that used the affected frameworks for their SFT baselines are the primary candidates for re-evaluation. These include papers proposing hybrid SFT+GRPO objectives, alternating SFT/RL curriculum methods, and online DPO variants.

### Earlier Skepticism of Multi-Stage Complexity

- **"Good SFT Optimizes for SFT, Better SFT Prepares for Reinforcement Learning"** (2602.01058): Argues that the quality of the SFT stage determines RL success — consistent with this paper's finding that a correctly implemented SFT stage is sufficient to win.
- **"From SFT to RL: Demystifying the Post-Training Pipeline"** (2602.14012): Provides a systematic overview of the two-stage process and identifies common failure modes.

### The Broader Gradient Accumulation + Offloading Problem

The underlying DeepSpeed bug is related to a class of known issues with gradient accumulation in distributed training:
- Hugging Face Accelerate has had gradient accumulation correctness issues in the past
- PyTorch Lightning has documented similar interactions with DeepSpeed gradient accumulation
- This pattern suggests distributed training frameworks need more systematic correctness testing for accumulation-offload interactions

### Where This Research May Lead

- **Framework testing standards**: Establishing correctness tests for training frameworks that specifically validate gradient accumulation under all offloading configurations
- **Baseline protocol papers**: Community calls for standardized baseline implementation protocols, similar to what NLP evaluation has done with shared task setups
- **Re-evaluation campaigns**: Systematic re-running of top LLM reasoning papers with corrected implementations
