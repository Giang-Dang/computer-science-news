# Vision-Language-Action in Robotics: A Survey of Datasets, Benchmarks, and Data Engines

**ArXiv ID:** [2604.23001](https://arxiv.org/abs/2604.23001)  
**Authors:** Ziyao Wang, Bingying Wang, Hanrong Zhang, Tingting Du, Tianyang Chen, Guoheng Sun, Yexiao He, Zheyu Shen, Wanghao Ye, Ang Li  
**Submitted:** April 24, 2026  
**Field:** Robotics / Embodied AI / Vision-Language-Action Models

---

## Executive Summary

Vision-Language-Action (VLA) models have emerged as the dominant paradigm for building generalist robot policies, combining the semantic understanding of vision-language models with the action-generation capabilities needed for physical manipulation and navigation. However, this survey argues that the central bottleneck to further progress is **not model architecture but data infrastructure**: the quality, diversity, and scale of training datasets, the rigor of evaluation benchmarks, and the efficiency of data collection engines. This comprehensive data-centric survey systematically analyzes the VLA ecosystem across three pillars — datasets, benchmarks, and data engines — identifying a persistent fidelity-cost trade-off and calling for co-design of data systems and model architectures as the primary path forward.

---

## Problem Statement

### The Data Bottleneck in Embodied AI

VLA models like RT-2, OpenVLA, π0, and Octo have demonstrated impressive zero-shot generalization across manipulation tasks when pre-trained on diverse robotic datasets. Yet progress has stalled in several dimensions:
- Models generalize well across *seen* environments but fail catastrophically on *novel* objects or task structures
- Sim-to-real transfer remains brittle despite improved simulation fidelity
- Data collection for real-robot training is prohibitively expensive (~$10–50 per demonstration)

The prevailing assumption has been that these failures reflect model architecture limitations. This survey challenges that assumption, arguing that **the training data distribution, not the model, is the primary constraint**. Specifically:
- Real-world datasets are narrow in embodiment diversity (mostly parallel-jaw grippers on tabletop tasks)
- Synthetic datasets have a fidelity gap (physics, lighting, material properties)
- Benchmarks inadequately test generalization (in-distribution evaluation dominates)
- Data engines (the pipelines that generate training data) are ad-hoc and do not scale

### The Co-Design Gap

Model architectures and data pipelines have evolved largely independently. A 7B-parameter VLA trained on 50 hours of robot demonstrations may underperform a 1B model trained on a carefully curated 500-hour dataset. The community lacks a systematic framework for deciding:
- What data to collect for a given task distribution?
- How much real vs. synthetic data is needed?
- Which benchmark best predicts real-world deployment performance?
- How to efficiently scale data collection using automation?

This survey provides that framework.

---

## Core Concepts & Theory

### The VLA Architecture

A Vision-Language-Action model $\pi_\theta$ maps an observation $o_t$ (RGB image, depth, proprioception) and a language instruction $l$ to an action $a_t$:

$$a_t = \pi_\theta(o_t, o_{t-1}, \ldots, o_{t-H}, l)$$

where $H$ is the observation history horizon. Modern VLAs are built on pretrained VLMs (typically LLaMA or Qwen backbone with CLIP/SigLIP vision encoder) and fine-tuned to output robot actions:
- **Discrete action tokenization:** Actions discretized into bins, predicted as next tokens (RT-2, OpenVLA)
- **Continuous flow matching:** Actions predicted as continuous distributions via diffusion or flow matching heads (π0, Octo with diffusion head)
- **Hybrid:** Discrete high-level decisions + continuous low-level control (Hierarchical VLA approaches)

### The Data-Model Scaling Framework

The survey adapts the standard neural scaling law framework to VLA:

$$\text{Task Success Rate} \propto N_\text{model}^{\alpha} \cdot D_\text{data}^{\beta} \cdot Q_\text{quality}^{\gamma}$$

where:
- $N_\text{model}$: model parameter count
- $D_\text{data}$: training data scale (hours of demonstration)
- $Q_\text{quality}$: a composite data quality metric
- $\alpha, \beta, \gamma$: scaling exponents

Empirically, the survey finds $\beta \approx 0.4$ and $\gamma \approx 0.7$, suggesting that **data quality has a larger return than raw data quantity** — a finding with profound implications for data engine design.

### Fidelity-Cost Trade-Off in Data Sources

| Data Source | Visual Fidelity | Physics Fidelity | Diversity | Cost |
|------------|-----------------|------------------|-----------|------|
| Real robot demos | High | Perfect | Low | $10–50/demo |
| Human video (in-the-wild) | High | Irrelevant | Very high | Near zero |
| Synthetic (IsaacSim/MuJoCo) | Medium | High | Medium | Low |
| Neural rendering synthetic | High | Medium | Medium | Low |
| Teleoperation in simulation | Medium | High | Medium | $1–5/demo |

The fidelity-cost trade-off is the central tension in VLA data design. The survey documents how different training regimes resolve (or fail to resolve) this tension.

### Task Representation and Action Space Formulation

The survey identifies four distinct action space formulations used across the literature:

**1. End-effector Cartesian control:** $a = (\Delta x, \Delta y, \Delta z, \Delta \text{roll}, \Delta \text{pitch}, \Delta \text{yaw}, \text{gripper})$ — most common, 7-DoF

**2. Joint-space control:** $a = (\Delta q_1, \ldots, \Delta q_n)$ — more precise, harder to generalize across robots

**3. Keypoint/waypoint control:** $a = (p_1, \ldots, p_K)$ — high-level target positions, requires low-level tracker

**4. Language action tokens:** $a = \text{token}_1, \ldots, \text{token}_m$ — most transferable across embodiments, lowest fidelity for precision tasks

The choice of action space fundamentally determines what data is useful, what benchmarks are valid, and how models generalize.

---

## Main Ideas & Key Contributions

### 1. Data-Centric VLA Taxonomy

The survey's primary contribution is a **systematic taxonomy of VLA data** along three dimensions:

**Embodiment diversity axis:**
- Single-arm (dominant), dual-arm (emerging), mobile manipulation (nascent), humanoid (very early)
- Survey finding: 78% of all VLA training data is single-arm tabletop manipulation

**Modality composition axis:**
- RGB only (most common), RGB-D, RGB + proprioception, multi-camera, tactile (rare)
- Survey finding: multimodal (RGB-D + proprioception) models improve task success by 12–18pp but adoption is low due to data collection complexity

**Action space axis:**
- As described above; mixing action spaces across datasets degrades performance without explicit normalization

### 2. Benchmark Analysis: What Evaluations Actually Measure

The survey's second major contribution is a critical evaluation of existing VLA benchmarks, finding that most **do not test what they claim to test**:

- **LIBERO:** Tests in-distribution generalization (train and test objects overlap); mislabeled as zero-shot evaluation
- **RoboSuite:** Covers only 6 object categories; insufficient for generalization claims
- **MetaWorld:** Physics-unrealistic (perfect segmentation masks provided); not predictive of real-robot performance
- **SIMPLER:** Closest to realistic evaluation, but limited to tabletop pick-and-place

**Proposed Evaluation Taxonomy (3-level hierarchy):**
1. **L1 — In-distribution:** Same objects, same backgrounds, same task structure (measures fitting)
2. **L2 — Compositional generalization:** Novel object-task combinations from seen categories (measures composition)
3. **L3 — Out-of-distribution:** Novel objects, backgrounds, and task structures (measures true generalization)

The survey finds that most published results are L1, a small minority are L2, and almost none are L3 — creating an overly optimistic picture of VLA progress.

### 3. Data Engine Classification

**Type 1 — Human teleoperation:** A human operator controls the robot in the real world via teleoperation interface (joystick, VR headset, kinesthetic teaching). Highest quality, lowest scalability.

**Type 2 — Human video imitation:** Extract robot-relevant actions from human activity videos. High diversity, sim-to-real gap for fine manipulation.

**Type 3 — Automated trajectory generation in simulation:** Planning + motion primitives generate training trajectories programmatically. High scalability, physics fidelity depends on simulator.

**Type 4 — LLM/VLM-guided data generation:** Use a VLM to generate language instructions, a planner to generate trajectories, and a renderer to produce observations. Emerging, promising for instruction diversity.

**Type 5 — Self-improving data engines:** Robot attempts tasks, success/failure annotations are used to improve the data engine and the policy jointly. Most promising, least mature.

### 4. The Cross-Embodiment Transfer Analysis

The survey systematically analyzes **cross-embodiment transfer** — training on data from one robot type and deploying on another:
- Cartesian action space transfers significantly better than joint-space (expected)
- Visual policy features transfer well (CLIP-pretrained backbones); action-specific features do not
- A 10× data scale from a different embodiment contributes ~4× less than same-embodiment data

---

## Methodology & Implementation

### Survey Scope

- **Datasets surveyed:** 47 robotic manipulation + 12 navigation + 8 humanoid datasets
- **Benchmarks surveyed:** 23 simulation benchmarks + 4 real-robot evaluation frameworks
- **Data engines surveyed:** 19 distinct data collection pipelines
- **Time range:** 2019–2026 (focus on post-2022 neural VLA era)

### Dataset Statistics

| Dataset | Size | Embodiments | Action Space | Real/Sim |
|---------|------|-------------|--------------|---------|
| Open X-Embodiment | 1M eps | 22 | Mixed | Real |
| RH20T | 110K eps | 1 | Cartesian | Real |
| DROID | 76K eps | 1 | Cartesian | Real |
| BridgeData V2 | 60K eps | 1 | Cartesian | Real |
| FurnitureBench | 30K eps | 1 | Cartesian | Real |
| GR1-Training | 50K eps | 1 | Whole-body | Real |
| ManipGen | 1M eps | 3 | Cartesian | Sim |
| RoboCasa | 100K eps | 1 | Cartesian | Sim |

### Key Analysis: What Data Matters Most

The survey conducts a comprehensive meta-analysis of ablation studies across 35 papers:

| Data factor | Impact on task success (average) |
|-------------|----------------------------------|
| Embodiment diversity | +12pp for new embodiment generalization |
| Scene diversity | +8pp for novel background generalization |
| Object diversity | +15pp for novel object generalization |
| Task instruction variety | +6pp for novel language instruction generalization |
| Data scale (10× more) | +9pp average, saturating at ~100K demos |

---

## Practical Applications & Real-World Use Cases

### 1. Manufacturing and Warehouse Automation

Industrial robotic arms need to handle an ever-expanding catalog of objects (new SKUs, packaging changes). VLAs pre-trained on diverse manipulation data can adapt to new objects with few or zero demonstrations. The survey's analysis of object diversity data shows this is achievable with proper data engine design.

**Current gap:** Existing datasets have limited industrial object diversity (mostly household items). Data engines based on Type 4 (LLM-guided synthesis) are the most promising path for industrial catalog coverage.

### 2. Home Assistance Robots

Household robots (ALOHA, Figure, Unitree) must perform unstructured tasks in diverse home environments. The survey shows that the **scene diversity** axis is most critical for home deployment.

**Practical guidance:** For home robot development, prioritize collecting data across many different room layouts and lighting conditions, even at the cost of fewer demonstrations per task.

### 3. Surgical Robotics

Surgical robots require extreme precision and cannot tolerate failure modes. The survey's analysis of **L3 evaluation frameworks** (true out-of-distribution testing) is critical here — developers must ensure their evaluation framework correctly identifies failure modes rather than reporting misleadingly optimistic in-distribution results.

### 4. Agricultural Robotics

Harvesting, pruning, and inspection robots operate outdoors with uncontrolled lighting, weather, and plant variation. The survey's analysis of cross-domain transfer suggests that human video (agricultural workers performing tasks) may be the most cost-effective data source for agricultural VLA training.

---

## Insights & Implications

### Data Infrastructure as the Primary Research Frontier

The survey's central argument will likely shift research priorities toward data-centric AI for robotics:
- More investment in scalable simulation with neural rendering
- Development of standardized data collection protocols
- Creation of L2/L3 evaluation benchmarks that test true generalization
- Research into Type 5 (self-improving) data engines

### The Benchmark Quality Crisis

The finding that most VLA benchmarks measure in-distribution performance (L1) while claiming to measure generalization (L2/L3) is a significant scientific problem. The community needs to adopt the paper's 3-level evaluation hierarchy as a standard.

### Sim-to-Real in the Neural Rendering Era

Neural rendering (NeRF, 3DGS) is rapidly closing the visual fidelity gap between simulation and real world. The survey argues this will unlock Type 3 and Type 4 data engines as practical options, potentially reducing the need for expensive real-robot teleoperation by 10×.

### Limitations

1. **Coverage bias:** English-language papers dominate; Chinese robotics research may be underrepresented
2. **Proprietary data:** Major lab datasets (Google, Amazon, Tesla) are not public and not surveyed
3. **Evaluation breadth:** Real-robot evaluation results are sparse and hard to compare
4. **Humanoid gap:** Humanoid VLA research is nascent; the survey acknowledges this section is incomplete

### Open Questions

- What is the minimum data diversity needed for robust real-world deployment?
- Can Type 5 (self-improving) data engines generate sufficient data quality without human intervention?
- How do VLA scaling laws differ from pure language model scaling laws?
- Can foundation models for action (trained on cross-embodiment data) achieve zero-shot performance on any new robot?

---

## Code & Resources

- **ArXiv Paper:** [https://arxiv.org/abs/2604.23001](https://arxiv.org/abs/2604.23001)
- **HTML Full Text:** [https://arxiv.org/html/2604.23001](https://arxiv.org/html/2604.23001)

### Key Referenced Datasets and Tools

| Resource | Link |
|----------|------|
| Open X-Embodiment | [https://robotics-transformer-x.github.io](https://robotics-transformer-x.github.io) |
| DROID Dataset | [https://droid-dataset.github.io](https://droid-dataset.github.io) |
| OpenVLA | [https://github.com/openvla/openvla](https://github.com/openvla/openvla) |
| SIMPLER Benchmark | [https://github.com/simpler-env/SimplerEnv](https://github.com/simpler-env/SimplerEnv) |
| LeRobot (HuggingFace) | [https://github.com/huggingface/lerobot](https://github.com/huggingface/lerobot) |
| RoboSuite | [https://robosuite.ai](https://robosuite.ai) |

### Getting Started with VLA Research

```python
# OpenVLA — the most accessible open VLA implementation
pip install openvla

from openvla.model import OpenVLAForActionPrediction
model = OpenVLAForActionPrediction.from_pretrained("openvla/openvla-7b")

# Predict action from image + instruction
import torch
from PIL import Image
image = Image.open("robot_scene.jpg")
instruction = "Pick up the red cup and place it on the plate"
action = model.predict_action(image, instruction, unnorm_key="bridge_orig")
```

---

## Related Work & Context

### Key VLA Models Referenced

| Model | Architecture | Key Data | Year |
|-------|-------------|----------|------|
| RT-2 | PaLI-X + RT | RT-1 dataset | 2023 |
| OpenVLA | LLaMA-2 7B + DINO | Open X | 2024 |
| π0 | PaliGemma + flow matching | DROID + proprietary | 2024 |
| Octo | Transformer + diffusion | Open X | 2024 |
| GR1 | Humanoid-specific VLA | GR1-Training | 2025 |

### Concurrent Surveys

- **Pure VLA Models Survey (2509.19012):** Focuses on architecture; complementary to this data-centric survey
- **Action Tokenization Survey (2507.01925):** Deep dive on action representation; aligns with this survey's action space taxonomy

### Where This Leads

1. **Standardized evaluation:** Adoption of the L1/L2/L3 benchmark hierarchy by major evaluation platforms
2. **Cross-embodiment foundation models:** Training on 100+ embodiment types to build truly generalizable robot policies
3. **Neural rendering data engines:** High-fidelity synthetic data generation that removes the sim-to-real gap
4. **Self-improving robot systems:** Robots that autonomously collect and label their own training data, creating a virtuous cycle of improvement
