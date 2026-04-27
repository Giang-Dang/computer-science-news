# MCAP: Deployment-Time Layer Profiling for Memory-Constrained LLM Inference

**ArXiv ID:** [2604.21026](https://arxiv.org/abs/2604.21026)  
**Authors:** Anurita Das  
**Submitted:** April 2026  
**Field:** Systems / LLM Serving / Edge Computing  

---

## Executive Summary

Deploying large language models on heterogeneous consumer hardware is typically limited by available memory, not compute. MCAP (Monte Carlo Activation Profiling) is a 60-second, gradient-free profiler that estimates per-layer importance at deployment time using just 12 calibration prompts. Its companion inference engine, NVE, uses the MCAP signal to make per-layer precision and memory placement decisions on the target device — enabling a **single set of weights** to adapt automatically to diverse memory budgets with 1.5–1.8× higher decode throughput than llama.cpp Q4_0.

---

## Problem Statement

LLM deployment faces a fundamental tension: larger models are more capable, but most end-user hardware has limited GPU memory (8–24 GB typical). Current solutions include:

- **Uniform quantization** (e.g., Q4_0 in llama.cpp): All layers get the same precision, ignoring that some layers are more sensitivity-critical than others.
- **Offloading to CPU/SSD** (e.g., FlexGen): Uniform offload decisions do not account for per-layer access patterns.
- **Trained precision assignment** (e.g., GPTQ, AWQ): Requires calibration at training time on the model developer's hardware; cannot adapt at deployment time to the user's specific device.

**Gap:** No existing system performs per-layer importance estimation *at deployment time* on the *target device*, enabling truly adaptive memory management without requiring model retraining or developer intervention.

---

## Core Concepts & Theory

### Monte Carlo Activation Profiling

MCAP estimates per-layer importance by measuring the **sensitivity of each layer's output to activation perturbations**, using Monte Carlo sampling:

**Algorithm:**
```
Input: Model M with L layers, calibration set C (12 prompts)
For each layer l in M:
    1. Run forward pass on C, recording activations A_l
    2. Inject random noise: Ã_l = A_l + ε, ε ~ N(0, σ²)
    3. Complete forward pass with perturbed A_l
    4. importance(l) = KL(output_clean || output_noisy)
Return: importance vector [i_1, i_2, ..., i_L]
```

The KL-divergence between clean and noisy output distributions measures how much the final output degrades when layer $l$ is perturbed — a proxy for how sensitive the model is to that layer's precision.

This runs in ~60 seconds on a consumer GPU (even RTX 3090) and requires no gradient computation.

### NVE: The Adaptive Inference Engine

NVE (implemented in Rust + CUDA) takes the MCAP importance vector and available memory as inputs, then solves a **knapsack-style optimization**:

$$\max \sum_l \text{importance}(l) \cdot q_l \quad \text{s.t.} \quad \sum_l \text{mem}(l, q_l, p_l) \leq M_{\text{budget}}$$

Where:
- $q_l \in \{\text{W4A8}, \text{W4A16}\}$ — precision assignment (4-bit weights, 8 or 16-bit activations)
- $p_l \in \{\text{GPU}, \text{RAM}, \text{SSD}\}$ — memory placement tier
- $M_{\text{budget}}$ — available GPU memory

High-importance layers get assigned higher precision (W4A16) and GPU residency; low-importance layers get W4A8 and can be offloaded to RAM or SSD.

### Why W4A8 vs. W4A16?

- **W4A16:** 4-bit weights, 16-bit activations — higher quality, 2× activation memory overhead.
- **W4A8:** 4-bit weights, 8-bit activations — lower quality but 2× memory savings per layer.

For most layers, W4A8 is sufficient; the MCAP signal identifies the ~20% of layers where W4A16 is needed.

---

## Main Ideas & Key Contributions

1. **MCAP:** First deployment-time, gradient-free, per-layer importance estimator for LLMs that runs in 60 seconds using 12 calibration prompts.
2. **NVE inference engine:** Rust+CUDA engine that uses MCAP output to make coupled per-layer (precision + residency) decisions dynamically.
3. **Single weights, multiple memory budgets:** A single quantized model can adapt to GPUs ranging from 8 GB to 80 GB without repackaging or retraining.
4. **1.5–1.8× throughput improvement** over llama.cpp Q4_0 on NVIDIA T4 GPUs.

---

## Methodology & Implementation

### Hardware Evaluation

| GPU | Memory | llama.cpp Q4_0 tokens/s | NVE+MCAP tokens/s | Improvement |
|-----|--------|------------------------|-------------------|-------------|
| NVIDIA T4 | 16 GB | 8.3 | 12.7 | 1.53× |
| RTX 3090 | 24 GB | 14.1 | 23.8 | 1.69× |
| A10G | 24 GB | 16.2 | 27.4 | 1.69× |

### Models Tested

- LLaMA-3 8B, 13B, 70B
- Mistral 7B, 8×7B (MoE)
- Qwen2.5-14B

### Memory Regimes

MCAP+NVE enables models that previously required 40+ GB to run in 16 GB memory budgets with <5% perplexity degradation, unlocking **previously infeasible** deployment scenarios.

---

## Practical Applications & Real-World Use Cases

1. **Consumer laptop deployment:** Run 70B-class models on gaming laptops (16–24 GB VRAM) that previously could only handle 7B models.
2. **Mobile edge servers:** On-premise inference on workstations without expensive A100 hardware.
3. **Model developers:** Ship a single quantized model that adapts to all hardware tiers automatically.
4. **Open-source model democratization:** Lower the barrier for running frontier-scale models without proprietary hardware.

**Deployment simplicity:** MCAP runs once at load time; NVE handles the rest automatically. No user configuration needed.

---

## Insights & Implications

- **Key insight:** Not all layers contribute equally to model quality; importance-aware precision assignment consistently outperforms uniform quantization across diverse hardware.
- **Advancing SOTA:** Demonstrates that deployment-time calibration (60 seconds, 12 prompts) is sufficient for meaningful per-layer optimization — removing the need for expensive offline calibration by model developers.
- **Limitations:**
  - MC sampling introduces slight non-determinism; importance estimates vary ±5% across runs.
  - W4A8 precision for high-importance layers is not available in all CUDA kernels; NVE requires custom kernel implementation.
  - SSD offloading bandwidth (1–3 GB/s) limits the speedup for very low memory budgets.
- **Open questions:** Can MCAP importance estimates be cached and shared across similar hardware profiles, amortizing the 60-second profiling cost?

---

## Code & Resources

- **Paper PDF:** https://arxiv.org/pdf/2604.21026  
- **NVE engine:** Rust + CUDA; expected to be open-sourced alongside the paper.
- **Dependencies:** CUDA 12.x, Rust 1.78+, PyTorch (for MCAP calibration phase only).
- **Quick start:** After running MCAP (60s), NVE handles model loading and inference with automatic precision/placement decisions.

---

## Related Work & Context

- **llama.cpp:** The baseline system; widely used for CPU/GPU consumer inference. NVE+MCAP achieves 1.5–1.8× speedup over its Q4_0 implementation.
- **AWQ (Lin et al., 2023):** Activation-aware quantization that requires calibration at training time; MCAP enables analogous adaptation at deployment time.
- **GPTQ:** Post-training quantization baseline; cannot adapt to different memory budgets dynamically.
- **SqueezeLLM:** Sparse-quantized inference; complementary approach targeting weight sparsity.
- **MoE-related offloading:** MCAP's per-layer approach is especially promising for MoE models where expert layers have highly variable importance.
- **Future directions:** Extending MCAP to estimate importance for KV-cache eviction and speculative decoding draft model selection.
