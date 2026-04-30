# A Systematic Post-Train Framework for Video Generation

**ArXiv ID:** [2604.25427](https://arxiv.org/abs/2604.25427)  
**Authors:** Zeyue Xue, Siming Fu, Jie Huang, Shuai Lu, Haoran Li, Yijun Liu, Yuming Li, Xiaoxuan He, Mengzhao Chen, Haoyang Huang, Nan Duan, Ping Luo  
**Affiliations:** The University of Hong Kong, JD Explore Academy, Tsinghua University, Peking University, Zhejiang University  
**Submitted:** April 28, 2026  
**Field:** Computer Vision / Generative Models

---

## Executive Summary

Large-scale video diffusion models achieve impressive pretraining results, but deploying them in practice exposes three critical failure modes: prompt sensitivity (small wording changes produce dramatically different outputs), temporal inconsistency (objects flicker or warp across frames), and prohibitive inference cost. This paper proposes a four-stage post-training framework — SFT → RLHF with GRPO → Prompt Enhancement → Inference Optimization — that systematically closes the gap between pretraining performance and deployment requirements. The RLHF stage alone delivers a 31% improvement on the GSB (Good–Same–Bad) human evaluation metric, and the full framework makes large-scale video generation practically deployable without retraining from scratch.

---

## Problem Statement

### The Pretraining–Deployment Gap in Video Generation

Modern video diffusion models (e.g., HunyuanVideo, Wan, CogVideoX) are pretrained on massive corpora of video data with denoising objectives. They can generate high-resolution, semantically rich content — yet when deployed for real users, they reveal persistent weaknesses:

1. **Prompt sensitivity**: Users phrase requests naturally and inconsistently. A pretrained model trained to match video-text pairs from curated datasets may be brittle to paraphrases, incomplete descriptions, or unusual syntax. Small prompt variations lead to large quality drops.

2. **Temporal inconsistency**: Diffusion models independently denoise each frame (or operate on latent sequences) without explicit temporal coherence constraints. Generated videos frequently show objects flickering, changing shape, or teleporting between frames — artifacts that are immediately obvious to human viewers.

3. **Inference cost**: Video generation requires generating hundreds to thousands of latent frames. At deployment scale, inference cost is prohibitive without careful optimization of the sampling schedule, distillation, or other compute-reduction techniques.

### Why Post-Training?

Pretraining is expensive and slow to iterate. Post-training methods (fine-tuning, RLHF, knowledge distillation) operate on an already-capable pretrained model and can be done at a fraction of the cost. The challenge is designing a coherent post-training strategy that addresses all three problems without introducing new failure modes or degrading the model's pretraining capabilities.

---

## Core Concepts & Theory

### Video Diffusion Models as Stochastic Differential Equations

Video diffusion models can be formalized under the stochastic differential equation (SDE) framework. The forward process adds Gaussian noise to a clean video latent `x_0` according to a noise schedule, producing increasingly noisy versions `x_t` for `t ∈ [0, T]`. The model learns to reverse this process, predicting `x_0` (or the noise `ε`) from `x_t` conditioned on a text prompt.

Formally, the forward SDE is:
```
dx = f(x, t)dt + g(t)dW
```
where `f` and `g` are drift and diffusion coefficients, and `W` is a Wiener process. The reverse SDE is:
```
dx = [f(x, t) - g(t)² ∇_x log p_t(x)] dt + g(t)dW̄
```
The score function `∇_x log p_t(x)` is approximated by the neural network.

### Group Relative Policy Optimization (GRPO) for Video Diffusion

Standard RL methods for language models (PPO, GRPO) operate on discrete token sequences. Adapting them to continuous video latent spaces requires care. The paper introduces GRPO tailored for video diffusion:

**Key insight**: Rather than computing absolute advantage estimates (which require a stable value function — notoriously hard to train), GRPO uses *relative comparisons within groups*. For each text prompt, multiple video samples are generated, and they are ranked by a reward signal. The policy is updated to increase the probability of higher-ranked samples relative to lower-ranked ones within the group.

Under the SDE formulation, the policy gradient is computed with respect to the denoising trajectory, allowing the model to learn which *generation paths* lead to better perceptual quality and temporal coherence.

**Reward signals** include:
- Perceptual quality metrics (CLIP alignment, aesthetic scoring)
- Temporal coherence metrics (inter-frame optical flow consistency)
- Human preference models trained on ranked video pairs

### Prompt Enhancement via Auxiliary Language Model

A specialized language model is trained to transform short, casual user prompts into well-structured, detailed prompts that the video generation model handles reliably. This is conceptually similar to prompt engineering but automated: the model learns, from data, which types of prompt elaborations improve generation quality.

---

## Main Ideas & Key Contributions

### Stage 1: Supervised Fine-Tuning (SFT)

The base pretrained video diffusion model is fine-tuned on a curated dataset of high-quality (prompt, video) pairs selected for instruction-following fidelity. 

**Goals of SFT:**
- Teach the model to follow structured instructions (not just match video-text co-occurrence statistics)
- Establish a stable policy initialization that makes the subsequent RL stage more efficient and stable
- Reduce prompt sensitivity by exposing the model to diverse phrasings of similar concepts

SFT alone is insufficient for temporal coherence and prompt robustness, but it provides the well-initialized policy that makes RL more effective — consistent with findings in the LLM post-training literature (e.g., the companion paper 2604.23747 on SFT-then-RL for reasoning).

### Stage 2: Reinforcement Learning from Human Feedback (RLHF) via GRPO

This is the most impactful stage. Using the GRPO formulation adapted for video diffusion under the SDE framework, the model is optimized against:
- A perceptual quality reward
- A temporal coherence reward
- A prompt-adherence reward

**Result**: 31% improvement in the GSB metric relative to the post-SFT model. This is a human evaluation result: human raters were shown pairs of videos (from the pre-RLHF and post-RLHF model) and asked to indicate which is "Good," "Same," or "Bad." A 31% swing in this metric represents a substantial, user-perceivable quality improvement.

**Why GRPO over PPO**: Standard PPO requires maintaining a value function (critic) alongside the policy, which doubles memory requirements and introduces training instability for continuous-space generation. GRPO's relative comparison approach avoids value-function estimation entirely, making it more memory-efficient and stable for large video diffusion models.

### Stage 3: Prompt Enhancement

A lightweight language model (much smaller than the video generation backbone) is trained to:
1. Accept a short, casual user prompt
2. Generate an expanded, well-structured prompt optimized for the video generation model's input distribution

This stage effectively decouples user-facing prompt flexibility from model-facing prompt requirements. Users can write naturally; the enhancement model translates their intent into a form the video model handles reliably.

### Stage 4: Inference Optimization

The final stage reduces inference cost without sacrificing quality:
- **Accelerated sampling schedules**: Fewer denoising steps using consistency model techniques or flow matching
- **Caching and reuse**: Identifying and caching redundant computations in the denoising network across sampling steps
- **Distillation**: A student model trained to match the full-pipeline output in fewer steps

The result is a model that can be served at commercially viable inference cost while maintaining the quality gains from stages 1–3.

---

## Methodology & Implementation

### Experimental Setup

**Base models**: The framework is described as model-agnostic and was evaluated on leading open-source and proprietary video diffusion architectures, with explicit references to the broader landscape including HunyuanVideo, Wan, and CogVideoX families as comparative baselines.

**Training data for SFT**: Curated high-quality (prompt, video) pairs with careful quality filtering for instruction fidelity, temporal coherence, and aesthetic quality.

**Reward modeling for RLHF**: Human preference data collected via pairwise comparison; preference models trained on these comparisons to provide scalable reward signals.

**Evaluation protocol**: Human evaluation via GSB (Good–Same–Bad) pairwise protocol. Annotators are shown two videos generated from the same prompt (one from the current model, one from a reference) and rate which is better.

### Results Summary

| Stage | GSB Improvement (vs. pretrained baseline) |
|-------|-------------------------------------------|
| After SFT | Moderate prompt following improvement |
| After RLHF/GRPO | **+31% GSB overall** (driven by visual quality and motion coherence) |
| After Prompt Enhancement | Additional robustness gains on naturalistic inputs |
| After Inference Opt. | Maintained quality at significantly reduced compute |

The 31% RLHF gain is the headline result. The paper breaks this down into contributions from visual quality improvement and motion coherence improvement, with both making substantial contributions.

### Evaluation Metrics

- **GSB (Good–Same–Bad)**: Primary metric for overall quality; captures human preference holistically
- **VQA-based metrics**: Vision-question-answering models used to assess prompt adherence automatically
- **Optical flow consistency**: Automated measure of inter-frame motion smoothness
- **Aesthetic scores**: CLIP-based aesthetic quality predictors

---

## Practical Applications & Real-World Use Cases

### 1. Commercial Video Generation Platforms

The direct application is improving consumer-facing AI video generation products. A 31% GSB improvement at the RLHF stage is the difference between a product that produces occasionally acceptable videos and one that reliably delivers high-quality, coherent outputs that users can actually use.

### 2. Creative Tools for Filmmakers and Designers

Temporal consistency is critical for video production use cases. A workflow where a designer can describe a scene verbally and receive a temporally consistent video — without flickering, morphing artifacts, or sudden style shifts — becomes viable with the framework's Stage 2 improvements.

### 3. Accessibility and Education

Prompt enhancement (Stage 3) lowers the barrier to entry for non-expert users. A student or educator who cannot write detailed prompts can still obtain high-quality video outputs because the enhancement model bridges the gap.

### 4. Data Generation for Downstream Tasks

Temporally consistent, high-quality synthetic video is valuable as training data for robotics policies, autonomous driving simulators, and other embodied AI systems. The post-trained model produces significantly more reliable synthetic data than the pretrained base.

### 5. Multi-Step Post-Training as a General Blueprint

The four-stage framework (SFT → RLHF → Enhancement → Optimization) is presented as a general blueprint applicable to any video diffusion model. Companies or research teams with proprietary pretrained models can apply this pipeline to their own systems.

---

## Insights & Implications

### Bridging Pretraining and Deployment

This paper's core insight is that pretraining objectives (denoising, video-text matching) are not aligned with deployment requirements (prompt following, temporal coherence, inference efficiency). Post-training is the systematic bridge. The four-stage framework makes this bridge explicit and modular.

### RLHF Works for Continuous Generation

A significant technical contribution is demonstrating that GRPO-style RL can be adapted for video diffusion in a stable, scalable way using the SDE framework and group-relative comparisons. This opens the door to applying RLHF to other continuous generative modalities (3D scenes, audio, motion capture).

### Human Preferences Drive Quality More Than Metrics

The GSB metric used for evaluation captures human preference holistically — including hard-to-quantify attributes like "does this look right?" that automated metrics miss. The 31% improvement validates that RLHF, trained on human preferences, learns to optimize dimensions of quality that matter to users.

### Prompt Enhancement as a Deployable Module

The Prompt Enhancement stage has a practical implication: it can be deployed independently as an API preprocessing step, separate from the generation model. This modular architecture allows the enhancement model to be updated without retraining the full video backbone.

### Limitations

- Human evaluation (GSB) is expensive and may not scale to rapid iteration; automated proxies may not fully capture human preference.
- The GRPO formulation requires collecting ranked video samples per prompt, which is computationally intensive at scale.
- Temporal coherence improvements may be constrained by the base model architecture; if the attention mechanism does not span the full video sequence, temporal awareness has a ceiling.
- The Prompt Enhancement model introduces a dependency on an additional model that must be maintained and updated as user behavior evolves.
- Four-stage post-training is complex to implement and requires careful ordering; the paper does not report ablations on alternative stage orderings.

---

## Code & Resources

- **Paper:** [https://arxiv.org/abs/2604.25427](https://arxiv.org/abs/2604.25427)
- **HTML version:** [https://arxiv.org/html/2604.25427v1](https://arxiv.org/html/2604.25427v1)
- **HuggingFace Paper page:** [https://huggingface.co/papers/2604.25427](https://huggingface.co/papers/2604.25427)

**Code:** Not released at submission time (paper from industrial research group at JD Explore Academy / University of Hong Kong collaboration)

**Computational Requirements:**
- Stage 1 (SFT): Comparable to standard fine-tuning for large video diffusion models; requires high-memory GPUs (A100/H100 class)
- Stage 2 (RLHF/GRPO): Most compute-intensive; requires running multiple video generations per prompt for group comparison, plus reward model inference
- Stage 3 (Prompt Enhancement): Lightweight; the enhancement model is much smaller than the video backbone
- Stage 4 (Inference Optimization): Once distilled/compressed, reduces ongoing inference cost substantially

**Related Video Diffusion Repositories:**
- [HunyuanVideo](https://github.com/Tencent-Hunyuan/HunyuanVideo): Tencent's open-source video generation model (referenced as baseline context)
- [Wan Video](https://github.com/Wan-Video/Wan2.1): Alibaba's video generation model family

---

## Related Work & Context

### Prior Post-Training Work for Video Generation

- **TeleBoost** (2602.07595): A related systematic alignment framework for video generation, focused on high-fidelity and controllability. This paper's framework is broader (four stages vs. TeleBoost's more focused scope) and introduces the GRPO adaptation for video diffusion.
- **Growing with the Generator: Self-paced GRPO for Video Generation** (2511.19356): Earlier work on applying GRPO to video generation; this paper generalizes and systematizes the approach as part of a comprehensive post-training pipeline.
- **HunyuanVideo** (2412.03603): Tencent's framework paper for large video generation models; provides context for the pretraining capabilities that this post-training work builds upon.

### Connections to LLM Post-Training

The framework is directly inspired by RLHF successes in language models (InstructGPT, ChatGPT, DeepSeek-R1). The key challenge is adapting the discrete-token RL formulations to continuous latent spaces — solved here via the SDE framework and GRPO's value-function-free approach.

### Connections to Image Diffusion Post-Training

Prior work on post-training for image diffusion (e.g., DDPO, DRaFT, SOAR) established that RL fine-tuning can improve image quality and prompt adherence. This paper extends those insights to the significantly harder video setting, where temporal coherence adds an entirely new optimization dimension.

### Where This Research May Lead

- **Multi-modal post-training**: The four-stage framework could be extended to other generative modalities (audio, 3D, motion) sharing the video diffusion's core challenges
- **Preference data flywheel**: Production deployment of post-trained models generates new human preference data, enabling iterative improvement cycles
- **GRPO standardization**: GRPO for video diffusion may become a standard component in video generation post-training pipelines, analogous to its role in LLM reasoning training
- **Benchmark development**: The GSB evaluation protocol, while expensive, sets a standard for human-centered video quality evaluation that may inspire automated approximations (reward models trained on GSB-labeled data)
