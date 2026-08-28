# Depth-Synergized Mamba Meets Memory Experts for All-Day Image Reflection Separation

**Authors:** Siyan Fang, Long Peng, Yuntao Wang, Ruonan Wei, Yuehuan Wang  
**ArXiv ID:** 2601.00322  
**Published:** January 1, 2026  
**Conference:** AAAI 2026  
**Links:** [arXiv](https://arxiv.org/abs/2601.00322), [PDF](https://arxiv.org/pdf/2601.00322)

## Executive Summary

Image reflection separation is a critical challenge in computer vision: disentangling the transmitted layer from unwanted reflections in real-world images. This paper addresses a particularly difficult scenario—all-day reflection separation where nighttime images are especially problematic. The authors propose the Depth-Memory Decoupling Network (DMDNet) combining depth-aware state-space models with memory expert compensation. The approach represents a significant advance in handling extreme lighting conditions, where existing methods fail due to similar contrast between reflection and transmission layers.

## Problem Statement

### Core Challenge
Image reflection separation (also called reflection removal) aims to recover a clean transmitted image when reflections are present. This is a severely ill-posed inverse problem, especially when:
- Reflections and transmission have similar luminance/contrast
- Lighting conditions vary dramatically (particularly at night)
- Textures of reflection and transmission layers overlap

### Prior Limitations
- Existing methods struggle when reflection and transmission contrasts are similar
- Nighttime reflection separation is significantly more challenging than daytime scenarios
- Standard deep learning approaches fail to distinguish layers with comparable visual properties
- Limited use of depth cues and temporal consistency across different lighting conditions

### Research Gap
While previous work addresses daytime reflection separation, the nighttime scenario—where contrast reversal and ambiguity are most severe—had limited exploration. A method specifically designed to handle all-day (including night) reflection separation with guidance from depth information was missing.

## Core Concepts & Theory

### Problem Formulation
Image reflection separation can be formulated as:
```
I = T + R
```
where:
- **I:** Observed blended image (input)
- **T:** Transmitted layer (clean scene, output target)
- **R:** Reflection layer (unwanted, to be suppressed)

The goal is to recover T and optionally R from I.

### Depth-Aware State-Space Models
The paper leverages Mamba, a recent efficient state-space model architecture, with novel depth-aware modifications:

**Depth-Aware Scanning (DAScan):**
```
Standard Mamba scanning: processes image features sequentially
Depth-Aware modification: 
  1. Extract depth map of scene
  2. Guide scanning order toward salient structures
  3. Promote information flow along semantic coherence boundaries
```

This ensures that the model preferentially processes features along object boundaries and depth discontinuities, where layer separation is clearest.

### State-Space Model Enhancement
**Depth-Synergized State-Space Model (DS-SSM):**
- Modulates state activation sensitivity by depth values
- Suppresses spread of ambiguous features that interfere with layer disentanglement
- Preserves layer-specific features while attenuating cross-layer information leakage

### Memory Expert Architecture
**Memory Expert Compensation Module (MECM):**
- Maintains cross-image historical knowledge from training distribution
- Provides layer-specific compensation guided by learned experts
- Adapts compensation strategies based on input characteristics
- Particularly effective for challenging nighttime scenarios where appearance is ambiguous

## Main Ideas & Contributions

### 1. Depth-Aware Mamba Architecture
First application of Mamba (modern state-space models) to reflection separation, with depth guidance to promote semantic coherence in feature processing.

### 2. Depth-Synergized State-Space Model (DS-SSM)
A novel component that:
- Learns to modulate state activations based on scene depth
- Suppresses ambiguous features more aggressively in low-depth-variation regions
- Enhances feature discrimination in depth-discontinuous areas

### 3. Memory Expert Compensation Module
Cross-image knowledge distillation that:
- Learns general compensation patterns from training data
- Specializes compensation through expert routing based on image characteristics
- Provides particularly strong benefits for nighttime reflection separation

### 4. All-Day Reflection Separation Dataset/Benchmark
Systematic evaluation including challenging nighttime scenarios, advancing beyond typical daytime-only benchmarks.

## Methodology & Implementation

### Architecture Components

**Input Processing:**
- RGB image and corresponding depth map (from stereo or single-image depth estimation)
- Depth preprocessing for meaningful gradient computation

**Depth-Aware Scanning:**
1. Compute depth gradients to identify semantic boundaries
2. Generate scanning order that prioritizes high-gradient regions
3. Use scanning order to guide Mamba's sequential feature processing

**Depth-Synergized State-Space:**
```
For each Mamba layer:
  - Standard SSM state update: h_t = A*h_{t-1} + B*x_t
  - Depth modulation: h_t = depth_weight(d_t) * h_t
  - Output: y_t = C*h_t + D*x_t
```

**Memory Expert Module:**
- Bank of learned expert networks from training data
- Expert selection based on image content features
- Output: expert-weighted compensation for layer separation

### Experimental Setup
- **Datasets:** Standard reflection separation benchmarks + new all-day dataset
- **Baselines:** Compared against state-of-the-art CNN-based and transformer-based methods
- **Evaluation metrics:** PSNR, SSIM, LPIPS for transmission layer quality
- **Lighting conditions:** Daytime (normal), dusk/dawn (transitional), nighttime (extreme)

### Evaluation Metrics

**Quantitative Results (confirmed from search):**
- Significant improvement on nighttime reflection separation
- Maintains or improves performance on daytime benchmarks
- [Exact figures unavailable — see full paper for numerical comparisons with baselines]

**Qualitative Results:**
- Visually cleaner transmission layer recovery in nighttime scenarios
- Better preservation of fine details compared to baselines
- More robust to edge cases where contrast is ambiguous
- Natural-looking reflection removal without over-smoothing

## Practical Applications & Use Cases

### 1. Mobile Photography Enhancement
- **Real-time reflection removal:** In-camera processing for smartphone photo capture
- **Post-processing:** Automatic cleanup of reflections from glass, windows, water surfaces
- **Night mode enhancement:** Improved quality of nighttime photography by removing reflections

### 2. Autonomous Driving
- **Windshield reflection handling:** Robust scene understanding from front-facing cameras
- **Adverse weather:** Improved perception in rain/snow with reflection artifacts
- **Night driving:** Critical for safety in low-light conditions

### 3. Cultural Heritage and Document Scanning
- **Museum artifact documentation:** Photography of items behind glass
- **Historical document digitization:** Removing reflection artifacts from scanned materials
- **Archive preservation:** Automated improvement of challenging archival photographs

### 4. Video Processing
- **Temporal consistency:** Applying separation consistently across video frames
- **Live streaming:** Real-time reflection removal for broadcast quality
- **Surveillance footage:** Improving visibility in reflective environments

### Feasibility Considerations
- **Depth dependency:** Requires depth information (can use single-image depth estimation as fallback)
- **Computational cost:** State-space models are efficient; practical for video processing
- **Training data:** Benefits from paired transmission/reflection data; synthetic data can supplement
- **Generalization:** Learned on diverse conditions but may need fine-tuning for specific domains

## Insights & Implications

### Field Impact
1. **All-day imaging:** Extends reflection separation beyond daytime-dominated research
2. **Depth integration:** Demonstrates effective fusion of geometric and learned representations
3. **Efficient architectures:** Shows Mamba's potential for dense prediction tasks beyond standard applications

### State-of-the-Art Advancement
- First method to specifically address nighttime reflection separation with strong empirical results
- Novel application of depth-guided state-space models to reflection separation
- Memory expert compensation provides a new paradigm for handling ambiguous cases

### Limitations and Open Questions
1. **Depth estimation accuracy:** Performance depends on quality of depth maps; sensitivity to depth errors not fully analyzed
2. **Generalization:** Cross-dataset generalization to dramatically different reflection/transmission distributions
3. **Computational efficiency:** Comparison with lightweight CNN approaches for mobile deployment
4. **Video artifacts:** Temporal consistency in video processing needs more detailed analysis
5. **Failure modes:** Behavior when reflection/transmission layers have strong structural similarity

## Code & Resources

### Official Repository
- Not explicitly mentioned; likely to be released post-publication

### Dependencies and Requirements
- **Core framework:** PyTorch
- **Depth estimation:** MiDaS or similar for single-image depth prediction
- **Dataset:** Reflection separation benchmark datasets (CEILNet, Real20, SIR²)
- **Compute:** GPU acceleration recommended for video processing

### Implementation Considerations
- State-space model implementation (Mamba) requires recent deep learning frameworks
- Depth preprocessing is straightforward but sensitive to estimation quality
- Memory expert module adds moderate parameter overhead but provides interpretability

## Related Work & Context

### Related Recent Papers
1. **Mamba: Linear-Time Sequence Modeling with Selective State Spaces:** Foundational SSM work
2. **Efficient Transformer variants:** Other recent efficient sequence models
3. **Reflection removal methods:** CNN and transformer-based baselines from recent years

### Prior Work Foundations
- **Classical reflection separation:** Polarization-based, edge-aware methods
- **Deep learning approaches:** CNN-based architectures for layer decomposition
- **Depth-guided vision:** Successful integration of depth in various computer vision tasks
- **State-space models:** Recent emergence as efficient alternatives to transformers

### Future Research Directions
1. **Self-supervised depth learning:** Joint optimization of reflection separation and depth estimation
2. **Video reflection separation:** Full temporal consistency modeling
3. **Multiple reflection layers:** Extension to scenes with multiple reflections
4. **Nighttime-specific datasets:** Larger-scale benchmarks for low-light reflection separation
5. **Adversarial robustness:** Behavior under adversarial perturbations and distribution shift
6. **Domain adaptation:** Generalizing across different cameras and lighting conditions

---

**Paper Citation:**  
Depth-Synergized Mamba Meets Memory Experts for All-Day Image Reflection Separation, AAAI 2026, arXiv:2601.00322

**Session:** Generated summary for computer-science-news repository  
**Date:** 2026-08-28
