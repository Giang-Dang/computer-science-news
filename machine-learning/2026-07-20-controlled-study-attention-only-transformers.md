# A Controlled Study of Attention-Only Transformers

**Authors:** Henry Ndubuaku, Karen Mosoyan, Jakub Mroz, Noah Cylich, Satyajit Kumar, Parkirat Sandhu, Roman Shemet, Justin H Lee

**ArXiv ID:** 2607.18363

**Date:** July 20, 2026

**Categories:** Machine Learning, Transformer Architecture, Model Design

## Executive Summary

This paper rigorously investigates whether feed-forward networks are necessary in transformer architectures through carefully controlled experiments. By comparing attention-only transformers (Simple Attention Networks, or SANs) against standard transformers while precisely matching parameter counts, training FLOPs, and depth, the authors find that attention-only architectures can match standard transformer performance when given equivalent computational resources. This finding challenges the conventional assumption that feed-forward layers are essential to transformer design and has significant implications for model architecture optimization.

## Problem Statement

Traditional transformer architectures consist of both multi-head self-attention layers and feed-forward networks (FFNs), where FFNs account for approximately two-thirds of non-embedding parameters. Despite their prevalence and widespread adoption, the necessity of feed-forward layers has not been rigorously tested through controlled experiments that simultaneously account for parameter count, computational budget, and architectural depth. This gap in architectural understanding motivates a systematic study to determine whether the quadratic compute of attention mechanisms can be effectively reallocated to create competitive attention-only alternatives.

## Core Concepts & Theory

### Transformer Architecture Basics

Standard transformers alternate between:
1. **Multi-head Self-Attention (MHSA)**: Captures relationships between all sequence positions with quadratic compute complexity
2. **Feed-Forward Networks (FFNs)**: Position-wise fully connected layers with linear activation patterns

The fundamental trade-off is computational: attention layers have lower parameter density per unit compute (due to quadratic compute) while FFNs have higher parameter density.

### Simple Attention Networks (SANs)

SANs are decoder-only transformers that remove feed-forward layers entirely, consisting only of stacked multi-head attention layers. This design requires deeper attention layers to maintain expressiveness, creating a different parameter-to-compute ratio compared to standard transformers.

### Controlled Experimental Design

The paper employs three distinct matching criteria:

1. **Parameter Matching**: Both architectures have the same total parameter count
2. **FLOPs Matching**: Both architectures use the same training compute budget
3. **Depth Matching**: Both architectures have the same number of layers

This multi-faceted matching approach isolates architectural differences from confounding factors.

## Main Ideas & Contributions

### Key Finding: Architecture Matters Less Than Resource Allocation

The study's central contribution is demonstrating that the choice between attention-only and standard transformers is less important than ensuring both receive appropriate computational resources:

1. **Direct Feed-Forward Deletion is Costly**: Removing FFNs without adjustment decreases performance by 0.47 nats (natural logarithmic loss units) when depth is matched
2. **Parameter-Matched Comparison**: When attention gets reallocated depth budget, the gap narrows to only 0.006 nats (0.27% of loss)
3. **Remarkable Reproducibility**: Results are reproducible to one part in ten thousand across different random seeds

### Insight: Parameter-Compute Tradeoff

Attention layers spend their compute budget differently than FFNs:
- Attention: Allocates compute to quadratic sequence similarity operations (parameter-sparse)
- FFNs: Allocates compute to parameter-dense position-wise transformations

By increasing attention depth and thereby the quadratic compute term, attention-only networks can recover performance despite having fewer parameters.

### Generalization Across Scales

The findings hold consistently across different training budgets:
- 5B token budget
- 30B token budget  
- 105B token budget (up to 1.5 epochs of reasoning-dense corpus)

This suggests the relationship between architecture and resource allocation is scale-invariant.

## Methodology & Implementation

### Experimental Setup

**Model Sizes:** 6M to 87M parameters (approximately 29x size range)

**Training Corpus:** 68B-token reasoning-dense corpus (up to 1.5 epochs = 105B tokens total)

**Architecture Variations Tested:**
- Layer depths: 2 to 48 layers across experimental arms
- Attention-only variants at each depth
- Standard transformers at matched depths

**Training Protocol:**
- Per-arm learning-rate sweeps to ensure fair comparison
- Reproducible randomization (testing across seed pairs)
- Measured in loss nats (base-e logarithmic units)

### Evaluation Metrics

**Primary Metric:** Loss in nats on validation set

**Performance Comparison Points:**
- Matched depth: 0.47 nats gap (unfavorable to SANs)
- Matched FLOPs: 0.26 nats gap  
- Matched parameters: 0.006 nats gap (0.27% loss)
- Across size range: Gap holds near 0.02 nats

### Results Summary

| Matching Criterion | Performance Gap (nats) | SANs Verdict |
|---|---|---|
| Depth-only matched | +0.47 | Significantly worse |
| FLOPs-only matched | +0.26 | Moderately worse |
| Parameters-only matched | +0.006 | Effectively tied |

[Exact figures unavailable — see full paper]

## Practical Applications & Use Cases

### Model Architecture Design

1. **Flexible Parameter Allocation**: Rather than assuming FFNs are necessary, architects can allocate parameters to depth based on computational constraints
2. **Efficient Scaling**: For parameter-constrained scenarios (mobile, edge devices), attention-only variants may be preferable
3. **Inference Optimization**: Attention-only networks with optimized depth may have different inference characteristics worth exploring

### Computational Efficiency

1. **Linear Scaling**: Attention-only variants could reduce memory bandwidth requirements compared to parameter-dense FFNs
2. **Hardware Alignment**: Different accelerator architectures may favor attention operations differently than FFNs
3. **Batch Size Implications**: Attention's quadratic compute may have different batch-size scaling properties

### Training Resource Planning

1. **Budget-Conscious Training**: Clear guidance on how to reallocate freed compute when removing FFNs
2. **Parameter Efficiency Tradeoffs**: Quantified understanding of parameter-compute relationships in transformers

## Insights & Implications

### Architectural Fundamentals

This work challenges the assumption that specific architectural components (FFNs) are universally necessary. Instead, it suggests that architectural necessity depends on how computational resources are distributed.

### State-of-the-Art Implications

The findings suggest that many transformer performance improvements attributed to specific components might actually reflect better resource allocation rather than fundamental architectural advances.

### Research Directions

1. **Hardware-Specific Optimization**: Different accelerators might benefit from attention-only designs differently
2. **Hybrid Architectures**: Exploring selective use of FFNs only where beneficial
3. **Theoretical Analysis**: Understanding why attention depth can substitute for FFNs from first principles
4. **Instruction Tuning**: How do these findings apply to fine-tuned models beyond pretraining?

### Limitations and Open Questions

1. The study focuses on decoder-only, causal language modeling tasks — encoder-decoder and bidirectional attention patterns may differ
2. Downstream task performance on evaluation benchmarks would complement pretraining loss metrics
3. Inference cost differences between architectures remain unexplored
4. Whether findings generalize to other modalities (vision, multimodal) is unclear

## Code & Resources

**Official Repository:** Not specified in abstract; likely available from authors' GitHub

**Paper Link:** https://arxiv.org/abs/2607.18363

**Dependencies:**
- Standard transformer training infrastructure (PyTorch, distributed training frameworks)
- Reasoning-dense pretraining corpus or equivalent LLM training data
- GPU compute for pretraining (105B tokens at 87M parameters)

**Quick Start:**
The paper provides a clear blueprint for implementing Simple Attention Networks:
1. Remove all feed-forward layers
2. Increase attention layer depth to match computational budget
3. Adjust learning rates per architectural variant
4. Monitor loss in nats across seeds

## Related Work & Context

### Foundation Work
- Attention Is All You Need (Vaswani et al., 2017) — established standard transformer architecture
- Evolution of transformer scaling laws and architectural choices

### Recent Related Papers
- Studies on transformer component ablation
- Linear attention mechanisms and their efficiency characteristics
- Feed-forward network analysis in large language models
- Architecture search and optimization for transformers

### Future Research Directions

1. **Extension to Other Domains:** How do these findings apply to vision transformers, cross-modal models, or other domains?
2. **Downstream Performance:** This study measures pretraining loss; downstream benchmark evaluation would provide fuller picture
3. **Inference Optimization:** Detailed analysis of attention-only inference characteristics and optimization opportunities
4. **Theoretical Foundation:** Deriving theoretical reasons why attention depth can substitute for FFN parameters
5. **Hybrid Strategies:** Exploring selective placement of FFNs only at critical depths or positions

## Papers Referenced in This Summary

- [A Controlled Study of Attention-Only Transformers](https://arxiv.org/abs/2607.18363) (2607.18363)
- [World Models: A Comprehensive Survey](https://arxiv.org/abs/2606.00133) — for broader architectural context
- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) — foundational transformer work

---

## Discussion Questions

1. How would you extend this work to encoder-decoder architectures?
2. What implications does this have for efficient inference on edge devices?
3. Could this inform neural architecture search strategies for transformers?
4. How might findings differ for instruction-tuned vs. base models?
