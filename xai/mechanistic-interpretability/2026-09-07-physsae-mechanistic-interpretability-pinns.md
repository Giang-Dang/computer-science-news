# PhysSAE: Mechanistic Interpretability of PINNs with Sparse Autoencoders

**ArXiv ID:** [2609.07061](https://arxiv.org/abs/2609.07061)  
**Authors:** Nandita N. Patil, Eshwar R. A., Gajanan V. Honnavar  
**Submitted:** September 7, 2026

## Executive Summary

PhysSAE is a mechanistic interpretability framework that applies sparse autoencoders (SAEs) to Physics-Informed Neural Networks (PINNs) to understand what physical features their hidden layers encode. By training SAEs on PINN activations and using direct causal intervention, the framework reveals that PINNs develop sparse, physically structured representations aligned with independently-defined physical observables. This work bridges mechanistic interpretability and scientific machine learning, enabling interpretability-aware development of neural network solvers for partial differential equations (PDEs).

**ArXiv ID**: 2609.07061  
**Submitted**: September 7, 2026  
**Authors**: Nandita N. Patil, Eshwar R. A., Gajanan V. Honnavar

---

## Problem Statement

Physics-Informed Neural Networks (PINNs) have become widely adopted in fluid mechanics, solid mechanics, and biomedical modeling. However, despite their practical success, PINNs remain "black boxes" at the feature level. Key challenges include:

- **Feature Opacity**: It is unclear what physical features the hidden layers of PINNs encode
- **Causality Ambiguity**: Unknown whether discovered features have a localized causal role in model predictions
- **Known Failure Modes**: PINNs exhibit well-characterized failure modes (spectral bias, gradient pathologies, causality violations) at the loss or gradient level, but mechanisms remain opaque at the representation level
- **Lack of Interpretability Tools**: No prior work systematically interrogated what a trained PINN actually represents in its hidden layers
- **No Post-Hoc Inspection Methods**: Absence of interpretability frameworks that can be applied to existing, frozen PINN models without retraining

Prior approaches to understanding neural network representations in scientific computing have relied on visualization or statistical analysis, lacking the mechanistic rigor needed to validate whether discovered features causally drive model behavior.

---

## Core Concepts & Theory

### Physics-Informed Neural Networks (PINNs)

PINNs are neural networks that solve PDEs by embedding the PDE residuals directly into the loss function. The training process forces the network to learn representations that simultaneously satisfy the PDE and boundary conditions. The loss function typically combines:

1. **PDE Residual Loss**: L_pde = mean_squared_error(u_t + u*u_x - nu*u_xx, 0)
2. **Boundary/Initial Condition Loss**: L_bc = mean_squared_error(predicted_BC, true_BC)

Total Loss = L_pde + L_bc

This design requires the network to develop internal representations that encode domain-specific physical knowledge, but these representations have historically been uninterpretable.

### Sparse Autoencoders (SAEs)

Sparse autoencoders are dictionary learning models that decompose high-dimensional activation vectors into sparse combinations of learned feature directions. The SAE objective combines reconstruction accuracy with sparsity:

Loss_SAE = ||x - decoder(encoder(x))||^2 + λ * L1(encoder(x))

Where:
- **x**: The activation vector from a neural network layer
- **encoder(x)**: Produces sparse codes
- **decoder**: Reconstructs the activation from sparse codes
- **λ**: Sparsity coefficient controlling the number of active features per sample
- **L1 term**: Encourages sparsity by penalizing the sum of absolute values of activations

**Key Property - Monosemanticity**: When trained with appropriate sparsity levels, SAEs discover features that encode single, interpretable concepts. This is in contrast to polysemantic features in raw neural network activations, where individual neurons respond to multiple unrelated concepts.

### Causal Intervention for Mechanistic Interpretability

PhysSAE employs direct causal intervention to validate whether discovered SAE features have a genuine causal role in PINN predictions:

**Intervention Pipeline**:
1. Identify a learned SAE feature (atom) from the dictionary
2. Ablate the feature by setting its activation to zero in the original frozen PINN hidden state
3. Measure how much the PINN output changes
4. Compute a "causal footprint" (spatial concentration of effects)

The intervention operates on frozen activations, requiring no backpropagation, enabling post-hoc analysis of any trained PINN.

**Advantage over alternatives**: Standard dimensionality reduction methods (PCA, ICA) produce orthogonal directions without enforcing interpretability or sparsity. SAE-based interventions directly validate causality rather than assuming statistical projection implies mechanistic understanding.

### Connection to Broader Mechanistic Interpretability

PhysSAE extends the sparse autoencoder framework from language models and vision transformers to scientific computing. The key insight is that SAEs discover interpretable features not just in artificial tasks, but in domain-specific hidden representations of PINNs trained to solve real PDEs.

---

## Main Ideas & Key Contributions

PhysSAE analyzes frozen PINNs through sparse dictionaries learned from their hidden activations. Physical concept fields are computed independently from reference solutions, making correlation an alignment measure rather than its own ground truth.

The study combines concept alignment with causal interventions, matched controls, and comparisons to PCA and ICA. Bilateral atom pairs offer an additional representation of physical structure and improve concept regression over individual atoms. Analysis includes both successful PINNs and difficult cases, enabling diagnosis of what a checkpoint has learned.

## Methodology & Implementation

Collect penultimate-layer activations on a space-time grid, standardize them, and train an overcomplete sparse autoencoder with a reconstruction term, an L1 penalty, and unit-normalized decoder columns. The study tunes sparsity to approximately 77-141 active atoms per sample.

Interventions remove a selected atom's contribution directly from the PINN hidden state and continue through the frozen output head, bypassing the SAE decoder. Alignment is checked against independent physical reference fields; causal footprint concentration is compared with PCA, ICA, and matched random directions.

The benchmark spans six PDE cases with multiple PINN and SAE seeds. Use the paper's tables for per-case values; the aggregate maximum does not imply that every PDE reaches that correlation.

## Main Results

Across the benchmark, maximum absolute Pearson alignment reaches 0.951. Top-aligned atom ablations have 1.2-4.2 times more concentrated causal footprints than PCA or ICA controls. Two-atom bilateral representations improve concept-regression R-squared by 0.05-0.15 over single atoms; random pairs decrease it.

Correlation, causal localization, and PINN solution quality answer different questions. Strong alignment of selected features does not certify the entire learned solution. Results concern frozen checkpoints and the tested PDE settings; training-time control and broader transfer require separate investigation.

## Practical Applications & Real-World Use Cases

### 1. **Scientific Machine Learning and Engineering Design**

**Application**: Understanding PINN solutions for fluid dynamics simulations
- **Use Case**: Design of airfoil shapes, optimizing aerodynamic efficiency
- **Benefit**: Engineers can verify that the PINN has learned the correct physics (pressure gradients, boundary layer separation)
- **Example**: In CFD simulations, PhysSAE atoms align with vorticity and velocity gradients, confirming physical correctness
- **Impact**: Reduces risk of deploying PINNs with incorrect learned behaviors

### 2. **Biomedical Modeling and Clinical Decision Support**

**Application**: Mechanistic interpretability for PDEs in cardiac electrophysiology or drug diffusion
- **Use Case**: Understanding neural network solutions to reaction-diffusion equations modeling drug concentrations in tissue
- **Benefit**: Verify that predicted drug distributions follow expected physiology
- **Challenge**: Regulatory compliance (FDA) requires explainability; PhysSAE provides mechanistic validation
- **Example**: Discovering atoms corresponding to drug-protein binding rates and tissue perfusion

### 3. **Climate and Weather Modeling**

**Application**: Interpretability in neural operators for climate predictions
- **Use Case**: Understanding what atmospheric physics a PINN-based climate model has learned
- **Benefit**: Identify whether the model captures feedback loops, energy conservation, and convection patterns
- **Impact**: Increased trust in neural surrogate models for climate simulations (e.g., replacing expensive numerical solvers)

### 4. **Failure Diagnosis and Debugging**

**Application**: Systematic diagnosis of PINN failure modes
- **Use Case**: When a PINN fails to solve a difficult PDE (e.g., Allen-Cahn with β=30)
- **Benefit**: PhysSAE reveals which physics components the network has not learned
- **Iterative Improvement**: Guided by interpretability insights, practitioners can:
  - Adjust loss weighting to emphasize neglected PDE terms
  - Modify network architecture or activation functions
  - Augment training data in regions where atoms show low alignment
- **Example**: Discovering that a PINN has not learned high-order derivatives, prompting architectural modifications

### 5. **Compliance and Trustworthiness in High-Stakes Systems**

**Regulatory Context**:
- **FDA Requirements**: Medical device software needs interpretability (21 CFR Part 11)
- **EU AI Act**: Explainability mandatory for high-risk AI systems
- **Regulatory Science**: PhysSAE provides formal mechanistic evidence that neural solvers behave as expected

**Example Use Case**:
- A pharmaceutical company uses PINNs to optimize drug delivery systems
- Regulators require proof that predictions are based on known pharmacokinetics
- PhysSAE demonstrates that discovered atoms align with known drug diffusion, clearance, and binding rates
- Documentation of mechanistic alignment supports regulatory approval

### 6. **Hybrid Symbolic-Neural Models**

**Application**: Extracting symbolic equations from interpretable PINN representations
- **Use Case**: Discovering that SAE atoms encode specific PDE terms (e.g., Laplacian operator, nonlinear coupling)
- **Benefit**: Enable "physics-in-the-loop" systems where neural and symbolic components coexist
- **Future Direction**: Use atom alignments to guide automatic symbolic equation discovery

---

## Insights & Implications

### For Mechanistic Interpretability Research

1. **Domain Transfer of SAE Methods**: PhysSAE demonstrates that sparse autoencoders, initially developed for language models, successfully apply to scientific computing representations. This suggests SAEs may be broadly useful for understanding domain-specialized neural networks.

2. **Bridging Representation Learning and Domain Knowledge**: The high alignment between discovered atoms and ground-truth physics validates a key hypothesis of mechanistic interpretability: neural networks learn structured, interpretable representations when solving well-posed problems with clear ground truth.

3. **Causal Interrogation at Scale**: The ability to perform direct causal intervention on frozen models opens a path for large-scale mechanistic studies. Unlike gradient-based explanations (which conflate importance and causality), PhysSAE's direct intervention cleanly isolates causal effects.

### For Scientific Machine Learning and Neural Operators

1. **Trustworthiness of Neural Solvers**: PhysSAE provides a principled method to validate whether neural PDEs solvers have learned correct physics, addressing a critical bottleneck in adoption for high-stakes applications.

2. **Interpretability as Training Signal**: The framework suggests new training strategies:
   - Add auxiliary loss terms encouraging alignment with known physical quantities
   - Use interpretability diagnostics (atom-physics correlation) as convergence criteria
   - Iteratively improve models by targeting low-alignment physics components

3. **Failure Mode Characterization**: The diagnostic capability (revealing what physics a model has not learned) enables systematic debugging of neural operators, potentially accelerating development cycles.

### For Trustworthy AI

1. **Mechanistic Validation Beyond Accuracy**: Standard metrics (MSE, relative error) do not guarantee that a PINN has learned the "right" physics. PhysSAE adds a mechanistic layer: verifying that internal representations correspond to known physics, not accidental correlations.

2. **Transparency for Regulatory Compliance**: Mechanistic interpretability evidence (atoms aligned with known quantities, causal footprints concentrated on expected regions) provides concrete documentation for regulators and stakeholders.

### Limitations and Open Questions

1. **Theoretical Foundations**: Why do SAEs discover atoms aligned with physics? What properties of PINNs guarantee this alignment?

2. **Scalability to Complex PDEs**: Current experiments use relatively simple PDEs and small domains. Questions remain for:
   - High-dimensional problems (>3D spatial dimensions)
   - Complex coupled systems (e.g., Navier-Stokes with turbulence)
   - Long-range dependencies (rare events in stochastic PDEs)

3. **Intervention-Training Gap**: Current SAEs are trained on frozen PINN activations. Could interpretability be improved by incorporating interpretability objectives during PINN training?

4. **Generalization Across Conditions**: Do atoms discovered from one PDE domain (e.g., specific diffusion coefficient) transfer to other domains? This remains unexplored.

5. **Counterfactual Predictions**: Beyond diagnosis, can mechanistic understanding guide generation of counterfactual scenarios (e.g., "what if this PDE parameter changed")?

---

## Future Research Directions

1. **Interpretability-Aware PINN Training**
   - Incorporate mechanistic interpretability objectives into PINN loss functions
   - Encourage emergence of atoms aligned with known physics from the start

2. **Automated Physics Discovery from Atoms**
   - Develop methods to automatically extract symbolic PDE terms from discovered atoms
   - Enable hybrid symbolic-neural systems that combine interpretability and accuracy

3. **Extension to Temporal Dynamics**
   - Analyze how atoms evolve during PINN training
   - Study whether atoms emerge in interpretable stages (e.g., learning low-order derivatives before high-order ones)

4. **Cross-Domain Transfer**
   - Investigate whether atoms learned for one PDE transfer to related PDEs (e.g., different diffusion coefficients)
   - Develop transfer learning strategies leveraging mechanistic interpretability

5. **Integration with Neural Operators**
   - Extend PhysSAE to neural operator architectures (DeepONet, Fourier Neural Operators)
   - Apply interpretability to learned operators that handle entire function classes

6. **Uncertainty Quantification through Atoms**
   - Relate atom interpretability to PINN uncertainty estimates
   - Develop confidence scores based on alignment with known physics

---

## Code & Resources

- [Primary paper](https://arxiv.org/abs/2609.07061)
- [Full text](https://arxiv.org/html/2609.07061)

Consult the full text for methods and experimental settings.

## Related Work & Context

### Connection to Broader SAE Literature

**Sparse Autoencoders in Language Models**:
- Seminal work by Anthropic (Bau et al., 2023; Sharkey et al., 2024) showed SAEs discover interpretable features in GPT-2 and larger language models
- PhysSAE applies the same dictionary learning principle to a new domain (scientific computing) and validates mechanistic interpretability through domain-specific ground truth (physics)

**Related Interpretability Work on SAEs**:
- "Sparse Autoencoders Learn Monosemantic Features in Vision-Language Models" (2504.02821): Extends SAE interpretability to multimodal models
- "From Geometric Recovery to Causal Validation" (2607.12166): Develops rigorous causal evaluation frameworks for SAE features
- "Measuring Monosemanticity in Sparse Autoencoders" (2607.17770): Quantifies interpretability of discovered atoms

### Mechanistic Interpretability for Neural Networks

PhysSAE builds on foundational mechanistic interpretability work:
- **Circuit Analysis**: Studying how neural network components compose to produce outputs
- **Causal Intervention Methods**: Direct intervention to establish causality (as opposed to gradient-based attribution)
- **Polysemanticity Problem**: Understanding how single neurons encode multiple concepts and how SAEs reduce this

**Related Mechanistic Interpretability Works**:
- "Mechanistic Interpretability for Neural Networks: Circuits, Sparse Features and Symbolic Reasoning" (2607.07316)
- "Mechanistic Interpretability of Large Language Models" (broader survey on MI techniques)

### PINN Research and Interpretability

**Physics-Informed Neural Networks**:
- Foundational work: Raissi et al., "Physics-informed neural networks: A deep learning framework for solving forward and inverse problems" (2019)
- PINN improvements focus on architecture and loss functions; interpretability has been largely neglected

**Known PINN Challenges**:
- Spectral bias: PINNs struggle to learn high-frequency components
- Gradient pathologies: Training instability when PDE terms have different magnitudes
- Convergence failures: Some PDEs (Allen-Cahn, higher-order) remain unsolved by standard PINNs

**Interpretability Needs**:
- No prior work systematically interrogated PINN hidden representations
- PhysSAE fills this gap by providing mechanistic understanding of PINN internals

### Causal Inference and Explainability

PhysSAE's causal intervention approach relates to:
- **Causal Inference**: Using interventions (do-calculus) to establish causal relationships
- **Feature Importance vs. Causality**: Distinguishing statistical importance from causal mechanism
- **Counterfactual Explanations**: Understanding model behavior through "what-if" scenarios

---

## Summary

PhysSAE represents a significant advance at the intersection of mechanistic interpretability and scientific machine learning. By systematizing how to understand the internal representations of Physics-Informed Neural Networks through sparse autoencoders and causal interrogation, the work enables:

1. **Validation of Learned Physics**: Confirming that neural solvers encode correct PDE semantics
2. **Diagnosis of Failures**: Identifying which physics components a network has not learned
3. **Guided Improvements**: Informing training strategies and architectural modifications
4. **Regulatory Compliance**: Providing mechanistic evidence for high-stakes applications
5. **Trustworthiness**: Bridging the gap between high accuracy and mechanistic correctness

The framework's applicability to existing, frozen PINN models and its requirement for no architectural modifications make it immediately practical. Future work on interpretability-aware training and extension to larger, more complex PDEs promises to accelerate adoption of neural solvers in trustworthy scientific and engineering applications.
