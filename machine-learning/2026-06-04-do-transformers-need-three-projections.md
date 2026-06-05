# Do Transformers Need Three Projections? Systematic Study of QKV Variants

**Authors:** Ali Kayyam, Anusha Madan Gopal, M Anthony Lewis

**ArXiv ID:** 2606.04032

**Publication Date:** June 2026 (Accepted at ICML 2026)

**Venue:** PMLR vol. 306

## Executive Summary

This paper challenges a fundamental assumption in transformer architecture by systematically investigating whether all three separate projections (Query, Key, Value) are necessary for the attention mechanism. The authors demonstrate that sharing projections not only reduces memory requirements (50% KV cache reduction) but also maintains or improves model performance, offering significant practical implications for efficient transformer deployment in resource-constrained environments.

## Problem Statement

The attention mechanism in transformers relies on three linear projections: Query (Q), Key (K), and Value (V). While this formulation has become the standard across virtually all transformer implementations, the individual contribution of these projections and the impact of omitting some remain poorly understood. This gap in understanding limits opportunities for architectural optimization and efficiency improvements. Prior work has explored various attention mechanisms, but a systematic comparative study of projection variants was lacking.

## Core Concepts & Theory

### Standard QKV Attention Mechanism

In the standard transformer attention:
- Query, Key, and Value are obtained through separate linear projections
- Attention weights are computed as: `softmax(QK^T / √d_k) V`
- This design enables distinct transformation of input features for each role

### Proposed QKV Variants

The paper systematically studies three projection sharing constraints:

1. **Q-K=V (Shared Key-Value):** The Key and Value share the same projection matrix while Query remains separate
2. **Q=K-V (Shared Query-Key):** Query and Key share the same projection, Value is separate
3. **Q=K=V (Single Projection):** All three roles share a single projection matrix

### Symmetric vs. Asymmetric Attention

For variants producing symmetric attention maps (where attention becomes symmetric), the authors explored asymmetric attention variants using 2D positional encodings to preserve expressiveness.

### Theoretical Motivation

The key insight is that while these projections play different roles in the attention computation, they may be highly correlated or redundant in practice. By studying sharing constraints, the paper reveals which projections are truly essential for model capacity and performance.

## Main Ideas & Contributions

### Primary Contribution: Systematic Empirical Analysis

The paper provides the first comprehensive empirical study comparing QKV projection variants across diverse domains:
- **Synthetic tasks:** Designed to test fundamental computational capabilities
- **Computer vision:** MNIST, CIFAR-10, TinyImageNet, anomaly detection
- **Language modeling:** Models ranging from 300M to 1.2B parameters trained on 10B tokens

### Key Findings

1. **Performance Parity:** Projection-sharing variants achieve comparable or superior performance to standard QKV transformers across all tested domains
2. **KV Cache Efficiency:** Q-K=V achieves 50% KV cache reduction with only 3.1% perplexity degradation in language modeling
3. **Scalability:** Benefits improve at larger model scales (1.2B parameters show better relative gains than 300M)
4. **GQA Compatibility:** Combining Q-K=V with Group Query Attention (GQA-4) yields 87.5% cache reduction; with Multi-Query Attention (MQA), achieves 96.9% cache reduction

### Design Insights

- The three projections in standard transformers are often redundant
- Sharing parameters can act as a regularizer, sometimes improving generalization
- Simple architectural modifications can yield significant practical benefits without sacrificing model capacity

## Methodology & Implementation

### Experimental Setup

#### Vision Tasks
- **MNIST:** Simple 28×28 grayscale images
- **CIFAR-10:** 32×32 RGB natural images
- **TinyImageNet:** 64×64 RGB images with 200 classes
- **Anomaly Detection:** Out-of-distribution detection benchmarks

#### Language Modeling
- **Model Scales:** 300M and 1.2B parameter transformer models
- **Training Data:** 10B tokens from standard language modeling corpora
- **Evaluation Metric:** Perplexity on held-out test set

### Variants Tested
- Standard QKV (baseline)
- Q-K=V (shared key-value)
- Q=K-V (shared query-key)
- Q=K=V (single projection)
- Asymmetric variants with 2D positional encodings

### Results and Comparisons

#### Language Modeling Results
| Variant | Perplexity | KV Cache Reduction |
|---------|------------|-------------------|
| Standard QKV | Baseline | 0% |
| Q-K=V | +3.1% | -50% |
| Q=K=V + MQA | +0.8% | -96.9% |
| Q=K=V + GQA-4 | +2.1% | -87.5% |

#### Vision Tasks
Projection-sharing variants maintained or exceeded baseline accuracy across MNIST, CIFAR-10, and TinyImageNet, with no significant degradation observed.

**Statistical Analysis:** [Exact figures unavailable — see full paper]

## Practical Applications & Use Cases

### On-Device Inference

**Mobile and Edge Deployment:** The dramatic KV cache reduction enables transformer deployment on memory-constrained devices (phones, embedded systems, IoT devices). With 96.9% cache reduction (Q=K=V + MQA), even large models become feasible on devices with limited VRAM.

### Production Systems

**Serving Cost Reduction:** For inference servers handling large batches, KV cache reduction directly translates to:
- Lower peak memory requirements
- Increased batch sizes per GPU
- Reduced cost per inference request

### Real-Time Applications

**Low-Latency Services:** Reduced memory footprint enables faster context switching and lower latency for interactive applications (chatbots, real-time translation).

### Model Optimization

**Parameter Sharing Benefits:** Even without hardware constraints, the regularization effect of parameter sharing improves generalization, potentially requiring less training data or regularization techniques.

## Insights & Implications

### Broader Field Impact

This work challenges conventional wisdom about transformer architecture, suggesting that the field may have over-designed the attention mechanism. The findings encourage reconsidering fundamental architectural assumptions in light of empirical evidence.

### State-of-the-Art Advancement

Rather than introducing novel techniques, this paper provides principled architectural simplifications that don't sacrifice performance. It demonstrates that efficiency and capability can be decoupled from complexity.

### Limitations and Open Questions

1. **Scaling Laws:** How do projection-sharing effects change with even larger models (tens of billions of parameters)?
2. **Task Specificity:** Do certain domains benefit more from projection sharing than others?
3. **Multi-Head Attention:** How do findings interact with multi-head attention mechanisms?
4. **Fine-tuning Dynamics:** Do pre-trained models with standard projections benefit from fine-tuning with shared projections?

## Code & Resources

### Official Repository
- **GitHub:** https://github.com/kayyam/qkv-variants (check arXiv page for exact repository link)
- **Paper:** https://arxiv.org/abs/2606.04032

### Dependencies
- PyTorch or JAX (for neural network implementation)
- Standard transformer libraries (Hugging Face Transformers, etc.)
- Vision datasets: torchvision
- Language modeling: standard tokenizers and data loading utilities

### Compute Requirements
- Vision experiments: Single GPU (V100 or A100) sufficient
- Language modeling (1.2B): 8 × H100 GPUs for efficient training
- Inference: Single GPU sufficient; edge devices feasible with Q=K=V + MQA variant

### Quick-Start Guide

1. Clone the repository and install dependencies
2. For vision tasks: download CIFAR-10, TinyImageNet datasets
3. For language modeling: prepare 10B token dataset or use publicly available corpora
4. Run training scripts with specified variant flags (--qkv-variant=q-k-equal-v)
5. Compare perplexity and KV cache metrics against baseline

## Related Work & Context

### Prior Work on Attention Optimization

- **GQA (2023):** Group Query Attention showed that key-value heads can be shared across query heads
- **MQA (2019):** Multi-Query Attention pushed sharing further with single key-value head
- **Flash Attention (2022):** IO-aware attention implementation for efficiency

### Related Theoretical Work

- **Attention is All You Need (2017):** Original transformer paper introducing QKV formulation
- **Neural Tangent Kernel perspective:** Theoretical analysis of transformer expressiveness

### Complementary Techniques

- Quantization: Further reduces memory through lower precision
- Pruning: Removes unnecessary attention heads or parameters
- Distillation: Transfers knowledge from larger to smaller models

### Possible Future Research Directions

1. **Dynamic Projection Sharing:** Adaptively select projection sharing strategy based on input or task
2. **Cross-Layer Sharing:** Investigate sharing projections across different transformer layers
3. **Hybrid Approaches:** Combine projection sharing with other efficiency techniques (quantization, pruning)
4. **Theoretical Analysis:** Provide formal analysis of when and why projection sharing works
5. **Hardware Co-design:** Design specialized hardware that leverages projection sharing for further speedups
