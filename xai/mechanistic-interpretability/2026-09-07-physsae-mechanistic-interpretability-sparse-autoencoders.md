# PhysSAE: Mechanistic Interpretability with Sparse Autoencoders

## Executive Summary

PhysSAE is the first mechanistic interpretability framework for Physics-Informed Neural Networks (PINNs), using sparse autoencoders to discover and interpret the sparse, physically-structured features that PINNs develop in their hidden representations. By combining sparse autoencoder feature discovery with direct causal intervention, PhysSAE enables systematic diagnosis of PINN internal mechanisms and failure modes, advancing trustworthy scientific machine learning.

## Problem Statement

Physics-Informed Neural Networks (PINNs) embed Partial Differential Equation (PDE) residuals directly into the training loss via automatic differentiation, enabling mesh-free solution of forward and inverse problems in scientific computing. Despite their widespread adoption in fluid mechanics, solid mechanics, biomedical modeling, and other domains, PINNs remain fundamentally opaque at the feature level—what do these networks learn and represent in their hidden layers?

Prior work has characterized PINN failure modes at the loss or gradient level (spectral bias, gradient pathologies, causality violations), but no systematic approach existed for understanding what physical features PINNs actually encode internally. This interpretability gap hinders:

1. **Diagnosis of failure**: When a PINN fails to converge or produces incorrect solutions, practitioners lack insight into what the network learned or failed to learn
2. **Trust and validation**: Critical scientific applications (medical diagnostics, engineering design) require understanding model internals, not just loss values
3. **Generalization understanding**: It is unclear how physical observables map to PINN representations or whether discovered features align with true physical quantities
4. **Optimization insights**: Hidden layer analysis could reveal optimization challenges and guide architecture improvements

## Core Concepts & Theory

### Physics-Informed Neural Networks (PINNs)

PINNs solve PDEs by encoding the residual $\mathcal{R}(u, \frac{\partial u}{\partial x}, \frac{\partial u}{\partial t}, ...) = 0$ into the loss function:

$$\mathcal{L}_{total} = \lambda_r \mathcal{L}_r + \lambda_bc \mathcal{L}_{bc} + \lambda_{ic} \mathcal{L}_{ic}$$

where:
- $\mathcal{L}_r$ is the PDE residual loss (evaluated at collocation points)
- $\mathcal{L}_{bc}$ enforces boundary conditions
- $\mathcal{L}_{ic}$ enforces initial conditions
- Automatic differentiation computes spatial and temporal derivatives

### Sparse Autoencoders for Mechanistic Interpretability

Sparse autoencoders (SAEs) decompose neural network activations into interpretable, localized features:

$$\mathbf{h} = \text{encoder}(\mathbf{a}) = W_e \mathbf{a}$$
$$\mathbf{a}_{reconstructed} = \text{decoder}(\mathbf{h}) = W_d \mathbf{h} + \mathbf{b}$$

where:
- $\mathbf{a}$ are hidden layer activations
- $\mathbf{h}$ are sparse features (dictionary atoms)
- Sparsity constraint ensures only a few atoms activate per input
- Overcomplete dictionaries ($\dim(\mathbf{h}) > \dim(\mathbf{a})$) capture fine-grained concepts

**Loss function with sparsity:**

$$\mathcal{L}_{SAE} = ||(\mathbf{a} - W_d \mathbf{h})||^2_2 + \lambda ||\mathbf{h}||_1$$

The L1 penalty enforces sparsity, promoting interpretability through activation locality.

### Causal Intervention for Faithfulness

Direct causal intervention evaluates whether a discovered feature has a localized causal role:

1. Identify a feature (atom) in the SAE dictionary
2. Ablate or modify that atom's contributions to the original hidden state
3. Measure the causal effect (change in model outputs or loss)
4. Compare spatial concentration to baseline methods (PCA, ICA)

This grounds interpretability in actual causality rather than correlation.

## Main Ideas & Key Contributions

### 1. First Mechanistic Interpretability Framework for PINNs

PhysSAE introduces the first systematic framework for understanding PINN internal mechanisms through sparse autoencoders applied to penultimate-layer activations. This is the first work to ask: what physical features do PINNs discover internally, and do those features causally influence the network's outputs?

### 2. Discovery of Sparse, Physically-Structured Representations

The framework reveals that PINNs develop **sparse, physically-structured latent representations**:

- Key atoms in the SAE dictionary align with independently-defined physical observables (max Pearson correlation |r| = 0.951)
- Bilateral (two-atom) representations often outperform single atoms, suggesting PINNs naturally decompose physics into complementary features
- Successful PINNs have lower-rank, well-localized representations; failed PINNs show higher-rank, more diffuse activations

### 3. Quantified Causal Localization

SAE achieves **1.2–4.2× more spatially concentrated causal footprints** than traditional dimensionality reduction (PCA, ICA) across six PDE families. This means:

- SAE-discovered atoms have more localized causal effects in the spatio-temporal domain
- Intervention on top-aligned atoms shows strong, localized impact on PDE residuals
- The sparsity constraint naturally produces more interpretable features than dense decompositions

### 4. Failure Diagnosis and Validation

PhysSAE enables **diagnostics for PINN training failure**:

- Failed PINNs show characteristic patterns: higher-rank representations, greater diffusion, degraded alignment with physical observables
- SAE can identify what a PINN has learned vs. failed to learn, guiding interventions
- This provides trustworthy diagnostics for scientific computing workflows where validation is critical

## Methodology & Implementation

### Experimental Setup

**PDE Families Tested** (six domains):
1. Burgers equation (1D advection-diffusion)
2. Schödinger equation (dispersive PDE)
3. Allen-Cahn equation (reaction-diffusion)
4. Korteweg-de Vries (KdV) equation (nonlinear waves)
5. Sine-Gordon equation (soliton dynamics)
6. Navier-Stokes equations (fluid mechanics)

**PINN Architecture**:
- Multi-layer fully-connected networks with 5–8 hidden layers
- Layer width: 128–256 neurons
- Activation: tanh or ReLU
- Training: Adam optimizer with learning rate scheduling
- Collocation points sampled uniformly in spatio-temporal domain

### Three-Stage Pipeline

**Stage 1: Activation Extraction**
- Train PINN on target PDE
- Sample dense spatio-temporal grid (e.g., 50×50 grid for 2D domain)
- Extract penultimate-layer activations on this grid
- Results in activation matrix: $A \in \mathbb{R}^{(N \times M) \times d}$ (spatio-temporal points × layer dimension)

**Stage 2: Sparse Autoencoder Training**
- Overcomplete SAE: $d_{decoder} = 2 \times d$ (2x expansion)
- Sparsity coefficient: $\lambda \in [0.1, 1.0]$ (tuned per network)
- Training objective: reconstruction loss + L1 sparsity
- Top-K activation: keep K most-active atoms, zero others (for discrete sparsity)

**Stage 3: Causal Intervention & Evaluation**
- For each discovered atom $i$:
  - Compute atom's contribution to each activation
  - Ablate atom in original hidden state
  - Measure change in: PDE residual, output values, loss
  - Localize effect to spatial coordinates
- Compare concentrations with PCA/ICA baselines

### Evaluation Metrics

**Alignment with Physical Observables** (max Pearson |r| = 0.951):
- Independently define ground-truth physical quantities (e.g., gradients, pressure, velocity magnitude)
- Compute correlation between discovered atoms and these observables
- High correlation indicates atoms represent interpretable physics

**Causal Footprint Concentration**:
- Measure spatial extent of a feature's causal effect
- Metric: standard deviation of effect across spatial coordinates, or fraction of domain where effect exceeds threshold
- 1.2–4.2× more concentrated for SAE vs. PCA/ICA → stronger localization

**Faithful Feature Detection**:
- Compare ablation effects for top-aligned atoms vs. random controls
- Top atoms show consistent, significant effects; random controls show negligible effects
- Bilateral representations outperform single atoms in explaining variance

**Failure Diagnosis**:
- Analyze rank and diffusion patterns of failed vs. successful PINNs
- Failed networks show: (1) higher feature rank, (2) less localized representations, (3) degraded alignment with physics

[Exact figures unavailable — see full paper for comprehensive results tables and visualizations]

### Limitations and Considerations

1. **Computational Cost**: Training SAEs on dense spatio-temporal grids for large networks is resource-intensive
2. **Hyperparameter Sensitivity**: Sparsity coefficient and expansion ratio require tuning; no universal optimal values identified
3. **Alignment Metric Dependency**: Pearson correlation assumes linear alignment; nonlinear relationships may be missed
4. **Domain-Specific**: Framework applied to residual-loss PINNs; applicability to other PINN variants (noise-robust, probabilistic) unclear
5. **Limited Scale**: Experiments on moderate-sized networks; scalability to very large scientific models not demonstrated

## Practical Applications & Real-World Use Cases

### 1. Scientific Computing & PDE Solving

**Medical Diagnostics**: Patient-specific cardiovascular simulations for surgical planning require millisecond-scale inference with validated accuracy. PhysSAE provides trustworthy diagnostics to confirm that a PINN has learned the correct cardiovascular dynamics before clinical deployment.

**Climate and Weather Modeling**: Inverse problems inferring material properties or forcing terms from observational data require repeatedly solving forward PDEs. PhysSAE can validate that learned representations align with expected climate physics (e.g., pressure gradients, temperature gradients).

**Materials Science**: Predicting material behavior under stress requires solving nonlinear PDEs. PhysSAE reveals whether the network learned stress-strain relationships or other unintended features, guiding model refinement.

### 2. Failure Detection and Debugging

When a PINN fails to converge or produces unphysical solutions:
- PhysSAE analyzes the learned representations
- Identifies what physics the network did vs. did not learn
- Guides architecture changes, hyperparameter tuning, or training strategies

Example: High-rank, diffuse representations suggest spectral bias or optimization failure, pointing toward higher-frequency activation functions or better initialization.

### 3. Inverse Problem Validation

Inferring unknown parameters (material properties, source terms) from observations requires trust in the solver. PhysSAE's interpretability provides evidence that the network learned physically meaningful representations, not dataset artifacts.

### 4. Regulatory & Compliance

In regulated domains (FDA-approved medical devices, NIST standards for scientific computing):
- Explainability and validation are mandatory
- PhysSAE provides mechanistic evidence of correct physics learning
- Addresses "black box" concerns for high-stakes scientific applications

## Insights & Implications

### Advancing Mechanistic Interpretability in Scientific ML

PhysSAE demonstrates that mechanistic interpretability—understanding neural networks at the level of individual features—is feasible and valuable even for domain-specific tasks like PDE solving. This bridges the gap between deep learning and traditional scientific computing, where interpretability is paramount.

### PINN Architecture and Optimization Insights

The discovery of sparse, physically-structured representations suggests that:
- PINNs naturally organize features around physical concepts
- Enforcing or encouraging this structure could improve training efficiency
- Failure modes have diagnostic signatures visible in feature space

### Trustworthy Scientific Computing

By providing interpretable, causally-grounded explanations of what PINNs learn, PhysSAE enhances trust in neural network-based scientific computing—critical for high-stakes applications in medicine, climate, and engineering.

### Future Directions

1. **Extension to other PINN variants**: Operator networks, probabilistic PINNs, multifidelity models
2. **Scalability**: Apply to very large networks and high-dimensional PDEs
3. **Automated failure recovery**: Use SAE diagnostics to automatically suggest architectural or training modifications
4. **Human-in-the-loop validation**: Integrate PhysSAE with domain expert feedback for collaborative interpretability
5. **Theoretical analysis**: Prove guarantees about alignment with true physical laws under certain conditions

## Code & Resources

**Official Repository**: [Available on arXiv paper page](https://arxiv.org/abs/2609.07061) (check supplementary materials section for GitHub link)

**Key Components**:
- Sparse autoencoder training on PINN activations
- Causal intervention machinery for direct effect evaluation
- Alignment computation with physical observables
- Visualization tools for feature activation and causal footprints

**Dependencies**:
- PyTorch (neural network training)
- JAX or PyTorch for automatic differentiation (PDE residual computation)
- NumPy, SciPy for numerical methods and causal analysis
- Matplotlib/Plotly for visualization

**Computational Requirements**:
- GPU recommended for efficient SAE training on large activation matrices
- Memory: 8GB+ for medium-sized networks and dense spatio-temporal grids
- Training time: hours to days depending on network size and PDE complexity

## Related Work & Context

### Connection to Broader xAI and Mechanistic Interpretability

**Feature Attribution Methods** (LIME, SHAP, Integrated Gradients):
- PhysSAE differs by focusing on **internal representations** rather than input attribution
- Provides causal evidence, not just correlational feature importance

**Concept-Based Explanations**:
- Similar to TCAV (Testing with Concept Activation Vectors) but tailored to scientific domains
- Atoms are automatically discovered from data, not manually specified

**Sparse Autoencoders in LLM Interpretability**:
- Related to recent work on SAEs for interpreting large language models (e.g., discovering interpretable features in transformer hidden states)
- PhysSAE applies this mechanistic approach to scientific computing, a distinct domain

**Mechanistic Interpretability Community**:
- Aligns with "circuits" perspective: understanding neural networks as compositions of interpretable, interacting components
- Extends mechanistic interpretability from vision/NLP to scientific ML

### Recent Related Work

- **Sparse autoencoders for transformers**: Bau et al., Touvron et al. (discovering features in large models)
- **Interpretable PINN improvements**: Work on structured, constrained PINNs that enforce known physics
- **Causal inference in neural networks**: Intervention-based analysis of learned representations
- **Trustworthy scientific computing**: Validation and uncertainty quantification for neural PDE solvers

### Positioning in xAI Research

PhysSAE positions mechanistic interpretability as essential for high-stakes scientific applications, complementing explainability work in domains where:
1. Ground truth (physical laws) is known
2. Validation is critical (medical, climate, engineering)
3. Internal mechanisms directly encode domain knowledge

This creates a bridge between classical interpretable machine learning (decision trees, GAMs) and modern mechanistic interpretability for deep networks.

## Key Takeaways

1. **First mechanistic interpretability framework for PINNs**: Reveals what physical features hidden layers learn
2. **Sparse, causal interpretability**: 1.2–4.2× more spatially-concentrated features than traditional methods
3. **Failure diagnosis**: Representation patterns diagnostic of training failure; enables validation
4. **Trustworthy scientific computing**: Interpretable evidence that PINNs learned correct physics, essential for high-stakes applications
5. **Mechanistic interpretability for scientific ML**: Bridges deep learning and classical scientific computing traditions

