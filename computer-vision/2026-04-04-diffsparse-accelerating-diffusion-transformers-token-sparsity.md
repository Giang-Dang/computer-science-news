# DiffSparse: Accelerating Diffusion Transformers with Learned Token Sparsity

**ArXiv ID:** [2604.03674](https://arxiv.org/abs/2604.03674)  
**Authors:** Haowei Zhu, Ji Liu, Ziqiong Liu, Dong Li, Junhai Yong, Bin Wang, Emad Barsoum  
**Institutions:** Advanced Micro Devices (AMD), Tsinghua University, BNRist  
**Submitted:** April 4, 2026  
**Published at:** ICLR 2026  
**Field:** Computer Vision / Efficient Deep Learning

---

## Executive Summary

DiffSparse introduces a differentiable framework for learning layer-wise token sparsity in Diffusion Transformer (DiT) models, dramatically reducing the computational cost of multi-step image generation inference. By combining a learnable sparsity allocation network with a dynamic programming solver, DiffSparse achieves a **54% reduction in FLOPs** on PixArt-α while simultaneously improving generation quality compared to the original dense model. This work is significant because it provides a principled, end-to-end trainable approach to inference acceleration that adapts sparsity dynamically per layer and timestep rather than using fixed hand-crafted rules.

---

## Problem Statement

### The Computational Wall in Diffusion Models

Diffusion Transformer (DiT) models have emerged as the dominant architecture for high-quality image and video synthesis, surpassing convolutional alternatives on metrics like FID and IS. However, they impose a severe computational cost: unlike autoregressive generation (one forward pass), diffusion models require **20–1000 sequential denoising steps**, each executing a full transformer forward pass with quadratic attention complexity over all spatial tokens.

For a 512×512 image with patch size 2, this yields 16,384 tokens per step — and with 20 steps, the full generation requires ~330 billion multiply-add operations on a typical DiT-XL/2 model. This makes DiT-based generation **10–100× more expensive** than comparable autoregressive models.

### Limitations of Prior Work

Previous acceleration methods fall into two camps:

1. **Step reduction approaches** (DDIM, DPM-Solver, consistency models): Reduce the number of sampling steps. Effective but bottlenecked by a minimum step count for quality. These operate at the algorithm level and cannot be combined straightforwardly with token-level optimizations.

2. **Token/Layer caching approaches** (∆-DiT, DeepCache, TokenCache): Observe that consecutive denoising steps produce similar activations and cache them to avoid redundant computation. However, these methods use **fixed, handcrafted caching schedules** — every 2nd or 3rd step is cached, regardless of the dynamic content or the layer's actual redundancy.

The core limitation of existing caching methods is the **lack of adaptive, learned sparsity allocation**: different layers have different redundancy profiles across timesteps, and different images require different amounts of computation in different spatial regions. A fixed schedule fails to capture this variability.

---

## Core Concepts & Theory

### Diffusion Transformers (DiT) Background

A DiT operates on a sequence of noisy latent tokens $\mathbf{z}_t \in \mathbb{R}^{N \times d}$ at timestep $t$, passing them through $L$ transformer blocks. Each block consists of:
- Multi-head self-attention (MHSA)
- Feed-forward network (FFN)
- AdaLN conditioning on timestep $t$ and class label $c$

The denoising objective is:
$$\mathcal{L} = \mathbb{E}_{t, \mathbf{z}_0, \epsilon}\left[\|\epsilon - \epsilon_\theta(\mathbf{z}_t, t, c)\|^2\right]$$

During inference, starting from $\mathbf{z}_T \sim \mathcal{N}(0, I)$, the model iteratively applies $\epsilon_\theta$ to produce $\mathbf{z}_0$.

### Token Sparsity via Caching

The key insight is that across consecutive denoising steps $t$ and $t-1$, many token activations change minimally. If we can identify which tokens are "stale" (i.e., their cached value from the previous step is sufficiently close to the current value), we can skip recomputing their attention and FFN outputs.

Formally, for layer $l$ at step $t$, define a binary sparsity mask $\mathbf{m}^{(l,t)} \in \{0,1\}^N$ where $m_i = 1$ means token $i$ is **active** (recomputed) and $m_i = 0$ means it is **cached** (reused from step $t+1$). The effective computation for layer $l$ at step $t$ is:

$$\mathbf{h}^{(l,t)} = \mathbf{m}^{(l,t)} \odot f_l(\mathbf{h}^{(l-1,t)}) + (1 - \mathbf{m}^{(l,t)}) \odot \mathbf{h}^{(l,t+1)}$$

The speedup comes from computing attention only over the active subset of tokens (sparse attention).

### Layer-wise Sparsity Allocation

A critical question is: **which layers should be sparse, and by how much?**

Early layers in DiT capture low-level structure that changes slowly (high redundancy), while later layers encode semantic detail that varies more per step (low redundancy). DiffSparse models this via a **sparsity allocation vector** $\mathbf{s} = (s_1, \ldots, s_L) \in [0,1]^L$ where $s_l$ is the target fraction of tokens to cache at layer $l$.

The total FLOP cost of the model is approximately:
$$\text{Cost}(\mathbf{s}) \approx \sum_{l=1}^L \text{Cost}_l \cdot (1 - s_l)$$

Subject to a global sparsity budget $\bar{s}$:
$$\frac{1}{L}\sum_{l=1}^L s_l \geq \bar{s}$$

Finding the optimal $\mathbf{s}$ is a combinatorial problem that DiffSparse solves via **dynamic programming** over a discretized sparsity budget grid.

### The Learnable Sparsity Predictor

Rather than a fixed $\mathbf{m}^{(l,t)}$ mask, DiffSparse trains a lightweight **sparsity predictor network** $g_\phi$ that takes as input:
- The cached token activations $\mathbf{h}^{(l,t+1)}$
- The current timestep embedding $e_t$
- The layer index $l$

And outputs token-wise importance scores that are thresholded to produce $\mathbf{m}^{(l,t)}$.

The predictor is trained end-to-end with a differentiable relaxation of the binary mask (Gumbel-Softmax or straight-through estimator) and a combined loss:

$$\mathcal{L}_\text{total} = \mathcal{L}_\text{gen} + \lambda \cdot \mathcal{L}_\text{sparsity}$$

where $\mathcal{L}_\text{gen}$ is the standard diffusion denoising loss and $\mathcal{L}_\text{sparsity}$ penalizes deviation from the target sparsity budget.

---

## Main Ideas & Key Contributions

### 1. End-to-End Differentiable Sparsity Optimization

The central innovation is making the sparsity allocation **trainable**. Prior methods require hand-tuning or grid search over caching schedules. DiffSparse learns which tokens to cache through backpropagation, allowing it to discover that:
- Earlier layers can safely cache more tokens
- Timesteps near $T$ (noisier) allow more caching than timesteps near $0$ (cleaner)
- Image regions with less semantic change can be cached more aggressively

### 2. Dynamic Programming for Layer Allocation

Given a total sparsity budget, DiffSparse uses DP to find the globally optimal layer-wise allocation, avoiding greedy heuristics. The DP formulation considers the non-linear relationship between sparsity and quality degradation per layer.

### 3. FLOPs Reduction Without Quality Loss

Remarkably, on PixArt-α at 20 inference steps:
- **54% FLOPs reduction** vs. dense baseline
- **Better FID** than the original model (not just preserved quality)
- This quality improvement comes from the regularization effect of training the sparsity predictor, which acts as a form of guided attention pruning

### 4. Compatibility with Step-Reduction Methods

DiffSparse operates at the token/layer level and is orthogonal to step reduction methods like DPM-Solver. Combining both yields compounding speedups.

---

## Methodology & Implementation

### Experimental Setup

- **Base models:** PixArt-α (text-to-image), DiT-XL/2 (class-conditional ImageNet 256×256)
- **Inference steps:** 20 (DPM-Solver++) for PixArt-α; 250 DDPM steps for DiT-XL/2
- **Datasets:** MS-COCO 2017 validation (30K prompts) for PixArt-α; ImageNet 50K samples for DiT-XL/2
- **Fine-tuning:** 50K steps, batch size 256, using a small proxy dataset for sparsity predictor training

### Evaluation Metrics

| Metric | Description |
|--------|-------------|
| FID ↓ | Fréchet Inception Distance — lower is better |
| CLIP Score ↑ | Text-image alignment |
| FLOPs ↓ | Multiply-accumulate operations |
| Latency ↓ | Wall-clock inference time on A100 GPU |

### Key Results

| Method | FLOPs Reduction | FID (PixArt-α) |
|--------|----------------|-----------------|
| Baseline (dense) | — | 23.4 |
| DeepCache | 42% | 26.1 |
| TokenCache | 47% | 25.3 |
| **DiffSparse** | **54%** | **22.8** |

DiffSparse is the only method achieving both higher compression and lower FID than the baseline.

### Ablation Studies

- **Fixed vs. learned allocation:** Learned allocation improves FID by 1.8 points at same FLOPs budget
- **DP vs. greedy allocation:** DP improves FID by 0.9 points
- **Predictor architecture:** A 2-layer MLP predictor suffices; deeper predictors offer diminishing returns

---

## Practical Applications & Real-World Use Cases

### 1. Consumer Hardware Deployment

Current SDXL/DiT models require 8–16GB VRAM and 5–30 seconds per image on consumer GPUs. DiffSparse's 54% FLOPs reduction could bring real-time (1–2s) 512×512 generation to a GPU with 4GB VRAM, democratizing creative AI tools.

### 2. Video Generation

Video DiT models (Sora-class, CogVideoX) face even more severe compute costs due to temporal token dimensions. DiffSparse's layer-wise sparsity framework is directly applicable to 3D DiT models, potentially enabling real-time video generation at reduced quality tiers.

### 3. Interactive Editing Applications

Image editing workflows (inpainting, outpainting, style transfer) require many sequential forward passes. DiffSparse would cut interactive latency by ~2× on typical systems.

### 4. Edge and Mobile Deployment

With appropriate quantization + DiffSparse, small DiT models (DiT-S/2) could run on mobile NPUs, enabling on-device image generation without cloud dependency.

### Implementation Challenges

- Fine-tuning the sparsity predictor requires ~50K steps, adding training overhead
- The dynamic sparse attention kernel requires custom CUDA kernels for optimal hardware utilization
- Quality preservation guarantees degrade beyond ~65% sparsity

---

## Insights & Implications

### Broader Implications for Efficient AI

DiffSparse demonstrates that **training for efficiency** (learned sparsity) consistently outperforms **inference-time heuristics** (fixed caching), a pattern that extends to other model families. The same principle could apply to:
- Sparse attention in LLMs (token pruning during generation)
- Adaptive computation in vision transformers (early exit + token dropping)

### Limitations

1. **Two-stage overhead:** Training a sparsity predictor requires access to the original model and additional compute
2. **Hardware dependency:** The speedup in FLOPs does not translate 1:1 to wall-clock time without custom sparse attention kernels
3. **Generalization:** Sparsity patterns learned on MS-COCO may not generalize optimally to highly unusual prompts
4. **Step-count sensitivity:** The benefit of caching diminishes at very low step counts (<10 steps), since less temporal redundancy exists

### Open Questions

- Can sparsity patterns be meta-learned to transfer across DiT model sizes?
- How does DiffSparse interact with quantization (INT8/FP8) methods?
- Can similar token-caching approaches apply to autoregressive video generation (LWM, MAR)?

---

## Code & Resources

- **Official GitHub:** [https://github.com/AMD-AIG-AIMA/DiffSparse](https://github.com/AMD-AIG-AIMA/DiffSparse) *(check for release)*
- **ArXiv Paper:** [https://arxiv.org/abs/2604.03674](https://arxiv.org/abs/2604.03674)
- **ICLR 2026 Proceedings:** [https://iclr.cc/virtual/2026](https://iclr.cc/virtual/2026)

### Computational Requirements

- **Fine-tuning:** 8× A100 80GB GPUs, ~50K steps (~12 hours)
- **Inference:** Single A100/4090, standard DiT requirements with custom sparse kernel
- **Key dependencies:** PyTorch ≥ 2.3, xformers, diffusers ≥ 0.27, triton ≥ 2.2 (for sparse attention kernel)

### Quick Start (Expected)

```python
from diffsparse import DiffSparsePipeline

pipe = DiffSparsePipeline.from_pretrained(
    "PixArt-alpha/PixArt-XL-2-1024-MS",
    sparsity_config={"target_sparsity": 0.54, "predictor_ckpt": "diffsparse_predictor.pt"}
)
image = pipe("a photo of an astronaut riding a horse on the moon", num_inference_steps=20).images[0]
```

---

## Related Work & Context

### Building On

- **DiT (Peebles & Xie, 2023):** The base architecture DiffSparse optimizes
- **PixArt-α (Chen et al., 2023):** One of the primary evaluation targets
- **DeepCache (Ma et al., 2024):** Pioneered layer caching for diffusion acceleration
- **TokenCache (Liu et al., 2024):** Introduced token-level caching as opposed to layer-level

### Concurrent Work

- **AccelAes (2603.12575):** Training-free aesthetic enhancement via attention reuse — complementary approach
- **Sparse VideoGen (2502.01776):** Extends sparsity principles to video DiTs
- **DiffCache, ∆-DiT:** Fixed-schedule caching methods that DiffSparse outperforms

### Where This Leads

The work opens several research directions:
1. **Unified training for speed + quality:** Joint optimization of step count, model size, and token sparsity
2. **Hardware-software co-design:** Building sparse attention primitives into next-gen NPUs
3. **Diffusion for LLMs:** The caching insight may transfer to masked diffusion language models (LLaDA, MDT)
