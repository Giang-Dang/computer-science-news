# AugMask: Training Diffusion Models on Incomplete Tabular Data via Stochastic Augmentation and Masking

**ArXiv ID:** 2606.03347  
**Submitted:** June 2, 2026  
**Authors:** Jungkyu Kim, Taeyoung Park, Kibok Lee

## Executive Summary

This paper introduces AugMask, a plug-and-play training framework that enables diffusion models to handle incomplete tabular data with missing values. Rather than requiring expensive data imputation or specialized missing-aware architectures, AugMask uses conditional stochastic augmentation to construct plausible context-dependent inputs and applies denoising supervision only to observed coordinates. The approach is theoretically grounded in Rao-Blackwellized estimation and demonstrates state-of-the-art performance across diverse datasets with varying missingness patterns, enabling standard diffusion-based tabular generators to outperform specialized missing-aware baselines.

## Problem Statement

Tabular data generation has become increasingly important for privacy-preserving data sharing and synthetic data creation. However, real-world tabular datasets frequently contain missing values, presenting a fundamental challenge:

1. **Standard Diffusion Assumption**: Score-based diffusion models assume fully specified inputs, yet real-world tabular data often contains missing entries
2. **Imputation Costs**: Preprocessing missing data through imputation is expensive and introduces bias based on choice of imputation method
3. **Backbones Are Missing-Unaware**: Standard transformer and neural network backbones used in diffusion models don't explicitly handle missing values
4. **Training Data Loss**: Existing approaches often discard partially observed records or require expensive specialized architectures
5. **Uncertainty Representation**: Proper treatment must represent uncertainty in missing values during training, not assume confident completions

Traditional solutions (mean imputation, KNN imputation, EM algorithms) lose information about missingness patterns and can bias synthetic data generation.

## Core Concepts & Theory

### Score-Based Diffusion Models

The forward process gradually adds noise to data:
```
x_t = √(ᾱ_t) x_0 + √(1 - ᾱ_t) ε,  where ε ~ N(0, I)
```

The reverse process learns to denoise:
```
score_model: ∇_x log p(x_t) ≈ -(x_t - x_0) / (1 - ᾱ_t)
```

The model is trained to predict the original data x_0 from noisy observations.

### The Missing Data Challenge

In incomplete data, we observe:
- O ⊂ {1, ..., d}: Set of observed dimensions
- x_O: Observed values in those dimensions
- x_M: Missing values (not observed during training)

Standard diffusion loss:
```
L = ||score_model(x_t) - actual_score||²
```

This requires knowing x (both O and M), but we only have x_O.

### AugMask Framework

AugMask addresses this through two components:

1. **Conditional Stochastic Augmentation (CSA)**:
   - Use lightweight auxiliary models to generate plausible values for x_M given x_O
   - Crucially: Multiple stochastic samples, not deterministic imputation
   - Captures uncertainty in missing values
   - Each training sample gets different augmentation, providing data diversity

2. **Masked Supervision**:
   - Apply denoising loss only to observed coordinates:
   ```
   L = Σ_{i∈O} ||score_model[i](x_t^aug) - actual_score[i]||²
   ```
   - Ignore loss on coordinates corresponding to originally missing values
   - Model learns to denoise observed values given uncertain augmentations

### Theoretical Justification: Rao-Blackwellization

The paper connects masked supervision to Rao-Blackwellized (RB) estimation:

1. **Original Objective**: Learn score function for fully observed data
2. **RB Marginalization**: When marginalizing over missing entries:
   ```
   E_missing[L] = E_missing[Σ_i (pred[i] - true[i])²]
                = Σ_i E_missing[(pred[i] - true[i])²]  (for observed i)
                + Σ_i E_missing[(pred[i] - true[i])²]  (for missing i)
   ```
3. **Key Insight**: Marginalizing over uncertain x_M (treating as random) introduces variance-weighted penalty that discourages over-reliance on uncertain augmentations

### Stochasticity is Critical

Unlike deterministic imputation:
- **Deterministic**: Commits to one completion, model learns to use that value confidently
- **Stochastic**: Different completions each epoch, model learns uncertainty-aware behavior
- **Variance Penalty**: Variance in augmentations induces implicit regularization

## Main Ideas & Contributions

1. **Plug-and-Play Design**: AugMask works with any diffusion backbone (transformer, MLP, etc.) without architectural changes

2. **Separation of Concerns**:
   - Conditioning: Lightweight auxiliary models generate plausible augmentations
   - Supervision: Denoising loss focuses only on truly observed values
   - Clear separation enables modularity

3. **Theoretical Foundation**: Grounded in Rao-Blackwellized estimation theory, providing principled justification for stochastic augmentation

4. **Variance Penalty**: Mathematically connects stochasticity to regularization that prevents overfitting to uncertain augmentations

5. **Flexibility**: Works across different missingness patterns, mechanisms (MCAR, MAR, MNAR), and datasets without retraining

6. **Empirical Strength**: Outperforms specialized missing-aware baselines across diverse datasets and missingness regimes

## Methodology & Implementation

### Training Procedure

**Phase 1: Auxiliary Model Training**
- Train lightweight models (KNN, MLP, etc.) on complete records to estimate P(x_M | x_O)
- These generate context-dependent augmentations for missing values

**Phase 2: Diffusion Model Training with AugMask**
```
For each batch:
  1. Sample incomplete records with missing values x_O
  2. Augment missing dimensions: x_M^aug ~ P_aux(·|x_O)
  3. Combine: x_aug = [x_O, x_M^aug]
  4. Add noise: x_t = √(ᾱ_t) x_aug + √(1 - ᾱ_t) ε
  5. Compute loss only on observed coordinates:
     L = Σ_{i∈O} ||model(x_t)[i] - denoise_target[i]||²
```

### Datasets and Benchmarks

[Exact figures unavailable — see full paper]

Tested across:
- Multiple tabular datasets with natural missing values
- Synthetic missingness at varying levels (MAR, MCAR, MNAR)
- Different types of data (numerical, categorical)

### Evaluation Metrics

- **Imputation Quality**: Accuracy of filled-in values compared to ground truth
- **Synthetic Data Quality**: Distributional similarity of generated data to original
- **Benchmark Datasets**: Standard tabular generation benchmarks

### Results

AugMask enables standard diffusion-based tabular generators to **outperform specialized missing-aware baselines** across:
- Diverse datasets
- Multiple missingness patterns (MCAR, MAR, MNAR)
- Varying missingness levels

## Practical Applications & Use Cases

1. **Healthcare Data**: Handle missing medical records for synthetic patient data generation (privacy-preserving research)
2. **Financial Data**: Generate synthetic transaction and credit datasets with naturally occurring missing values
3. **E-commerce Data**: Synthetic customer behavior data with incomplete user profiles
4. **Sensor Networks**: Generate synthetic sensor readings from distributed IoT devices with communication gaps
5. **Survey Data**: Handle missing survey responses common in social science datasets
6. **Data Augmentation**: Synthetic data generation for datasets with missing entries to improve downstream ML
7. **Privacy Protection**: Synthetic data generation enables sharing sensitive datasets with missing values without privacy breaches
8. **Data Imputation**: Use trained diffusion model as imputation method itself

## Insights & Implications

1. **Simplicity Over Complexity**: A simple framework (lightweight augmentation + masked loss) outperforms complex specialized architectures

2. **Stochasticity as Regularization**: The variance induced by stochastic augmentation provides implicit regularization against overfitting to uncertain values

3. **Flexible Framework**: Single method works across different missingness mechanisms and patterns without adaptation

4. **Auxiliary Models Effectiveness**: Even simple auxiliary models (KNN, MLP) sufficient for conditional augmentation; no need for complex generative models

5. **Theoretical Grounding Matters**: Connecting to Rao-Blackwellized estimation provides confidence that the approach is not heuristic

6. **Data Efficiency**: Enables use of incomplete records during training, recovering signal from partially observed data

## Limitations & Open Questions

1. **Auxiliary Model Choice**: How sensitive is performance to choice of auxiliary model architecture and capacity?

2. **Computational Overhead**: What is the computational cost of auxiliary model augmentation compared to baseline diffusion training?

3. **Scalability to Large Datasets**: How does the approach scale to million-row tabular datasets? Memory requirements for auxiliary models?

4. **Complex Dependencies**: How well does the approach handle complex dependencies between missing values (e.g., if feature A is missing, feature B is likely missing)?

5. **Mixed Data Types**: Performance on datasets with mixed numerical, categorical, and text columns?

6. **Missingness Mechanism Agnostic**: While claims to work across mechanisms, formal analysis of when approach might fail would be valuable

## Code & Resources

- **Paper**: https://arxiv.org/abs/2606.03347
- **Official Implementation**: [Not yet provided in search results]
- **Dependencies**: PyTorch, scikit-learn, standard generative modeling libraries
- **Compute Requirements**: GPU for diffusion model training; modest for auxiliary models

## Related Work & Context

### Related Papers on Diffusion and Missing Data

1. **MissDiff: Training Diffusion Models on Tabular Data with Missing Values** (2307.00467) - Prior work specifically for missing data
2. **Self-Supervision Improves Diffusion Models for Tabular Data Imputation** (2407.18013) - Self-supervised approach to imputation
3. **MissHDD: Hybrid Deterministic Diffusion for Heterogeneous Incomplete Data** (2511.14543) - Hybrid approach to missing data
4. **Diffusion Models for Tabular Data Imputation and Synthetic Data Generation** (2407.02549) - Broader work on tabular diffusion

### Related Work on Incomplete Data

1. **Imputation-free Learning of Tabular Data with Missing Values using Incremental Feature Partitions** (2504.14610) - Alternative imputation-free approach
2. **DeepIFSAC: Deep Imputation Using Feature and Sample Attention** (2501.10910) - Attention-based imputation

### Foundations

- **Score-Based Diffusion Models**: Theoretical foundations and implementations
- **Rao-Blackwellized Gradient Estimation**: Variance reduction technique from statistics
- **Missing Data Mechanisms**: MCAR, MAR, MNAR theory from statistics
- **Tabular Data Generation**: Prior work on GANs and VAEs for tabular data

### Future Research Directions

1. **Conditional Generation**: Extend to conditional generation given observed features
2. **Large-Scale Evaluation**: Systematic evaluation on datasets with millions of rows
3. **Benchmark Suite**: Develop standard benchmarks for missing-data-aware tabular generation
4. **Hybrid Approaches**: Combine AugMask with other efficiency improvements for diffusion models
5. **Theoretical Analysis**: Formal convergence guarantees and sample complexity analysis
6. **Real-World Deployment**: Case studies on actual healthcare, financial, and survey data
7. **Uncertainty Quantification**: Provide confidence intervals for filled-in values

## References & Further Reading

- **ArXiv**: https://arxiv.org/abs/2606.03347
- **MissDiff (Prior Work)**: https://arxiv.org/abs/2307.00467
- **Self-Supervised Imputation**: https://arxiv.org/abs/2407.18013
- **Hybrid Approaches**: https://arxiv.org/abs/2511.14543
