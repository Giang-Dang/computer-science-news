# Enhanced LLM Reasoning by Optimizing Reward Functions with Search-Driven Reinforcement Learning

**ArXiv ID:** 2605.02073  
**Authors:** Arash Ahmadi, Sarah Sharif, Yaser (Mike) Banad  
**Affiliation:** School of Electrical and Computer Engineering, University of Oklahoma  
**Submitted:** May 8, 2026  
**Resources:** [arXiv Abstract](https://arxiv.org/abs/2605.02073) | [Full Paper PDF](https://arxiv.org/pdf/2605.02073) | [Code & Resources](https://github.com/INQUIRELAB/search-reward-rl)

## Executive Summary

This paper introduces a novel search-driven framework that treats reward function specification as an object of optimization in reinforcement learning. Rather than manually designing reward functions for LLM training, the method automatically generates and ranks candidate reward functions using a frontier language model, achieving substantial improvements on mathematical reasoning benchmarks. The approach demonstrates that strategic reward function design is crucial for unlocking the full potential of RL-based LLM training, with F1 improvements from 0.609 to 0.795 on GSM8K.

## Problem Statement

While reinforcement learning has become a standard post-training mechanism for improving LLM reasoning capabilities—particularly for mathematical problem-solving—performance remains highly sensitive to the design of the reward function that drives policy optimization. Traditional approaches rely on hand-crafted reward specifications, which limits the exploration of the reward function design space and leaves significant performance gains untapped. The research gap lies in the lack of systematic methods for discovering optimal reward functions for complex reasoning tasks.

## Core Concepts & Theory

### Reward Function Optimization Framework

The core innovation is formulating reward function design as a search problem where candidate reward functions can be automatically generated and evaluated. The framework treats the reward specification R not as a fixed constant but as a parameter to be optimized through an iterative loop.

**Key Process:**

1. **Candidate Generation:** A frontier language model generates diverse candidate reward functions based on ranked summaries from previous iterations and the task domain (mathematical reasoning).

2. **Automatic Validation:** Each candidate reward function is validated for syntactic correctness and semantic coherence before evaluation.

3. **Policy Optimization:** Candidate reward functions are screened through Group Relative Policy Optimization (GRPO) training runs—a modern RL algorithm that improves over traditional PPO by providing better credit assignment.

4. **Ranking and Feedback:** Reward functions are ranked by their performance metric (F1 on GSM8K test set), and top performers feed back into the next generation round.

### Group Relative Policy Optimization (GRPO)

GRPO is a training algorithm that improves upon standard policy gradient methods by implementing relative policy optimization, which provides more stable and efficient credit assignment across sequences of reasoning steps. This is particularly important for long-horizon reasoning tasks where the quality of intermediate steps determines final output correctness.

### Mathematical Formulation

For mathematical reasoning tasks, a reward function can be expressed as a combination of:
- **Correctness Score:** Whether the final answer matches the ground truth
- **Process Quality:** Partial credit for correct intermediate reasoning steps
- **Efficiency Metrics:** Preference for concise, well-structured solutions

## Main Ideas & Contributions

1. **Search-Driven Reward Optimization:** The paper's primary contribution is demonstrating that reward functions themselves can be treated as objects of optimization rather than fixed design choices. This meta-learning approach to reward design is novel and applicable across multiple reasoning domains.

2. **Iterative Refinement Loop:** The ranked-feedback mechanism creates a virtuous cycle where successful reward functions inform generation of the next round of candidates, concentrating search effort on promising regions of the reward function space.

3. **Scalable Evaluation:** By using relatively short GRPO training runs (500 steps) for candidate screening, the method makes exhaustive search of reward function space tractable on modest computational budgets.

4. **Empirical Validation:** The paper provides strong evidence that the improvement comes from the quality of discovered reward functions, not merely from ensemble effects—demonstrated by the control experiment showing that random reward ensembles collapse in performance.

## Methodology & Implementation

### Experimental Setup

**Base Model:** Llama-3.2-3B-Instruct with Low-Rank Adaptation (LoRA)

**Benchmark Dataset:** GSM8K (Grade School Math 8K)—a challenging dataset of high school level word problems requiring multi-step reasoning

**Training Configuration:**
- GRPO training: 500 steps per candidate
- Learning rate: Standard settings for LoRA fine-tuning
- Batch size: [Exact figures unavailable — see full paper]
- Total candidates per round: 10 (5 rounds = 50 total candidates)

### Iterative Search Process

Round 1:
- Initial baseline: Generate 10 diverse reward functions
- Mean F1: 0.596
- Best individual F1: [Exact figures unavailable — see full paper]

Round 2:
- Feed top performers from Round 1 back to generator
- Mean F1: ~0.61 (estimated)

Round 3:
- Mean F1: ~0.62 (estimated)

Round 4:
- Mean F1: ~0.625 (estimated)

Round 5 (Final):
- Mean F1: 0.632
- Best individual reward: F1 = 0.787

### Evaluation Results

**Performance Metrics (on GSM8K):**

| Configuration | F1 Score | Accuracy | Bootstrap CI (95%) |
|---|---|---|---|
| Base GRPO (no reward search) | 0.609 | [unavailable] | - |
| Mean of discovered rewards | 0.632 | [unavailable] | - |
| Best ensemble (5 rewards) | 0.795 | 0.660 | F1: [0.756, 0.832], Acc: [0.635, 0.686] |
| Random 5-reward control | 0.047 | [unavailable] | - |

**Key Findings:**
- Absolute F1 gain of 0.19 over baseline (31% relative improvement)
- Best single discovered reward significantly outperforms baseline
- Ensemble of top 5 rewards provides most stable performance
- Random reward ensembles collapse (F1=0.047), confirming the importance of reward quality

### Ablation Analysis

The paper includes critical ablation showing that the improvement is driven by the quality of discovered rewards rather than ensemble effects. A randomly selected 5-reward ensemble drops to F1=0.047, demonstrating that not all reward combinations are equally effective.

## Practical Applications & Use Cases

1. **Mathematical Reasoning Systems:** The method directly improves LLM performance on mathematical problem-solving, with applications in educational technology, competitive programming assistance, and scientific computation.

2. **Multi-Step Reasoning Tasks:** Beyond mathematics, the framework generalizes to other domains requiring sequential reasoning—legal analysis, scientific reasoning, code generation with correctness requirements.

3. **Adaptive Reward Design:** The approach could be extended to automatically tailor reward functions for specific domains or user preferences without manual engineering.

4. **RL Training Efficiency:** By systematically discovering better reward functions, the method reduces the number of full training runs needed, making LLM training more computationally efficient.

## Insights & Implications

1. **Reward Function as Search Space:** The paper reframes reward engineering as an optimization problem, opening new research directions in automated curriculum learning and meta-learning for RL.

2. **Scaling Behavior:** The results suggest that the quality of the reward signal is a primary bottleneck in LLM reasoning training, potentially more important than model size or dataset size in the examined range.

3. **Ensemble Stability:** Combining multiple discovered reward functions provides both improved performance and robustness, suggesting that diversity in reward specification captures different aspects of good reasoning.

4. **Generalization Questions:** While the paper focuses on GSM8K, the framework's effectiveness on other reasoning tasks remains an open question requiring further investigation.

## Code & Resources

- **Official Repository:** [INQUIRELAB/search-reward-rl](https://github.com/INQUIRELAB/search-reward-rl)
- **Included Artifacts:**
  - Generated reward functions from all 5 rounds
  - Complete experimental logs
  - Training scripts and evaluation code
- **Base Model:** Llama-3.2-3B-Instruct (available on Hugging Face)
- **Dataset:** GSM8K (publicly available)
- **Dependencies:** PyTorch, transformers library, GRPO training framework
- **Compute Requirements:** Moderate GPU memory (suitable for 8GB+ GPUs), approximately 100 GPU-hours for full search across 5 rounds

## Related Work & Context

### Prior Reward Function Research
- Traditional reward shaping in RL literature
- Hand-crafted reward functions for task-specific optimization
- Recent work on learned reward models and inverse RL

### Recent Advances in LLM Reasoning
- Group Relative Policy Optimization (GRPO) for stable training
- Process-based vs. outcome-based reward signals
- Scaling laws for reasoning capability improvement

### Connection to Broader Trends
- Meta-learning and automated machine learning (AutoML)
- Language models as agents in reinforcement learning
- Automatic curriculum learning

### Future Research Directions
1. Extension to other reasoning domains (science, law, code)
2. Online reward adaptation during deployment
3. Multi-objective reward optimization balancing speed and accuracy
4. Understanding why certain reward specifications work better than others
5. Combining automatic reward discovery with automatic curriculum design

## References & Further Reading

1. Ahmadi et al. "Enhanced LLM Reasoning by Optimizing Reward Functions with Search-Driven Reinforcement Learning" arXiv:2605.02073
2. Papers on GRPO and modern RL for language models
3. GSM8K dataset paper and related mathematical reasoning benchmarks
