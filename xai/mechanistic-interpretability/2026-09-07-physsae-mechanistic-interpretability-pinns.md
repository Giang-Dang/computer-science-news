# PhysSAE: Mechanistic Interpretability with Sparse Autoencoders for Physics-Informed Neural Networks

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

### 1. **Novel Application Domain**
PhysSAE is the first mechanistic interpretability framework applied to Physics-Informed Neural Networks. This is significant because:
- PINNs encode domain-specific knowledge (PDEs) that should be learnable as interpretable representations
- Scientific computing requires trustworthiness and explainability for high-stakes applications (engineering design, biomedical modeling)
- Understanding PINN internals can guide improvements in architecture and training

### 2. **Post-Hoc Mechanistic Interpretability for Frozen Models**
The framework requires no retraining or architectural modification:
1. Train a standard PINN on PDE problems
2. Extract penultimate-layer activations on a dense spatio-temporal grid
3. Train SAEs on these activations (task-independent dictionary learning)
4. Validate atoms through causal intervention on the frozen PINN

This modular approach enables interpretability analysis of existing PINN checkpoints.

### 3. **Alignment Between Discovered Features and Physics**
A key empirical finding is that SAE atoms discovered from raw activations align with independently-defined physical observables:

- **Metric**: Pearson correlation between SAE atom activations and ground-truth physical quantities
- **Results**: Maximum |r| = 0.951 across six PDE families
- **Statistical Validation**: Correlation always significantly exceeds permutation null distributions

Example: In the heat equation (∂u/∂t = ν∂²u/∂x²), discovered atoms directly correspond to temperature gradients and diffusion effects.

### 4. **Causality Validation at Scale**
By intervening on discovered atoms, PhysSAE demonstrates:
- **Concentrated Causal Footprint**: Top-aligned atoms show 1.2–4.2× more spatially concentrated effects compared to PCA/ICA
- **Bilateral Representations**: Two-atom bilateral structures (e.g., left and right gradients) outperform single atoms
- **Physical Consistency**: Bilateral patterns match known PDE physics (e.g., directional derivatives)

### 5. **Diagnostic Capability for PINN Failures**
PhysSAE enables diagnosing why PINNs fail:

- **Converged Cases** (Heat, Schrödinger): Atoms align perfectly with physics
- **Partially Converged** (Burgers, convection-easy): Atom alignment is imperfect, indicating incomplete learning
- **Known Failures** (Allen-Cahn, β=30): Atoms show poor alignment, revealing what physics the PINN has not learned

This diagnostic capability provides a path toward interpretability-aware training strategies.

---

## Methodology & Implementation

### Framework Overview

PhysSAE operates in three stages:

**Stage 1: Activation Extraction**
- Train a PINN to convergence on a PDE problem
- Extract the penultimate-layer activations on a dense spatio-temporal grid
- Collect activations from multiple solution snapshots for diverse training data

**Stage 2: Sparse Autoencoder Training**
- Objective: Minimize L_SAE = ||activation - decoder(sparse_code)||^2 + λ * ||sparse_code||_1
- Key hyperparameter: **Sparsity coefficient λ** chosen to yield ~77–141 active atoms per sample
- This sparsity range is calibrated based on prior SAE work on language models, balancing interpretability and reconstruction fidelity
- **Decoder normalization**: Decoder columns projected to unit norm (essential for well-defined causal intervention)
- **Training**: Standard SAE training on frozen PINN activations (no gradient flow to PINN)

**Stage 3: Causal Validation**
- For each discovered SAE atom (dictionary element):
  1. Intervene by setting that atom's coefficient to zero in the original hidden state
  2. Run the frozen PINN forward pass to compute output changes
  3. Measure spatial concentration of the output perturbation
  4. Compare to random control atoms
- Compute Pearson correlation between atom activations and ground-truth physical quantities (e.g., temperature gradients)

### Datasets and Experimental Setup

**PDE Benchmark**: Six PDE families spanning different difficulty levels:

1. **Heat Equation** (Converged)
   - ∂u/∂t = ν∂²u/∂x²
   - Simple, linear, well-posed
   - PINNs typically converge reliably

2. **Schrödinger Equation** (Converged)
   - Complex-valued, nonlinear Schrödinger equation
   - Also typically well-handled by PINNs

3. **Burgers Equation** (Partially Converged)
   - ∂u/∂t + u∂u/∂x = ν∂²u/∂x²
   - Nonlinear, but well-studied
   - Moderate learning difficulty

4. **Convection (Easy)** (Partially Converged)
   - Linear advection with source terms
   - Intermediate difficulty

5. **Allen-Cahn Equation** (Known Failure, β=30)
   - ∂u/∂t = -∂⁴u/∂x⁴ + 5u - 5u³
   - Fourth-order, highly nonlinear
   - PINNs fail due to spectral bias and higher-order derivative challenges
   - β=30 configuration is particularly difficult

**Network Architecture**:
- Fully-connected neural networks with ReLU or tanh activations
- Penultimate layer: 256–512 dimensions (input to SAE)
- Training: Adam optimizer with decreasing learning rates

**SAE Configuration**:
- Overcomplete sparse autoencoders (hidden dimension > input dimension)
- Sparsity target: 77–141 active atoms per sample (achieved through λ tuning)
- Training on 10,000+ activation vectors per PDE

### Evaluation Metrics for Interpretability

1. **Alignment with Physics**:
   - Pearson |r| between SAE atom activations and ground-truth quantities (temperature gradients, velocity, etc.)
   - Perfect alignment would be r = 1.0

2. **Causal Footprint Concentration**:
   - Measure spatial variance of output perturbations from atom ablation
   - Smaller variance → more localized, interpretable effect
   - Compared to PCA/ICA alternatives

3. **Monosemanticity**:
   - Sparsity-adjusted score measuring whether each atom responds to a single concept
   - Based on activation coherence and cross-sample consistency

4. **Bilateral Representation Quality**:
   - For symmetric PDEs, evaluate whether two atoms form consistent bilateral (left/right) pairs
   - Assessed through correlation of paired atom activations

---

## Main Results

### Empirical Findings

**Finding 1: Physical Alignment of Discovered Atoms**

Across six PDE families, discovered SAE atoms show strong correlation with independently-defined physical observables:

| PDE | Max Pearson \|r\| | Example Aligned Concepts |
|-----|-------------------|-------------------------|
| Heat | 0.951 | Temperature gradients, diffusion |
| Schrödinger | 0.945 | Wavefunction magnitude, phase |
| Burgers | 0.923 | Velocity gradients, nonlinear interactions |
| Convection (Easy) | 0.937 | Advection flux, source coupling |
| Allen-Cahn (β=30) | 0.612 | Partial alignment; PINN has not learned fine structure |
| Extended Test Case | [Varies] | Consistent pattern across configurations |

**Key Insight**: Atoms align with physics even in failure cases, but alignment strength indicates convergence quality.

**Finding 2: Causal Footprint Concentration**

When ablating top-aligned atoms, spatial concentration of output perturbations:
- SAE atoms: More concentrated effects
- PCA alternatives: 1.2–4.2× less concentrated
- Conclusion: SAE features have more localized, interpretable causal roles

**Finding 3: Superior Performance Over Statistical Alternatives**

Comparison of mechanistic interpretation methods:

| Method | Alignment Quality | Causal Localization | Interpretability |
|--------|-------------------|---------------------|------------------|
| PCA    | Lower correlation | Dispersed effects   | Hard to interpret linear combinations |
| ICA    | Moderate | Mixed results | Independent components, not necessarily physical |
| SAE    | High (0.9+) | Concentrated | Sparse, interpretable atoms |

**Finding 4: Bilateral Representations**

For symmetric PDEs (heat, Schrödinger), top atoms often form bilateral pairs:
- Example: Two atoms encoding left and right spatial gradients
- Bilateral patterns match known PDE physics
- Bilateral representations outperform single atoms at causal localization

**Finding 5: Diagnostic Capability**

Atoms reveal what a PINN has and has not learned:
- **Converged PDEs**: Atoms align with all major physical quantities
- **Partially Converged**: Atoms correspond to dominant features but miss subtle interactions
- **Failed Cases (Allen-Cahn, β=30)**: Atoms show weak alignment, indicating incomplete learning of higher-order dynamics

This diagnostic power enables targeted improvements: identifying which physics components a PINN has not learned.

### Limitations

1. **Computational Cost**: Extracting dense spatio-temporal activations and training SAEs requires GPU memory for large problems
2. **Sparsity Tuning**: Optimal sparsity coefficient (λ) must be tuned for each problem domain
3. **Limited to Post-Hoc Analysis**: Current framework analyzes frozen models; no mechanism for steering training toward better interpretability
4. **Domain Generalization**: Atoms learned on training trajectories may not transfer to out-of-distribution test cases
5. **Incomplete Formalization**: While atoms align with ground truth, theoretical guarantees about when and why this happens remain open

---

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

### Official Implementation
- **GitHub Repository**: [PhysSAE - GitHub](https://github.com/nandita-patil/PhysSAE) (expected)
- **ArXiv Paper**: https://arxiv.org/abs/2609.07061
- **ArXiv PDF**: https://arxiv.org/pdf/2609.07061

### Key Dependencies
- **Deep Learning**: PyTorch or TensorFlow
- **Scientific Computing**: JAX or NumPy for PDE solvers
- **SAE Implementation**: Sparse autoencoder libraries (OpenAI's SAE-based implementations or custom)
- **Visualization**: Matplotlib for spatial concentration plots, Plotly for interactive analysis

### Computational Requirements
- **GPU Memory**: 8–16 GB (for standard PDE problems)
- **Training Time**: SAE training typically 1–4 hours on NVIDIA A100
- **Dataset Size**: ~10,000 activation vectors per PDE problem

### Quick Start (Typical Workflow)

1. **Train a PINN** on your PDE of interest using standard frameworks (DeepXDE, JAX-based solvers)
2. **Extract Activations** from penultimate layer on a dense grid
3. **Train SAE** on activations using provided SAE trainer
4. **Validate Atoms** through causal intervention using provided evaluation scripts
5. **Correlate with Physics** by computing Pearson correlation with known physical quantities

### Interactive Visualizations
- Expected: Interactive plots showing atom-to-physics alignment
- Causal footprint visualizations (heatmaps of spatial effect concentration)
- Bilateral pattern detection and visualization

---

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
