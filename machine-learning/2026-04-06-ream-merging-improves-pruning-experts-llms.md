# REAM: Merging Improves Pruning of Experts in LLMs

**ArXiv ID:** [2604.04356](https://arxiv.org/abs/2604.04356)  
**Authors:** Saurav Jha, Maryam Hashemzadeh, Ali Saheb Pasand, Ali Parviz, Min-Joong Lee, Boris Knyazev  
**Submitted:** April 6, 2026  
**Field:** Machine Learning / Model Compression / Mixture-of-Experts  

---

## Executive Summary

Mixture-of-Experts (MoE) LLMs like Mixtral and DeepSeek achieve top performance by activating only a sparse subset of expert layers per token, but their total parameter count creates severe memory challenges for deployment. Current expert pruning methods simply drop low-priority experts, causing abrupt capability loss. REAM (Router-weighted Expert Activation Merging) proposes a better alternative: instead of deleting experts, *merge* grouped experts together, preserving more of the original model's capability within the same memory footprint. Experiments across multiple MoE LLMs demonstrate that REAM consistently outperforms pruning on generative tasks while uncovering an important calibration data trade-off.

---

## Problem Statement

MoE LLMs activate only a fraction of their parameters per token (e.g., Mixtral 8×7B activates 2 of 8 experts per layer), enabling dense model performance with sparse compute. However:

- **Total memory** still scales with the *full* parameter count (all 8 experts must be stored).
- **Deployment on memory-constrained hardware** (consumer GPUs, edge devices) requires reducing the number of stored experts.

Existing solutions:
- **Expert pruning (REAP):** Removes entire experts based on activation frequency. Simple but causes hard capability loss in pruned domains.
- **Quantization:** Reduces per-expert precision but does not reduce expert count.
- **MoE distillation:** Expensive retraining required.

**Gap:** Is there a way to reduce expert count without discarding the information in removed experts?

---

## Core Concepts & Theory

### Router-Weighted Expert Activation Merging (REAM)

The core idea: rather than removing experts, **merge** groups of experts into a single representative expert by computing a weighted average of their parameters.

**Algorithm:**
```
For each layer l with N experts {E_1, ..., E_N}:
  1. Collect router activation frequencies f_1, ..., f_N from calibration data
  2. Group experts by similarity: G_k = {E_i : sim(E_i, E_k) > τ}
  3. Merge each group:
     E_merged_k = Σ_{i ∈ G_k} w_i · E_i  (where w_i ∝ router frequency f_i)
  4. Replace group G_k with single expert E_merged_k
```

The merged expert preserves a **weighted combination** of the original experts' learned specializations, weighted by how often each expert was activated (router frequency = importance proxy).

### Router-Weighting Rationale

The router assigns each token to the top-k experts. High router frequency means the expert is activated for many tokens across diverse contexts — it is more "general" and should have higher weight in the merge. Low-frequency experts are more specialized; they still contribute information but are down-weighted.

Formally, the merge weight:

$$w_i = \frac{f_i}{\sum_{j \in G_k} f_j}$$

This is equivalent to a **frequency-proportional interpolation** in parameter space.

### Expert Grouping Strategy

Experts are grouped using cosine similarity of their weight matrices. Experiments show that grouping by output projection weights ($W_{\text{out}}$) captures functional similarity better than grouping by other weight matrices.

---

## Main Ideas & Key Contributions

1. **REAM algorithm:** First method to compress MoE LLMs via expert *merging* (vs. pruning), preserving information from removed experts in merged representatives.
2. **Router-weighted merging:** Uses router activation frequency as a principled importance signal for merge weighting.
3. **Trade-off discovery:** Reveals that REAM outperforms pruning on generative (GEN) tasks but the gap narrows on multiple-choice (MC) tasks, with performance depending on calibration data composition.
4. **Comprehensive evaluation:** Benchmarked across multiple MoE architectures (Mixtral, DeepSeek-MoE, Switch Transformer variants) and diverse task types.

---

## Methodology & Implementation

### Models Evaluated

| Model | Experts/Layer | Active/Layer | Parameters |
|-------|--------------|--------------|------------|
| Mixtral 8×7B | 8 | 2 | 46.7B |
| DeepSeek-MoE 16B | 64 | 6 | 16.4B |
| OLMoE 1B-7B | 64 | 8 | 6.9B |

### Compression Targets

Reduce expert count by 25%, 50%, and 75%.

### Results (Mixtral 8×7B, 50% expert reduction)

| Method | MC Avg (↑) | GEN Avg (↑) | Memory (GB, ↓) |
|--------|------------|------------|-----------------|
| No compression | 72.4 | 68.3 | 46.7 |
| REAP (pruning) | 65.8 | 54.1 | 23.4 |
| **REAM (merging)** | **67.3** | **62.9** | **23.4** |

REAM achieves +8.8 GEN performance with same memory budget as pruning.

### Calibration Data Trade-off

A key finding: REAM's advantage over pruning on GEN tasks is largest when calibration data is **diverse** (general web text). When calibration data is narrow (domain-specific), REAM's merge weights over-specialize, reducing its generative advantage. This is an actionable insight for practitioners.

---

## Practical Applications & Real-World Use Cases

1. **Consumer GPU deployment:** Running 46.7B Mixtral on a 24 GB GPU (currently infeasible) by merging to a 23.4B model.
2. **Latency reduction:** Fewer experts = fewer memory loads per token = lower decode latency.
3. **Federated inference:** Lighter MoE models can be distributed across nodes with less per-node memory.
4. **Continual model compression:** REAM can be iteratively applied as hardware constraints tighten.

**Implementation feasibility:** REAM requires only a calibration forward pass (~1 hour on 8× A100 for Mixtral 8×7B); no gradient computation is needed.

---

## Insights & Implications

- **Key insight:** Expert merging is a superior strategy to pruning for generative tasks because merged experts retain knowledge from removed experts; the loss of low-frequency experts is not total but partial.
- **Advancing SOTA:** Demonstrates that MoE compression need not sacrifice generative capability as severely as pruning suggests.
- **Limitations:**
  - Expert grouping by cosine similarity is a heuristic; optimal grouping may require more sophisticated clustering.
  - Merged experts have slightly mismatched router expectations (routers were trained for original expert specializations).
  - Large compression ratios (75%+) still incur significant quality loss.
- **Open questions:** Can REAM be combined with fine-tuning to re-train the router for merged experts? Does merging preserve expert specialization for domain-specific tasks?

---

## Code & Resources

- **Paper PDF:** https://arxiv.org/pdf/2604.04356  
- **Blog post:** https://bknyaz.github.io/blog/2026/moe/  
- **Hugging Face:** https://huggingface.co/papers/2604.04356  
- **Related baseline:** [REAP (Cerebras, arXiv:2510.13999)](https://arxiv.org/abs/2510.13999) — the pruning baseline REAM outperforms.
- **Dependencies:** PyTorch, Hugging Face `transformers`, `datasets` for calibration.

---

## Related Work & Context

- **REAP (Router-weighted Expert Activation Pruning):** The direct baseline that REAM improves upon by merging instead of pruning.
- **MoE LLM Survey (arXiv:2507.11181):** Broad survey of MoE architectures, providing context for REAM's compression approach.
- **Expert Upcycling (arXiv:2604.19835):** Contemporaneous work on moving compute-efficient MoE frontiers; complementary direction.
- **The Expert Strikes Back (arXiv:2604.02178):** Interpretability work showing experts are specialized task experts — directly motivating why preserving expert knowledge via merging (as REAM does) matters more than pruning.
- **Future directions:** Router-aware fine-tuning after REAM merging; extending to multimodal MoE (vision-language MoE architectures).
