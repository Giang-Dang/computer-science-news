# MultiWorld: Scalable Multi-Agent Multi-View Video World Models

**ArXiv ID:** [2604.18564](https://arxiv.org/abs/2604.18564)  
**Published:** April 20, 2026  
**Authors:** Haoyu Wu, Jiwen Yu, Yingtian Zou, Xihui Liu  
**Institutions:** The University of Hong Kong, Sreal AI  
**Field:** Computer Vision / Generative Models / Robotics  
**Code:** [https://github.com/CIntellifusion/MultiWorld](https://github.com/CIntellifusion/MultiWorld)

---

## Executive Summary

MultiWorld is a unified framework for video world models that scales to *multiple* interacting agents observed from *multiple* views simultaneously. Prior world models handle single agents with single cameras; MultiWorld introduces the Multi-Agent Condition Module for precise per-agent control and the Global State Encoder for cross-view coherence, enabling scalable generation of multi-agent video consistent across viewpoints. Experiments on multi-player game environments and multi-robot manipulation tasks demonstrate that MultiWorld outperforms baselines in video fidelity, action-following accuracy, and multi-view consistency.

---

## Problem Statement

Video world models—action-conditioned video generators that simulate how a scene evolves in response to agent actions—have become foundational tools for model-based reinforcement learning, simulation-based training, and data augmentation in robotics and autonomous driving.

However, all major world models (Genie, DIAMOND, UniSim, etc.) share a critical limitation: **they model a single agent in a single-camera view**. Real-world environments are fundamentally multi-agent and multi-camera:
- Autonomous driving involves multiple vehicles, cyclists, and pedestrians observed by multiple onboard cameras
- Robot manipulation in collaborative settings involves multiple robots
- Multi-player games have multiple characters each with agency
- Surveillance and sports analytics require consistent modeling across a camera array

Extending world models to these settings introduces two new challenges:
1. **Multi-agent control**: How to precisely condition the generator on the actions of multiple agents independently?
2. **Multi-view consistency**: How to ensure that a scene generated from camera A is geometrically consistent with the same scene generated from camera B?

---

## Core Concepts & Theory

### Video World Models: Foundations

A video world model learns a conditional distribution:

```
p(f_{t+1}, ..., f_{t+T} | f_1, ..., f_t, a_1, ..., a_t)
```

Where:
- `f_i` = video frames
- `a_i` = agent actions

Training is typically done on paired (video, action) data, and the model learns to generate future video frames that are consistent with the action history.

### Action-Conditioned Diffusion

MultiWorld uses a video diffusion backbone. Given:
- Historical frames and actions as conditioning context
- The target generation window `[t+1, ..., t+T]`

The diffusion model denoises a noise sample conditioned on this context, guided by the learned world dynamics. Standard score-matching or DDPM training is used.

### Multi-Agent Condition Module

The key challenge with multiple agents is that each agent's action must independently control the corresponding agent's behavior in the generated video without affecting other agents. Naive action conditioning (concatenating all agent actions into a single vector) leads to entanglement: one agent's action influences another agent's behavior.

The **Multi-Agent Condition Module (MACM)** addresses this by:
1. Encoding each agent's action separately with agent-specific embeddings
2. Using **cross-attention** between each agent's action embedding and its spatial region in the video frame (using bounding box coordinates to localize each agent)
3. Aggregating agent-specific attention outputs into the overall conditioning signal

Formally, for agent `i` with action `a_i` and bounding box `b_i`:
```
c_i = CrossAttend(Embed(a_i), SpatialMask(video_tokens, b_i))
C = Aggregate(c_1, ..., c_N)
```

This ensures each agent's action modulates only the corresponding spatial region, preventing cross-agent interference.

### Global State Encoder

Ensuring multi-view consistency requires a shared representation of the underlying 3D scene. The **Global State Encoder (GSE)** maintains a global scene representation that is shared across all camera views:

1. Encode each view's frame into a partial scene representation
2. Aggregate partial representations into a **global state** using a shared scene encoder
3. Condition each view's generation on the global state

This creates a consistency constraint: all views must be explainable by the same global 3D scene, preventing the model from generating inconsistent views of the same environment.

---

## Main Ideas & Key Contributions

### 1. First Scalable Multi-Agent, Multi-View World Model

MultiWorld is the first framework that jointly addresses (a) multi-agent action conditioning and (b) multi-view consistency in a single model, and demonstrates scalability to varying numbers of agents and cameras.

### 2. Multi-Agent Condition Module (MACM)

Spatially-grounded, agent-specific action conditioning via cross-attention with spatial masking. This enables precise control of individual agents while maintaining their independence.

### 3. Global State Encoder (GSE)

A shared scene representation that synchronizes video generation across multiple camera views, ensuring geometric and semantic consistency.

### 4. Parallel Multi-View Generation

MultiWorld generates all views in parallel (rather than sequentially), enabling efficient inference that scales with the number of cameras. Generation time is essentially constant as camera count increases.

### 5. Flexible Scaling

The framework supports arbitrary numbers of agents and views at test time, even if the training distribution had different counts—demonstrating compositional generalization.

---

## Methodology & Implementation

### Architecture Overview

```
Input:
  - Historical frames (N views × T_history frames)
  - Agent actions (M agents × action dimensions)
  - Agent bounding boxes (M agents × 4 coordinates)

Processing:
  1. Per-agent action encoding (MACM)
  2. Cross-view feature extraction (Global State Encoder)
  3. Global state aggregation
  4. Parallel video generation (diffusion, conditioned on global state + agent conditions)

Output:
  - Future frames (N views × T_future frames)
```

### Datasets

| Dataset | Type | Agents | Views | Notes |
|---------|------|--------|-------|-------|
| Multi-player game environment | Synthetic | 2-4 | 4-8 | Custom simulator |
| Multi-robot manipulation | Robot | 2-3 | 3-4 | Real robot data |

### Evaluation Metrics

| Metric | Measures |
|--------|----------|
| FVD (Frechet Video Distance) | Video quality/realism |
| PSNR / SSIM | Frame-level fidelity |
| Action Following Accuracy | Does agent behavior match the specified actions? |
| Multi-View Consistency Score | Geometric consistency across views |

### Results

MultiWorld outperforms baselines (single-agent models extended naively to multi-agent, and prior multi-agent video generation methods) on all four metrics, with especially large improvements on the multi-view consistency score.

---

## Practical Applications & Real-World Use Cases

### 1. Autonomous Driving Simulation

Autonomous driving datasets require generating realistic driving scenarios with multiple vehicles and pedestrians, observed by multiple onboard cameras. MultiWorld could:
- Generate synthetic training data for edge cases (near-misses, unusual maneuvers)
- Enable imagination-based planning for autonomous vehicles
- Create consistent multi-camera data from sparse sensor inputs

### 2. Multi-Robot Collaboration

Training multi-robot systems in simulation before deploying in the real world (sim-to-real transfer) requires a world model that accurately simulates multiple robots interacting. MultiWorld provides the missing ingredient: multi-agent, multi-view consistency for robotic simulation.

### 3. Game Development and Testing

Game developers can use MultiWorld to:
- Generate new game content automatically
- Test game AI agents against diverse opponents
- Create multi-perspective replays and highlights

### 4. Sports Analytics

Sports analytics platforms that track multiple players across multiple cameras could use MultiWorld-style models to:
- Simulate counterfactual plays ("what if the goalkeeper had dived left?")
- Generate training data for player tracking models
- Create synthetic replay footage

---

## Insights & Implications

### The Multi-Agent World Model Gap

MultiWorld makes explicit a gap that has been implicitly recognized but rarely addressed: world models for single agents are mature, but world models for multi-agent environments are still in their infancy. This work provides the first systematic treatment of the challenges and solutions.

### Compositional Scene Understanding

The Global State Encoder implicitly learns a compositional representation of scenes: the global scene state can be reconstructed from partial views, and views can be generated from the global state. This is a form of compositional 3D scene understanding that emerges naturally from the multi-view consistency constraint.

### Limitations

- **Scalability to many agents**: The MACM uses spatial cross-attention which scales quadratically with the number of agents; very large numbers of agents (e.g., a stadium crowd) may be challenging
- **Occlusion handling**: When agents occlude each other or step out of frame, the model must reason about partially observed agents—an open challenge
- **3D grounding**: The model achieves consistency implicitly through the GSE rather than explicit 3D geometry, which may limit geometric precision

---

## Code & Resources

- **Paper (arXiv)**: [https://arxiv.org/abs/2604.18564](https://arxiv.org/abs/2604.18564)
- **GitHub**: [https://github.com/CIntellifusion/MultiWorld](https://github.com/CIntellifusion/MultiWorld)
- **HuggingFace**: [https://huggingface.co/papers/2604.18564](https://huggingface.co/papers/2604.18564)

**Dependencies**:
- PyTorch, diffusers (HuggingFace)
- Video processing: decord, OpenCV
- 3D/spatial: numpy, scipy
- GPU: Multi-GPU training recommended (H100 or A100)

---

## Related Work & Context

### Prior World Model Work
- **Genie 2** (DeepMind): Interactive world model for 3D environments, single-agent
- **DIAMOND**: Diffusion-based world model for Atari, single-agent
- **UniSim**: Unified simulator for robotics, single-robot
- **DreamerV3**: World model for general RL, single-agent

### Multi-Agent Generative Models
- **Revisiting Multi-Agent World Modeling from a Diffusion-Inspired Perspective** (2505.20922): Parallel work on diffusion-based multi-agent world models

### Future Directions
- Integration with LLM-based planning for multi-agent decision making
- Extension to 3D (NeRF/Gaussian Splatting) world models
- Real-world deployment in autonomous driving simulation pipelines
