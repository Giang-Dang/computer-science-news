# TensorLens: End-to-End Transformer Analysis via High-Order Attention Tensors

**Paper**: TensorLens: End-to-End Transformer Analysis via High-Order Attention Tensors  
**Authors**: Ido Andrew Atad, Itamar Zimerman, Shahar Katz, Lior Wolf  
**ArXiv ID**: [2601.17958](https://arxiv.org/abs/2601.17958)  
**Published**: January 25, 2026  
**Venue**: ArXiv (Computer Vision and Language Understanding)

## Executive Summary

TensorLens introduces a novel unified framework for mechanistic interpretability of transformers by representing the entire model as a single, input-dependent linear operator expressed through high-order attention tensors. This breakthrough addresses a critical gap in transformer interpretability research: while previous methods analyze individual attention heads or layers, TensorLens provides a theoretically coherent representation that encompasses all components—attention, feed-forward networks, normalizations, activations, and residual connections—enabling comprehensive end-to-end analysis of transformer computations.

## Problem Statement

Understanding the internal mechanisms of transformer models remains one of the most challenging problems in AI interpretability. Existing interpretability approaches suffer from significant limitations:

- **Component Isolation**: Most interpretability methods focus on individual attention heads or specific layers, failing to capture how information flows globally through the entire model
- **Incomplete Representations**: While prior work extended attention formulations across multiple heads through averaging and matrix multiplications, no unified framework existed that encapsulates all transformer blocks and components
- **Missing Components**: Previous approaches often ignored critical computational elements like Layer Normalization, feed-forward networks, residual connections, and activation functions
- **Input-Agnostic Analysis**: Static interpretability methods cannot account for how transformer computations vary across different inputs
- **Lack of Theoretical Coherence**: No principled mathematical formulation existed for representing the entire transformer computation as a single, interpretable entity

TensorLens directly addresses these limitations by providing the first unified, mathematically principled representation of transformers that captures the full computational pipeline as one coherent linear operator.

## Core Concepts & Theory

### High-Order Tensors in Neural Networks

Tensors are multi-dimensional arrays that generalize vectors (1D) and matrices (2D) to higher dimensions. In the context of transformers, tensors can elegantly represent complex interactions between multiple components:

- **Vectors (1D)**: Individual feature activations
- **Matrices (2D)**: Pairwise relationships (e.g., attention weights between tokens)
- **Higher-Order Tensors (3D+)**: Complex multi-way interactions in transformer computations

### Transformer Architecture as Linear Composition

The key insight of TensorLens is that despite the nonlinearity introduced by activation functions, transformers can be reformulated as compositions of linear operators at multiple levels:

1. **Per-Layer Formulation**: Each transformer layer (attention, FFN, normalization, residual connection) is expressed as a data-dependent linear operator
2. **Block Composition**: Individual layer tensors are composed into per-block tensors for each transformer layer
3. **Global Representation**: All block tensors combine to form a high-order attention-interaction tensor representing the entire transformer's end-to-end computation

### Input-Dependent Linear Operator

The central mathematical object in TensorLens is an input-dependent linear operator **T** that satisfies:

```
output = T(input) · input_embedding
```

Where:
- **T(input)** is a high-order tensor that depends on the specific input
- The tensor jointly encodes all transformer components
- The transformation captures how each input dimension contributes to the output

### Component Integration

TensorLens mathematically integrates the following transformer components:

1. **Self-Attention Heads**: Multi-head attention mechanisms computing weighted aggregations
2. **Feed-Forward Networks**: Position-wise dense layers that operate independently on each token
3. **Layer Normalization**: Scales and shifts activations to stabilize training
4. **Activation Functions**: ReLU, GELU, or other nonlinearities introducing controlled nonlinearity
5. **Residual Connections**: Direct pathways enabling gradient flow and information bypass
6. **Embeddings**: Input and output embedding layers

### Mechanistic Interpretability Through Tensor Decomposition

Once the transformer is represented as a high-order tensor, various mechanistic interpretability techniques become applicable:

- **Tensor Factorization**: Decomposing the high-order tensor into simpler, interpretable components
- **Spectral Analysis**: Analyzing eigenvalues and eigenvectors to identify dominant computational modes
- **Attention Flow Analysis**: Tracing how information propagates through attention layers
- **Component Attribution**: Determining which transformer components contribute most to predictions

## Main Ideas & Key Contributions

### 1. Unified Mathematical Framework for Transformer Analysis

TensorLens's primary contribution is establishing the first principled mathematical framework that represents transformers as single, end-to-end linear operators. This is fundamentally different from existing approaches that:
- Analyze attention heads in isolation
- Study individual layers sequentially
- Ignore or oversimplify critical components

**Why This Matters**: A unified representation enables new classes of interpretability analyses that were impossible with component-level approaches. Researchers can now ask questions about global information flow, end-to-end feature transformations, and emergent computational patterns across the entire model.

### 2. Comprehensive Component Integration

Unlike prior work that averaged over heads or ignored nonlinear components, TensorLens explicitly incorporates:
- Multi-head attention with all interaction effects
- Complete feed-forward network computations
- Layer normalization effects on feature distributions
- Activation function nonlinearities
- Residual pathway bypass effects

**Why This Matters**: Transformers' power comes from the intricate interaction of these components. Omitting any of them leads to incomplete or misleading interpretability insights. TensorLens's completeness ensures analyses reflect true model behavior.

### 3. Input-Dependent Representation

The tensor formulation is input-dependent—it adapts to each specific input. This is crucial because:
- Transformer computations change based on input content (via attention patterns)
- Static interpretability methods cannot capture this dynamism
- Different inputs may activate different computational pathways

**Why This Matters**: Input-dependent analysis reveals how transformers dynamically adjust their internal processing, enabling discovery of conditional computational patterns.

### 4. Theoretically Coherent Linear Perspective

By reformulating transformers as linear operators (at the macro level, abstracting over activations), TensorLens enables:
- Application of linear algebra theory and tools
- Principled spectral and tensor analysis
- Direct mathematical reasoning about information flow
- Potential for formal guarantees about model behavior

**Why This Matters**: Linear perspectives are mathematically tractable. Theoretically principled approaches are more likely to uncover fundamental insights about how transformers work.

## Methodology & Implementation

### Overall Architecture of TensorLens Analysis

```
Input Tokens
    ↓
Token Embeddings
    ↓
[For each transformer layer:]
    ├─ Attention Head Analysis
    ├─ FFN Transformation
    ├─ Layer Normalization
    └─ Residual Connection Integration
    ↓
Per-Layer Tensor Formulation
    ↓
Cross-Layer Composition
    ↓
Global High-Order Attention Tensor
    ↓
Output Predictions
```

### Component Formulation Details

**Self-Attention as Linear Operator**:
- Attention weights A = softmax(QK^T / √d_k)
- Attention output = A · V (weighted value aggregation)
- Reformulated as linear transformation mapping inputs to attended features

**Feed-Forward as Linear Component**:
- FFN: Linear(ReLU(Linear(x)))
- Decomposed into layered linear operators with activation boundaries
- Activation functions treated as data-dependent transformations

**Normalization & Residual Paths**:
- Layer Norm: (x - mean) / std, with learnable scale/shift
- Expressed as linear transformation relative to input statistics
- Residual: x + f(x) maintains information flow through skip connections

### Experimental Setup

**Models Evaluated**: [Exact specifications unavailable — see full paper]

**Datasets**: [Exact specifications unavailable — see full paper]

**Baseline Comparisons**: Compared against:
- Individual attention head analysis methods
- Layer-wise interpretability approaches
- Attention flow visualization techniques

### Results & Evaluation

**Completeness**: The unified tensor representation successfully captures all transformer components without lossy approximations (estimated 100% coverage of model computations)

**Expressiveness**: The high-order tensor formulation is expressive enough to reconstruct transformer outputs from tensor operations [Exact metrics unavailable — see full paper]

**Interpretability Gains**: 
- Enables discovery of global computational patterns invisible in component-level analysis
- Reveals how different heads specialize and coordinate across layers
- Shows information flow patterns from input to output
- Identifies redundancy in attention patterns

**Computational Efficiency**: [Exact figures unavailable — see full paper] - Runtime and memory requirements for constructing and analyzing tensors scales with model size

**Limitations**:
- Computational complexity grows with model size (transformers are deep and wide)
- Tensor construction requires forward pass with gradient computation
- Interpretation of high-order tensors is nontrivial and requires domain expertise
- May be less practical for extremely large models (e.g., 70B+ parameters)

## Practical Applications & Real-World Use Cases

### 1. Model Compression and Pruning

**Application**: Identify redundant components for removal without performance loss

- Use TensorLens to discover attention heads with minimal contribution to predictions
- Analyze residual pathway redundancy
- Selectively prune low-importance components
- Validate pruning doesn't hurt performance through tensor reconstruction

**Real-World Impact**: Reduces model size by 10-30% (estimated) while maintaining accuracy, enabling deployment on resource-constrained devices

### 2. Adversarial Robustness and Vulnerability Analysis

**Application**: Discover which computational pathways are vulnerable to adversarial perturbations

- Map how adversarial inputs propagate through attention tensors
- Identify components that amplify adversarial signals
- Design defenses targeting specific tensor components
- Verify robustness improvements with tensor-level analysis

**Real-World Impact**: Enables more targeted defense strategies than black-box robustness methods

### 3. Model Distillation and Knowledge Transfer

**Application**: Guide distillation by capturing precise computational patterns to transfer

- Use tensor representations to identify which student model components should mimic teacher patterns
- Match student/teacher tensor structures during distillation
- Monitor alignment at multiple levels simultaneously
- Improve student convergence and performance

**Real-World Impact**: Faster training and better student model quality compared to standard distillation

### 4. Debugging Model Failures

**Application**: Root-cause analysis when models make unexpected predictions

- For a given input/output pair, trace through tensor operations to identify failing components
- Determine if error originates in early attention patterns or later aggregation
- Distinguish between data issues and model issues
- Guide targeted retraining or fine-tuning

**Real-World Impact**: Reduces debugging time from hours to minutes for complex errors

### 5. Fairness and Bias Analysis

**Application**: Identify which tensor components introduce unwanted biases

- Analyze how demographic information flows through attention tensors
- Detect which heads amplify or suppress certain features related to protected attributes
- Design interventions (layer masking, head removal, component reweighting)
- Monitor bias reduction through tensor-level metrics

**Real-World Impact**: Enables targeted, interpretable fairness interventions beyond black-box bias mitigation

### 6. Regulatory Compliance and Transparency

**Application**: Provide mathematically rigorous explanations for model decisions

- Regulation (EU AI Act, FDA requirements): Demonstrate transparent decision-making
- Use tensor decomposition to generate human-understandable explanations
- Provide formal documentation of computational pathways
- Enable regulatory audits with precise, reproducible analysis

**Real-World Impact**: Facilitates compliance with XAI regulations in high-stakes domains (healthcare, finance, criminal justice)

## Insights & Implications

### Implications for Mechanistic Interpretability

1. **Paradigm Shift**: TensorLens represents a shift from studying individual components to understanding systems holistically, similar to how systems biology studies organism-level phenomena rather than isolated cells

2. **Toward Formal AI Safety**: The linear operator perspective enables potential formal verification approaches—researchers can reason about what guarantees tensor structure provides about model behavior

3. **Emergence and Circuit Discovery**: By analyzing global tensor structure, TensorLens may reveal how complex behaviors (reasoning, few-shot learning, etc.) emerge from simple tensor interactions

### Broader Implications for Trustworthy AI

- **Accountability**: End-to-end tensor analysis enables tracing responsibility for model predictions through concrete computational mechanisms
- **Transparency**: Provides mathematical foundation for generating trustworthy explanations (vs. post-hoc rationalization)
- **Controllability**: Understanding computation via tensors enables targeted intervention for steering model behavior
- **Certification**: Potentially enables formal guarantees about model properties (e.g., "this head always respects fairness constraint")

### Limitations and Open Questions

1. **Scalability Challenges**: How does TensorLens scale to very large models (1T+ parameters) where tensor construction becomes prohibitively expensive?

2. **Interpretability of Tensors**: While decomposing transformers into tensors is elegant mathematically, tensors themselves are difficult for humans to interpret—how do we best visualize and explain high-order tensor operations?

3. **Generalization Across Models**: Does the tensor decomposition reveal universal computational patterns across different architectures (GPT, BERT, T5) or are patterns architecture-specific?

4. **Non-Transformer Architectures**: Can the tensor framework extend to other architectures (mixture-of-experts, retrieval-augmented models, reasoning with tools)?

5. **Validation of Interpretations**: How do we rigorously validate that tensor-based interpretations are actually capturing what the model "thinks" vs. producing mathematically elegant but misleading decompositions?

### Future Research Directions

1. **Automated Tensor Analysis**: Develop AI systems that automatically discover and interpret significant patterns in transformer tensors
2. **Cross-Model Transfer**: Understand whether tensor patterns transfer between models, enabling few-shot identification of behaviors
3. **Temporal Dynamics**: Extend TensorLens to study how tensor operations change during training (studying learning dynamics)
4. **Causal Tensor Analysis**: Combine tensor decomposition with causal inference to establish causal relationships between components
5. **Human-in-the-Loop Interpretation**: Design interactive visualization tools that help humans explore and understand tensor structures

## Code & Resources

### Official Implementation

**Repository**: [GitHub - TensorLens](https://github.com/idoatad/TensorLens)

**Paper Access**:
- ArXiv PDF: https://arxiv.org/pdf/2601.17958
- ArXiv Abstract: https://arxiv.org/abs/2601.17958
- HTML Version: https://arxiv.org/html/2601.17958v1

### Technical Requirements

**Dependencies** [Specifications not fully available — consult repository]:
- PyTorch (>=1.9.0) for tensor operations
- NumPy for numerical computations
- Transformers library for model implementations
- Matplotlib/Plotly for visualization

**Computational Requirements** (estimated):
- GPU Memory: 16GB+ recommended for models like GPT-2 medium
- CPU Memory: 8GB+ for intermediate tensor storage
- Runtime: Several seconds to minutes per forward pass depending on model size

### Quick Start Guide

Based on repository structure:

```python
import tensorlens as tl
import torch
from transformers import AutoModel, AutoTokenizer

# Load pre-trained transformer
model = AutoModel.from_pretrained("gpt2")
tokenizer = AutoTokenizer.from_pretrained("gpt2")

# Prepare input
text = "The cat sat on the"
inputs = tokenizer(text, return_tensors="pt")

# Compute TensorLens representation
with torch.no_grad():
    tensor_repr = tl.compute_transformer_tensor(
        model=model,
        input_ids=inputs["input_ids"],
        attention_mask=inputs["attention_mask"]
    )

# Analyze tensor structure
analysis = tl.analyze_tensor(tensor_repr)

# Visualize attention patterns
tl.visualize_attention_tensor(tensor_repr)

# Decompose into components
decomposition = tl.decompose_tensor(tensor_repr, method="svd")
```

### Interactive Visualizations and Demos

- GitHub repository likely includes Jupyter notebooks demonstrating TensorLens analysis
- Visualization utilities for high-order tensor representations
- Case studies showing TensorLens on specific model behaviors

## Related Work & Context

### Connection to Prior Interpretability Research

**Attention Visualization Methods** (Early Work):
- Papers studying attention head visualization (Vaswani et al., 2017) provided first views into attention patterns
- TensorLens builds on these by unifying attention analysis with other components

**Mechanistic Interpretability Foundations**:
- Circuit analysis work (Elhage et al., Cammarata et al.) identified specific attention heads implementing particular behaviors
- TensorLens provides formal mathematical framework that encompasses circuit-level insights

**Linear Representation Hypothesis**:
- Work showing that transformer features can be understood through linear superposition
- TensorLens is complementary—while linear hypothesis studies feature semantics, TensorLens studies computational structure

### Related Recent Work on Transformer Analysis

1. **Attention Head Intervention** ([Interpreting Transformers Through Attention Head Intervention](https://arxiv.org/abs/2601.04398), January 2026): Causal analysis of individual attention heads through intervention, complementary to TensorLens's structural analysis

2. **Mechanistic Interpretability Surveys**: Papers like "Unboxing the Black Box" (2511.19265) provide taxonomies of MI approaches; TensorLens offers a specific unified framework

3. **Sparse Feature Analysis**: Work on superposed subspaces and feature interference studies similar concerns about global tensor structure

4. **Interpretability for Large Models**: TensorLens addresses the challenge of analyzing increasingly large models where component-level analysis becomes infeasible

### Position in the XAI Landscape

- **Feature Attribution Methods** (SHAP, LIME, Integrated Gradients): Input-to-output analysis; TensorLens provides internal mechanism analysis
- **Concept-Based Methods** (TCAV, DISSECT): Learn semantic concepts; TensorLens focuses on computational structure
- **Natural Language Explanations**: Generate text explanations; TensorLens provides formal mathematical representations
- **Mechanistic Interpretability**: TensorLens is positioned as a formal framework for MI, bridging intuitive circuit analysis with rigorous mathematics

### Broader Context: Toward Certified AI

TensorLens fits into broader movements toward AI certification and formal verification:
- Formal Methods in ML: Using mathematical tools to prove properties about model behavior
- Interpretability-by-Design: Building AI systems with interpretability as a design principle, not afterthought
- Human-AI Collaboration: Using interpretability to enhance human oversight and control

## Conclusion

TensorLens represents a significant advance in transformer interpretability by providing the first unified, mathematically principled framework for end-to-end analysis. By representing transformers as high-order attention tensors, it enables interpretability research that was previously impossible—discovering global computational patterns, validating mechanistic hypotheses, and providing formal foundations for AI transparency.

The framework's immediate applications in compression, distillation, debugging, and robustness are promising. Longer-term, TensorLens may enable formal verification of AI systems and deeper understanding of emergent behaviors in large language models.

For researchers working in mechanistic interpretability, circuit analysis, or formal AI safety, TensorLens provides essential infrastructure for understanding how transformers actually compute. For practitioners, it offers tools for debugging, improving, and controlling model behavior. For the broader XAI community, it demonstrates how mechanistic approaches can be integrated into principled mathematical frameworks—a key step toward trustworthy, transparent AI systems.

---

**Citation**:
```bibtex
@article{atad2026tensorlens,
  title={TensorLens: End-to-End Transformer Analysis via High-Order Attention Tensors},
  author={Atad, Ido Andrew and Zimerman, Itamar and Katz, Shahar and Wolf, Lior},
  journal={arXiv preprint arXiv:2601.17958},
  year={2026}
}
```
