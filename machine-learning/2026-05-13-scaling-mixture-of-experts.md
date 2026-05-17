# How to Scale Mixture-of-Experts: From muP to the Maximally Scale-Stable Parameterization

**ArXiv ID:** 2605.14200  
**Submitted:** May 13, 2026  
**Authors:** [See official paper]  
**Field:** Machine Learning / Deep Learning Architecture

## Executive Summary

This paper addresses a critical gap in Mixture-of-Experts (MoE) scaling by developing a principled approach to hyperparameter scaling across network width, expert width, number of experts, sparsity, and depth. Building on the Maximum Update Parametrization (muP) framework, the authors derive the Maximally Scale-Stable Parameterization (MSSP) for MoE architectures, enabling stable and optimal scaling laws that hold across model sizes and training durations—a foundational advance for next-generation large-scale sparse models.

## Problem Statement

### Research Gap and Limitations

Despite the widespread adoption of Mixture-of-Experts architectures in large language models and vision transformers, fundamental questions about scaling remain unanswered:

1. **Hyperparameter Transfer Failure**: Traditional hyperparameters optimized for small models often fail to work at scale
2. **Multi-Dimensional Scaling Complexity**: MoE scaling involves 5+ independent dimensions (width, expert width, expert count, sparsity, depth), with unclear interaction effects
3. **Unstable Training Dynamics**: Models exhibit different learning curves at different scales, complicating reproducibility and cost estimation
4. **Expert Utilization Imbalance**: Load balancing and expert specialization properties change non-uniformly with scale
5. **Computational Cost Uncertainty**: Inability to predict training cost and optimal configurations for new scales

### Prior Work Limitations

Previous scaling research has fallen short:
- **Chinchilla Scaling Laws**: Derived for dense models; unclear how principles extend to sparse MoE
- **muP Framework**: Provides width-scaling guarantees for dense networks but not sparse architectures
- **Empirical MoE Papers**: Report results at specific scales without principled scaling prescriptions
- **Architecture Search**: Requires expensive grid search; no theoretical guidance for hyperparameter choices

## Core Concepts & Theory

### Maximum Update Parametrization (muP) Review

muP ensures that the learning rate and other hyperparameters remain stable as model width increases, achieving three key properties:
1. **Feature Learning**: Learned features transition smoothly with width
2. **Hyperparameter Transfer**: Small models' hyperparameters work at large scale
3. **Stable Training Dynamics**: Loss curves and training curves remain stable across scales

#### Key muP Insight:
```
For dense networks: Loss ∝ 1/width
Therefore: Learning rate, initialization must scale as 1/width
Result: Stable loss curves across all widths
```

### MoE-Specific Scaling Challenges

Standard muP breaks down for MoE due to:

1. **Gating Function Dynamics**: 
   - Gating network creates non-uniform scaling relationships
   - Expert load imbalance increases with scale
   - Router temperature requires scale-dependent tuning

2. **Sparsity Scaling Effects**:
   - Effective batch size per expert decreases as experts increase
   - Activation sparsity changes learning dynamics
   - Token-to-expert assignment becomes increasingly stochastic at scale

3. **Expert Specialization**:
   - Expert feature learning diverges from dense networks
   - Expert diversity-complexity trade-off shifts with scale
   - Routing entropy affects convergence properties

### Maximally Scale-Stable Parameterization (MSSP)

The paper derives MSSP by extending muP to MoE architectures through:

#### 1. **Width Scaling for Expert Networks**
```
For sparse networks with E experts and width W:

Expert Parameter Scale: σ_expert = 1/√E (instead of 1/√W)
Router Parameter Scale: σ_router = 1/√max(W, E)

Intuition: Expert parameters are shared across sparser subnetworks
```

#### 2. **Gating Function Scaling**
```
Router Temperature: τ ∝ √(W/E)
Auxiliary Loss Weight: λ ∝ 1/E

Effect: Load balancing becomes more important as E increases
```

#### 3. **Learning Rate Adaptation**
```
Base Learning Rate: lr ∝ 1/√W
Sparsity Correction: lr_adjusted = lr × √(E/total_tokens_per_expert)

Ensures stable gradient flow regardless of expert utilization
```

#### 4. **Sparsity Scaling**
```
Tokens Per Expert (dynamic): TPE = batch_size / E
Effective Batch Size Per Expert: EBSE = TPE × sparsity

Learning dynamics stable when: EBSE remains O(1) relative to expert hidden dimension
```

### Mathematical Framework

#### Parameterization for Layer i with Width W_i, E_i Experts:

**Weight Initialization:**
```
Expert weights: W_expert ~ N(0, σ²/n_in) where σ = 1/√E_i
Router weights: W_router ~ N(0, τ²/n_in) where τ = 1/√max(W_i, E_i)
```

**Gradient Flow Analysis:**
```
∂L/∂W_expert ∝ gradient_scale × 1/E_i (not 1/W_i)
∂L/∂W_router ∝ gradient_scale × 1/max(W_i, E_i)

Result: Stable gradient magnitudes as (W_i, E_i) grow
```

#### Learning Rate Schedule:

```
lr(W) = lr_base / √W
lr_final = lr_base / √(W × correction_factor(E, sparsity))

Correction factor accounts for reduced effective batch size per expert
```

### Comparison with Alternative Approaches

| Aspect | Empirical Tuning | Dense muP | MSSP (MoE-muP) |
|--------|-----------------|-----------|----------------|
| Hyperparameter Transfer | No | Yes (dense only) | Yes (sparse + dense) |
| Stability Across Scales | Varies | High (W scaling) | High (W, E, sparsity) |
| Training Cost Prediction | Unreliable | Good | Excellent |
| Expert Load Balancing | Manual tuning | N/A | Principled |
| Inference Cost Scaling | Unpredictable | Linear | Controlled |
| Empirical Coverage | Limited | 2-3 scales | 4-5+ scales tested |

## Main Ideas & Contributions

### 1. **Unified Scaling Framework for MoE**
- First principled scaling theory specifically for sparse mixture-of-experts architectures
- Extends muP framework to handle architectural sparsity
- Provides complete hyperparameter prescription as function of (W, E, experts_width, sparsity, depth)

### 2. **Stability Theorem for Sparse Networks**
- Proves that appropriately parameterized MoE networks maintain stable training dynamics across scales
- Shows expected loss follows predictable scaling laws
- Demonstrates hyperparameter transfer properties hold empirically

### 3. **Sparsity-Aware Learning Rate Schedule**
- Novel learning rate correction that accounts for reduced effective batch size per expert
- Maintains stable gradient flow despite decreasing tokens-per-expert ratio
- Works across different sparsity levels (1/32, 1/64, 1/128)

### 4. **Expert Balancing Principles**
- Quantifies relationship between router temperature, expert count, and load balance
- Derives auxiliary loss weight scaling with expert count
- Predicts expert specialization behavior at scale

### 5. **Empirical Validation Across Six Orders of Magnitude**
- Validates theory from 100M to 1T parameter models
- Shows transfer works for models 100-1000x size differences
- Demonstrates cost savings through accurate scaling prediction

## Methodology & Implementation

### Experimental Setup

#### Model Architectures Tested
1. **Dense Baselines**: Standard Transformer, Dense-1B to Dense-100B
2. **Sparse MoE**: Expert counts 32→2048, Expert width 1x→16x
3. **Configurations**: 
   - Token-to-expert ratio: 1:4 to 1:256
   - Sparsity levels: 1/32 to 1/256 top-k routing
   - Depths: 12→96 transformer blocks

#### Datasets and Training
- **Language Modeling**: The Pile, LAION, mix of web data
- **Training Duration**: 300B to 10T tokens
- **Optimization**: Adam with standard schedules
- **Batch Sizes**: Dynamic to maintain constant tokens-per-expert

#### Evaluation Metrics
- **Convergence Speed**: Number of tokens to reach loss plateau
- **Hyperparameter Sensitivity**: Variation in final loss across ±10% parameter changes
- **Transfer Success Rate**: Percentage of configurations working without retuning
- **Cost Efficiency**: FLOPs required to reach target loss

### Key Results

#### Transfer Learning Success
- **Small-to-Large Transfer**: 97% of hyperparameters transfer from 1B to 100B models
- **Setting-Specific Changes**: Only router temperature and auxiliary loss weight require minor adjustments
- **Downstream Task Transfer**: Fine-tuning hyperparameters also follow MSSP rules

#### Scaling Law Validation

**Loss Scaling with Model Capacity:**
```
Loss ≈ C₁ × (FLOPs)^(-α) 

where α ≈ 0.08-0.12 (consistent across MoE and dense)
and C₁ depends on (W, E, sparsity) configuration
```

**Surprising Finding**: Scaling exponent remains nearly identical between dense and sparse models when properly parameterized.

#### Expert Utilization
- Load balance metrics improve with MSSP parameterization
- Expert redundancy (duplicate routes) decreases by 15-40%
- Expert specialization becomes more pronounced at scale (good property)

#### Training Efficiency
- 30-50% reduction in hyperparameter search costs
- Accurate cost prediction within ±15% for new configurations
- Optimal configurations identifiable without extensive tuning

### Ablation Studies

1. **Width Scaling Component**:
   - Using 1/√W: loss diverges 2-3x at 100B scale
   - Using 1/√E: achieves stable training
   - Combination 1/√max(W,E): optimal for all regimes

2. **Router Temperature Scaling**:
   - Fixed temperature: load balance degrades with E
   - τ ∝ √(E): maintains <5% load imbalance across all E
   - Incorrect scaling: >50% load imbalance at large E

3. **Auxiliary Loss Weight**:
   - Constant λ: causes gradient oscillations at large E
   - λ ∝ 1/E: smooth training dynamics
   - Effect size: 10-20% convergence speed difference

## Practical Applications & Use Cases

### 1. **Large Language Model Scaling**
- **Challenge**: Designing models like GPT-5, Claude-4 with 10T+ parameters
- **Solution**: MSSP predicts optimal MoE configurations without expensive trials
- **Impact**: 50% reduction in training cost for architecture search
- **Example**: Configuring 1T parameter model with 512-4096 experts

### 2. **Efficient Model Deployment**
- **Challenge**: Different compute budgets (edge devices to data centers)
- **Solution**: MSSP guides trade-offs between width, depth, and expert count
- **Impact**: Optimal models at any target latency/compute budget
- **Example**: 10B mobile model vs 100B data center model with consistent hyperparameters

### 3. **Vision Model Scaling**
- **Challenge**: Applying MoE to vision transformers (ViT with experts)
- **Solution**: Spatial attention routing benefits from MSSP theory
- **Impact**: 2-3x speedup for vision model training at scale
- **Example**: Scaling vision transformers from 1B to 100B parameters

### 4. **Multi-Modal Model Development**
- **Challenge**: Balancing text, image, and audio routing in unified model
- **Solution**: MSSP provides guidance for expert allocation across modalities
- **Impact**: Principled approach to multi-modal architecture design
- **Example**: Unified model with separate text/vision expert pools

### 5. **Continual Learning and Model Expansion**
- **Challenge**: Adding experts to existing trained model
- **Solution**: MSSP predicts new hyperparameters for expanded model
- **Impact**: No-reset training for model expansion
- **Example**: Growing model from 256 to 1024 experts online

### Implementation Challenges

1. **Distributed Training Complexity**: Maintaining sparsity patterns across devices
2. **Load Balancing Overhead**: Auxiliary losses add 5-10% computation
3. **Expert Redundancy**: Some experts underutilized despite tuning
4. **Dynamic Sparsity**: Token-to-expert ratios vary with sequence length
5. **Numerical Stability**: Softmax over many experts requires careful implementation

## Insights & Implications

### Broader Field Impact

1. **Democratization of Model Scaling**: Organizations no longer need massive compute budgets for hyperparameter search
2. **Reproducibility**: Consistent scaling laws enable more reliable model comparisons
3. **Architectural Exploration**: Faster iteration on new MoE variants
4. **Cost Reduction**: Industry-wide reduction in training carbon footprint through better efficiency

### State-of-the-Art Advancement

- **Previous Approach**: Empirical hyperparameter tuning at each scale (months of work)
- **MSSP Contribution**: Principled transfer from small models (days of work)
- **Accuracy Maintained**: No loss of performance quality
- **Cost Reduction**: 50-70% decrease in architecture search overhead

### Theoretical Implications

1. **Universality of Scaling Laws**: Suggests deep principles governing neural network behavior regardless of density
2. **Sparse vs Dense Equivalence**: Under proper parameterization, sparse and dense networks follow similar dynamics
3. **Compositionality of Scale**: Complex scaling behaviors decompose into interpretable components

### Limitations and Open Questions

1. **Expert Specialization**: Theory predicts emergence but doesn't explain why certain specializations occur
2. **Dynamic Routing**: How to handle sequence-length-dependent sparsity patterns?
3. **Domain-Specific Variations**: Do different domains (vision, language, code) require different scaling constants?
4. **Hardware-Software Codesign**: How should MSSP adapt to different hardware architectures?
5. **Conditional Computation**: Can theory extend to conditional layer skipping and other dynamic execution?

### Future Research Directions

1. **Multi-Task MoE Scaling**: Theory for shared experts across diverse task sets
2. **Adaptive Expert Allocation**: Automatic determination of optimal expert count for given capacity
3. **Hardware-Aware MSSP**: Scaling parameterization optimized for specific accelerators
4. **Lifelong Learning**: Scaling rules for continually growing model architectures
5. **Interpretable Experts**: Understanding what each expert specializes in at scale

## Code & Resources

### Official Resources
- **ArXiv Paper**: https://arxiv.org/abs/2605.14200
- **Supplementary Material**: Includes scaling law tables and hyperparameter prescriptions

### Dependencies
- **PyTorch**: 2.0+
- **DeepSpeed**: For distributed training with MoE
- **Megatron-LM**: Reference implementation with MSSP parameterization
- **NVIDIA Apex**: Optional, for mixed-precision training

### Compute Requirements
- **Training Reference Models**:
  - 8×A100 80GB: Full scaling study from 1B to 100B takes ~4 weeks
  - 16×H100: Equivalent study takes ~2 weeks
  - 64×H100: Full validation with multiple random seeds takes ~1 week

- **Inference**:
  - Latency: Scales with (W/E) × expert_latency + router_latency
  - Typical: ~50ms for 100B model with 1024 experts, batch size 32

### Quick Start Guide

```python
from megatron.core.models.mixture_of_experts import MoE
from mssp import MSSpParameterizer

# Define MoE configuration
config = {
    'width': 4096,
    'num_experts': 256,
    'expert_width': 16384,
    'sparsity': 1/64,  # top-k sparsity
    'depth': 32
}

# Apply MSSP parameterization
parameterizer = MSSpParameterizer()
scaled_config = parameterizer.get_hyperparameters(config)

print(f"Learning rate: {scaled_config['lr']}")
print(f"Router temperature: {scaled_config['router_temp']}")
print(f"Auxiliary loss weight: {scaled_config['aux_loss_weight']}")

# Create model with scaled hyperparameters
model = MoE(config, **scaled_config)
```

## Related Work & Context

### Related Recent Papers

1. **Mixture of Experts in Dense Transformers**: Shazeer et al., 2019
   - Pioneering work on combining MoE with transformer architectures
   - Basis for modern sparse LLMs

2. **muP: Tensor Programs III**: Yang et al., 2021
   - Foundational work on hyperparameter transfer across scales
   - Theoretical framework extended in this work

3. **Chinchilla Scaling Laws**: Hoffmann et al., 2022
   - Optimal compute allocation between model size and data
   - Adapted for sparse models in this work

4. **Switch Transformers**: Lepikhin et al., 2021
   - Simple routing mechanism for extreme sparsity
   - Example application of MSSP principles

5. **Expert Choice Routing**: Zhou et al., 2022
   - Alternative routing mechanism (tokens choose experts)
   - Compatible with MSSP framework

### Prior Work Foundations

- **Deep Learning Theory**: Universal approximation and optimization dynamics
- **Scaling Laws**: Emergent capabilities and predictable learning curves
- **Distributed Training**: Communication patterns in sparse architectures
- **Neural Architecture Search**: Efficient configuration space exploration

### Possible Future Research Directions

1. **Cross-Architecture Transfer**: MSSP for attention variants, RNN-like models
2. **Data-Dependent Sparsity**: Routing patterns that depend on input characteristics
3. **Energy-Aware Scaling**: Incorporating power consumption into scaling laws
4. **Federated MoE Training**: Scaling across multiple organizations
5. **Automated Scaling Discovery**: ML-based discovery of scaling laws for new architectures

## Summary

"How to Scale Mixture-of-Experts: From muP to the Maximally Scale-Stable Parameterization" represents a major theoretical and practical advance in deep learning architecture design. By extending the muP framework to sparse architectures, the paper provides the first principled approach to MoE hyperparameter scaling, enabling stable training dynamics across model sizes, expert counts, and sparsity levels. The implications are profound: organizations can now reliably design and scale large sparse models without expensive empirical search, democratizing access to cutting-edge architecture design. As MoE becomes increasingly central to next-generation AI systems, this theoretical foundation will prove invaluable.
