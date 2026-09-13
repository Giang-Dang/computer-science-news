# Depth-Synergized Mamba Meets Memory Experts for All-Day Image Reflection Separation

**Authors:** Siyan Fang, Long Peng, Yuntao Wang, Ruonan Wei, Yuehuan Wang
**ArXiv ID:** 2601.00322
**Submitted:** January 2026
**Conference:** AAAI 2026
**Available:** https://arxiv.org/abs/2601.00322

## Executive Summary

This paper addresses the challenging problem of image reflection separation—disentangling transmission (scene) and reflection layers from blended images—with a novel approach that combines depth-guided state-space models (Mamba) with memory expert compensation. The key innovation is leveraging depth information to guide the Mamba architecture's information flow while using cross-image historical knowledge through memory experts to provide layer-specific compensation. The method excels particularly in challenging low-light conditions where conventional approaches struggle due to poor contrast between layers. This represents a significant advancement in real-world image processing applications.

## Problem Statement

Image reflection separation is the task of decomposing a single blended image into:
1. **Transmission Layer:** The actual scene content (desired output)
2. **Reflection Layer:** Unwanted reflections from surfaces (e.g., glass windows, mirrors)

**Fundamental Challenges:**

- **Ambiguity Problem:** Single image lacks depth information; infinite layer pair solutions could explain the observation
- **Contrast Sensitivity:** Methods fail when transmission and reflection have similar brightness
- **All-Day Operation:** Particularly difficult at night with low contrast and high noise
- **Lack of Constraints:** Limited physical priors about reflection properties

**Prior Limitations:**

- Existing methods rely on limited information from single images
- Struggle with similar-contrast scenarios
- Fail in low-light conditions (nighttime photography)
- Hand-crafted features become unreliable in challenging lighting

## Core Concepts & Theory

### State-Space Models and Mamba

**Background:**
- State-space models (SSMs) provide efficient sequence processing alternatives to transformers
- Mamba: A selective state-space model with input-dependent state dynamics
- Advantages over RNNs: Parallelizable, maintains long-range dependencies
- Advantages over Transformers: Linear complexity in sequence length

**Depth-Synergized Modification:**
- Augment Mamba to accept depth as modulation signal
- Depth gates control information flow through state transitions
- Salient structures (high depth variation) receive stronger information flow
- Ambiguous regions (low depth variation) receive weaker flow

### Memory Expert Architecture

**Expert System Components:**
- Multiple experts: specialized networks for different scene characteristics
- Routing mechanism: dynamic selection based on input features
- Cross-image memory: historical knowledge from similar scenes
- Compensation strategy: experts provide residual corrections for layer-specific properties

**Depth-Aware Scanning (DAScan):**
- Scan image using depth-guided paths
- Guide Mamba toward salient structures
- Promote information flow along semantic coherence
- Construct stable state representations

### Information Bottleneck Principle

The framework addresses layer ambiguity through:
1. **Depth Constraint:** Physical depth structure differs between layers
2. **Semantic Coherence:** Transmission layer has semantic meaning
3. **Memory Guidance:** Historical examples inform layer properties
4. **Expert Compensation:** Specialized experts handle layer-specific artifacts

## Main Ideas & Contributions

1. **Depth-Synergized State-Space Model (DS-SSM):** Novel architecture modulating Mamba state activations by depth, enhancing focus on salient structures while suppressing ambiguous features

2. **Depth-Aware Scanning (DAScan):** Innovative input processing that guides state-space traversal toward structurally important image regions

3. **Memory Expert Compensation Module (MECM):** Leverages cross-image historical knowledge to provide layer-specific compensation, addressing limitations of single-image processing

4. **All-Day Performance:** First method to successfully handle low-light and nighttime reflection separation, crucial for real-world deployment

5. **Unified Framework:** Demonstrates that state-space models can be effectively adapted for dense pixel-prediction tasks with architectural innovations

## Methodology & Implementation

### Architecture Overview

**Three Main Components:**

**1. Depth-Aware Scanning (DAScan)**
- Input: RGB image and depth map
- Process: Generate depth-guided scanning paths
- Output: Ordered sequence highlighting salient regions
- Benefit: Mamba processes image following semantic structure

**2. Depth-Synergized State-Space Model (DS-SSM)**
- Input: Scanned sequences from DAScan, depth values
- Core Innovation: Depth modulates state activation sensitivity
- Mechanism: Element-wise multiplication of state transitions by depth factors
- Output: Enhanced feature representations emphasizing structured regions

**3. Memory Expert Compensation Module (MECM)**
- Expert Pool: Multiple expert networks for different scene types
- Memory Database: Historical features from processed images
- Routing: Retrieve similar examples from memory
- Compensation: Each expert provides layer-specific residual corrections

### Experimental Setup

**Datasets:**

- **SIR-BBM Dataset:** Synthetic images with known ground truth layers
- **Real World Reflected Images (RWRI):** Real-world examples from various environments
- **Custom Nighttime Dataset:** Low-light images with challenging conditions
- **In-the-wild examples:** Diverse real-world scenarios

**Evaluation Metrics:**

- **PSNR (Peak Signal-to-Noise Ratio):** Reconstruction quality in dB
- **SSIM (Structural Similarity Index):** Perceptual quality (0-1 scale)
- **LPIPS (Learned Perceptual Image Patch Similarity):** Perceptual loss using deep features
- **User Studies:** Human evaluation of separation quality

**Preprocessing:**

1. Estimate depth map (using off-the-shelf depth estimator or stereo)
2. Normalize RGB and depth to canonical ranges
3. Apply DAScan depth-guided ordering
4. Retrieve k-nearest historical examples from memory

### Implementation Details

**Model Specifications:**
- DS-SSM depth modulation factor: trainable per layer
- Memory bank size: [Specific value unavailable]
- Expert count: [Specific value unavailable]
- Input resolution: Up to [resolution unavailable]
- Parameters: [Count unavailable]

**Training Configuration:**
- Loss function: Combination of L1 reconstruction + perceptual loss + adversarial loss
- Optimizer: [Type unavailable]
- Learning rate schedule: [Details unavailable]
- Batch size: [Unavailable]
- Training duration: [Unavailable]

### Results

[Exact figures unavailable — see full paper]

The paper demonstrates:
- Superior performance on both synthetic (SIR-BBM) and real (RWRI) datasets
- Particularly strong improvements in low-light scenarios
- Competitive results compared to state-of-the-art methods (DefocusNet, ERRNet, etc.)
- Improved night-time reflection separation capability
- Qualitative results showing clean layer separation in challenging conditions

## Practical Applications & Use Cases

### Immediate Applications

1. **Smartphone Photography:** Remove unwanted reflections from photos taken through glass
2. **Autonomous Driving:** Process images from vehicle cameras obscured by window reflections
3. **Surveillance Systems:** Enhance video quality by removing reflections from camera lenses
4. **Medical Imaging:** Separate actual tissue from reflected artifacts in optical systems
5. **Night Photography:** Enable high-quality image capture in low-light reflection scenarios
6. **AR/VR Systems:** Pre-process environmental images for virtual environment mapping

### Real-World Scenarios

- Tourist photos through museum glass cases
- Security camera footage through dirty windows
- Dashboard camera recordings from vehicles
- Night-time street photography
- Interior photography near windows and mirrors
- Documentation photography of reflective surfaces

## Insights & Implications

### Broader Field Impact

1. **State-Space Models for Dense Prediction:** Successfully demonstrates Mamba's applicability beyond language tasks to dense pixel-prediction problems

2. **Depth as Structural Prior:** Shows how geometric information (depth) can guide learned representations without explicit geometric constraints

3. **Memory-Augmented Vision:** Introduces effective memory-based expert compensation for challenging computer vision tasks

4. **Night Vision Processing:** Addresses practical limitation of existing methods—poor low-light performance—critical for 24/7 real-world deployment

### State-of-the-Art Advancement

- First to combine state-space models with depth guidance for image separation
- Superior handling of low-contrast scenarios compared to CNN-based methods
- Extends dense prediction capabilities to a previously difficult application

### Limitations and Open Questions

1. **Depth Dependency:** Requires accurate depth maps; performance degrades with poor depth estimation
2. **Computational Cost:** Mamba + memory retrieval may be slower than feed-forward approaches
3. **Memory Scalability:** How does memory bank size affect generalization to novel scenes?
4. **Generalization:** How well does the method transfer to non-trained lighting conditions?
5. **Multi-Reflection:** Current approach assumes two layers; extension to multiple reflections unclear

## Code & Resources

**Model Availability:**
- Likely available on GitHub (common for AAAI accepted papers)
- Pre-trained weights for SIR-BBM and RWRI datasets
- Depth estimation module (possibly uses MiDaS or similar)

**Dependencies:**
- PyTorch or JAX for model implementation
- Depth estimation library (MiDaS, DPT, or similar)
- Image processing libraries (PIL, OpenCV, scikit-image)
- CUDA support for GPU acceleration

**Compute Requirements:**
- GPU: Likely requires 8GB+ VRAM for inference
- Training: Multiple GPUs recommended (typical for transformer/SSM-based vision)
- Inference time: Real-time capability achievable on modern GPUs

### Quick-Start Guide

1. Obtain test image and estimate depth map
2. Load pre-trained Depth-Synergized Mamba weights
3. Initialize memory bank from training dataset
4. Process image through DAScan
5. Run DS-SSM inference
6. Apply MECM expert compensation
7. Composite transmission layer output

## Related Work & Context

### Related Recent Papers

- **Image Restoration:** Various denoising, deblurring, and restoration methods
- **Reflection Removal:** Prior work (DefocusNet, ERRNet, etc.)
- **Depth Estimation:** Related work on monocular depth prediction
- **Mamba Architecture:** State-space models for vision tasks

### Prior Work Foundations

- Reflection separation research (classical and deep learning approaches)
- State-space models and recurrent architectures
- Mixture of experts in neural networks
- Depth-guided image processing
- Memory-augmented neural networks

### Future Research Directions

1. **End-to-End Depth Estimation:** Joint depth and reflection layer prediction
2. **Multi-Layer Separation:** Extending beyond two-layer assumption
3. **Video Reflection Separation:** Temporal consistency for video sequences
4. **Adaptive Memory Management:** Efficient memory retrieval for large-scale applications
5. **Real-time Optimization:** Lightweight variants for mobile deployment
6. **Cross-Domain Generalization:** Transfer to different camera types and sensors
7. **Physical Constraints:** Incorporating reflection properties (specularity, angle-dependence)
