# VideoWeave: Unlocking Geometric Consistency in Video Generation via Joint Geometry-Video Modeling

**Authors:** Xunzhi Xiang, Zixuan Duan, Yabo Chen, Zhengxuan Wei, Guiyu Zhang, Zixiao Gu, Zhe Gao, Haibin Huang, Chi Zhang, Qi Fan, Xuelong Li

**ArXiv ID:** 2606.14162

**Date Published:** June 2026

## Executive Summary

VideoWeave addresses a critical limitation of large-scale video diffusion models: their inability to preserve 3D geometric structure over time, leading to geometric drift and implausible motion under viewpoint changes. By introducing a latent-space post-training framework that uses implicit geometry-model features to constrain the generative distribution, VideoWeave enables camera-guided and geometrically consistent 3D-aware video synthesis. This approach represents a significant advancement in video generation quality and consistency.

## Problem Statement

Traditional video diffusion models excel at generating visually plausible content but fail to maintain geometric coherence across frames. Key limitations include:

- **Geometric Drift:** The 3D scene structure deteriorates over time during generation
- **Viewpoint Inconsistency:** Camera motion and object geometry become implausible under viewpoint changes
- **Dependency on Upstream Errors:** Existing approaches using explicit geometry reconstructions (depth maps, point clouds, 3D structures) are sensitive to errors from upstream geometry pipelines
- **Reconstruction Overhead:** Decoding intermediate representations (depth, point clouds, rendered views) adds computational cost and error propagation

Prior methods attempted to enforce geometric consistency through explicit geometry supervision, but this approach introduces fragility and computational overhead. VideoWeave tackles this by shifting from explicit reconstruction-based guidance to implicit, learned geometry representations.

## Core Concepts & Theory

### Key Innovation: Implicit Geometry Guidance

VideoWeave treats geometry not as explicit reconstruction outputs (depth maps, point clouds) but as latent features learned during post-training. This allows:

- **Flexible Guidance:** Geometry shapes the generative distribution without requiring perfect reconstructions
- **Error Mitigation:** Errors from geometry models have reduced impact since they guide through learned latent representations
- **Non-Rigid Modeling:** Supports both rigid scene structures and non-rigid object deformations

### Architecture Overview

The framework employs a U-Net-like architecture that bridges heterogeneous geometry and video representations:

1. **Geometry Latent Adaptation:** Convert geometry features into a shared latent space compatible with video latents
2. **Joint Diffusion Modeling:** Geometry and video latents are jointly modeled in a shared denoising space
3. **Score Transfer:** Distribution-level score transfer preserves the pretrained video prior during adaptation

### Theoretical Foundation

VideoWeave operates in latent space to:
- Avoid decoding overhead of explicit geometry representations
- Leverage pretrained video diffusion model priors
- Enable flexible, non-rigid guidance that accommodates various geometry extraction methods

The joint modeling approach allows geometry to implicitly constrain the video generation process without requiring explicit reconstruction-based supervision.

## Main Ideas & Contributions

### 1. Latent-Space Post-Training Framework
- Adapts pretrained video diffusion models by introducing geometry latents alongside video latents
- Preserves pretrained video priors while incorporating geometric constraints
- More efficient than retraining from scratch

### 2. Implicit Geometry Modeling
- Uses learned geometry features rather than explicit reconstructions
- Reduces sensitivity to upstream geometry pipeline errors
- Supports flexible, non-rigid guidance applicable to various scene types

### 3. Progressive Training Strategy
- **Stage 1:** Geometry latent adaptation to align geometry and video representations
- **Stage 2:** Joint geometry-video diffusion modeling in shared denoising space
- **Stage 3:** Distribution-level score transfer to preserve video generation quality

### 4. Curated Training Dataset
- GeoVid-80K: 80K-video dataset with paired appearance and geometry representations
- Includes diverse cinematography: indoor, outdoor, aerial
- Features pronounced camera motion and both static and dynamic scenes

## Methodology & Implementation

### Training Dataset: GeoVid-80K

**Composition:**
- Sourced from unconstrained web videos and public datasets (DL3DV, RealEstate10K, MiraData, SpatialVid)
- Licensed commercial footage from high-quality sources (Mixkit, Pexels, Pixabay)
- 80,000 carefully curated videos

**Coverage:**
- Indoor, outdoor, and aerial cinematography
- Static scenes with pure background geometry
- Dynamic scenes with object interactions
- Pronounced camera motion: panning, tracking, fly-throughs

### Experimental Setup

**Applications Tested:**
- Text-to-video generation with geometric guidance
- Image-to-video generation with geometric constraints

**Evaluation Protocol:**
- VBench benchmark for comprehensive video quality assessment
- 3D reconstruction metrics for geometric consistency
- Epipolar geometry analysis for view-consistency verification
- Direct comparison with 2D-only video generation baselines

### Evaluation Metrics & Results

**Quantitative Results:**

| Metric | Performance |
|--------|-------------|
| VBench Subject Consistency | Best among compared methods |
| VBench Motion Smoothness | Best among compared methods |
| VBench Imaging Quality | Best among compared methods |
| PSNR (3D Reconstruction) | Improved over baselines |
| SSIM (Structural Similarity) | Best alignment with geometry |
| LPIPS (Perceptual Distance) | Improved visual consistency |
| MSE (Mean Squared Error) | Reduced reconstruction error |
| Epipolar Error | Improved view-consistency |

**Qualitative Results:**
- Produces temporally stable videos with consistent scene layout
- Maintains object geometry and camera motion consistency
- Generates more complete and better-aligned 3D reconstructions compared to 2D-only generators
- Improves geometric coherence while preserving strong visual quality
- Supports both camera-guided and text-guided generation modes

## Practical Applications & Use Cases

### 1. Camera-Guided Video Generation
- Cinematography with precise camera control
- Virtual production and film/VFX industry applications
- Dynamic camera path planning for video synthesis

### 2. 3D Scene Reconstruction and Video
- Real-time capture-to-video workflows
- Converting single-image or sparse-view inputs to consistent video
- Geometric consistency in extended video sequences

### 3. Virtual Environments and Spatial Computing
- Consistent 3D-aware content generation for AR/VR applications
- Multiplayer virtual environments with consistent geometry
- 360-degree video generation with geometric constraints

### 4. Video Editing and Post-Production
- Temporal coherence preservation in edited sequences
- Geometric-aware video inpainting and completion
- Motion-consistent view synthesis

### 5. Robotics and Autonomous Systems
- Generating realistic training data with consistent 3D geometry
- Simulator content generation for embodied AI tasks
- Consistent spatial reasoning for robotic perception

## Insights & Implications

### Broader Field Impact

**State-of-the-Art Advancement:**
- Bridges the gap between video generation quality and geometric consistency
- Demonstrates that latent-space guidance is more effective than explicit reconstruction-based approaches
- Shows that implicit geometry modeling preserves video generation quality better than previous methods

**Paradigm Shift:**
- Shifts from treating geometry and appearance generation separately to joint, unified modeling
- Demonstrates the value of post-training adaptation over full retraining
- Opens new directions for conditioning video generation with implicit representations

### Theoretical Insights
- Implicit geometry guidance is more robust to upstream errors than explicit approaches
- Leveraging pretrained priors while adding new constraints is more efficient than retraining
- Latent-space operations reduce computational overhead of explicit geometry operations

### Limitations and Open Questions

1. **Computational Overhead:** Even with latent-space modeling, post-training adds training time
2. **Geometry Quality Dependency:** Quality still depends on upstream geometry extraction, though impact is mitigated
3. **Scalability:** Evaluating performance on higher resolutions and longer sequences needed
4. **Generalization:** Transferability to other video generation models beyond tested baselines

### Future Research Directions

- Extension to dynamic scene understanding with temporal geometry tracking
- Integration with other implicit representations (neural fields, signed distance functions)
- Real-time inference optimization for practical deployment
- Multi-modal guidance combining geometry, text, and sketch-based constraints

## Code & Resources

**Official Repository:** Not yet publicly available. Check arxiv paper for supplementary materials.

**Dependencies:**
- Large-scale video diffusion model (pre-trained model required)
- Geometry extraction pipeline (depth estimation or 3D reconstruction)
- Training framework: PyTorch or similar deep learning library

**Compute Requirements:**
- GPU: High-end GPU recommended (likely A100/H100 class for training)
- Training time: Post-training phase (faster than full model retraining)
- Inference: Real-time or near-real-time generation on modern GPUs

**Quick-Start Guide:**
1. Prepare video data with paired geometry representations
2. Initialize from pretrained video diffusion model
3. Adapt geometry latents to shared representation space
4. Train with joint geometry-video loss objectives
5. Deploy for text-to-video or image-to-video tasks

## Related Work & Context

### Related Recent Papers

- **Making Time Editable in Video Diffusion Transformers** (2026-06-08) - Temporal control in video generation without architectural redesign
- **Spectral Progressive Diffusion for Efficient Image and Video Generation** (2026-05-18) - Efficient video generation through spectral methods
- **A Systematic Post-Train Framework for Video Generation** (2026-04-30) - Post-training approaches for video models
- **MultiWorld: Scalable Multi-Agent Multi-View Video World Models** (2026-04-20) - Multi-view video generation consistency

### Prior Work Foundations

- Diffusion-based video generation models (foundational work on video diffusion)
- Explicit geometry conditioning methods (depth-guided, point-cloud-based approaches)
- Latent diffusion models (efficient latent-space generation)
- 3D-aware image and video generation (scene structure understanding)

### Possible Future Research Directions

1. **Implicit Representations:** Extend to other implicit geometry representations (occupancy networks, neural fields)
2. **Real-Time Inference:** Optimization techniques for edge deployment
3. **Multi-Modal Guidance:** Combine geometric, textual, and sketch-based guidance
4. **Temporal Consistency:** Improved temporal coherence through geometry-aware attention mechanisms
5. **Generalizable Geometry:** Learn geometry representations that transfer across multiple video domains

## Conclusion

VideoWeave represents a significant advancement in video generation by demonstrating that implicit, learned geometry guidance is superior to explicit reconstruction-based approaches. The latent-space post-training framework preserves the quality and efficiency of pretrained video models while adding powerful geometric consistency constraints. This work opens new possibilities for applications requiring both visual quality and geometric coherence, from virtual production to AR/VR content generation.
