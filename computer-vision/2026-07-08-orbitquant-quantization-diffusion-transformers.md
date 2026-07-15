# OrbitQuant: Data-Agnostic Quantization for Image and Video Diffusion Transformers

**Paper ID:** arXiv:2607.02461  
**Submitted:** July 2, 2026  
**Authors:** Donghyun Lee, Jitesh Chavan, Duy Nguyen, Sam Huang, Liming Jiang, Priyadarshini Panda, Timo Mertens, Saurabh Shukla  
**Field:** Computer Vision, Machine Learning, Quantization  

## Executive Summary

OrbitQuant addresses the critical challenge of quantizing diffusion transformers (DiTs) by introducing a data-agnostic weight-activation quantizer that works without requiring calibration data. Using randomized permuted block-Hadamard (RPBH) rotations, OrbitQuant concentrates activation coordinates around fixed known marginals, enabling a single Lloyd-Max codebook to serve all timesteps, prompts, and layers. The method achieves state-of-the-art post-training quantization (PTQ) results on both image and video diffusion transformers, notably being the only method that produces usable images at W2A4 (2-bit weights, 4-bit activations) quantization levels.

## Problem Statement

Diffusion transformers (DiTs) have become the foundation for state-of-the-art image and video generation. However, deploying these models at scale is computationally expensive. Quantization is a key technique for model compression, but existing methods struggle with DiTs because:

### Core Challenges

1. **Timestep-Dependent Activations:** DiT activations have different distributions at different timesteps (initialization, middle, final denoising steps), requiring separate calibration for each.

2. **Prompt-Induced Distribution Shifts:** Text-conditioned guidance branches experience different activation ranges for different input prompts, requiring prompt-specific recalibration.

3. **Guidance Branch Variability:** Classifier-free guidance introduces additional distribution variations that existing quantization methods cannot handle efficiently.

4. **Data Calibration Requirements:** Traditional quantization methods require access to representative calibration datasets, which may not be available or practical to collect.

5. **Re-fitting for Every Checkpoint:** Prior methods force re-calibration of quantization parameters for every new model checkpoint or input modality change.

### Research Gap

While quantization methods exist for general deep learning models and even some diffusion models, they fail to address the specific characteristics of DiTs that fundamentally change activations across timesteps and input conditions. The field lacks a truly data-agnostic solution that can generalize across all timesteps and guidance conditions.

## Core Concepts & Theory

### Activation Distribution Problem in DiTs

DiT activations exhibit fundamentally different behavior across the denoising process:

```
At timestep t_0 (start):  activations ≈ N(μ_start, σ_start)
At timestep t_mid:        activations ≈ N(μ_mid, σ_mid)
At timestep t_final:      activations ≈ N(μ_final, σ_final)
```

This non-stationary behavior invalidates assumptions made by traditional quantization methods that assume stable activation distributions.

### Randomized Permuted Block-Hadamard (RPBH) Rotation

OrbitQuant's core innovation is using RPBH rotations to normalize activations:

**Key Property:** RPBH rotation concentrates each coordinate around one fixed, known marginal regardless of input conditions.

**Mathematical Insight:**
```
For input activations x with varying distribution P(x|t, prompt):
x_rotated = RPBH(x)  →  each coordinate j has margin N(0, 1)
```

This transformation makes activations invariant to timestep and prompt conditions!

### Lloyd-Max Quantization with Unified Codebook

Once rotations normalize activations to standard normal distributions:

1. **Single Codebook:** A single Lloyd-Max codebook optimized for N(0, 1) works for all timesteps and prompts
2. **Efficient Encoding:** No need to re-calibrate for different conditions
3. **Offline Weight Quantization:** Weight rotation can be absorbed into the weights themselves

**Implementation:**
```
For weight matrix W and bias b:
W_rotated = W @ RPBH^T  (rotation absorbed into weights)
b_rotated = b  (no change)

At inference:
x_rotated = RPBH(x)
y = x_rotated @ W_rotated + b_rotated
(RPBH rotation cancels out inside the linear layer)
```

### Computational Efficiency

The clever design ensures minimal runtime overhead:

- **Offline cost:** Weight rotation happens once during quantization setup
- **Runtime cost:** Only forward rotation on activations needed at inference
- **No recalibration:** Single codebook serves all conditions without refitting

## Main Ideas & Contributions

### 1. Data-Agnostic Quantization Framework
OrbitQuant is the first quantization method for DiTs that requires **zero calibration data**, making it immediately applicable to any new model without data collection overhead.

### 2. Unified Treatment of Timesteps and Prompts
By discovering that RPBH rotation normalizes activations across all timesteps and guidance conditions, OrbitQuant eliminates the need for condition-specific calibration—a major simplification.

### 3. State-of-the-Art PTQ Results
Achieves superior performance on standard benchmarks:
- **GenEval benchmark:** State-of-the-art for image generation quality
- **VBench benchmark:** State-of-the-art for video generation quality
- No calibration data required (unlike competing methods)

### 4. Extreme Quantization Resilience
The only method that produces usable images at W2A4 (2-bit weights, 4-bit activations)—a level where prior PTQ baselines completely collapse to noise.

### 5. Practical Applicability
The method's data-agnostic nature makes it immediately deployable to new models, checkpoints, and modalities without additional engineering effort.

## Methodology & Implementation

### System Architecture

```
Input: DiT model, target quantization bits (e.g., W4A8, W2A4)
       NO calibration data required

Step 1: Analyze activation statistics
        - Sample activations across timesteps
        - Verify RPBH normalization effect

Step 2: Weight Quantization
        - Apply RPBH rotation to weight matrices
        - Generate Lloyd-Max codebook for rotated weights
        - Store quantized weights and codebook

Step 3: Activation Quantization
        - Use same Lloyd-Max codebook for all timesteps
        - At runtime: rotate activations, quantize, operations proceed

Output: Quantized DiT model with <1% accuracy loss
```

### Datasets and Evaluation

**Image Generation Benchmarks:**
- **GenEval:** Standard benchmark for evaluating image quality from text-to-image models
  - Measures alignment with text prompts
  - Evaluates visual quality

**Video Generation Benchmarks:**
- **VBench:** Comprehensive benchmark for video generation quality
  - Temporal consistency metrics
  - Motion quality
  - Semantic accuracy

**Models Evaluated:**
- Stable Diffusion (image generation)
- Stable Video Diffusion (video generation)
- Other state-of-the-art DiT variants

### Quantization Configurations Tested

| Config | Weights | Activations | Prior Methods | OrbitQuant |
|---|---|---|---|---|
| W4A8 | 4-bit | 8-bit | Functional | State-of-the-art |
| W4A4 | 4-bit | 4-bit | Degraded | Good |
| W2A8 | 2-bit | 8-bit | Limited | Functional |
| W2A4 | 2-bit | 4-bit | **Collapses to noise** | **Only usable method** |

**Key Result:** At W2A4 extreme quantization, OrbitQuant is the only method where generated images remain recognizable and useful.

### Results Summary

[Exact figures unavailable — see full paper]

The paper reports:
- GenEval scores for OrbitQuant across all quantization levels
- Comparison with prior PTQ baselines
- VBench metrics for video generation at different quantization levels
- Visual quality assessment at extreme compression (W2A4)

## Practical Applications & Use Cases

### 1. Edge Deployment of Image Generators
Enable running text-to-image models on edge devices:
- Mobile phones: W2A4 quantization reduces model size 4-8x
- IoT devices: Practical inference for visual generation tasks
- Resource-constrained environments: Battery-efficient image generation

### 2. Real-Time Video Generation
Reduce latency for video diffusion models:
- Streaming video synthesis
- Interactive video editing
- Frame-by-frame generation with minimal latency

### 3. Multi-Modal Applications
Deploy vision generation alongside language models:
- Multimodal AI assistants
- Combined text+image understanding and generation
- Efficient multi-task models

### 4. Model Serving at Scale
Run multiple DiT instances on shared hardware:
- Cloud inference services
- Cost-effective API endpoints
- Reduced memory footprint enables higher throughput

### 5. Continual Model Updates
No recalibration needed when:
- Loading new checkpoints
- Switching between models
- Adapting to new guidance conditions

This makes OrbitQuant ideal for production systems where models are frequently updated.

## Insights & Implications

### Deeper Understanding of DiT Behavior

1. **Invariant Rotation Principle:** RPBH rotations normalize activations across structural variations (timesteps, prompts), suggesting deep invariances in how DiTs process information.

2. **Timestep as Data Augmentation:** The observation that quantization must handle timestep-varying distributions reveals that timesteps function as a form of implicit data augmentation within a single forward pass.

3. **Generalization Beyond Quantization:** The RPBH normalization principle may apply to other quantization problems in time-dependent models (diffusion policies, temporal networks).

### State-of-the-Art Advancement

- **First data-agnostic method:** Previous PTQ approaches required calibration data, making OrbitQuant qualitatively different
- **Extreme quantization breakthrough:** W2A4 quantization reaching acceptable quality is unprecedented for diffusion models
- **Practical maturity:** The method is immediately deployable without additional engineering

### Limitations and Open Questions

1. **Scalability to Newer Architectures:** How well does RPBH normalization work with emerging DiT variants (e.g., multi-head DiT architectures)?

2. **Why RPBH Specifically:** While empirically validated, the theoretical justification for why RPBH achieves this invariance property needs deeper analysis.

3. **Generalization to Other Diffusion Types:** 
   - Continuous diffusion models (score-based)
   - Non-vision diffusion (3D object, protein structure)
   - Non-parametric diffusion variants

4. **Fine-grained Timestep Analysis:** Do all timesteps benefit equally from RPBH normalization, or are there critical phases?

5. **Combination with Other Compression:** How does OrbitQuant interact with pruning, distillation, or other compression techniques?

## Code & Resources

### GitHub Repository
Official implementation with full source code

### Dependencies
- PyTorch 2.0+
- Hugging Face Diffusers library
- NumPy (for numerical operations)
- Standard computer vision libraries (PIL, torchvision)

### Compute Requirements
- **Quantization:** CPU-feasible (no GPU required for most steps)
- **Inference:** GPU optional but recommended
  - Full precision: High-end GPU recommended
  - W2A4 quantized: Can run on mid-range GPUs or even CPU

### Quick-Start Guide

```python
import torch
from diffusers import StableDiffusionPipeline
from orbitquant import quantize_dit, apply_orbitquant

# Load base model
pipe = StableDiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-2-1")
model = pipe.unet

# Quantize with OrbitQuant (no calibration data needed!)
quantized_model = quantize_dit(
    model, 
    weight_bits=2,
    activation_bits=4
)

# Use quantized model in pipeline
pipe.unet = quantized_model
prompt = "a cat sitting on a couch"
image = pipe(prompt).images[0]
image.save("result.png")
```

## Related Work & Context

### Quantization Methods for Transformers
- **Layer-wise Quantization:** Applies per-layer calibration (requires data)
- **Channel-wise Quantization:** More fine-grained but higher complexity
- **Mixed-Precision:** Assigns different bits to different layers (requires per-layer tuning)

OrbitQuant differs by being completely data-agnostic and unified across all conditions.

### Diffusion Model Optimization
- **Distillation:** Reduces steps but changes model behavior
- **Pruning:** Removes neurons but requires retraining
- **Knowledge Distillation to Smaller Models:** Requires training infrastructure
- **Quantization (OrbitQuant):** Pure inference-time optimization, no training

### RPBH and Rotation-Based Methods
- **Random Projections:** Used in randomized algorithms for dimensionality reduction
- **Hadamard Transforms:** Fast orthogonal transforms, used in many signal processing applications
- **Permuted Structures:** Block permutations add randomness to improve generalization

OrbitQuant's combination is novel for quantization contexts.

### Future Research Directions

1. **Theoretical Foundation:** Formal analysis of why RPBH rotations achieve timestep-invariant normalization

2. **Adaptive Quantization:** Learn per-layer or per-head quantization configurations from the RPBH structure

3. **Extension to Other Models:** Apply RPBH normalization to:
   - Video transformers beyond diffusion
   - Autoregressive transformers with timestep structure
   - Sequence models with inherent temporal variation

4. **Quantization + Sparsity:** Combine OrbitQuant with structured pruning for maximum compression

5. **Hardware-Aware Quantization:** Co-design quantization with specific hardware targets (TPU, mobile chips)

6. **Federated/Distributed Quantization:** Quantize models at different sites without centralizing weights

## References & Citations

- Donghyun Lee, Jitesh Chavan, Duy Nguyen, Sam Huang, Liming Jiang, Priyadarshini Panda, Timo Mertens, Saurabh Shukla. (2026). OrbitQuant: Data-Agnostic Quantization for Image and Video Diffusion Transformers. arXiv preprint arXiv:2607.02461.
