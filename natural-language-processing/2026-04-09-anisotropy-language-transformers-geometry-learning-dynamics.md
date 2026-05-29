# Revisiting Anisotropy in Language Transformers: The Geometry of Learning Dynamics

**ArXiv ID:** 2604.08764  
**Authors:** Raphael Bernas, Fanny Jourdan, Antonin Poché, Céline Hudelot  
**Submitted:** April 9, 2026

## Executive Summary

This paper investigates the geometric properties of how Transformer models learn, focusing on the inherent **anisotropy phenomenon**—where gradient updates concentrate in low-dimensional subspaces rather than spreading uniformly across parameter space. The authors combine theoretical analysis with empirical mechanistic interpretability to reveal that activation-derived directions capture both unusually large gradient energy and a substantially larger share of gradient anisotropy, providing new insights into Transformer learning dynamics.

## Problem Statement

Transformer architectures have dominated Natural Language Processing since their introduction, but recent research has highlighted an inherent anisotropy phenomenon in these models. This anisotropy presents a significant challenge to geometric interpretation: gradients in neural networks do not update parameters uniformly in all directions, instead concentrating in specific subspaces. Previous theoretical studies on this phenomenon are rarely grounded in the underlying representation geometry, creating a gap between theory and practice.

**Key Limitations in Prior Work:**
- Theoretical explanations lack empirical grounding in actual representation geometry
- The relationship between frequency-biased sampling and gradient anisotropy is not fully understood
- Limited mechanistic interpretability of how anisotropy manifests during training

## Core Concepts & Theory

### Anisotropy in Neural Networks

**Definition:** Anisotropy refers to the directional dependence in how gradients update neural network parameters. Rather than updating uniformly across the parameter space, gradients concentrate in low-dimensional subspaces or particular directions.

**Mathematical Foundation:**
- Gradient vectors can be decomposed into components across different dimensions
- In isotropic systems, gradient magnitude would be similar across all directions
- In anisotropic systems, certain directions ("tangent directions") receive disproportionately large gradient updates

### Frequency-Biased Sampling and Curvature Visibility

The authors derive geometric arguments explaining:
1. How frequency-biased sampling in Transformers (non-uniform token frequencies) attenuates the visibility of curvature
2. Why training preferentially amplifies certain tangent directions
3. The relationship between data distribution and gradient concentration

**Key Insight:** The distribution of input tokens creates a biased sampling effect that makes certain gradient directions more "visible" to the optimization process, leading to preferential updates in those directions.

### Mechanistic Interpretability During Training

Rather than analyzing model behavior only post-hoc, this work applies **concept-based mechanistic interpretability during training**:
- Extract activation-derived low-rank tangent proxies (approximations of the true tangent directions)
- Compare these against ordinary backpropagated true gradients
- Validate whether activation patterns predict gradient direction

**Mathematical Framework:**
- Fit low-rank approximations to activation space
- Measure cosine similarity between activation-derived proxies and true backpropagated gradients
- Quantify the proportion of gradient energy captured by these approximations

## Main Ideas & Contributions

### 1. Theoretical Analysis of Anisotropy

**Contribution:** Extends previous theoretical work with rigorous geometric arguments showing:
- Frequency-biased sampling reduces curvature visibility in parameter space
- Training dynamics preferentially amplify tangent directions
- Connection between data distribution characteristics and gradient concentration

### 2. Empirical Validation Through Mechanistic Interpretability

**Contribution:** First large-scale mechanistic interpretability study of gradient anisotropy during training, showing:
- Activation-derived directions capture both unusually large gradient energy
- These directions account for a substantially larger share of total gradient anisotropy
- The effect is consistent across different model architectures

### 3. Unified Understanding Across Model Types

**Contribution:** Demonstrates that anisotropy patterns manifest similarly across:
- Encoder-style language models (e.g., BERT-like architectures)
- Decoder-style language models (e.g., GPT-like architectures)
- Suggesting anisotropy is a fundamental property of Transformer learning

### 4. Novel Interpretability Methodology

**Contribution:** Demonstrates value of studying mechanistic interpretability during training rather than only post-training, revealing dynamic aspects of how representations emerge

## Methodology & Implementation

### Experimental Setup

**Models Studied:**
- Multiple encoder-style Transformers
- Multiple decoder-style Transformers
- Various model sizes and configurations

**Data:**
- Standard language modeling benchmarks
- Different tokenization and frequency distributions

**Training Setup:**
- Standard supervised training procedures
- Tracking gradients and activations throughout training

### Mechanistic Interpretability Procedure

1. **Activation Collection:** Capture activations at each layer during forward pass
2. **Low-Rank Approximation:** Fit low-rank tangent proxies to activation spaces
3. **Gradient Measurement:** Compute true backpropagated gradients via backpropagation
4. **Comparison:** Measure cosine similarity and energy overlap between:
   - Activation-derived proxy directions
   - True gradient directions

### Key Metrics

- **Gradient Energy:** Sum of squared gradient components in specified directions
- **Cosine Similarity:** Measure alignment between proxy and true gradients
- **Anisotropy Proportion:** Fraction of total gradient variance concentrated in top-k directions
- **Coverage:** Percentage of gradient energy captured by activation-derived proxies

### Results

**Key Findings:**

1. **High Coverage of Gradient Energy:** Activation-derived directions capture unexpectedly large proportions of total gradient energy (specific percentages vary by layer and model)

2. **Concentration of Anisotropy:** The directions identified through mechanistic interpretability concentrate a substantially larger share of gradient anisotropy than random directions

3. **Consistency Across Architectures:** Both encoder and decoder architectures exhibit similar anisotropy patterns, suggesting this is a fundamental property of Transformers

4. **Layer-Specific Patterns:** Different layers show varying degrees of anisotropy, with some layers showing higher concentration than others

5. **Validation Against Baselines:** Activation-derived proxies significantly outperform random direction selection and other baseline approaches in predicting gradient directions

[Exact figures unavailable — see full paper]

## Practical Applications & Use Cases

### 1. Understanding Transformer Training Dynamics

**Application:** This work provides interpretability into why Transformers learn effectively, even when trained on non-uniform data distributions.

**Use Case:** Model designers can use these insights to predict which components of a Transformer will learn fastest and prioritize computational resources accordingly.

### 2. Optimizing Training Efficiency

**Application:** Understanding where gradient concentration occurs enables:
- More efficient training algorithms that focus updates on high-leverage directions
- Better initialization strategies that align with natural gradient flow
- Smarter learning rate scheduling per-direction

**Use Case:** Training infrastructure could be optimized by allocating more computational resources to layers/directions exhibiting high anisotropy.

### 3. Architecture Design and Adaptation

**Application:** Insights into gradient concentration can inform:
- Design of new Transformer variants with different geometric properties
- Attention mechanisms that better distribute gradient updates
- Positional encoding strategies that reduce undesired anisotropy

**Use Case:** Designing models for domains with different token frequency distributions (e.g., code, mathematics, natural language).

### 4. Mechanistic Interpretability and Safety

**Application:** Understanding training dynamics helps:
- Predict which components will develop strong representations first
- Identify potential failure modes in model development
- Design better evaluation criteria for model behavior

**Use Case:** Developing safer language models through better understanding of how problematic behaviors emerge during training.

### 5. Transfer Learning and Fine-Tuning

**Application:** Different tasks may have different optimal gradient directions. This work could enable:
- Better transfer learning by identifying task-relevant gradient directions
- More efficient fine-tuning strategies
- Understanding when and why transfer learning fails

**Use Case:** Fine-tuning pre-trained models for specialized domains with non-standard token distributions.

## Insights & Implications

### Broader Field Impact

This work bridges theory and practice in understanding Transformer learning dynamics, addressing a long-standing gap where theoretical understanding of neural network optimization (from convex optimization theory) doesn't directly apply to modern deep learning.

### Advancement of State-of-the-Art

**Mechanistic Interpretability Progress:** Demonstrates that mechanistic interpretability can be productively applied during training, not just post-hoc. This opens new avenues for:
- Real-time monitoring of model learning
- Early detection of training problems
- Active intervention during training

**Geometric Understanding:** Provides a more complete geometric picture of how Transformers learn, moving beyond purely spectral or representation norm analyses.

### Limitations and Open Questions

1. **Computational Cost:** Mechanistic interpretability during training adds significant computational overhead; scalability to very large models remains unclear

2. **Causality:** While the paper shows activation-derived directions correlate with gradient concentration, the causal mechanism remains partially unexplained

3. **Generalization:** Results focus on language models; applicability to vision Transformers and other domains is not yet established

4. **Temporal Dynamics:** How these patterns change during the course of training deserves further investigation

5. **Alternative Hypotheses:** Other explanations for anisotropy (e.g., information-theoretic bottlenecks) deserve deeper exploration

### Future Research Directions

- Scaling mechanistic interpretability approaches to billion-parameter models
- Investigating whether anisotropy is beneficial or detrimental to downstream task performance
- Exploring interventions that modify gradient geometry and measuring their effects
- Extending analysis to multimodal Transformers and other architectures
- Connecting gradient anisotropy to learning speed and convergence properties

## Code & Resources

### Paper and References

- **ArXiv:** https://arxiv.org/abs/2604.08764
- **HTML Version:** https://arxiv.org/html/2604.08764v1

### Related Tools and Libraries

**Mechanistic Interpretability Frameworks:**
- Anthropic's Transformer Circuits framework
- Distill's research on neural network interpretability
- TransformerLens (GitHub)

**Gradient Analysis Tools:**
- PyTorch's autograd for gradient computation
- Hugging Face Transformers for model implementations
- Custom profiling tools for gradient measurement

### Dependencies and Compute Requirements

**Computational Requirements:**
- GPU access (NVIDIA A100 or equivalent) for large-model experiments
- Significant memory (40GB+ RAM) for tracking activations during training
- Distributed training capabilities for multi-GPU experiments

**Software Stack:**
- PyTorch 2.0+
- Hugging Face Transformers library
- NumPy, SciPy for numerical analysis
- Matplotlib/Plotting libraries for visualization

### Quick-Start Conceptual Guide

To understand and replicate this work:

1. **Start with Basics:** Review attention mechanisms and gradient flow in Transformers
2. **Theory Phase:** Study the geometric arguments about frequency-biased sampling
3. **Implementation Phase:**
   - Implement gradient tracking during training
   - Extract activation patterns at each layer
   - Compute low-rank approximations to activation spaces
   - Measure cosine similarity between proxies and true gradients
4. **Validation:** Compare results across encoder and decoder architectures
5. **Analysis:** Visualize gradient concentration patterns and interpret findings

## Related Work & Context

### Prior Work on Anisotropy in Transformers

**Key Previous Papers:**
- "Is Anisotropy Inherent to Transformers?" (2306.07656) - Earlier investigation of anisotropy
- "Anisotropy Is Inherent to Self-Attention in Transformers" (2401.12143) - Mathematical analysis of self-attention
- "The Shape of Learning: Anisotropy and Intrinsic Dimensions in Transformer-Based Models" (2311.05928) - Dimensionality analysis

### Foundations: Mechanistic Interpretability

**Seminal Works:**
- Distill research on neural network circuits and interpretability
- "Mechanistic Interpretability" frameworks and methodologies
- Work on feature visualization and attribution methods

### Related Recent Work

**Gradient Analysis:**
- Loss landscape studies in deep learning
- Sharpness and flatness of minima
- Understanding neural network optimization

**Representation Learning:**
- Token representation geometry in Transformers
- Isotropy and representation collapse
- Spectral analysis of network representations

**Training Dynamics:**
- Phase transitions in neural network training
- Feature learning in deep networks
- Implicit biases of gradient descent

### Future Directions and Open Problems

1. **Causal Understanding:** Moving from correlation to causation—what mechanisms *cause* anisotropy?

2. **Intervention Studies:** Can we modify architectures or training to reduce harmful anisotropy or enhance beneficial patterns?

3. **Task-Specific Analysis:** Does optimal anisotropy differ for language modeling, classification, translation, etc.?

4. **Cross-Modal Studies:** How does anisotropy manifest in vision Transformers, multimodal models, or other architectures?

5. **Scalability:** Can mechanistic interpretability approaches scale to frontier models while maintaining insights?

6. **Theoretical Foundations:** Can we develop more rigorous mathematical frameworks explaining why anisotropy emerges?

---

**Citation:** Bernas, R., Jourdan, F., Poché, A., & Hudelot, C. (2026). Revisiting Anisotropy in Language Transformers: The Geometry of Learning Dynamics. *arXiv preprint arXiv:2604.08764*.
