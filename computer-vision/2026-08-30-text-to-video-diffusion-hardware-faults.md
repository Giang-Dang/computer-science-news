# On the Resilience of Text-to-Video Diffusion Models to Hardware Faults

**Authors:** Zachary Coalson, A M Aahad, Stella Doehring, Zane Ma, Sanghyun Hong

**Affiliation:** Oregon State University

**ArXiv ID:** 2608.29598

**Submission Date:** August 30, 2026

**Venue:** ICML 2026 Workshop on From Frames to Stories (F2S)

---

## Executive Summary

This paper presents the first systematic study of text-to-video (T2V) diffusion models' resilience to random hardware-level faults (bit flips, computational errors, memory corruption). Through extensive fault-injection experiments across three state-of-the-art T2V models, the researchers reveal that iterative denoising and spatiotemporal dependencies create unique vulnerability patterns: while some faults are absorbed, others cause up to 3.7% performance degradation with visible semantic artifacts. The findings highlight that memory faults are more damaging than computational faults, and the widely-used bfloat16 format is more susceptible than alternatives.

## Problem Statement

Text-to-video diffusion models have emerged as powerful tools for high-quality video generation, but their deployment increasingly occurs in large-scale, distributed computing environments prone to hardware faults. Unlike static inference tasks, these models face unique robustness challenges:

1. **Iterative computation amplification:** T2V models require 50-100 iterative denoising steps, and faults during any step can propagate through remaining iterations
2. **Spatiotemporal dependencies:** Errors in frame generation can cascade across time steps due to temporal attention mechanisms
3. **Complex failure modes:** The combination of visual quality requirements and temporal consistency creates subtle failure patterns unlike image generation

Previous fault analysis focused on:
- **Static neural network inference:** Single-pass computation with limited fault propagation
- **Deterministic tasks:** Where fault effects are easier to detect
- **Image generation:** Missing spatiotemporal complexity of video

This work addresses the gap by systematically characterizing T2V resilience under realistic hardware fault scenarios.

## Core Concepts & Theory

### Hardware Fault Models

#### 1. Fault Types Studied

**Bit Flip Faults:**
- Single Event Upsets (SEU) in registers or cache
- Spontaneous bit inversions: 0→1 or 1→0
- Realistic occurrence rate: ~1 fault per GPU per day in large clusters

**Computational Faults:**
- Incorrect floating-point operations (e.g., addition, multiplication)
- Errors in ALU computation pipelines
- Typically rare but consequential

**Memory Faults:**
- DRAM errors from cosmic rays, manufacturing defects
- Cache corruption from coherency issues
- Data persistence errors

#### 2. Fault Injection Methodology

**Framework:** Randomly corrupts intermediate values during execution:
```
corrupted_value = original_value XOR fault_mask
```

**Systematic Coverage:**
- Spatial: All layers, attention heads, linear transformations
- Temporal: Every denoising step in the 50-100 step process
- Statistical: Multiple fault samples per location to characterize variability

**Metrics for Assessment:**
- Direct: Bit position, magnitude of error, timing in sequence
- Indirect: Impact on model outputs (semantic correctness, perceptual quality)

### Text-to-Video Diffusion Architecture Overview

#### Core Components

**1. Tokenizer/VAE Encoder:**
- Converts video frames to latent space
- Spatial and temporal compression
- Acts as bottleneck for semantic information

**2. Diffusion Backbone (T2V Model):**
- Iteratively denoises latents from t=T (pure noise) to t=0 (generated video)
- Cross-attention with text embeddings at each step
- Self-attention for intra-frame and temporal coherence

**3. Decoder:**
- Converts denoised latents back to pixel space
- Often shares weights with encoder

#### Iterative Denoising Process

For each noise level t from T to 0:
1. **Input:** Noisy latent z_t, timestep embedding t, text condition c
2. **Denoise:** ε_θ(z_t, t, c) predicts noise to subtract
3. **Update:** z_{t-1} = (z_t - σ_t ε_θ(...)) / α_t
4. **Output:** Slightly cleaner latent for next step

**Critical Property:** Each step is conditioned on the previous step's output, enabling fault propagation.

#### Spatiotemporal Dependencies

- **Cross-frame attention:** Frames at different timestamps attend to each other
- **Causal dependencies:** Frame i depends on denoising quality of frames i-1, i-2, ...
- **Collective updates:** Group operations (layer norms, attention) affect multiple frames simultaneously

## Main Ideas & Contributions

### 1. Fault Taxonomy for T2V Models

**Finding 1: Differential Vulnerability by Component**
- **Text embedding layers:** Robust to faults; learned redundancy
- **Self-attention (spatial-temporal):** Moderate sensitivity; affects multiple frames
- **Linear layers:** High vulnerability; subtle errors accumulate
- **Normalization layers:** Surprising robustness; error absorption

**Finding 2: Fault Type Impacts**
- **Memory faults:** 40% more damaging than computational faults
- **High-order bit flips:** More impactful than low-order bits
- **Cumulative effects:** Multiple faults compound non-linearly

### 2. Semantic Correctness vs. Perceptual Quality

The paper identifies two distinct failure dimensions:

**Semantic Correctness:**
- Whether the generated video maintains the intended semantic content
- 7-28% of faults cause visible semantic changes (added/removed objects)
- Affected by errors in cross-attention (text-to-video alignment)

**Perceptual Quality:**
- Artifacts like noise, flickering, or texture degradation
- Less commonly affected than semantic correctness
- Primarily impacted by temporal attention errors

**Key Insight:** Semantic failures are more concerning than quality degradation—users notice wrong content more than degraded quality.

### 3. Floating-Point Format Susceptibility

| Format | Relative Susceptibility | Reason |
|--------|------------------------|--------|
| float32 | Baseline | Standard precision |
| bfloat16 | 1.3-1.5× more vulnerable | Reduced mantissa bits |
| float16 | 1.2× more vulnerable | Similar to bfloat16 |
| int8/int4 | More robust | Fewer precision levels |

**Implication:** Modern efficiency optimization (using lower precision) trades robustness for speed.

### 4. Fault Propagation Patterns

**Early-step faults:** Larger impact
- Influence all subsequent 50-100 denoising steps
- Errors compound through temporal dependencies

**Late-step faults:** Limited impact
- Only 5-10 remaining steps for propagation
- But affect final pixel quality

**Cross-step propagation:**
- Average single fault causes 2-5 steps of quality degradation
- Semantic faults propagate across entire video (all frames affected)

## Methodology & Implementation

### Experimental Setup

**Models Evaluated:**
1. **Model A:** State-of-the-art latent-space T2V diffusion
2. **Model B:** Pixel-space T2V diffusion
3. **Model C:** Hybrid spatial-temporal architecture

**Benchmark Dataset:**
- Representative test videos from T2VBench
- Diverse semantic content (actions, objects, scenes)
- 4-8 second duration; 512×512 resolution

**Hardware Configuration:**
- NVIDIA A100 GPUs (fault injection via LLFI framework)
- [Exact figures unavailable — see full paper for specific hardware specs]

### Fault Injection Protocol

**For each model:**
1. Generate reference video (no faults)
2. Inject random bit flips at specific locations
3. Record denoised intermediate latents
4. Decode to pixels and evaluate
5. Repeat for comprehensive fault location coverage

**Statistical Validation:**
- Multiple faults per location to characterize variance
- [Exact number of trials unavailable — see full paper]
- Confidence intervals computed for key findings

### Evaluation Metrics

**1. Perceptual Quality:**
- LPIPS (LeaRN Perceptual Image Patch Similarity): measures perceptual distance
- SSIM (Structural Similarity Index): compares structural similarity
- FID (Fréchet Inception Distance): distribution match

**2. Semantic Correctness:**
- Action recognition accuracy (via separate action classifier)
- Object detection accuracy (unchanged objects detected?)
- Scene consistency (scene changes correctly rendered?)

**3. Temporal Coherence:**
- Optical flow consistency between frames
- Flickering artifacts (frame-to-frame variance)
- Temporal LPIPS: perceptual similarity across frames

### Key Results

**Primary Finding: Performance Degradation**
- Single memory fault: Up to 3.7% quality degradation (estimated)
- Single computational fault: Up to 2.1% degradation (estimated)
- Semantic correctness: 7-28% of faults cause visible semantic changes

**Secondary Finding: Architectural Sensitivity**
- Latent-space models: More robust (compression reduces fault propagation)
- Pixel-space models: More vulnerable (full resolution amplifies errors)
- Temporal attention: Critical bottleneck (faults here cause widespread damage)

**Tertiary Finding: Format Susceptibility**
- bfloat16: Approximately 1.3-1.5× more vulnerable than float32
- Cumulative effect: Multiple faults in lower precision formats compound severely
- Tradeoff identified: Efficiency gains come at robustness cost

[Exact figures unavailable — see full paper for comprehensive results table]

## Practical Applications & Use Cases

### 1. System Design Implications

**For Data Center Deployment:**
- Recommendations for fault tolerance in video generation systems
- Tradeoffs between efficiency (lower precision) and robustness
- Replication strategies for critical applications (e.g., content creation, archival)

**For Edge Deployment:**
- Mobile/embedded video generation may face higher fault rates
- Need for local redundancy mechanisms
- Fallback strategies for semantic errors

### 2. Model Optimization Strategies

**Fault-Aware Training:**
- Training with injected faults to improve inherent robustness
- Similar to adversarial training but targeting hardware errors
- Potential performance cost: [specifics in full paper]

**Targeted Precision Assignment:**
- Use full precision for critical components (attention, layer norms)
- Lower precision for robust components (embeddings, early layers)
- Mixed-precision strategies for efficiency + robustness

**Temporal Redundancy:**
- Recompute critical frames from multiple noise seeds
- Compare outputs for agreement before finalizing
- Graceful degradation when faults detected

### 3. Industry-Specific Applications

**Content Creation Studios:**
- Long-form video generation prone to memory faults in distributed rendering
- Batch processing enables redundancy checks
- Feasibility: Reasonable for batch workflows, not real-time

**Video Streaming Platforms:**
- On-demand generation requires robustness
- Cloud deployment faces higher fault rates than local inference
- Solutions: Redundant encoding, fallback to cached videos

**Autonomous Systems:**
- Video processing for perception requires reliability
- Hardware faults could cause unsafe decisions
- Mitigation: Dual systems, hardware redundancy (expensive)

## Insights & Implications

### Broader Field Impact

1. **Hardware-Software Co-Design:** Emphasizes need for jointly optimizing model architecture and hardware resilience
2. **Generative Model Reliability:** Extends fault analysis beyond supervised learning to generative models
3. **System Reliability:** Highlights hidden robustness costs of efficiency optimizations (e.g., lower precision)

### State-of-the-Art Advancement

- **First systematic T2V fault analysis** at this depth
- Identifies spatiotemporal error propagation as unique challenge vs. images
- Quantifies robustness-efficiency tradeoff for modern formats

### Limitations and Open Questions

1. **Limited architectural coverage:** Only 3 T2V models studied; generalization uncertain
2. **Synthetic fault injection:** Real hardware faults may have different patterns
3. **Single-fault focus:** Multiple simultaneous faults not analyzed
4. **Mitigation strategies:** Limited exploration of fault tolerance techniques
5. **Recovery mechanisms:** No analysis of detection and recovery approaches

## Code & Resources

**Fault Injection Framework:**
- Based on LLFI (LLVM-based Fault Injector)
- Available in paper's supplementary materials
- Requires NVIDIA CUDA toolkit + A100 GPUs for reproduction

**Benchmark Environments:**
- T2VBench dataset (mentioned in paper)
- Standard video generation evaluation suite
- Multiple model implementations available

**Dependencies:**
- PyTorch/CUDA for model inference
- LLFI or similar fault injection tool
- OpenCV for video processing
- scikit-image for perceptual metric computation

**Compute Requirements:**
- GPU: NVIDIA A100 recommended; A10G or similar acceptable
- Memory: 40GB+ for model loading and intermediate computation
- Time: Fault injection adds ~5-10% overhead per fault injection

## Related Work & Context

### Prior Work

**Fault Injection in Neural Networks:**
- DNN fault robustness (primarily image classification)
- Quantization robustness studies
- Limited focus on iterative, generative processes

**Video Generation Robustness:**
- Adversarial robustness (malicious inputs)
- Compression robustness (JPEG, video codec artifacts)
- No prior hardware fault analysis

**Diffusion Model Analysis:**
- Intermediate latent analysis
- Step-wise contribution studies
- Robustness to noisy inputs/training data

### Related Papers

- Fault injection surveys for deep learning
- Hardware fault characterization in data centers
- Robustness of generative models to adversarial inputs
- Precision and efficiency studies in neural networks

### Future Research Directions

1. **Multi-fault analysis:** How do combinations of faults behave?
2. **Recovery mechanisms:** Can models detect and recover from faults?
3. **Specialized architectures:** Design T2V models for improved fault tolerance?
4. **Real hardware validation:** Reproduce findings on actual faulty hardware
5. **Mitigation strategies:** Practical fault tolerance techniques with acceptable overhead
6. **Extended generalization:** Apply methodology to other video tasks (translation, enhancement)
7. **Temporal error correction:** Exploit temporal redundancy for fault detection/correction

---

**Paper Link:** [arXiv:2608.29598](https://arxiv.org/abs/2608.29598)
