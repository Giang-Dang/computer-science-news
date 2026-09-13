# Spectral Outliers Reveal Dominant Learned Structure in Transformer Attention

**ArXiv ID:** 2608.07921  
**Submission Date:** August 8, 2026  
**Authors:** Kasun Dewage, Marianna Pensky, Suranadi De Silva, T. H. Bandara  
**Accepted at:** International Conference on Machine Learning and Applications (ICMLA)

## Executive Summary

This paper applies random matrix theory, specifically the Marchenko-Pastur theorem, to decompose attention weights in pre-trained transformers into a random-like bulk and interpretable spectral outliers. The work demonstrates that spectral outliers encode the dominant learned structure and that their removal severely degrades model performance, providing empirical validation for mechanistic interpretability through mathematical rigor.

## Problem Statement

Understanding what transformers learn internally remains a fundamental challenge in mechanistic interpretability. Attention weights are high-dimensional matrices whose structure is difficult to interpret directly. Previous work lacked principled mathematical methods to separate signal from noise in attention matrices. This gap limits our ability to understand and control transformer behavior at the mechanistic level.

## Core Concepts & Theory

### Marchenko-Pastur Random Matrix Theory

The paper leverages the Marchenko-Pastur (MP) theorem from random matrix theory to analyze attention weights. The MP theorem describes the distribution of eigenvalues in large random matrices and provides a theoretical framework for distinguishing:
- **Bulk**: Random-like eigenvalues that follow the MP distribution
- **Outliers**: Eigenvalues deviating significantly from the bulk distribution, indicating structure

### Mathematical Foundation

For an attention weight matrix W ∈ ℝ^(n×m):

1. Compute the Gram matrix G = WW^T
2. Calculate eigenvalue spectrum of G
3. Fit MP distribution to the bulk portion
4. Identify spectral outliers as eigenvalues exceeding theoretical boundaries
5. Decompose: W = Signal (outlier-associated) + Noise (bulk-associated)

### Key Observations

The authors identify five recurring patterns across 11 pre-trained transformers:

1. **Spectral outliers encode dominant structure**: Outliers capture the most important learned information for model behavior
2. **Q projections carry most outliers**: Query projections show the strongest structured signals
3. **V projections under grouped-query attention lack clean separation**: Grouped-query attention variants show degraded signal/noise separation
4. **Entry-level outliers form structured patterns**: Q shows row-bands, O shows column-bands at entry layers
5. **Band outliers persist across layers**: Specific residual-stream dimensions maintain band-structured outliers across layers in K and O projections

## Main Ideas & Contributions

### Novel Approach to Attention Interpretation

Rather than treating attention weights as black-box matrices, this work applies principled statistical decomposition. The key innovation is using random matrix theory—typically applied in statistical physics and signal processing—to mechanistic interpretability.

### Theoretical-Empirical Bridge

The paper bridges theory and practice:
- **Theoretical**: MP theorem provides principled separation criteria
- **Empirical**: Validation through causal intervention on Mistral-7B, GPT-2, and other models

### Practical Mechanistic Insights

Identifying which attention components (outliers) drive behavior enables:
- Parameter-efficient fine-tuning targeting critical components
- Structured pruning based on component importance
- Better understanding of layer-wise information flow

## Methodology & Implementation

### Experimental Setup

**Models Tested:** 11 pre-trained transformers including:
- Mistral-7B
- GPT-2 variants
- BERT variants
- Other open-source transformers

**Validation Method:** Causal intervention through selective zeroing

### Experiments & Results

#### Main Validation: Selective Zeroing

**Setup:** Remove components and measure performance degradation

**Results on Mistral-7B:**
- **Zeroing MP-identified signal (outliers)**: HellaSwag, MMLU, and PIQA scores drop to near random-chance performance
- **Zeroing count-matched bulk components**: Smaller, non-negligible degradation

**Interpretation:** Spectral outliers are not merely correlated with performance—they causally drive it

#### Benchmark Performance

Tested on standard NLP evaluation benchmarks:
- **HellaSwag**: Commonsense reasoning
- **MMLU**: Multi-task language understanding
- **PIQA**: Physical commonsense reasoning

[Exact figures unavailable — see full paper]

### Findings

The hierarchical pattern of outliers across layers suggests:
- Early layers organize information into structured bands
- These bands propagate through residual connections
- Attention heads specialize in distinct signal dimensions

## Practical Applications & Use Cases

### Parameter-Efficient Fine-Tuning (PEFT)

Rather than fine-tuning all weights, target the spectral outliers:
- Reduce parameters by focusing on structured components
- Improve transfer learning efficiency
- Enable adaptation of large models on limited hardware

### Structured Pruning

Replace unstructured pruning with knowledge from spectral analysis:
- Identify non-critical bulk components safely
- Preserve structured signal components
- Reduce model size while maintaining performance

### Model Interpretation & Safety

- Understand which components drive specific behaviors
- Identify potential sources of biases or vulnerabilities
- Design interventions for mechanistic safety improvements

### Knowledge Distillation

- Compress student model by focusing on outlier structure
- Teach student to replicate band patterns in attention
- Maintain interpretability through structural similarity

## Insights & Implications

### Broader Field Impact

This work demonstrates that random matrix theory provides powerful tools for AI interpretability. The result suggests mechanistic interpretability requires rigorous mathematical frameworks beyond hand-coded interpretations.

### State-of-the-Art Advancement

- **First application** of Marchenko-Pastur theorem to transformer interpretability
- **Causal validation** of interpretability findings through systematic intervention
- **Unified framework** explaining attention structure across diverse architectures

### Limitations & Open Questions

1. **Computational cost**: Eigenvalue decomposition adds overhead
2. **Generalization across scales**: Does the pattern hold for extremely large models (>70B)?
3. **Dynamic attention**: How do outlier patterns change during inference?
4. **Mechanistic causal model**: Can we build a complete causal model from outlier identification?
5. **Cross-layer interactions**: How do outlier patterns in different layers interact?

## Code & Resources

**Official Repository:** [https://github.com/Kasun-Dewage/spectral-outliers-attention](https://github.com/Kasun-Dewage/spectral-outliers-attention)

**Dependencies:**
- PyTorch for model loading and intervention
- NumPy/SciPy for eigenvalue decomposition
- Standard NLP evaluation libraries (lm_harness)

**Quick Start:**

```python
import torch
from spectral_outliers import analyze_attention_structure

# Load a pre-trained model
model_name = "mistralai/Mistral-7B"
model = torch.hub.load(model_name)

# Analyze attention structure
outliers, bulk = analyze_attention_structure(model, layers=[0, 5, 10])

# Perform causal intervention (zero outliers)
intervened_model = zero_components(model, outliers)
accuracy = evaluate(intervened_model)  # Near random-chance
```

**Compute Requirements:**
- GPU memory: ~16-24GB for analyzing 7B parameter models
- Runtime: Minutes to hours per model for full analysis
- Batch processing available for efficiency

## Related Work & Context

### Prior Work in Mechanistic Interpretability

- **Sparse Autoencoders (SAEs)**: Extract interpretable features from activation patterns
- **Attention Head Ablation**: Earlier work removing individual heads (less principled)
- **Activation Patching**: Causal intervention on intermediate representations

### Connections to Random Matrix Theory

- **Signal processing**: MP theorem used for noise reduction in communications
- **Statistics**: Applied to covariance structure estimation
- **Neuroscience**: Random matrix analysis of neural populations

### Related Recent Papers

- Work on transformer circuits and mechanistic interpretability
- Studies on attention head specialization and clustering
- Research on parameter-efficient fine-tuning and pruning strategies

### Future Research Directions

1. **Multi-model universality**: Apply framework across modalities (vision transformers, multimodal models)
2. **Temporal dynamics**: Study how outlier patterns evolve during training
3. **Layer-wise compilation**: Build complete mechanistic model from layer-level structures
4. **Adversarial robustness**: Can outlier-based interventions improve robustness?
5. **Scaling laws**: Derive theoretical scaling relationships for outlier abundance

## Key Takeaways

1. **Rigor in interpretability**: Random matrix theory provides principled signal/noise separation
2. **Causal grounding**: Spectral outliers are not just correlated but causally important
3. **Actionable insights**: Results enable practical improvements in efficiency and control
4. **Universal patterns**: Structures repeat across diverse transformer architectures
5. **Mechanistic foundations**: Work advances the mathematical basis for AI interpretability
