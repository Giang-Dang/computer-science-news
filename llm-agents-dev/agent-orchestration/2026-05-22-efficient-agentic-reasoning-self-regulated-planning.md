# Efficient Agentic Reasoning Through Self-Regulated Simulative Planning

**ArXiv ID:** [2605.22138](https://arxiv.org/abs/2605.22138)  
**Authors:** Mingkai Deng, Jinyu Hou, Lara Sá Neves, Varad Pimpalkhute, Taylor W. Killian, Zhengzhong Liu, Eric P. Xing  
**Affiliations:** Carnegie Mellon University, Institute of Foundation Models (IFM)  
**Submitted:** May 2026  
**Field:** Agents / AI Systems / Machine Learning

---

## Executive Summary

This work introduces a novel three-system architecture for agentic reasoning that achieves competitive performance with systems 120-355× larger while using 25-95% fewer reasoning tokens. The key insight is decomposing agent decision-making into simulative reasoning (System II for planning), self-regulation (System III for deciding when to plan), and reactive execution (System I for action), enabling efficient and generalizable reasoning across diverse tasks without per-domain engineering.

## Problem Statement

Current agentic reasoning systems face a critical trade-off between performance and efficiency:

1. **Implicit Planning Limitations**: Systems that rely on chain-of-thought reasoning to implicitly handle planning dramatically increase reasoning length without reliable accuracy gains

2. **Domain-Specific Engineering**: Most planning approaches require extensive per-domain engineering, limiting their generalization across task categories

3. **Inefficient Token Use**: Reactive systems forced to use extended reasoning sequences waste computational resources on unnecessary planning steps

4. **Unclear When to Plan**: Systems lack mechanisms to determine when planning is actually necessary versus when direct action is preferable

The core challenge: How can agents efficiently decide when and how deeply to plan across diverse tasks without task-specific engineering?

## Core Concepts & Theory

### Three-System Architecture

The framework decomposes agentic reasoning into three complementary systems:

#### System I: Reactive Execution
- Handles fine-grained action selection
- Direct, fast response without deliberation
- Used for simple, straightforward tasks

#### System II: Simulative Reasoning (World Model)
- Grounds deliberation in future-state prediction
- Enables planning through simulation
- Uses world model for trajectory rollout and evaluation

#### System III: Self-Regulation
- Meta-level decision making: "Should I plan? How deeply?"
- Learned configurator that adapts to task complexity
- Routes between Systems I and II based on problem requirements

### World Model as Planning Foundation

The world model is realized as an LLM that can:
1. Simulate potential future states based on actions
2. Evaluate trajectories for feasibility
3. Generate rollouts of different decision branches
4. Provide grounded predictions for planning

### Self-Regulated Decision Making

Instead of always planning or never planning, the system learns when planning provides value:
- Detect when direct execution suffices
- Identify cases requiring deliberation
- Adapt planning depth to task difficulty

## Main Ideas & Contributions

### Novel Contribution: Unified Planning Without Domain Engineering

The key innovation is achieving domain-agnostic planning through simulative reasoning. Unlike prior approaches requiring task-specific planning modules, this system generalizes across:
- Mathematical reasoning
- Scientific problem-solving
- Tabular data analysis
- Web information seeking
- Open-ended reasoning tasks

### Efficiency Through Selective Planning

By learning when to invoke planning, the system dramatically reduces token consumption:
- Only plans when necessary
- Adjusts planning depth based on problem characteristics
- Maintains performance while reducing computational cost

### From Reactive to Deliberative Reasoning

The architecture realizes cognitive science insights about dual-process reasoning:
- Fast, automatic responses (System I)
- Deliberative, planned reasoning (System II)
- Meta-cognitive control (System III)

## Methodology & Implementation

### System Implementation Details

**System I (Reactive)**: Direct LLM generation with minimal context

**System II (Simulative)**: 
- LLM-based world model
- Trajectory sampling for future-state prediction
- Multi-step lookahead planning

**System III (Self-Regulation)**:
- Learned configurator module
- Policy that selects between Systems I and II
- Trained via supervised learning then RL

### Training Approach

1. **Version 0.1**: Prompted multi-module system with manual traces
2. **Version 1.0**: Structured plans reconstructed from reasoning traces
3. **Training**: Supervised learning on trajectories, then RL fine-tuning

### Experimental Setup

**Evaluated Tasks:**
- Mathematical reasoning (arithmetic, algebra, calculus)
- Scientific problem-solving (physics, chemistry)
- Tabular analysis and data interpretation
- Web information seeking and retrieval
- Open-ended reasoning tasks

### Results & Metrics

**Remarkable Efficiency Gains:**

| Model | Parameters | Pass@1 | Token Efficiency |
|-------|-----------|--------|-----------------|
| v0.1-8B | 8B | Competitive with 120-355B systems | - |
| v1.0-30B | 30B | Competitive with 685B-1T systems | 25.8-95.3% fewer tokens |

**Key Metrics:**
- Achieves performance of 120-355× larger models (v0.1)
- Maintains performance of 685B-1T parameter systems while using 25.8-95.3% fewer reasoning tokens (v1.0)
- Effective planning across diverse task domains
- Generalizable without domain-specific engineering

**Token Efficiency Comparison:**
- v1.0-30B uses 25.8% fewer tokens than comparable 120B+ agentic systems
- Scales to 95.3% token reduction on certain tasks
- Maintains or exceeds performance despite dramatic efficiency improvements

## Practical Applications & Use Cases

### Mathematics & Science Education
- Tutoring systems that plan when to provide guidance
- Problem-solving assistance with adaptive difficulty
- Automated homework verification and generation

### Scientific Research & Analysis
- Research hypothesis generation and evaluation
- Data analysis with automated planning
- Experimental design optimization

### Business Intelligence
- Tabular data analysis and insight generation
- Decision support systems with reasoning transparency
- Report generation with multi-step reasoning

### Interactive Systems
- Question-answering with planning transparency
- Information retrieval with reasoning trails
- Dialogue systems with deliberative reasoning

## Insights & Implications

### Broader Field Impact

1. **Efficiency Revolution**: Demonstrates that large parameter models are not always necessary—intelligent architecture design can achieve comparable performance with much smaller models

2. **Generalization**: Shows that domain-agnostic planning is achievable through world models, reducing the need for extensive task-specific engineering

3. **Cognitive Plausibility**: Aligns with cognitive science understanding of dual-process reasoning, suggesting these insights may scale to other domains

4. **Token Economy**: Highlights that token efficiency is achievable without sacrificing reasoning quality

### State-of-the-Art Advancement

- Pushes boundaries of efficient reasoning in LLMs
- Challenges the scaling hypothesis that larger is always better
- Opens new research directions in adaptive reasoning systems

### Limitations & Open Questions

1. **World Model Quality**: Performance depends on accuracy of the learned world model
2. **Task Diversity**: Unclear how well approach generalizes beyond tested domains
3. **Planning Complexity**: May struggle with very complex planning scenarios requiring deep lookahead
4. **Computational Overhead**: Self-regulation mechanism adds some overhead

### Future Research Directions

- Improving world model accuracy through additional training
- Extending to longer-horizon planning problems
- Combining with other reasoning techniques (chain-of-thought, etc.)
- Applying to multimodal reasoning and planning
- Studying theoretical foundations of optimal planning allocation

## Code & Resources

### Official Resources
- Paper available at: https://arxiv.org/abs/2605.22138
- Implementation framework and code (to be released)

### Dependencies & Requirements
- Transformers library (Hugging Face)
- PyTorch for training and inference
- LLM-as-world-model framework
- GPU compute (A100 recommended for efficient training)

### Quick Start Guide

The framework can be integrated as:
1. Install base LLM and world model
2. Initialize System I (reactive), System II (world model), System III (configurator)
3. Prepare task-specific datasets for evaluation
4. Fine-tune self-regulation policy with RL
5. Evaluate on target reasoning tasks

### Compute Requirements
- Training: 8×A100 GPUs for efficient training
- Inference: Single GPU sufficient for reasonable batch sizes
- Memory: ~80GB for 30B parameter model

## Related Work & Context

### Related Recent Papers
- **SimuRA**: World-model-driven simulative reasoning architecture
- **Planning in LLMs**: Prior work on integrating planning into language models
- **Chain-of-Thought**: Implicit planning through token generation
- **Adaptive Computation**: Dynamic allocation of compute based on problem complexity

### Prior Work Foundations
- Cognitive science of dual-process reasoning (Kahneman et al.)
- Hierarchical reinforcement learning and options framework
- Model-based planning in reinforcement learning
- Meta-learning for task adaptation

### Theoretical Connections
- Bayesian approaches to planning under uncertainty
- Information theory and optimal decision making
- Optimal control and trajectory optimization

## Related Systems & Comparisons

### Similar Approaches
- **Process Reward Models**: Provide step-level feedback but still require full planning
- **Mixture of Experts**: Different architecture but similar efficiency goals
- **Speculative Decoding**: Parallel efficiency technique but different mechanism

### Advantages Over Baselines
- Generalizes across domains without engineering
- More efficient than always-planning approaches
- More accurate than always-reactive approaches
- Theoretically grounded in cognitive science

## References

- Paper: Efficient Agentic Reasoning Through Self-Regulated Simulative Planning
- arXiv: https://arxiv.org/abs/2605.22138
- Authors: Mingkai Deng, Jinyu Hou, Lara Sá Neves, Varad Pimpalkhute, Taylor W. Killian, Zhengzhong Liu, Eric P. Xing
- Institutions: Carnegie Mellon University, Institute of Foundation Models (IFM)
