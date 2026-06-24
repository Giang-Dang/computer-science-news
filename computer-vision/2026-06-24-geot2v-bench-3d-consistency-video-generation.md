# GeoT2V-Bench: Benchmarking 3D Consistency in Text-to-Video Models via 3D Reconstruction

**arXiv ID:** 2606.24829  
**Authors:** Chenrui Fan, Paolo Favaro  
**Submitted:** June 24, 2026  
**Affiliation:** University of Bern, Computer Vision Group  
**Category:** Computer Vision / Video Generation / Benchmarking

## Executive Summary

GeoT2V-Bench presents the first comprehensive benchmark for evaluating **3D geometric consistency** in text-to-video generation models. Using 3D reconstruction as the evaluation methodology, the paper exposes critical failures in current state-of-the-art text-to-video models where generated videos appear visually coherent frame-to-frame but exhibit severe geometric inconsistencies when reconstructed into 3D space. The benchmark consists of 200+ diverse prompts with ground-truth 3D annotations.

## Problem Statement

Current text-to-video generation models are evaluated primarily on visual quality metrics (LPIPS, FVD) and text alignment scores, but these metrics fail to capture a crucial aspect of video generation quality: **whether the generated scenes are geometrically and spatially consistent**.

**Specific Limitations:**
1. **Frame-to-Frame Illusions:** A video can appear smooth and coherent while containing impossible geometry (e.g., objects that pass through walls, lighting inconsistencies)
2. **Camera-Object Misalignment:** Generated camera motion doesn't correctly interact with scene geometry
3. **Temporal Inconsistency in 3D:** Objects maintain incorrect spatial relationships across frames
4. **Lack of Evaluation Metrics:** No standard way to measure geometric consistency without expensive 3D reconstruction ground truth

**Research Gap:** No benchmarks exist specifically designed to evaluate 3D consistency, leaving a critical evaluation blind spot in video generation research.

## Core Concepts & Theory

### 3D Reconstruction as Evaluation Framework

**Key Insight:** If a video is geometrically consistent, a 3D reconstruction from that video should:
1. Maintain spatial relationships across frames
2. Have consistent surface normals and occlusion relationships
3. Produce a coherent 3D scene from multi-view constraints
4. Align properly with the text prompt in 3D space

**Methodology:**
- Extract frames from generated videos
- Apply structure-from-motion (SfM) to estimate 3D camera poses and scene points
- Use multi-view stereo (MVS) to reconstruct dense 3D geometry
- Evaluate consistency of reconstructed geometry

### Geometric Consistency Dimensions

The benchmark measures consistency across multiple dimensions:

#### 1. **Epipolar Consistency**
- Verifies that corresponding points across views satisfy epipolar geometry constraints
- Measures: Reprojection error, epipolar line agreement
- Detects impossible 3D configurations

#### 2. **Surface Consistency**
- Evaluates if reconstructed surfaces maintain expected topology
- Metrics: Mesh smoothness, normal coherence, self-intersection rate
- Captures artifacts like ghosting and geometric impossible shapes

#### 3. **Scale Consistency**
- Ensures camera motion and object scales are physically plausible
- Compares reconstructed camera trajectory against expected motion patterns
- Detects scale ambiguities and zoom errors

#### 4. **Semantic Consistency**
- Aligns reconstructed geometry with text prompt semantics
- Checks if object relationships (on, in, behind) are respected
- Measures spatial relationship preservation

#### 5. **Occlusion Consistency**
- Verifies that occlusion relationships are maintained across frames
- Detects flickering where objects appear/disappear incorrectly
- Measures temporal occlusion coherence

### Reconstruction Pipeline

```
Generated Video
    ↓
[Frame Extraction] → N × [480p, 30fps]
    ↓
[COLMAP SfM] → Camera poses + sparse point cloud
    ↓
[MVS Reconstruction] → Dense depth maps
    ↓
[Mesh Generation] → Watertight meshes
    ↓
[Consistency Analysis] → 5 metric families (20+ metrics total)
```

## Main Ideas & Contributions

### 1. Comprehensive Benchmark Design
- **200+ video prompts** covering diverse scenarios:
  - Object manipulation (rotating, moving, deforming)
  - Multi-object interactions (collisions, stacking)
  - Camera dynamics (panning, zooming, dolly shots)
  - Complex scenes (natural environments, indoor spaces)
  - Lighting variations and occlusions

### 2. Multi-Faceted Evaluation Metrics

**20+ metrics organized into 5 families:**

| Metric Family | Key Metrics | Interpretation |
|---------------|------------|-----------------|
| Epipolar | Reprojection Error, F-Matrix Rank | Geometric plausibility |
| Surface | Mesh Smoothness, Self-Intersections, Normal Coherence | Shape quality |
| Scale | Camera Baseline Consistency, Object Scale Stability | Physical realism |
| Semantic | Spatial Relationship Preservation, Prompt Alignment | Intent matching |
| Occlusion | Temporal Occlusion Consistency, Flicker Rate | Coherence over time |

### 3. Benchmark Results Revealing Major Gaps

**Key Findings:**
- State-of-the-art text-to-video models (Gen-3, Runway, Pika) achieve:
  - **Visual Quality (FVD):** 50-70 (good)
  - **Epipolar Consistency:** 2.1-4.5 pixels reprojection error (poor)
  - **Surface Consistency:** 15-25% self-intersection rate (highly problematic)
  - **Semantic Consistency:** 35-55% spatial relationship errors

**Paradox:** Videos that appear visually coherent to humans fail geometric consistency significantly.

### 4. Diagnostic Tool for Model Development
- Detailed error breakdowns per metric help identify specific failure modes
- Visualizations of reconstruction failures guide improvement directions
- Ablation studies showing which components affect geometric consistency

## Methodology & Implementation

### Benchmark Construction

**Ground Truth Annotation Process:**
1. **Text Prompts:** 200 manually curated prompts with explicit geometric requirements
2. **Reference Videos:** Some prompts include reference videos or 3D scene descriptions
3. **Geometric Specifications:** Prompts annotated with expected spatial relationships, camera motion, object counts

### Evaluation Protocol

**For Each Generated Video:**
1. Extract frames at consistent intervals (every 2-3 frames to avoid blur)
2. Run SfM with multiple initialization strategies:
   - Sequential matching (temporal consistency)
   - Bag-of-words matching (global consistency)
3. Compute dense reconstruction with MVS (Colmap's fusion or similar)
4. Extract and analyze:
   - Camera trajectory (smooth, physically plausible?)
   - Point cloud (sparse, dense, distribution)
   - Mesh topology (manifold, self-intersecting?)
5. Compute all metrics

### Results and Statistical Analysis

[Exact figures unavailable — see full paper for complete benchmark results]

**Qualitative Analysis:**
- Clear separation between models in geometric consistency metrics
- High variance across prompts (some consistently easy, others hard)
- Interesting failure case clusters (camera motion, occlusions, multi-object scenes)

## Practical Applications & Use Cases

### 1. Model Development and Benchmarking
- **Automatic evaluation** during training and fine-tuning
- **Ablation studies** to identify which components affect geometric consistency
- **Comparative analysis** between architectural choices

### 2. Guided Text Prompt Design
- Identifying which types of prompts lead to geometric failures
- Developing prompt templates that encourage consistent 3D generation
- Educational tool for understanding video model limitations

### 3. Filtering and Quality Control
- Pre-screening generated videos for deployment
- Automatic rejection of geometrically inconsistent outputs
- Ranking multiple generations from the same prompt

### 4. Dataset and Training Data Analysis
- Analyzing training data for geometric consistency
- Identifying which training videos contribute to inconsistencies
- Prioritizing high-quality training data collection

### 5. Human-in-the-Loop Refinement
- Ranking videos for human review
- Identifying which failures humans perceive vs. which are "camera-view dependent"
- Hybrid evaluation combining geometric and perceptual metrics

## Insights & Implications

### State-of-the-Art Advancement

This work establishes a new evaluation paradigm for video generation, shifting from purely visual/perceptual metrics to **physically grounded geometric evaluation**. This is analogous to how depth estimation moved from pixel-level metrics to geometric consistency measures.

**Field Impact:**
- Raises the bar for what "high-quality" video generation means
- Reveals that current models have fundamental geometric understanding limitations
- Opens new research directions (3D-aware video diffusion, geometry-guided generation)

### Architectural Implications

The consistent failures across models suggest:
1. **2D Generative Priors Are Insufficient:** Models trained purely on image data lack 3D geometric understanding
2. **Need for 3D Constraints:** Future architectures should incorporate 3D consistency losses or 3D-aware conditioning
3. **Multi-View Consistency:** Training with multi-view consistency objectives may help

### Limitations and Challenges

1. **Reconstruction Dependency:** Evaluation depends on SfM/MVS quality; poor reconstruction could mask good generation
2. **Metric Interpretability:** Not all geometric inconsistencies are equally visible to humans
3. **Computation Cost:** 3D reconstruction is expensive (minutes per video)
4. **Reference Ambiguity:** For some prompts, multiple valid 3D interpretations exist

### Open Questions

1. How to balance geometric consistency with visual quality in generation?
2. Can geometric metrics guide generation without explicit 3D supervision?
3. Which geometric failures are actually perceptually noticeable?
4. How to incorporate physics constraints into video generation?

## Code & Resources

**Evaluation Pipeline:**
- Based on COLMAP for SfM
- MVS reconstruction using state-of-the-art methods
- Custom metric computation code (point cloud analysis, mesh geometry)
- Visualization tools for reconstruction debugging

**Benchmark Access:**
- 200+ video generation prompts with geometric annotations
- Evaluation scripts for computing all metrics
- Pre-computed reference reconstructions (if available)

**Quick Start:**
```python
# Pseudo-code for benchmark evaluation
from geot2v_bench import benchmark

prompts = load_benchmark_prompts()  # 200 prompts
metrics_config = default_metrics_config()

for prompt in prompts:
    video = generate_video(prompt)  # Your model
    results = benchmark.evaluate(video, metrics_config)
    print(f"Epipolar Error: {results['epipolar_error']:.2f}")
    print(f"Self-Intersection Rate: {results['self_intersection_rate']:.1%}")
    print(f"Semantic Consistency: {results['semantic_consistency']:.1%}")
```

**Compute Requirements:**
- Per-video: 5-10 minutes (SfM + MVS + metrics)
- For 200 prompts: ~2-3 hours for baseline evaluation
- Hardware: Single GPU (V100+) sufficient

## Related Work & Context

### Prior Benchmarking Efforts in Video Generation
- **T2V-CompBench:** Compositional consistency (but not 3D geometric)
- **T2VPhysBench:** Physical plausibility (but not geometric reconstruction)
- **LoCoT2V-Bench:** Long-form and complex scenarios
- **GeoT2V-Bench:** First to focus on 3D geometric consistency via reconstruction

### Geometric Consistency in 3D Vision
- **Multi-view geometry:** Epipolar geometry, camera calibration
- **3D Reconstruction:** SfM, MVS, neural radiance fields
- **Consistency metrics:** Used extensively in novel view synthesis, 3D object detection

### Connection to 3D-Aware Generation
- Recent work on NeRF-based generation explores geometric awareness
- Diffusion models with 3D-aware conditioning (e.g., TriplaneGaussian)
- Score matching with geometric constraints

### Future Research Directions

1. **End-to-End 3D Video Generation:**
   - Train models with explicit 3D loss functions
   - Incorporate multi-view consistency from start of generation
   - Use benchmark as supervision signal

2. **Efficient Evaluation:**
   - Develop proxy metrics that approximate 3D consistency without full reconstruction
   - Real-time consistency checking during generation

3. **Human Perception Studies:**
   - Correlate geometric metrics with human perception of quality
   - Identify which geometric failures are visible to humans

4. **Physics-Grounded Generation:**
   - Integrate physics simulation with video generation
   - Train models to understand object interactions

---

**Paper Link:** [arXiv:2606.24829](https://arxiv.org/abs/2606.24829)
