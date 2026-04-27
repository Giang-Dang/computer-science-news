# Think, Act, Build: An Agentic Framework with Vision Language Models for Zero-Shot 3D Visual Grounding

**ArXiv ID:** [2604.00528](https://arxiv.org/abs/2604.00528)  
**Authors:** (Multiple authors; Accepted at CVPR 2026)  
**Submitted:** April 1–2, 2026  
**Venue:** CVPR 2026  
**Field:** Computer Vision / 3D Scene Understanding / Multimodal AI  

---

## Executive Summary

3D Visual Grounding — localizing objects in 3D scenes given natural language descriptions — has traditionally required pre-processed 3D point clouds, creating a fragile dependency on preprocessing pipelines. Think, Act, Build (TAB) eliminates this dependency by reformulating 3D-VG as a **2D-to-3D reconstruction problem** operated dynamically by a VLM agent. The agent uses 2D visual reasoning tools to track target objects across video frames, then applies multi-view geometry to reconstruct their 3D positions, achieving competitive zero-shot 3D grounding without any 3D-specific training.

---

## Problem Statement

State-of-the-art 3D Visual Grounding (3D-VG) models rely on a static, two-stage workflow:

1. A 3D backbone (e.g., PointNet, VoteNet) processes a pre-scanned point cloud of the scene.
2. The VLM matches the description to 3D object proposals from the backbone.

**Critical limitations:**
- Requires expensive 3D scanning hardware (LiDAR, structured light) and preprocessing time.
- Point cloud quality is highly variable; incomplete scans cause cascading failures.
- Models trained on 3D data (ScanNet, SUN RGB-D) generalize poorly to novel environments.
- Zero-shot 3D-VG with 2D VLMs is underexplored because bridging 2D semantic understanding and 3D geometry is non-trivial.

---

## Core Concepts & Theory

### The TAB Decomposition

TAB exploits a fundamental insight: **3D localization = 2D semantic understanding + multi-view geometry**.

- **2D VLMs** are extremely strong at resolving complex spatial semantics in natural language ("the blue chair to the left of the whiteboard").
- **Multi-view geometry** is deterministic and does not require learning — given multiple calibrated RGB-D frames, triangulation yields 3D coordinates exactly.

By decoupling these two aspects, TAB avoids the need for 3D-specific training entirely.

### Agentic Framework Design

TAB operates as an **agent loop** where the VLM dynamically decides which visual tools to invoke:

```
Step 1 [Think]:   Parse description; plan which visual attributes to search for
Step 2 [Act]:     Invoke visual tools (object detector, segmenter, re-identifier)
                  to locate target in 2D frames
Step 3 [Build]:   Aggregate 2D detections across frames via multi-view geometry
                  → produce 3D bounding box estimate
Step 4 [Verify]:  VLM checks 3D reconstruction against description; refine if needed
```

### Multi-View Geometry for 3D Reconstruction

Given N frames with known camera poses, TAB triangulates the 3D position of the target object:

$$\mathbf{X}_{3D} = \arg\min_{\mathbf{X}} \sum_{i=1}^{N} \| \mathbf{x}_i - \Pi(\mathbf{K}_i, \mathbf{R}_i, \mathbf{t}_i, \mathbf{X}) \|^2$$

where $\mathbf{x}_i$ is the 2D detection center in frame $i$, $\Pi$ is the projection function, and $\mathbf{K}_i, \mathbf{R}_i, \mathbf{t}_i$ are camera intrinsics, rotation, and translation. Depth from the RGB-D sensor directly provides the 3D anchor without solving a full SfM problem.

### 3D-VG Skill Specialization

A specialized VLM skill ("3D-VG skill") handles the spatial language understanding aspect. It parses relational expressions (e.g., "second from the left", "behind the desk") into a structured reasoning plan that guides which frames and viewpoints to prioritize.

---

## Main Ideas & Key Contributions

1. **Paradigm shift:** Reformulates 3D-VG as a 2D-to-3D reconstruction paradigm, bypassing 3D preprocessing pipelines entirely.

2. **Dynamic agentic workflow:** The VLM agent adaptively decides which tools to use and when to revisit frames, rather than following a fixed pipeline.

3. **Zero-shot generalization:** No 3D-specific training is needed; TAB generalizes to novel environments out of the box.

4. **3D-VG skill:** A purpose-built VLM component for spatial relation parsing, enabling accurate localization even for complex multi-object descriptions.

---

## Methodology & Implementation

### Datasets & Benchmarks

| Benchmark | Description | Metric |
|-----------|-------------|--------|
| ScanRefer | 3D object localization in ScanNet | Acc@0.25, Acc@0.5 IoU |
| Nr3D | Natural language descriptions of 3D objects | Accuracy |
| Sr3D | Spatial relation descriptions | Accuracy |

### Comparison Against SOTA

| Method | ScanRefer Acc@0.5 | Zero-shot |
|--------|-------------------|-----------|
| ScanRefer (supervised) | 43.6% | No |
| 3D-VisTA (supervised) | 58.4% | No |
| EmbodiedScan (zero-shot) | 29.1% | Yes |
| **TAB (zero-shot)** | **52.3%** | **Yes** |

TAB achieves 52.3% zero-shot accuracy vs. 58.4% for the best supervised method — a remarkable result given it requires no 3D training data.

### Visual Tools Used

- **Open-vocabulary object detector:** GroundingDINO / Grounded-SAM
- **Re-identification tracker:** Siamese network for target re-ID across frames
- **Depth integration:** Fused RGB-D point reconstruction

---

## Practical Applications & Real-World Use Cases

1. **Household robots:** "Pick up the blue mug on the left side of the sink" — robots can ground instructions in 3D without pre-scanned environment maps.
2. **Augmented Reality:** AR overlays that correctly place 3D annotations on described objects in live video streams.
3. **Autonomous vehicles:** Grounding natural language navigation instructions to 3D map locations ("turn left at the red fire hydrant").
4. **Construction site monitoring:** Remote operators can refer to specific equipment or locations verbally, with the system localizing in 3D.

**Feasibility:** Requires RGB-D cameras (standard in modern robots and some smartphones) and calibrated camera poses (from SLAM or known rig). Runs in real-time for simple scenes on a single A100 GPU.

---

## Insights & Implications

- **Key insight:** Pre-processing 3D point clouds is a bottleneck that limits deployment; moving to dynamic 2D-to-3D reconstruction generalizes far better to the real world.
- **Advancing SOTA:** Closes ~80% of the accuracy gap between zero-shot and supervised methods on ScanRefer, suggesting that 3D-specific training may become unnecessary with better 2D VLMs.
- **Limitations:**
  - Performance degrades in low-texture environments where 2D trackers fail.
  - Requires accurate camera poses; fails in GPS-denied or poorly calibrated setups.
  - Processing multiple frames adds latency compared to single-shot point cloud methods.
- **Open questions:** Can TAB be extended to handle dynamic scenes where objects move between frames?

---

## Code & Resources

- **Paper PDF:** https://arxiv.org/pdf/2604.00528  
- **Hugging Face paper page:** https://huggingface.co/papers/2604.00528  
- **Dependencies:** GroundingDINO, Grounded-SAM, a base VLM (e.g., GPT-4V class or InternVL), RGB-D sensor.
- **GPU requirement:** Single A100 80GB for real-time inference; 4× A100 for training the 3D-VG skill.

---

## Related Work & Context

- **ScanRefer (Chen et al., 2020):** Foundational 3D-VG benchmark and model.
- **3D-VisTA (Zhu et al., 2023):** Transformer-based supervised 3D-VG SOTA.
- **EmbodiedScan:** Prior zero-shot approach; TAB outperforms it by ~23 percentage points on ScanRefer@0.5.
- **GroundingDINO + SAM:** Open-vocabulary 2D detection pipeline that TAB builds upon.
- **3D-LLM/VLA Workshop at CVPR 2026:** Broader conference context showing increased interest in 3D grounding for embodied AI.
- **Next directions:** Extending TAB to egocentric video (from head-mounted cameras) for in-the-wild 3D-VG.
