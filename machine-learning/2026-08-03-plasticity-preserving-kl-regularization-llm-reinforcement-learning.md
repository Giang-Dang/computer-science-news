# Toward Plasticity-Preserving KL Regularization for Capability Retention in LLM Reinforcement Learning

## Executive Summary

This paper presents Correctness-Conditioned KL Regularization (CoKL), a novel approach to mitigating capability degradation during reinforcement learning fine-tuning of large language models. Rather than constraining the entire output distribution, CoKL narrows regularization to correctness-conditioned objectives, allowing models to explore new behaviors while preserving existing capabilities. The work demonstrates a more favorable balance between target-task improvement and prior-capability retention than existing regularization methods, making it a crucial advancement for practical deployment of RL-tuned LLMs.

## Problem Statement

**The Stability-Plasticity Dilemma in LLM Reinforcement Learning**

When applying reinforcement learning to large language models, practitioners face a fundamental trade-off:

- **Standard KL regularization too restrictive**: Conventional full-policy KL regularization constrains the entire response distribution equally, which unnecessarily restricts exploration and limits learning on the target task
- **Capability collapse**: Without sufficient regularization, RL optimization toward new objectives degrades capabilities the base model already possesses
- **One-size-fits-all constraints**: Treating all parts of the response distribution equally prevents the model from learning task-specific variations while preserving general knowledge

**Formal Problem**

Standard KL divergence penalty in policy optimization:
```
L_policy = -E[log π_θ(a|s) × A(s,a)]
L_total = L_policy + β × KL(π_θ || π_ref)
```

Issues:
- KL penalty affects all outputs equally
- Cannot distinguish between harmful divergence (capability loss) and beneficial divergence (task-specific learning)
- Results in suboptimal learning and capability retention

## Core Concepts & Theory

### Theoretical Framework: Correctness-Conditioned Constraints

The key innovation is conditioning the KL regularization on correctness rather than applying it uniformly:

**Intuition**: We want to preserve behavior on tasks where the model is already correct, but allow divergence when the model needs to learn new behaviors for the target task.

### The CoKL Mechanism

```
┌──────────────────────────────────────────────────────────┐
│     Correctness-Conditioned KL Regularization (CoKL)     │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  Original Response Distribution π_θ:                      │
│  ├─ Correct Behaviors (on base tasks)     [Preserve]     │
│  └─ Incorrect Behaviors (on base tasks)   [Can diverge]  │
│                                                           │
│  Standard KL: Constrains ALL behaviors equally           │
│  Problem: Wastes constraint budget on behaviors that     │
│           can safely change                              │
│                                                           │
│  CoKL: Condition on Correctness                          │
│  ├─ If response is CORRECT: KL(π_θ || π_ref) active      │
│  │  Preserves known-good behaviors                       │
│  │                                                        │
│  └─ If response is INCORRECT: No KL penalty              │
│     Allows exploration of alternatives                   │
│                                                           │
│  Result: Tighter control where it matters most           │
│         Greater freedom where exploration needed         │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

### Mathematical Formulation

**Correctness-Conditioned KL Divergence**:
```
KL_correct = E_{(s,a)~π_θ}[mask(correct(s,a)) × log(π_θ(a|s) / π_ref(a|s))]
```

Where:
- `mask(correct(s,a))` = 1 if response is correct on base task, 0 otherwise
- Effect: KL penalty only applies when diverging from correct behaviors
- `β` can be larger (more aggressive constraint) since applied more selectively

### Key Properties

1. **Plasticity preservation**: Model remains plastic to learn new target-task behaviors
   - Not constrained on behaviors it was wrong about
   - Can explore different approaches to new tasks

2. **Capability retention**: Strongly preserves correct existing behaviors
   - Focused regularization on most important behaviors
   - Prevents catastrophic forgetting of known-good responses

3. **Exploration efficiency**: Learning algorithm can focus on genuinely new behaviors
   - Reward signal not diluted by unnecessary constraints
   - Faster convergence on target task

### Comparison with Prior Work

| Method | Mechanism | Exploration | Capability Preservation | Efficiency |
|--------|-----------|-------------|------------------------|------------|
| No regularization | None | Excellent | Poor | N/A |
| Full-policy KL | Uniform KL penalty | Limited | Good | Suboptimal |
| Activity regularization | L2 on activations | Good | Fair | Moderate |
| Replay buffer mixing | Mixed training | Good | Fair | Data-intensive |
| CoKL (This work) | Conditional KL | Excellent | Excellent | High |

## Main Ideas & Contributions

### Primary Innovation: Correctness-Conditioned Regularization

1. **Selective constraint application**
   - First to condition KL regularization on task correctness
   - Focuses regularization budget on most critical behaviors
   - Allows principled exploration for new task learning

2. **Correctness detection mechanisms**
   - Task-specific correctness criteria (factuality, safety, etc.)
   - Model-based correctness prediction
   - Hybrid human-in-the-loop approaches

3. **Unified framework**
   - Applies to any RL objective (reward, process-based, etc.)
   - Compatible with standard policy optimization algorithms
   - Easy integration into existing training pipelines

### Technical Contributions

- **Formal analysis**: Shows why conditional regularization outperforms unconditional
- **Empirical validation**: Controlled experiments demonstrating improvements
- **Implementation guidance**: Practical recommendations for practitioners
- **Generalization**: Framework applicable beyond LLMs to general policy learning

## Methodology & Implementation

### Experimental Setup

**Target Tasks**:
- Code generation and synthesis
- Mathematical reasoning
- Knowledge-grounded question answering
- Creative writing with style preservation
- Multi-step planning and tool use

**Base Model Benchmarks** (to measure capability preservation):
- General knowledge QA
- Factual accuracy
- Safety and alignment metrics
- Code correctness on standard benchmarks
- Mathematical problem-solving

**Experimental Design**:
1. Fine-tune model with different regularization methods
2. Measure performance on new task (RL target)
3. Measure performance on base capabilities (generic benchmarks)
4. Compute trade-off curve between task improvement and capability retention

**Baseline Methods**:
- No regularization (pure RL)
- Standard full-policy KL
- KL with lower β (relaxed constraint)
- Activity regularization
- Importance-weighted replay

### Implementation Details

**Correctness Detection**:
- Task-dependent: For code, use execution; for QA, use gold reference
- Model-based: Train classifier to predict correctness
- Flexible: Allows different definitions for different tasks

**Training Algorithm**:
```
Initialize π_θ with base model
While not converged:
  Collect trajectories from target environment
  Compute rewards R(τ) for trajectories
  
  For each (state, action) pair:
    Compute A(s,a) = advantage estimate
    Predict correct(s,a) using correctness model
    
  Compute loss:
    L_rl = -E[log π_θ(a|s) × A(s,a)]
    L_kl = E[mask(correct) × log(π_θ/π_ref)]
    L_total = L_rl + β × L_kl
    
  Update π_θ via gradient descent
  Optionally update π_ref to be π_θ with decay
```

**Hyperparameters**:
- β: KL weight (can be larger with conditional KL)
- τ: Decay rate for reference model updates
- Correctness threshold: How conservative in defining "correct"
- Adapter parameters: Task-specific fine-tuning parameters

## Practical Applications & Use Cases

### Software Development

- **Specialized code generators**: RL agents learning domain-specific coding patterns while maintaining general programming knowledge
- **Debugging assistants**: Learning to fix domain-specific bugs without forgetting basic programming constructs
- **API learning**: Adapting to new APIs or frameworks while preserving knowledge of standard libraries

### Knowledge-Intensive Tasks

- **Domain adaptation**: Fine-tuning on specialized knowledge (medical, legal) without losing general knowledge
- **Multi-language models**: Improving performance on target languages while preserving others
- **Factual reasoning**: Learning task-specific reasoning while maintaining factual accuracy

### Creative and Complex Tasks

- **Style transfer**: Learning target style or genre while preserving writing quality
- **Personalization**: Adapting to user preferences without losing general competence
- **Multi-objective optimization**: Balancing multiple goals without catastrophic trade-offs

### Safety-Critical Applications

- **Alignment preservation**: Learning new capabilities while maintaining safety constraints
- **Medical AI**: Improving performance on specific diagnoses while maintaining quality across domains
- **Financial AI**: Learning domain-specific strategies while maintaining risk management capabilities

## Insights & Implications

### Broader Field Impact

1. **Fundamental advance in capability preservation**
   - Solves critical problem in RLHF and RL fine-tuning
   - Enables safer, more targeted LLM adaptation
   - Relevant to any learning from feedback paradigm

2. **Reframes regularization theory**
   - Shows uniform regularization is suboptimal
   - Suggests broader applicability to conditional constraints
   - Opens research into task-specific and behavior-specific regularization

3. **Practical deployment implications**
   - Enables more confident RL deployment in production systems
   - Reduces risk of capability degradation
   - Suggests path to real-time adaptation without retraining

4. **Connections to continual learning**
   - Addresses stability-plasticity dilemma from continual learning literature
   - Shows connections between RLHF and continual learning theory
   - Suggests unified framework for incremental learning

### Limitations & Open Questions

- **Correctness definition**: Requires explicit definition of "correct" for target task
- **Computational overhead**: Detecting correctness adds computational cost
- **Scalability**: Efficiency of correctness detection at very large scales unclear
- **Theoretical guarantees**: Formal convergence analysis not provided
- **Transfer and generalization**: How well does this work across very different task distributions?

### Future Research Directions

1. **Learning correctness definitions**: Automatically discover which behaviors to preserve
2. **Dynamic regularization**: Adapt β and correctness thresholds during training
3. **Multi-task regularization**: Extend to scenarios with multiple concurrent tasks
4. **Theoretical analysis**: Formal convergence and optimality guarantees
5. **Causal perspective**: Identifying causal mechanisms behind capability preservation
6. **Meta-regularization**: Learning task-specific regularization strategies

## Code & Resources

**Authors**: Li Wang, Xiaodong Lu, Xiaohan Wang, Jiajun Chai, Wei Lin, Tianhao Peng, and Guojun Yin

**Submission Status**: Submitted to AAAI 2027

**Available Resources**:
- arXiv preprint: [https://arxiv.org/abs/2608.01743](https://arxiv.org/abs/2608.01743)
- HTML version: [https://arxiv.org/html/2608.01743](https://arxiv.org/html/2608.01743)
- Code: Contact authors for implementation details (available upon request)

**Estimated Requirements**:
- GPU: Single A100 or V100 for most experiments
- Training time: Hours to days depending on model size and task
- Model size: Compatible with 7B-70B parameter models
- Dependencies: PyTorch, transformers, RL libraries (ray, stable-baselines3)

**Quick-Start Implementation**:
1. Load base LLM and task-specific reward/correctness model
2. Define correctness criterion for your task
3. Replace standard KL loss with conditional KL computation:
   - For each response, compute correctness prediction
   - Only apply KL penalty when correctness is high
4. Train with policy gradient method (PPO, GRPO, etc.)
5. Evaluate on both target task and base capabilities

## Related Work & Context

### Foundational Research

- **KL regularization**: Classic approach to constraining policy drift in RL (Policy Gradient Theorem)
- **Stability-plasticity dilemma**: Fundamental challenge in continual learning (French, 1999)
- **RLHF for LLMs**: Recent work on human feedback for language model alignment
- **Catastrophic forgetting**: Long-studied problem in continual learning and transfer learning

### Recent Related Papers

- [Maintaining Plasticity in Continual Learning via Regenerative Regularization](https://arxiv.org/pdf/2308.11958) - Plasticity-preserving techniques in continual learning
- [A Study of Plasticity Loss in On-Policy Deep Reinforcement Learning](https://proceedings.neurips.cc/paper_files/paper/2024/file/ce7984e36d58659211a8dc7d5457cd6f-Paper-Conference.pdf) - Analysis of plasticity loss in RL
- [PLASTIC: Improving Input and Label Plasticity for Sample Efficient Reinforcement Learning](https://arxiv.org/pdf/2306.10711) - Plasticity-aware RL methods
- [Maintaining Plasticity in Deep Continual Learning](https://arxiv.org/pdf/2306.13812) - Continual learning approaches to plasticity

### Potential Future Research

1. **Automatic correctness detection**: Learning to identify correct behaviors without explicit labels
2. **Adaptive regularization**: Dynamically adjust regularization strength based on learning progress
3. **Hierarchical regularization**: Conditional constraints at multiple abstraction levels
4. **Multi-task variants**: Handling multiple concurrent objectives and constraints
5. **Uncertainty-aware regularization**: Account for uncertainty in correctness predictions
6. **Causal regularization**: Regularize based on causal importance rather than just correctness

**Paper ID:** arXiv:2608.01743  
**Submission Date:** August 3, 2026  
**Submission Target:** AAAI 2027  
**Authors:** Li Wang, Xiaodong Lu, Xiaohan Wang, Jiajun Chai, Wei Lin, Tianhao Peng, Guojun Yin
