# Ego2Robot: Scalable Robot Data Synthesis from Egocentric Human Data

**Authors:** Ye Wang, Pei Lin, Xiong-Hui Chen, Haoqi Yuan, Zhixuan Liang, Yiyang Huang, Anzhe Chen, Zixing Lei, Jie Zhang, Tao Zhang, Haoyang Li, Tong Zhang, Chenxi Xiao, Ziyuan Jiao, Qin Jin  
**Affiliations:** AIM3 Lab (Renmin University of China), Qwen Team (Alibaba Inc.), ShanghaiTech University, BIGAI, Beijing University of Aeronautics and Astronautics  
**ArXiv ID:** 2608.02580  
**Submitted:** August 2026  
**Category:** Computer Vision, Robotics

## Executive Summary

Ego2Robot presents a breakthrough in scalable robot learning by converting egocentric human manipulation videos into large-scale robot training data. The system bridges the embodiment gap between human hands and robot manipulators through a three-stage pipeline of action retargeting, visual synthesis, and quality curation. Processing approximately 1,940 hours of egocentric video from diverse sources, the pipeline generates **18,561 hours of robot training data spanning 15 robot morphologies**—making it the largest ego-to-robot dataset to date. When jointly trained with real robot data, Ego2Robot-synthesized data improves out-of-distribution generalization by 2-8 percentage points across multiple visual and embodiment variations, with improvements validated through real-robot deployment.

## Problem Statement

Robot learning faces a critical bottleneck: obtaining large-scale, diverse demonstration data for training generalizable manipulation policies. Traditional approaches rely on:

1. **Teleoperation:** Time-consuming, expensive, and limited to single robot embodiments
2. **Simulation:** Domain gap between simulated and real robots limits transferability
3. **Human demonstration annotation:** Difficult to collect at scale while maintaining quality

However, a massive resource remains largely untapped: **billions of hours of egocentric video from human activities**. These videos contain rich scene diversity, task variety, and natural demonstrations of manipulation skills. The challenge is bridging the substantial embodiment gap—human hands have 23 degrees of freedom with articulated fingers, while most robot manipulators use parallel-jaw grippers with 2-3 DOF.

### Prior Work and Limitations

Previous research (EgoDex, EgoEngine) demonstrated that retargeting egocentric videos to robot format can work, but faced critical limitations:
- **Scale:** Limited to small datasets (hundreds of hours)
- **Single embodiments:** Focused on specific robot platforms
- **Manual curation:** High-quality synthesis required extensive human filtering
- **Limited sources:** Leveraged single-source egocentric video datasets

Ego2Robot overcomes these limitations through systematic scaling, multi-source integration, and automated quality curation.

## Core Concepts & Theory

### Embodiment Gap

The fundamental challenge is the mismatch between human and robot morphologies:

**Human Hand Characteristics:**
- 23 degrees of freedom (fingers, wrist, arm)
- Fine tactile sensing and proprioception
- Dexterous manipulation capabilities
- Natural, fluid motion patterns

**Parallel-Jaw Gripper (Standard Robot):**
- 2-3 degrees of freedom (grip, position)
- Limited sensing
- Binary grasp states (open/closed)
- Discrete motion patterns

### Key Insight

Rather than attempting to preserve all human hand articulation, Ego2Robot focuses on extracting **task-relevant motion patterns**:
- Gripper open/close actions map to finger state
- Hand trajectory maps to end-effector position
- Grasp timing transfers to manipulation timing

This pragmatic approach acknowledges that parallel-jaw grippers can't execute dexterous finger work, but can learn the essential manipulation semantics from human video.

## Main Ideas & Contributions

### 1. Scalable Three-Stage Pipeline

**Stage 1: Action Retargeting**
- Maps egocentric hand poses to parallel-jaw gripper actions
- Extracts temporal dynamics of grasping and manipulation
- Preserves task-relevant motion sequences
- Handles multiple embodiment types

**Stage 2: Robot-Arm Visual Synthesis**
- Renders robot arms into egocentric video frames using inpainting and depth-aware compositing
- Adapts visual appearance across 15 robot morphologies
- Maintains scene context and realistic visual integration
- Ensures robots appear naturally within human-scale environments

**Stage 3: Multi-Level Quality Curation**
- Hierarchical filtering at multiple stages
- Validates action retargeting accuracy
- Checks visual alignment and realism
- Removes low-quality or misaligned demonstrations
- Ensures downstream training data quality

### 2. Multi-Morphology Rendering

A key innovation is supporting **15 distinct robot morphologies** from unified source data:
- Different arm lengths and joint configurations
- Various gripper designs
- Diverse visual appearances and color schemes
- Platform-specific characteristics

This multiplicity amplifies the dataset from 1,940 hours of input to 18,561 hours of output—nearly 10x expansion while maintaining quality.

### 3. Diverse Source Integration

Ego2Robot synthesizes data from four egocentric video sources:
- **ANT:** 7 hours of specialized manipulation
- **EgoDex:** 732 hours of large-scale dexterous manipulation
- **ViTRA:** 249 hours of task-relevant video
- **EgoVerse:** 954 hours of global collaborative platform data

This diversity ensures the synthesized dataset captures varied tasks, scenes, and manipulation strategies.

### 4. Systematic Generalization Evaluation

Rather than reporting single performance metrics, the paper introduces **disentangled perturbation analysis**:
- Visual appearance variation (background, lighting, colors)
- Scene layout changes
- Robot embodiment differences
- Task semantic variations

This framework goes beyond standard benchmarking to understand where synthesized data helps most.

## Methodology & Implementation

### Pipeline Architecture

```
Egocentric Videos
    ↓
[Stage 1: Action Retargeting]
    - Hand pose extraction
    - Gripper action inference
    - Trajectory mapping
    ↓
[Stage 2: Visual Synthesis]
    - Robot arm inpainting
    - Depth-aware compositing
    - Embodiment adaptation
    ↓
[Stage 3: Quality Curation]
    - Automated filtering
    - Alignment validation
    - Consistency checks
    ↓
Robot Training Data (Multiple Morphologies)
```

### Datasets and Experimental Setup

**Input Data:**
- ANT: 7 hours
- EgoDex: 732 hours
- ViTRA: 249 hours
- EgoVerse: 954 hours
- **Total:** 1,940 hours of egocentric video

**Output Data:**
- 18,561 hours of robot-format training data
- 15 robot morphologies
- Expansion ratio: ~9.5x

**Primary Benchmark:** RoboTwin2.0 (extended with disentangled perturbations)

**Robot Platforms:** Validation across 15 distinct morphologies

**Evaluation Conditions:**
- Clean conditions (original rendering)
- Randomized conditions (all perturbations applied)

### Training Protocol

- Joint pretraining on Ego2Robot-synthesized and robot-collected data
- 1:1 mixing ratio (equal amounts of egocentric and real robot data)
- Out-of-distribution generalization assessment
- Real-robot deployment validation

## Results, Comparisons & Statistical Analysis

### Primary Performance Results

**Quantitative Metrics (on RoboTwin2.0):**

| Condition | Performance |
|-----------|------------|
| Robot data only | 50.9% (Clean), 51.0% (Randomized) |
| + Ego2Robot 1:1 | 68.1% (Clean), 53.5% (Randomized) |
| **Improvement** | **+17.2% (Clean), +2.5% (Randomized)** |

### Generalization Improvements by Perturbation Type

When using 1:1 mixing of Ego2Robot + real robot data:

| Perturbation Type | Improvement |
|------------------|------------|
| Background variation | +4 percentage points |
| Lighting conditions | +8 percentage points |
| Robot color/embodiment | +6 percentage points |
| Composite (all perturbations) | +2.5 percentage points |

### Key Insight

The results demonstrate that Ego2Robot provides **targeted improvements where out-of-distribution robustness matters most**:
- Lighting and appearance changes are particularly well-handled
- Embodiment variation benefits substantially (+6%)
- Real-robot deployment shows consistent improvements across tested platforms

### Comparison with Other Robot Learning Methods

**Advantages of Ego2Robot:**

1. **Scale:** 18,561 hours (largest ego-to-robot dataset vs. prior work limited to ~100-500 hours)
2. **Multi-morphology:** Covers 15 platforms vs. single-embodiment prior approaches
3. **Source diversity:** 4 integrated datasets vs. single-source prior work
4. **Dual-mode support:** Handles both curated and in-the-wild videos
5. **Validated generalization:** Systematic perturbation evaluation vs. point metrics
6. **Real-world validation:** Results confirmed through actual robot deployment

**Positioning:** Ego2Robot represents both quantitative (10x data) and qualitative (systematic evaluation) advances over prior ego-to-robot approaches.

## Practical Applications & Use Cases

### Foundation Model Pretraining
- Large-scale pretraining for vision-language-action (VLA) models
- Improved transfer to downstream robot tasks
- Cross-platform capability learning

### Core Manipulation Tasks
- Picking tasks with improved success rates
- Pushing and sliding operations
- Object manipulation with varied scenes and lighting

### Multi-Platform Robotics
- Single unified training benefits multiple robot embodiments
- Reduces platform-specific data collection requirements
- Enables generalization across hardware variants

### Out-of-Distribution Robustness
- Robots maintain performance under visual variation
- Lighting changes don't degrade grasp success
- Scene background shifts handled gracefully

### Scalable Data Collection Alternative
- Reduces dependency on expensive robot teleoperation
- Leverages existing human video repositories
- Democratizes robot learning data creation

## Insights & Implications

### For Robotics Research

1. **Human Videos as Training Data:** Demonstrates the viability of human demonstration video as a data source for robot learning (with appropriate engineering)

2. **Embodiment Transfer:** Shows that meaningful skill transfer is possible despite substantial morphological differences

3. **Practical Scaling:** Proves that large-scale (18,561 hours) synthesized data can contribute meaningful improvements to robot policies

4. **Multi-Morphology Learning:** A single dataset supporting 15 platforms indicates generalized capability learning

### Broader Impact

1. **Democratization:** Makes large-scale robot training data accessible without proprietary teleoperation systems
2. **Scalability Path:** Suggests how to scale robot learning beyond proprietary data collection
3. **Human-Robot Collaboration:** Validates using human demonstrations for robot learning even with embodiment gaps

### Limitations and Open Challenges

#### Current Limitations

1. **Gripper Scope:** Maps only to parallel-jaw grippers, discarding dexterous finger articulation
   - Future: Multi-finger hand support could enable richer manipulation skills

2. **Visual Rendering Fidelity:** Inpainting and compositing may introduce artifacts under heavy occlusion or complex lighting
   - Future: Generative models could reduce visual domain gap

3. **Embodiment Gap Remains:** Despite multi-morphology support, fundamental differences between human and robot embodiments persist
   - Ongoing: Better embodiment transfer mechanisms needed

4. **Evaluation Scope:** Assessment limited to RoboTwin2.0 benchmark
   - Future: Broader task evaluation needed to strengthen generality claims

5. **Data Quality Dependency:** Quality of synthesized data depends on input egocentric video quality
   - Challenge: In-the-wild video variability affects reproducibility

#### Future Research Directions

1. **Dexterous Manipulation:** Extending pipeline to multi-finger hands for fine-grained skills
2. **Broader Tasks:** Validation beyond manipulation to includes locomotion and other robot capabilities
3. **Real-to-Sim Dynamics:** Incorporating dynamics models for improved sim-to-real transfer
4. **Compositional Learning:** Whether skills learned separately transfer to novel task combinations
5. **Active Learning:** Selective synthetic data generation targeting weak robot performance areas

## Code & Resources

**Project Resources:**
- **Official Blog:** https://www-ye.github.io/ego2robot_blog/
- **arXiv Paper:** https://arxiv.org/abs/2608.02580
- **HTML Version:** https://arxiv.org/html/2608.02580

**Code Availability:** [Exact code release status unavailable — check project blog and arXiv page for latest resources]

**Dataset Access:** 18,561 hours of synthesized robot data availability details to be confirmed on project page

## Related Work & Context

### Egocentric Vision Research
- **EgoVerse:** 1,362 hours of egocentric video from collaborative platform
- **EgoLive:** Large-scale annotated egocentric data from real-world tasks
- **EgoDex:** Prior work on dexterous manipulation from egocentric video

### Robot Learning Paradigms
- **Imitation Learning:** Learning from demonstrations (scaled by Ego2Robot)
- **Teleoperated Learning:** Traditional robot data collection approach
- **Sim-to-Real Transfer:** Alternative scaling approach (complementary to Ego2Robot)

### Foundation Models in Robotics
- **VLA Models:** Vision-language-action models that could leverage Ego2Robot pretraining
- **Cross-embodiment Generalization:** Related challenges in multi-robot learning

### Future Directions

1. **Vision-Language-Action Models:** Pre-training on Ego2Robot data for improved downstream performance
2. **Embodiment-Agnostic Skills:** Learning representations that transfer across morphologies
3. **In-the-Wild Video Processing:** Improving quality curation for less-controlled egocentric videos
4. **Cross-Task Generalization:** Whether tasks learned separately combine into novel behaviors

---

**Research Significance:** Ego2Robot makes a critical contribution to scaling robot learning by unlocking the vast resource of egocentric human video. By developing practical solutions to the embodiment gap and demonstrating real improvements on real robots, it points toward a future where robot training data can be generated at scale, accelerating the field's progress toward general-purpose robotic systems.
