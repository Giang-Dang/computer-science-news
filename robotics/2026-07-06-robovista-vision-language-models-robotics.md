# RoboVista: Evaluating Vision Language Models for Diverse Robot Applications

**arXiv ID:** 2607.04610  
**Submission Date:** July 6, 2026  
**Authors:** Shuangyu Xie, Kaiyuan Chen, Ziyang Chen, Simeon Adebola, Yixuan Huang, Zehan Ma, Tianshuang Qiu, Wentao Yuan, Dhruv Shah, Pannag R. Sanketi, Ken Goldberg  
**Affiliations:** UC Berkeley, Princeton University, Google DeepMind

## Executive Summary

RoboVista introduces a benchmark and evaluation framework for assessing Vision-Language Models (VLMs) across diverse robotic applications. The paper presents the Robot Question Answering (RQA) framework that unifies 474 expert-annotated questions spanning 39 distinct robot task types (surgical, agricultural, industrial, domestic, and autonomous driving). RoboVista demonstrates strong correlations between VLM performance on the benchmark and real-world robotic task success, establishing VLMs as viable foundations for general-purpose robotic reasoning.

## Problem Statement

Traditional robot perception benchmarks rely primarily on end-to-end teleoperated datasets that don't effectively evaluate Vision-Language Models' capability to reason about robotic decision-making. The research gap lies in:
- Lack of unified frameworks for evaluating VLMs across diverse robot embodiments
- No standardized way to assess modular robotic reasoning components
- Absence of benchmarks that correlate with real-world robotic task performance
- Limited evaluation across different robot morphologies, sensing modalities, and task domains

The paper addresses how VLMs can serve as interpretable foundations for general-purpose robotic systems while requiring evaluation approaches that capture cross-domain robotic understanding.

## Core Concepts & Theory

### Robot Question Answering (RQA) Framework

The RQA framework decomposes robotic decision-making into modular Visual Question Answering formulations. It unifies three evaluation methodologies:

1. **Human Expert Annotation:** Domain experts (surgeons, roboticists, engineers) annotate reasoning behind robot decisions
2. **Algorithmic Task Execution:** Capture decision points during actual robot task execution
3. **Automated Question Construction:** Generate multiple-choice VQA instances from captured decision points

This modular approach preserves the structure of robotic reasoning while enabling VLM evaluation through standard VQA metrics.

### Task Representation

Tasks are characterized across multiple dimensions:
- **Embodiment:** Single-arm, dual-arm, mobile manipulators, autonomous vehicles
- **Visual Complexity:** Fine-grained spatial understanding, variable lighting, occluded objects
- **Temporal Horizon:** Single-step decisions vs. long-horizon task progress
- **Interaction Complexity:** Rigid objects, deformable objects, dynamic environments

### Evaluation Methodology

Rather than end-to-end success metrics, RoboVista evaluates intermediate decision quality:
- Visual scene understanding
- Object and gripper pose estimation
- Action feasibility and safety assessment
- Task-stage progression understanding

This decomposition enables diagnosis of VLM reasoning failures across specific robotic competencies.

## Main Ideas & Contributions

### Novel Contributions

1. **First Comprehensive VLM Benchmark for Robotics:** 474 questions covering 39 task types with expert annotations
2. **Real-World Validation:** Demonstrated strong correlation between benchmark performance and actual robotic task success
3. **Diverse Robot Coverage:** Spans surgical, agricultural, industrial, domestic, and autonomous systems
4. **Modular Evaluation Framework:** Enables diagnosing VLM strengths/weaknesses in specific robotic reasoning components

### Technical Innovations

- **Cross-Domain Unification:** Single benchmark captures reasoning patterns across fundamentally different robot types
- **Multiple Validation Approaches:** Correlates VLM scores with bi-manual alignment errors, surgical task progression, and autonomous driving performance
- **Scalable Annotation:** Systematic question construction from algorithmic task execution enables efficient benchmark expansion

## Methodology & Implementation

### Dataset Details

**Scale:**
- 474 multiple-choice Visual Question Answering instances
- 39 distinct robotic task types
- Human expert annotations for reasoning transparency

**Task Coverage:**

| Domain | Task Types | Examples |
|--------|-----------|----------|
| Surgical Robotics | 8 | Knot-tying, suturing, tissue manipulation |
| Agricultural Robotics | 6 | Fruit picking, plant monitoring, soil analysis |
| Industrial Robotics | 12 | Assembly, precision positioning, tool manipulation |
| Domestic Robotics | 7 | Grasping, placement, household navigation |
| Autonomous Driving | 4 | Lane following, obstacle avoidance, intersection crossing |
| Open Robot Datasets | 2 | Multi-domain robotic manipulation |

**Question Types:**
- Fine-grained spatial reasoning (gripper-object relationships)
- State estimation (object poses, robot configuration)
- Action feasibility assessment
- Safety and constraint satisfaction
- Long-horizon task progress

### Experimental Results

**Bi-Manual Alignment Task (Panda Robot):**
- Pearson correlation ρ = -0.75 between RoboVista scores and physical alignment errors
- Interpretation: Models scoring higher on RoboVista achieve lower distance estimation errors
- Validates that improved VLM understanding translates to better real-world performance

**Surgical Knot-Tying Task (da Vinci Surgical Robot):**
- Strong correlation between RoboVista-surgical subscores and task progress
- Higher-performing VLMs complete more procedural stages
- Demonstrates applicability to precision surgical tasks

**Autonomous Driving Scenarios:**
- VLM reasoning on road conditions correlates with autonomous driving metrics
- Validates cross-domain applicability

### Benchmarked VLMs
- GPT-4V
- Claude Vision
- Gemini Vision
- LLaVA-1.5
- Qwen-VL
- And additional vision-language models

[Exact figures unavailable — see full paper]

## Practical Applications & Use Cases

### Immediate Applications

1. **Robot System Development:** Evaluate VLM suitability before deployment to physical systems
2. **Transfer Learning:** Identify which robotic domains transfer well to new applications
3. **Safety Validation:** Assess VLM reasoning reliability for safety-critical applications
4. **Model Selection:** Benchmark VLMs to choose appropriate foundation models for specific robot tasks

### Industry Applications

- **Surgical Robotics:** Validate VLM understanding of anatomical precision and procedural constraints
- **Agricultural Technology:** Assess crop-specific reasoning and environmental awareness
- **Manufacturing:** Verify precise positioning and tool manipulation understanding
- **Autonomous Vehicles:** Evaluate real-world driving scenario comprehension
- **Household Robotics:** Validate understanding of domestic object interactions and manipulation constraints

### Feasibility and Implementation Challenges

**Strengths:**
- VLMs provide interpretable reasoning explanations
- Modular framework enables task-specific fine-tuning
- Enables rapid evaluation without physical robot infrastructure

**Challenges:**
- Sim-to-real gap remains: visual reasoning may differ between synthetic benchmark images and real robot sensors
- Domain-specific VLM adaptation needed for specialized tasks (surgical, agricultural)
- Long-horizon reasoning still challenging for current VLMs
- Embodiment-specific features (arm length, gripper design) may not transfer between robots

## Insights & Implications

### Broader Field Impact

1. **VLM Foundation Models for Robotics:** Establishes VLMs as viable foundation models for robotic reasoning, moving beyond specialized robot-specific architectures
2. **Interpretability Advantage:** VLM-based approaches provide explicit reasoning traces, improving trust and debuggability versus black-box end-to-end models
3. **Benchmark-Task Alignment:** Demonstrates that well-designed intermediate benchmarks can correlate with downstream task performance

### State-of-the-Art Advancement

- First standardized evaluation framework across diverse robot embodiments
- Bridges gap between academic VLM benchmarks and robotic applications
- Enables systematic comparison of VLM families on robotic reasoning

### Limitations and Open Questions

1. **Limited to Visual Reasoning:** Cannot evaluate multimodal reasoning with proprioceptive, tactile, or force-feedback data
2. **Image-Based Limitations:** Real-time robot feedback loops and tactile sensing not captured
3. **Annotation Scalability:** Expert annotation limits benchmark expansion rate
4. **Generalization:** Questions remain about how well benchmark performance predicts performance on novel robot types or tasks

## Code & Resources

**Official Resources:**
- Project Website: berkeleyautomation.github.io/robovista
- GitHub: Berkeley Automation Lab repositories
- Dataset: Available for research use

**Dependencies:**
- Vision-Language Models (GPT-4V, Claude Vision, Gemini, etc.)
- Standard Python data science stack

**Quick-Start Guide:**
1. Load RoboVista benchmark dataset
2. Query VLM with benchmark questions
3. Compare accuracy across VLMs and task domains
4. Analyze error patterns to diagnose reasoning failures

## Related Work & Context

### Prior Work Foundations

- **Robot VQA:** Building on initial RoboVQA work from Google DeepMind
- **VLM Evaluation:** Extends existing VLM benchmarks (MMVP, LMM-Eval) to robotic domains
- **Robotic Learning:** Complements behavior cloning and end-to-end learning approaches
- **Embodied AI:** Part of broader embodied AI evaluation paradigm (Sim2Real, BenchBot)

### Related Recent Papers

- Vision Transformers for robotic perception
- Multi-modal learning for robot control
- Foundation models for embodied AI
- VLM-based robot planning and reasoning

### Possible Future Research Directions

1. **Multimodal Extensions:** Incorporate proprioceptive, tactile, and force feedback into VLM-based reasoning
2. **Real-Time Performance:** Evaluate VLMs in closed-loop robot control scenarios
3. **Continual Learning:** Adapt VLMs to new robot embodiments through few-shot learning
4. **Embodiment Transfer:** Study how well reasoning transfers between different robot morphologies
5. **Failure Analysis:** Deep investigation of VLM failure modes in specific robotic scenarios
6. **Grounding in Physics:** Enhance VLM understanding of robot dynamics and physical constraints
