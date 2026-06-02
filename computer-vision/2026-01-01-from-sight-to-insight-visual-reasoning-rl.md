# From Sight to Insight: Improving Visual Reasoning Capabilities of Multimodal Models via Reinforcement Learning

**ArXiv ID:** 2601.00215  
**Authors:** Omar Sharif, Eftekhar Hossain, Patrick Ng  
**Submission Date:** January 1, 2026

## Executive Summary

This paper addresses a critical limitation in multimodal large language models (MLLMs): their difficulty in integrating visual information while reasoning, particularly on visual reasoning tasks like visual puzzles. By applying reinforcement learning with carefully designed reward functions, the authors demonstrate substantial improvements in visual reasoning capabilities. The key insight—that visual perception rather than reasoning is the bottleneck—leads to practical solutions for enhancing MLLMs without requiring expensive human supervision, with improvements of 23.6-26.7% on Claude models.

## Problem Statement

Despite their impressive capabilities, multimodal large language models face fundamental challenges in visual reasoning:

1. **Perception-reasoning disconnect:** MLLMs excel at describing images but struggle when reasoning requires deep visual understanding. When asked to solve visual puzzles, models generate reasoning chains that neglect visual information, relying instead on generic reasoning patterns.

2. **Visual information underutilization:** Converting images to text descriptions and then reasoning about them significantly improves performance (26.7% gain for Claude 3.5), suggesting models fail to effectively leverage visual input during reasoning.

3. **Lack of visual grounding:** Current MLLMs lack mechanisms to ground reasoning steps in specific visual observations. They generate abstract reasoning without connecting it to what they see.

4. **Training data limitations:** MLLMs are typically trained on image-caption pairs where explicit visual reasoning is not emphasized, leading to models that are generally capable but specifically weak at reasoning about visual properties.

5. **High annotation cost:** Creating large-scale datasets of visual reasoning examples with step-by-step annotations is expensive, limiting the supervised fine-tuning approach.

## Core Concepts & Theory

### Visual Reasoning in MLLMs

Visual reasoning differs fundamentally from pure language reasoning:

```
Pure Language Reasoning:
Question → [Reasoning: think about concepts] → Answer

Visual Reasoning:
Question + Image → [Perception: identify visual elements] 
                 → [Reasoning: apply logic to visual observations]
                 → [Grounding: validate against image]
                 → Answer
```

The critical difference is that visual reasoning requires continuous reference back to the image, not just abstract reasoning.

### Chain-of-Thought (CoT) Reasoning

The approach builds on the insight that generating intermediate reasoning steps (CoT) improves reasoning:

**Standard CoT:**
```
Q: Solve this puzzle
A: [Reasoning step 1]
   [Reasoning step 2]
   [Final answer]
```

**Visual CoT with grounding:**
```
Q: Solve this visual puzzle
A: [Visual perception: identify key elements in image]
   [Reasoning step 1: apply logic referencing image]
   [Reasoning step 2: validate against visual observation]
   [Final answer: synthesize visual + logical reasoning]
```

### Reward Modeling for Visual Reasoning

The paper designs multiple reward functions targeting different aspects:

1. **Vanilla reward:** Simple binary feedback (correct/incorrect)
2. **Only-accuracy reward:** Focus purely on final answer correctness
3. **Mixture reward:** Combine multiple signals
4. **Continuous reward:** Graduated rewards for partial correctness
5. **Visual-fusion reward:** Explicitly reward visual element identification
6. **No-accuracy reward:** Maximize reasoning length without accuracy constraint

The reward function $R(s, a)$ guides the RL algorithm:
$$\max_{\pi} \mathbb{E}[R(s, a) + \lambda L(a)]$$

where $\pi$ is the model policy, and $L(a)$ is a length regularizer to avoid output explosion.

### Reinforcement Learning Objective

The RL formulation uses policy gradient methods to optimize:
$$\mathcal{L}_{RL} = -\mathbb{E}[R(s, a) \log \pi(a|s)]$$

This encourages the model to generate trajectories (reasoning chains) that maximize the reward signal while maintaining valid probability distributions over tokens.

## Main Ideas & Contributions

### 1. Problem Diagnosis: Visual Perception is the Bottleneck

Through analysis of model outputs and controlled experiments:
- Identified that visual perception (understanding what's in the image) is the main limitation
- Showed that even naive image-to-text conversion provides massive improvements
- Demonstrated that open-source MLLMs have sufficient reasoning capability but insufficient visual grounding

**Key Finding:** Converting images to text descriptions yields:
- Claude 3.5: +26.7% performance improvement
- Claude 3.7: +23.6% performance improvement

This suggests the models can reason adequately if visual information is properly presented.

### 2. Reward-Driven Visual Reasoning

Novel approach combining RL with visual reasoning:
- Design six distinct reward functions targeting different aspects
- Enable unsupervised or weak-supervised training (no expensive annotations required)
- Achieve improvements without relying on external models for supervision

**Reward functions:**
- **Vanilla:** Simple correctness
- **Visual-fusion:** Explicitly identify image elements before reasoning
- **Continuous:** Partial credit for progress toward correct answer
- **Mixture:** Balance between different evaluation criteria

### 3. Empirical Validation on Open-Source MLLMs

Comprehensive evaluation on practical models:
- Applied to open-source models (accessible to broader community)
- Compared with proprietary models (Claude, GPT-4V)
- Demonstrated consistent improvements without model distillation

### 4. Scalable Training Framework

Practical RL training approach:
- Can be applied to any MLLM architecture
- Doesn't require expensive labeled data
- Computationally feasible for research teams
- Transferable across different visual reasoning tasks

## Methodology & Implementation

### Experimental Setup

**Models Evaluated:**
- Open-source: LLaVA, Qwen-VL, Phi-3-Vision
- Proprietary baselines: Claude 3.5, Claude 3.7, GPT-4V

**Visual Reasoning Datasets:**
- Visual puzzle datasets (geometric reasoning, counting, relationships)
- Visually-grounded QA (requiring integration of text and image)
- Complex reasoning (multiple steps with visual validation)

### Six Reward Functions

**1. Vanilla Reward:**
```
R(answer) = {
  1.0  if answer == ground_truth
  0.0  otherwise
}
```

**2. Only-Accuracy Reward:**
```
R(answer) = {
  1.0  if final answer correct
  0.0  otherwise
  (ignores intermediate reasoning)
}
```

**3. Mixture Reward:**
```
R(trajectory) = α * R_accuracy 
              + β * R_reasoning_length
              + γ * R_visual_grounding
```

**4. Continuous Reward:**
```
R(answer) = similarity(answer, ground_truth)
            (rewards partial correctness)
```

**5. Visual-Fusion Reward:**
```
R(trajectory) = {
  1.0  if identifies visual elements AND correct answer
  0.5  if identifies visual elements but wrong answer
  0.0  otherwise
}
```

**6. No-Accuracy Reward:**
```
R(trajectory) = length(reasoning) / max_length
(encourages longer reasoning without correctness constraint)
```

### RL Algorithm

**Policy Optimization:**
- Algorithm: PPO (Proximal Policy Optimization) or REINFORCE variants
- Baseline: Value function for variance reduction
- Updates: Per-episode training on collected trajectories

**Training Procedure:**
1. Sample trajectory from current policy
2. Compute reward based on final answer
3. Estimate advantages using baseline value function
4. Apply policy gradient updates
5. Repeat with updated policy

### Evaluation Metrics

[Exact figures unavailable — see full paper]

**Performance Measurements:**
- Accuracy on visual reasoning benchmarks
- Length of generated reasoning chains
- Semantic similarity of generated reasoning to ground truth
- Computational efficiency (tokens per second)

**Analysis Metrics:**
- Ablation studies on reward function components
- Effect size comparison across different reward designs
- Convergence analysis during RL training
- Transfer learning to unseen visual puzzles

## Practical Applications & Use Cases

### 1. Visual Question Answering (VQA) Systems

**Application:** Building robust VQA systems for practical domains
- Medical imaging diagnosis assistance
- Document understanding and extraction
- Scene understanding for autonomous systems
- Product recognition in e-commerce

**Benefits:**
- Improved accuracy on reasoning-heavy questions
- Reduced hallucinations through visual grounding
- Better explanation generation for human trust

### 2. Accessibility Technologies

**Application:** Enhanced image understanding for blind and low-vision users
- Detailed scene descriptions with logical reasoning
- Complex diagram interpretation
- Chart and graph analysis with insights

**Benefits:**
- More comprehensive scene understanding
- Better reasoning about spatial relationships
- Improved explanation clarity

### 3. Educational Tools

**Application:** Intelligent tutoring systems with visual learning
- Math problem solving with diagram interpretation
- Physics simulation explanation
- Geometry problem assistance

**Benefits:**
- Step-by-step visual reasoning explanations
- Identification of student misconceptions
- Pedagogically sound explanation generation

### 4. Scientific Research Assistance

**Application:** Research paper figure understanding and analysis
- Graph interpretation and trend identification
- Table extraction and numerical reasoning
- Research visualization understanding

**Benefits:**
- Literature review automation
- Quantitative reasoning about research results
- Hypothesis generation from data

### 5. Autonomous Systems

**Application:** Vision-based reasoning for robotics and autonomous vehicles
- Scene understanding for navigation
- Object interaction planning
- Spatial reasoning for manipulation

**Benefits:**
- More robust visual reasoning
- Better planning with visual constraints
- Improved safety through visual validation

## Insights & Implications

### Fundamental Insights

1. **Visual perception is distinct from reasoning:** Improving visual reasoning in MLLMs requires addressing perception quality, not just reasoning ability.

2. **RL without expensive supervision:** Reward functions can be designed to guide visual reasoning without requiring large annotated datasets.

3. **Open-source models are competitive:** Open-source MLLMs can be significantly improved to match or exceed proprietary model performance on specific tasks.

4. **Visual grounding matters:** Explicitly rewarding visual element identification improves overall reasoning quality.

### Broader Field Impact

- **MLLM capabilities:** Demonstrates that current MLLMs have latent visual reasoning abilities that can be unlocked through RL
- **Training efficiency:** Shows that task-specific improvements can be achieved without full retraining
- **Accessibility:** Techniques applicable to improving model outputs for users with different needs
- **Research methodology:** Establishes RL as viable approach for improving model behavior without human feedback

### Limitations and Open Questions

1. **Generalization:** How well do improvements on visual puzzles transfer to other visual reasoning tasks?

2. **Scalability:** How do results scale to larger models and more complex reasoning scenarios?

3. **Reward design:** How sensitive are results to reward function design? Can rewards be learned from data?

4. **Computational cost:** What is the total computational budget for RL training compared to supervised fine-tuning alternatives?

5. **Safety implications:** Could RL training inadvertently optimize for undesirable behaviors? How to ensure safety during policy learning?

## Code & Resources

**Framework:** Open-source implementation using Hugging Face Transformers

**Dependencies:**
- Transformers >= 4.30
- PyTorch or TensorFlow
- Vision libraries (PIL, OpenCV)
- RL frameworks (TRL, Ray RLlib, or custom implementation)

**Quick Start:**

```python
from transformers import AutoModel, AutoProcessor
from trl import PPOTrainer

# Load MLLM
model = AutoModel.from_pretrained("lava-hf/llava-1.5-7b-hf")
processor = AutoProcessor.from_pretrained("lava-hf/llava-1.5-7b-hf")

# Define reward function
def visual_fusion_reward(generated_text, image, ground_truth):
    identifies_elements = check_visual_elements(generated_text, image)
    correct_answer = extracted_answer(generated_text) == ground_truth
    
    if identifies_elements and correct_answer:
        return 1.0
    elif identifies_elements:
        return 0.5
    else:
        return 0.0

# Initialize PPO trainer
trainer = PPOTrainer(
    model=model,
    config=ppo_config,
    reward_fn=visual_fusion_reward
)

# Train
trainer.train()
```

**Computational Requirements:**
- GPU memory: 40GB+ (A100 recommended)
- Training time: 100-200 GPU hours for convergence
- Inference: Real-time on consumer GPUs with quantization

## Related Work & Context

### Foundation Papers on MLLMs

- [LLaVA: Large Language and Vision Assistant](https://arxiv.org/abs/2304.08485) - Instruction-tuned VLM
- [Flamingo: a Visual Language Model for Few-Shot Learning](https://arxiv.org/abs/2204.14198) - In-context few-shot learning
- [GPT-4V: Visual Question Answering with Vision Transformers](https://arxiv.org/abs/2310.20744)

### Related RL for Vision Papers

- [Perception Before Reasoning](https://arxiv.org/abs/2509.13031) - Two-stage RL for visual reasoning
- [RewardMap: Tackling Sparse Rewards](https://arxiv.org/abs/2510.02240) - Multi-stage RL for visual reasoning
- [Visionary-R1: Mitigating Shortcuts](https://arxiv.org/abs/2505.14677) - RL to prevent visual reasoning shortcuts

### Self-Supervised and RL for Multimodal Learning

- [SSL-R1: Self-Supervised Visual Reinforcement](https://arxiv.org/abs/2604.20705) - Self-supervised RL for MLLMs
- [Look Carefully: Adaptive Visual Reinforcements](https://arxiv.org/abs/2602.24041) - RL for hallucination mitigation

### Future Research Directions

1. **Multi-step reasoning:** Extending to tasks requiring longer reasoning chains with visual validation at each step

2. **Reward learning:** Automatically learning optimal reward functions from demonstration data

3. **Transfer learning:** Understanding how improvements on visual puzzles transfer to other tasks

4. **Theoretical analysis:** Formal analysis of convergence and optimality in visual RL settings

5. **Human-in-the-loop:** Incorporating human feedback to iteratively improve reward functions

6. **Interpretability:** Understanding which visual features the model learns to use through RL training

## References

- [2601.00215] Sharif, O., Hossain, E., Ng, P. "From Sight to Insight: Improving Visual Reasoning Capabilities of Multimodal Models via Reinforcement Learning." arXiv, January 2026.
- [2509.13031] Perception Before Reasoning: Two-Stage Reinforcement Learning for Visual Reasoning
- [2510.02240] RewardMap: Tackling Sparse Rewards in Fine-grained Visual Reasoning
- [2604.20705] SSL-R1: Self-Supervised Visual Reinforcement Post-Training for Multimodal LLMs
- [2602.24041] Look Carefully: Adaptive Visual Reinforcements in MLLMs for Hallucination Mitigation
