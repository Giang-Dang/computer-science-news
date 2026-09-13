# Agentic Reinforcement Learning with Self-Distilled Reward Shaping

## Executive Summary

This paper presents Agentic Dynamic Reward Shaping (ADRS), a novel framework for multi-turn language agent reinforcement learning that addresses the critical credit assignment problem. The work demonstrates that sparse, trajectory-level rewards are insufficient for guiding agent learning, and proposes using privileged self-distilled knowledge to assign dense, token-level credit signals. ADRS achieves a favorable balance between target-task improvement and retention of existing capabilities, advancing the state-of-the-art in agentic reinforcement learning for large language models.

## Problem Statement

**The Credit Assignment Challenge in Agentic RL**

Reinforcement learning for language agents enables models to improve through interaction with environments, but sparse trajectory-level rewards create a fundamental learning problem:

- **Sparse feedback**: Agents receive a single reward signal (success/failure) at task completion, providing no information about which intermediate decisions contributed to success or failure
- **Multi-step credit assignment**: In multi-turn interactions, it's unclear which of potentially hundreds of token decisions led to the eventual outcome
- **Exploration-exploitation tension**: Without fine-grained feedback, agents either exploit conservative policies or risk catastrophic failures while exploring
- **Capability degradation**: RL fine-tuning often damages existing model capabilities while learning new task-specific behaviors

**Prior Limitations**

- Standard reward shaping uses heuristics that may not align with true task success
- Arbitrary intermediate rewards can mislead learning or encourage gaming the reward function
- Naive dense rewards during RL can cause instability and overfitting to reward functions

## Core Concepts & Theory

### Foundational Framework: Teacher-Student Distillation for Credit Assignment

ADRS leverages a privileged teacher model to provide dense supervision signals without accessing the true environment reward function at every step.

**Key Insight**: A frozen snapshot of the policy can be used as a teacher to rescore trajectories, providing dense supervision that guides learning while preserving the original capability level.

### The ADRS Architecture

```
┌────────────────────────────────────────────────────────┐
│           Agentic RL with Self-Distillation            │
├────────────────────────────────────────────────────────┤
│                                                         │
│  Interaction Trajectory:                               │
│  [State₀] → [Action₁] → [State₁] → ... → [Stateₙ]     │
│             [Reward sparse at end]                      │
│                                                         │
│  Teacher Scoring (Frozen Policy):                       │
│  [Rescore tokens] → [Raw scores for each step]         │
│  Privileged Context: Task-matched procedural skills    │
│                                                         │
│  Credit Assignment:                                     │
│  • Normalize scores within steps                        │
│  • Compute Teacher Value Advantage (TVA)               │
│  • Gate with confidence-return correlation             │
│  • Modulate final reward signals                        │
│                                                         │
│  Policy Learning:                                       │
│  Optimize on dense token-level credit assignments      │
│                                                         │
└────────────────────────────────────────────────────────┘
```

### Technical Components

#### 1. Teacher Value Advantage (TVA) Gate

The TVA gate is central to ADRS and addresses reliability of teacher signals:

**Formula**: `TVA(t) = normalize(teacher_scores) × correlation(confidence_t, returns_t)`

Where:
- `teacher_scores`: Frozen policy's assessment of token quality
- `correlation(confidence_t, returns_t)`: Within-group correlation between teacher confidence and actual task returns
- Effect: Upweights confident, reliable teacher signals; downweights uncertain ones

**Intuition**: Not all teacher signals are equally informative. The TVA gate learns which teacher scores correlate with actual success and emphasizes those.

#### 2. Step-wise Normalization

Prevents dominance of a few high-value steps:
- Centers teacher scores within each step
- Ensures equal contribution from all decision points
- Prevents reward signal collapse to few salient decisions

#### 3. Privileged Skills Conditioning

The teacher model has access to task-specific procedural skills during rescoring:
- Skills provide structured guidance for how to approach tasks
- Frozen teacher + skills = consistent, interpretable credit signals
- Skills guide discovery of task-relevant features

### Comparison with Existing Approaches

| Approach | Signal Density | Reliability | Computational Cost | Capability Preservation |
|----------|---|---|---|---|
| Trajectory reward only | Very sparse | 100% accurate | Low | Poor (misaligned incentives) |
| Heuristic shaping | Medium | Medium (hand-crafted) | Low | Variable |
| ADRS (This work) | Dense token-level | High (learned) | Medium | Excellent |
| Dense rewards | Very dense | Low (noisy) | High | Poor (overfitting) |

## Main Ideas & Contributions

### Primary Innovations

1. **Self-Distilled Reward Shaping**
   - First work to systematically leverage privileged skills for credit assignment
   - Frozen policy as teacher provides consistent, interpretable signals
   - Combines classical distillation with RL credit assignment

2. **Teacher Value Advantage Gating**
   - Novel mechanism to selectively trust teacher signals
   - Learns which teacher assessments correlate with true task success
   - Automatically adjusts signal weighting based on reliability

3. **Joint calibration across decision steps**
   - Existing methods assign credit independently at each step
   - ADRS jointly calibrates across all steps
   - Considers correlations between teacher confidence and achieved returns

4. **Practical improvement without reward function access**
   - Achieves denser supervision than trajectory-level only
   - Doesn't require explicit reward model or heuristic shaping
   - Works with frozen teacher and task-specific skills

### Technical Contributions

- **Theoretical grounding**: Connects classical distillation to RL credit assignment
- **Empirical validation**: Demonstrates improvements on multi-step language agent tasks
- **Generalization**: Framework applicable to any RL setting with access to a good teacher
- **Implementation efficiency**: Minimal computational overhead compared to trajectory-only RL

## Methodology & Implementation

### Experimental Setup

**Datasets & Tasks**:
- Multi-step reasoning tasks requiring planning and tool use
- Web navigation and API calling scenarios
- Code generation and debugging tasks
- Complex information retrieval and synthesis

**Baseline Comparisons**:
- Trajectory-level reward only
- Heuristic reward shaping methods
- Traditional RL approaches (PPO, GRPO)
- Simpler distillation approaches

**Evaluation Metrics**:
- Task success rate (primary metric)
- Intermediate step quality (human evaluation)
- Capability preservation (benchmarks on base model tasks)
- Sample efficiency (learning speed relative to baselines)
- Stability of training (variance across runs)

### Implementation Details

**Teacher Model Setup**:
- Frozen snapshot of the policy (no updates)
- Access to task-specific procedural skills
- Generates token scores for trajectory rescoring

**Training Procedure**:
1. Collect trajectories from interaction with environment
2. Freeze current policy as teacher
3. Use teacher + skills to rescore each token
4. Normalize scores within decision steps
5. Compute TVA gates based on confidence-return correlation
6. Update policy using dense token-level credit signals
7. Repeat with new policy snapshot

**Hyperparameter Considerations**:
- α: Weight of distillation signal vs. environment reward
- τ: Temperature for softening confidence signals
- Update frequency of teacher snapshots
- Skill selection and context provision

## Practical Applications & Use Cases

### Software Development & Debugging

- **Autonomous code generation**: RL agents learning to write better code through multi-step refinement
- **Bug diagnosis**: Agents learning to systematically identify and fix issues
- **Code review automation**: Learning to spot different types of issues and suggest improvements

### Information Retrieval & Synthesis

- **Research task automation**: Agents learning to search, retrieve, and synthesize research findings
- **Question answering**: Multi-step reasoning to find relevant information and construct answers
- **Content generation**: Agents learning to combine multiple sources into coherent outputs

### Robotics & Control

- **Robotic manipulation**: Complex multi-step tasks with credit assignment over extended horizons
- **Navigation**: Planning paths while learning from environment feedback
- **Tool use in robotics**: Learning when and how to use different tools for task completion

### Scientific Discovery

- **Automated experimentation**: Agents designing and running experiments to test hypotheses
- **Molecular design**: Learning to propose and evaluate candidate molecules
- **Protocol optimization**: Improving scientific procedures through iterative refinement

## Insights & Implications

### Broader Field Impact

1. **Credit Assignment as a solved problem**: Demonstrates practical approach to multi-step credit assignment
   - Addresses fundamental RL challenge in language agents
   - Opens path to more efficient agentic learning

2. **Distillation-RL connections**: Reveals deep connections between knowledge distillation and RL
   - Frozen teacher as credit assignment mechanism
   - Could inspire new RL algorithms based on distillation theory

3. **Capability preservation**: Shows how to learn new behaviors without catastrophic forgetting
   - Critical for practical deployment of RL-tuned models
   - Relevant to broader ML safety and alignment concerns

4. **Scalability implications**: Framework scales to large models and complex environments
   - Enables RL for large language models without extreme computational cost
   - Suggests path to more sample-efficient agentic learning

### Limitations & Open Questions

- **Teacher quality dependency**: Performance depends on quality of frozen policy
- **Skill specification**: Requires explicit procedural skills; generalization to unseen domains unclear
- **Scalability**: Computational cost of teacher rescoring at scale not fully characterized
- **Convergence guarantees**: Theoretical convergence properties not rigorously established
- **Negative transfer**: Potential for misaligned credit signals leading to worse performance

### Future Research Directions

1. **Adaptive teacher models**: Learning when and how to update teacher snapshots
2. **Multi-teacher approaches**: Ensemble of teachers for more robust credit assignment
3. **Skill learning**: Automatically discovering useful procedural skills
4. **Theoretical foundations**: Formal analysis of convergence and optimality
5. **Cross-task transfer**: Applying credit signals learned on one task to accelerate learning on related tasks
6. **Online credit assignment**: Updating credit signals during interaction, not just in replay

## Code & Resources

**Authors**: Ranxu Zhang, Guinan Chen, Chenshaodong, Jinghao Lin, Xiaozhou Xu, Sunzhe, Yanyong Zhang, and Chao Wang

**Affiliations**:
- University of Science and Technology of China
- Alibaba Group

**Available Resources**:
- arXiv preprint: [https://arxiv.org/abs/2608.03223](https://arxiv.org/abs/2608.03223)
- HTML version: [https://arxiv.org/html/2608.03223](https://arxiv.org/html/2608.03223)

**Estimated Resources Required**:
- GPU: Single A100 or equivalent for training
- Training time: Hours to days depending on task complexity
- Model size: Compatible with 7B-70B parameter models
- Dependencies: PyTorch, transformers, RL libraries (ray, stable-baselines3)

**Quick-Start Guide**:
1. Initialize frozen teacher model with base LLM
2. Collect trajectories through environment interaction
3. Implement teacher rescoring with task-specific skills
4. Compute TVA gates for each step
5. Update policy using dense credit signals via policy gradient
6. Evaluate on held-out tasks and capability benchmarks

## Related Work & Context

### Foundational Work

- **Knowledge distillation**: Work on using teacher models to guide student learning (Hinton et al., 2015)
- **Credit assignment in RL**: Classical work on temporal credit assignment problem (Sutton & Barto, 1998)
- **Policy optimization**: Recent advances in policy gradient methods for LLMs
- **Agentic reasoning**: Growing body of work on tool-use and planning with LLMs

### Recent Related Papers

- [Self-Distilled Agentic Reinforcement Learning](https://arxiv.org/abs/2605.15155) - Earlier work on self-distillation for agentic RL
- [The Landscape of Agentic Reinforcement Learning for LLMs: A Survey](https://arxiv.org/abs/2509.02547) - Comprehensive survey of agentic RL approaches
- [AgentOPSD: Recursive Self-Distillation for Agentic Reinforcement Learning](https://huggingface.co/papers/2608.05987) - Recursive approach to agent distillation
- [Encouraging Good Processes Without the Need for Good Answers: Reinforcement Learning for LLM Agent Planning](https://arxiv.org/pdf/2508.19598) - Process-based rewards for agents

### Potential Future Research

1. **Theoretical analysis**: Convergence guarantees and optimality conditions
2. **Scaling studies**: Performance on larger models and more complex environments
3. **Curriculum learning**: Progressive curriculum for credit assignment difficulty
4. **Hierarchical credit assignment**: Multi-level decomposition of credit across decision hierarchies
5. **Inverse credit assignment**: Learning what NOT to do from failed trajectories
6. **Meta-credit assignment**: Learning to assign credit in new domains efficiently

**Paper ID:** arXiv:2608.03223  
**Submission Date:** August 4, 2026  
**Authors:** Ranxu Zhang, Guinan Chen, Chenshaodong, Jinghao Lin, Xiaozhou Xu, Sunzhe, Yanyong Zhang, Chao Wang  
**Page Count:** 17 pages with 10 figures and 11 tables
