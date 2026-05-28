# Generative Recursive Reasoning

**ArXiv ID:** 2605.19376  
**Authors:** Junyeob Baek, Mingyu Jo, Minsu Kim (KAIST), Mengye Ren (New York University), Yoshua Bengio (Mila – Québec AI Institute), Sungjin Ahn (Université de Montréal)  
**Submitted:** May 19-20, 2026  
**Field:** Machine Learning, Reasoning, Generative Modeling

## Executive Summary

This paper introduces GRAM (Generative Recursive reAsoning Models), a framework that elevates recursive reasoning models from deterministic single-trajectory computation to probabilistic multi-trajectory reasoning. By modeling reasoning as stochastic latent trajectories, GRAM enables multiple solution hypotheses, alternative reasoning strategies, and principled inference-time scaling. With Yoshua Bengio among the co-authors, this work represents a significant advance in understanding and scaling reasoning capabilities in neural networks.

## Problem Statement

### Limitations of Existing Recursive Reasoning Models

Traditional Recursive Reasoning Models (RRMs) suffer from several critical limitations:

1. **Deterministic Convergence:** Follow a single latent trajectory, converging to one prediction even when multiple valid solutions exist
2. **No Hypothesis Exploration:** Cannot explore alternative reasoning paths or compare different solution strategies
3. **Fixed Inference Compute:** Inference cost fixed regardless of problem complexity
4. **Lack of Uncertainty:** No principled way to represent confidence in predictions or reasoning paths
5. **Single-Solution Bias:** Deterministic processing favors quick convergence over thorough exploration

### Research Gap

Prior work either:
- Used deterministic recursive models for point predictions
- Employed ensemble methods for uncertainty (computationally expensive)
- Lacked principled frameworks for multi-hypothesis reasoning

No prior work successfully unified probabilistic reasoning with recursive computation in a learnable, scalable framework.

## Core Concepts & Theory

### Generative Model Framework

GRAM models reasoning as a **stochastic latent trajectory**, treating the reasoning process as a sequence of latent random variables:

```
z₁ → z₂ → z₃ → ... → zₜ → prediction
   ↑    ↑    ↑           ↑
 sample from conditional distributions
```

Rather than deterministic transformations, each step in reasoning is stochastic, allowing:
- Multiple paths through latent space
- Different reasoning strategies for the same input
- Natural representation of uncertainty

### Probabilistic Modeling

**Conditional Distribution:**
```
p(y|x) = ∫ p(y|z₁,...,zₜ) p(z₁,...,zₜ|x) dz₁...dzₜ
```

The model learns:
- **Prior:** p(z₁) for initial reasoning state
- **Transition:** p(zₜ₊₁|zₜ, x) for recursive reasoning steps
- **Likelihood:** p(y|zₜ) for final prediction

**Unconditional Generation:**
With absent or fixed inputs, GRAM supports:
```
p(x) = ∫ p(x, z₁,...,zₜ) dz₁...dzₜ
```

This enables the model to generate solutions without specific input constraints.

### Mathematical Formulation

**Amortized Variational Inference:**

For training, GRAM uses amortized variational inference with:
- **Encoder q(z₁,...,zₜ|x,y):** Posterior over latent trajectories
- **Decoder p(y|z₁,...,zₜ):** Likelihood of outputs given trajectories
- **Prior p(z₁,...,zₜ):** Recursive latent variable distribution

**ELBO Objective:**
```
ELBO = E[log p(y|z)] - KL(q(z|x,y) || p(z|x))
```

Balances:
- Likelihood: Accurate predictions
- KL divergence: Matching learned posterior to prior

## Main Ideas & Contributions

### Primary Innovation: Probabilistic Multi-Trajectory Reasoning

GRAM transforms reasoning from:
- **Deterministic:** Single latent path → Single prediction
- **Stochastic:** Multiple latent paths → Distribution over predictions

### Key Technical Contributions

1. **Probabilistic Recursion:** First framework unifying probabilistic latent variable models with recursive computation
2. **Amortized Inference:** Efficient training strategy for complex latent variable models
3. **Multi-Hypothesis Support:** Native support for exploring multiple solution strategies simultaneously
4. **Inference-Time Scaling:** Principled way to trade computation for accuracy through trajectory sampling

### Advantages Over Alternatives

| Aspect | Deterministic RRM | Ensemble Methods | GRAM |
|--------|------------------|------------------|------|
| **Hypothesis Exploration** | No | Yes (via multiple models) | Yes (via sampling) |
| **Uncertainty** | None | Implicit | Explicit |
| **Training Efficiency** | High | Low (train multiple) | Medium |
| **Inference Flexibility** | Fixed | Fixed (ensemble size) | Variable (control sampling) |
| **Parameter Efficiency** | High | Low (K× models) | Medium (single model) |

### Intuition Behind Design Choices

**Why stochastic trajectories?**
- Reasoning involves exploration: multiple paths may be viable
- Biological reasoning is probabilistic, not deterministic
- Uncertainty is crucial for decision-making

**Why recursive?**
- Reasoning is iterative: solutions build on previous thoughts
- Allows sharing parameters across reasoning steps
- Matches human reasoning refinement process

**Why amortized inference?**
- More efficient than solving inference problem at test time
- Leverages all training data to learn shared inference mechanism
- Scales to complex problems

## Methodology & Implementation

### Model Architecture

**Recursive Latent Layer:**
```
z_t ~ p(z_t | z_{t-1}, x, t)
Each layer:
  - Takes previous latent state
  - Incorporates input information
  - Produces stochastic update
```

**Prediction Head:**
```
y ~ p(y | z_T, x)
Output distribution depends on final latent trajectory
```

**Posterior Encoder (training):**
```
q(z_1,...,z_T | x, y) = ∏_t q(z_t | z_{t-1}, x, y)
Reverse direction: uses both input and target for efficient inference
```

### Training Procedure

**Dataset Types:**
- Structured reasoning tasks (symbolic manipulation, constraint satisfaction)
- Multi-solution constraint satisfaction problems
- Tasks where multiple valid solutions exist

**Training Strategy:**
1. Encode input and target into posterior distribution
2. Sample latent trajectories from posterior
3. Compute ELBO loss
4. Backpropagate through stochastic sampling (reparameterization trick)
5. Iterate

**Optimization Details:**
- Amortized variational inference with reparameterization
- KL annealing: gradually increase KL weight during training
- Trajectory sampling during training for gradient estimation

### Experimental Evaluation

**Benchmarks:**
1. **Structured Reasoning:** Tasks requiring step-by-step logical reasoning
2. **Constraint Satisfaction:** Problems with multiple valid solutions
3. **Multi-Solution Tasks:** Benchmarks where exploring alternatives is critical

**Evaluation Metrics:**
- Accuracy on held-out test sets
- Coverage of diverse solution modes
- Uncertainty calibration
- Inference-time computation efficiency

**Key Results:**
- Improvements over deterministic RRMs on structured reasoning
- Better performance on multi-solution constraint satisfaction
- Successful generation without specific inputs
- Efficient inference-time scaling through trajectory sampling

**Specific Performance Numbers:**
[Exact figures unavailable — see full paper for complete benchmark results]

### Ablations Studies

Likely ablations:
- Recursive depth: Impact of number of reasoning steps
- Trajectory sampling: Effect of number of samples at inference time
- Stochasticity: Comparison with deterministic variant
- Inference strategy: Different sampling and aggregation methods

## Practical Applications & Use Cases

### High-Impact Domains

1. **Scientific Discovery & Theorem Proving:**
   - Multiple proof strategies for same theorem
   - Efficient exploration of solution space
   - Generate novel hypotheses and solutions

2. **Combinatorial Optimization:**
   - Multiple near-optimal solutions for routing problems
   - Constraint satisfaction with diverse solutions
   - Real-time solution generation with variable compute

3. **Creative & Design Tasks:**
   - Generate diverse design options
   - Explore alternative architectural solutions
   - Multi-solution generation for brainstorming

4. **Decision Support Systems:**
   - Present multiple reasoning pathways
   - Uncertainty quantification for decisions
   - Interpretable alternative recommendations

5. **Planning & Robotics:**
   - Generate multiple action plans
   - Rank plans by reasoning confidence
   - Adaptive planning with resource constraints

### Real-World Examples

- **Automated Theorem Proving:** Find alternative proofs, compare proof strategies
- **Software Testing:** Generate diverse test cases and reasoning about coverage
- **Medical Diagnosis:** Multiple diagnostic pathways with confidence scores
- **Game AI:** Multi-strategy planning with adaptive compute
- **Supply Chain:** Alternative solutions for resource allocation problems

### Implementation Feasibility

**Advantages:**
- Principled probabilistic framework
- Single model vs. ensembles (parameter efficient)
- Flexible inference-time computation
- Naturally interpretable (reasoning trajectories)

**Challenges:**
- Training complexity (variational inference)
- Requires problems with multiple solutions for benefits
- May not improve single-solution tasks
- Posterior collapse risk (KL term vanishes)

## Insights & Implications

### Broader Field Impact

1. **Reasoning Architectures:** Demonstrates power of recursive+probabilistic combination
2. **Uncertainty in AI:** Better framework for principled uncertainty in neural networks
3. **Inference-Time Scaling:** New paradigm for trading compute for accuracy
4. **Interpretability:** Reasoning trajectories provide natural interpretability

### Limitations & Open Questions

1. **Scaling:** How well does GRAM scale to very complex reasoning tasks?
2. **Generalization:** Do learned reasoning strategies transfer across domains?
3. **Efficiency:** How does training time compare to simpler alternatives?
4. **Curriculum Learning:** What curriculum helps train better trajectories?
5. **Posterior Collapse:** How to prevent KL term from vanishing?

### Future Research Directions

1. **Hierarchical Reasoning:** Multi-level recursive reasoning with different scales
2. **Structured Representations:** Integration with symbolic reasoning systems
3. **Continual Learning:** How to extend trajectories for continual reasoning
4. **Cross-Domain Transfer:** Knowledge transfer across reasoning tasks
5. **Theory & Analysis:** Better understanding of learned reasoning strategies
6. **Human-AI Collaboration:** Using trajectories for human-in-the-loop reasoning

## State-of-the-Art Advancement

- **First unified framework** for probabilistic recursive reasoning
- **Competitive performance** on structured reasoning benchmarks
- **Superior capability** for multi-solution exploration
- **Principled inference-time scaling** through trajectory sampling
- **Strong theoretical foundation** from probabilistic modeling

## Code & Resources

### Official Resources
- **Paper:** https://arxiv.org/abs/2605.19376
- **ArXiv ID:** 2605.19376

### Dependencies & Requirements
- PyTorch or JAX for implementation
- GPU support for efficient training (40GB+ VRAM recommended)
- Structured reasoning datasets (custom or public benchmarks)

### Quick-Start Guide
[Implementation guidance and code expected — check repository for details]

## Related Work & Context

### Related Papers & Methods

1. **Recursive Neural Networks:** Foundation for recursive computation
2. **Variational Autoencoders (VAEs):** Probabilistic latent variable modeling
3. **Neural Module Networks:** Compositional reasoning with neural networks
4. **Diffusion Models:** Alternative probabilistic generative approach
5. **In-Context Learning:** Reasoning through few-shot examples

### Prior Work Foundations

- Variational inference and ELBO optimization (Kingma & Welling, 2013)
- Sequence models and RNNs (Hochreiter et al., 1997)
- Neural module networks and compositional reasoning
- Uncertainty quantification in deep learning
- Probabilistic graphical models

### Possible Future Research Directions

1. **Hybrid Models:** Combining GRAM with Transformers for longer reasoning
2. **Metalearning:** Learning how to reason better across tasks
3. **Causal Reasoning:** Integration with causal inference frameworks
4. **Self-Supervised Reasoning:** Learning reasoning from unlabeled data
5. **Reasoning-Aware Architectures:** Designing networks with reasoning in mind
6. **Benchmark Development:** Creating standardized multi-solution reasoning benchmarks
