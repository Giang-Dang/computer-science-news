# Physics-Guided Convolutional Neural Network for Domain Growth Prediction in Systems with Conserved Kinetics

**Authors:** Vijay Yadav, Madhu Priya, Manish Dev Shrimali, Prabhat K. Jaiswal

**ArXiv ID:** 2606.26128

**Date Published:** June 2026

## Executive Summary

This paper presents a novel approach to surrogate modeling for physics-governed systems by proposing an attention-based, physics-guided convolutional neural network to learn microstructural evolution described by nonlinear partial differential equations (PDEs). Specifically, the model accurately predicts phase separation in binary mixtures governed by the Cahn-Hilliard equation while preserving conservation laws and remaining consistent with the Lifshitz-Slyozov domain-growth scaling law. This work demonstrates that deep learning surrogates can encode fundamental physics principles, offering significant computational advantages over traditional numerical solvers.

## Problem Statement

The spatiotemporal evolution of many physical, chemical, and biological systems is governed by complex nonlinear partial differential equations (PDEs). Traditional numerical solvers for these systems face significant computational challenges:

**Limitations of Traditional Approaches:**
- **Computational Cost:** Solving nonlinear PDEs numerically is expensive and time-consuming
- **Long-Time Integration:** Accurate long-term predictions require fine temporal and spatial discretization
- **Scaling Issues:** Many systems require large domain sizes and long simulation times
- **Inflexibility:** Changing parameters or initial conditions requires complete resimulation

**Why Physics-Guided Learning Matters:**
Recent successes with neural network surrogates demonstrate potential, but prior approaches face critical issues:

1. **Conservation Law Violation:** Standard deep learning models often violate fundamental physics principles
2. **Long-Time Instability:** Without physics constraints, predictions diverge from true solutions over extended timesteps
3. **Generalization Failure:** Models trained on specific initial conditions fail on others

**The Phase Separation Problem:**
Phase separation in binary mixtures (described by the Cahn-Hilliard equation) is a canonical test case for surrogate models:
- Requires capturing nonlinear dynamics
- Must preserve mixture composition (conservation law)
- Exhibits well-understood scaling laws (Lifshitz-Slyozov growth)
- Relevant to materials science and other domains

## Core Concepts & Theory

### The Cahn-Hilliard Equation

The Cahn-Hilliard equation models phase separation in binary mixtures:

```
∂φ/∂t = ∇²(M ∂f/∂φ - λ∇²φ)
```

Where:
- **φ:** Composition field (volume fraction of one component)
- **M:** Mobility coefficient (governs kinetics)
- **f(φ):** Free energy density function
- **λ:** Interface energy parameter

**Key Physics Principles:**
1. **Mass Conservation:** The total composition integral must be conserved over time
2. **Energy Minimization:** The system evolves to minimize free energy
3. **Spinodal Decomposition:** Unstable compositions spontaneously separate into distinct phases
4. **Domain Growth:** Phase domains grow according to characteristic scaling laws

### Lifshitz-Slyozov Domain-Growth Law

As phase separation progresses, the characteristic domain size grows following:

```
⟨R(t)⟩ ∝ t^(1/3)
```

This power-law scaling is a fundamental prediction of phase separation theory and any accurate surrogate must respect this relationship.

### Physics-Guided Neural Network Approach

The key innovation is encoding physics constraints directly into the neural network architecture and training process:

**Soft Constraint Approach:**
- Physics principles included in loss function rather than as hard constraints
- Allows for principled trade-offs between data fit and physics satisfaction
- More flexible than hard constraint enforcement

**Loss Function Components:**
1. **Data Fitting Loss:** Standard supervised learning loss on predicted vs. true fields
2. **Conservation Loss:** Penalty for violating mass conservation
3. **Physics-Informed Loss:** Additional terms enforcing physical principles

### Architecture Design

**U-Net-Like Structure with Attention:**

```
Input Field (spatial composition)
        ↓
    Encoder (Downsampling)
    ├─ Downblock 1 (Conv + ReLU)
    ├─ Downblock 2
    ├─ Downblock 3
    ├─ Downblock 4
        ↓
    Bridge (Attention Mechanism)
    ├─ Multi-head self-attention
    ├─ Feature interaction learning
        ↓
    Decoder (Upsampling)
    ├─ Upblock 1 (Transpose Conv + ReLU)
    ├─ Upblock 2
    ├─ Upblock 3
    ├─ Upblock 4
    ├─ Residual connections
        ↓
Output Field (next timestep)
```

**Key Architectural Features:**
1. **Residual Connections:** Preserve low-level features during upsampling
2. **Attention Mechanisms:** Learn which spatial regions are most important for prediction
3. **Symmetric U-Net:** Contracting and expanding paths preserve spatial information
4. **Multiple Scale Processing:** Captures both fine-scale details and coarse-scale structure

## Main Ideas & Contributions

### 1. Attention-Based Physics-Guided Architecture
- Combines convolutional neural networks with attention mechanisms
- Integrates physics constraints as soft penalties in training
- Specifically designed for spatiotemporal PDE systems

### 2. Conservation-Respecting Surrogate Model
- Explicitly enforces mixture composition conservation during training
- Provides guarantees on physical validity of predictions
- Enables long-time rollouts without violation accumulation

### 3. Lifshitz-Slyozov Consistency
- Model predictions consistent with theoretical domain growth scaling law
- Demonstrates that neural networks can learn fundamental physics principles
- Validates model generalization across different initial conditions

### 4. Long-Time Prediction Stability
- Accurate predictions over extended timestep sequences (tested over long rollouts)
- Unlike standard neural networks, maintains accuracy as rollout length increases
- Enables practical use as computational surrogate

### 5. General Framework for Conserved Dynamics
- Approach extensible to other physical systems with conserved quantities
- Applicable to chemical reaction systems, biological pattern formation, materials evolution
- Provides template for future physics-guided surrogate modeling

## Methodology & Implementation

### Training Dataset

**Phase Separation Simulation Data:**
- Generated using Cahn-Hilliard equation numerical solver
- Both critical compositions (φ = 0.5) and off-critical compositions (φ ≠ 0.5)
- Diverse initial conditions simulating realistic material preparation

**Data Characteristics:**
- Spatiotemporal field data: composition distribution φ(x,y,t)
- Multiple time sequences capturing full phase separation process
- Various system sizes and parameters

### Experimental Setup

**Model Training:**
1. Initialize model with random weights
2. Optimize with physics-informed loss combining:
   - Prediction accuracy (MSE between predicted and true fields)
   - Conservation penalty (mass balance violation)
   - Physics consistency terms
3. Training on GPU hardware for efficiency

**Evaluation Protocol:**

**Test Cases:**
- **Critical Mixture (φ = 0.5):** Symmetric phase separation
- **Off-Critical Mixture (φ ≠ 0.5):** Asymmetric domain growth
- **Long-Time Rollouts:** Extended predictions to test stability

**Comparison Baselines:**
- Traditional Cahn-Hilliard numerical solver (ground truth)
- Standard CNN without physics constraints
- Other deep learning surrogate approaches

### Evaluation Metrics & Results

**Quantitative Results:**

| Metric | Result |
|--------|--------|
| Long-Time Prediction Accuracy | Stable across long rollouts |
| Mass Conservation Error | Minimal during evolution |
| Domain Size Growth Consistency | Matches Lifshitz-Slyozov law |
| RMSE vs Numerical Solver | Low error maintaining over time |
| Computational Speedup | Orders of magnitude faster than traditional solvers |

**Key Findings:**

1. **Stability Over Long Timesteps:**
   - Model maintains accuracy even for extended rollouts
   - Traditional neural networks diverge rapidly; physics-guided model remains accurate
   - Demonstrates value of physics constraints for long-term prediction

2. **Conservation Law Preservation:**
   - Mixture composition conserved throughout evolution
   - No accumulation of conservation violations
   - Physics-informed training directly prevents this failure mode

3. **Scaling Law Consistency:**
   - Predicted domain growth follows t^(1/3) scaling
   - Holds across different compositions and system parameters
   - Indicates model learned fundamental physics principles

4. **Generalization Capability:**
   - Model trained on specific compositions generalizes to new initial conditions
   - Predictions accurate for both compositions in training distribution and novel compositions
   - Suggests model captures fundamental dynamics rather than memorizing training data

5. **Computational Efficiency:**
   - Surrogate model provides significant speedup over numerical solver
   - Single forward pass vs. iterative numerical solution
   - Enables real-time predictions and inverse design applications

## Practical Applications & Use Cases

### 1. Materials Science and Microstructure Evolution
- **Alloy Design:** Predict phase separation in new alloy compositions
- **Solidification Modeling:** Accelerate microstructure prediction during casting
- **Aging Studies:** Simulate long-term phase evolution without expensive computation
- **Parameter Optimization:** Rapidly evaluate processing conditions

### 2. Chemical Separation Processes
- **Liquid-Liquid Extraction:** Predict demixing in multi-component systems
- **Polymer Processing:** Model phase separation in polymer blends
- **Emulsion Stability:** Predict evolution of emulsion microstructure

### 3. Biological Pattern Formation
- **Morphogenesis:** Simulate biological pattern formation governed by similar PDEs
- **Tissue Engineering:** Predict structure evolution in biological systems
- **Developmental Biology:** Model pattern formation in developmental processes

### 4. Climate and Earth Sciences
- **Crystal Growth:** Accelerate crystal nucleation and growth simulations
- **Mineral Formation:** Model mineral phase evolution in geological processes
- **Atmospheric Processes:** Simulate phase change processes in atmosphere

### 5. Inverse Design and Optimization
- **Target Microstructure:** Given desired final structure, find initial conditions
- **Process Control:** Optimize processing parameters to achieve desired microstructure
- **Real-Time Adaptation:** Adjust parameters during manufacturing based on surrogate predictions

## Insights & Implications

### Broader Field Impact

**Paradigm Shift in Scientific Computing:**
- Demonstrates that physics-guided deep learning surrogates can be both accurate and efficient
- Shows that neural networks can encode fundamental physics principles (conservation laws, scaling laws)
- Opens new possibilities for accelerating scientific simulations across domains

**State-of-the-Art Advancement:**
- Advances in physics-informed machine learning (PIML) and scientific computing
- Provides template for other conserved kinetics systems
- Validates long-time prediction capability of physics-guided models

### Theoretical Insights

1. **Physics Encoding:** Physics constraints can be effectively integrated into deep learning through loss function design
2. **Generalization:** Physics-constrained models generalize better to unseen initial conditions
3. **Scaling Laws:** Neural networks trained with physics guidance naturally learn fundamental scaling relationships
4. **Long-Time Behavior:** Physics constraints prevent drift and divergence in extended predictions

### Limitations and Open Questions

1. **Parameter Generalization:** How well does model transfer to different Cahn-Hilliard parameters?
2. **Dimensionality:** Validation on 3D systems (typically more computationally expensive)
3. **Complex PDEs:** Applicability to more complex systems with multiple conserved quantities
4. **Noise Robustness:** How does model perform with noisy initial conditions?

### Future Research Directions

1. **Extended Dynamics:** Apply to coupled PDE systems (e.g., reaction-diffusion, chemotaxis)
2. **Real-Time Applications:** Develop efficient inference for real-time process control
3. **Uncertainty Quantification:** Develop probabilistic variants predicting prediction uncertainty
4. **Inverse Problems:** Use as surrogate in inverse design and parameter estimation
5. **Multi-Physics:** Extend to systems with multiple conserved quantities and coupled dynamics

## Code & Resources

**Official Repository:** Not yet publicly available. Check arxiv paper for supplementary materials and contact authors.

**Dependencies:**
- PyTorch: Deep learning framework for model implementation
- NumPy/SciPy: Numerical computing and scientific functions
- FEniCS or deal.II: For generating training data via PDE solver
- Matplotlib/Visualization: For analysis and visualization

**Compute Requirements:**
- GPU: Recommended for training (NVIDIA GPU with CUDA support)
- Training Time: Hours to days depending on dataset size and model complexity
- Inference: Milliseconds per prediction on modern GPU
- Memory: ~8GB GPU memory for typical model and batch sizes

**Quick-Start Guide:**

1. **Generate Training Data:**
   ```python
   # Use numerical PDE solver to generate trajectories
   # Store composition field snapshots at regular intervals
   ```

2. **Prepare Dataset:**
   ```python
   # Organize spatiotemporal data
   # Create input-output pairs (current field → next timestep)
   ```

3. **Define Physics-Guided Model:**
   ```python
   # Initialize U-Net with attention mechanisms
   # Define loss function with physics constraints
   ```

4. **Training:**
   ```python
   # Train with physics-informed loss
   # Monitor conservation and scaling law metrics
   ```

5. **Evaluation:**
   ```python
   # Validate on test compositions and initial conditions
   # Compare with numerical solver
   # Verify conservation laws and scaling laws
   ```

6. **Deployment:**
   ```python
   # Use as efficient surrogate for predictions
   # Integrate into design/optimization workflows
   ```

## Related Work & Context

### Related Recent Papers

- **Theory of Learning High-Dimensional Controlled Non-Linear Dynamical Systems** (2026-06-07) - Theoretical analysis of neural network learning for dynamical systems
- **Can Deep Neural Networks Improve Compression of Very Large Scientific Data?** (2026-06-14) - Deep learning for scientific data processing
- **Algorithmic Foundations of Deep Learning** (2026-06-26) - Theoretical foundations of neural network approximation

### Prior Work Foundations

- Physics-Informed Neural Networks (PINNs) - Raissi et al., 2017
- Scientific Machine Learning (SciML) - Early work on combining ML with domain knowledge
- Convolutional Neural Networks - LeCun et al., 1998
- Attention Mechanisms - Vaswani et al., 2017

### Possible Future Research Directions

1. **Coupled Systems:** Extend to systems with multiple PDEs and conserved quantities
2. **Operator Learning:** Learn neural operators applicable to wide parameter ranges
3. **Uncertainty Quantification:** Probabilistic surrogates with confidence intervals
4. **Hybrid Solvers:** Combine neural surrogates with traditional solvers for speed-accuracy trade-off
5. **Transfer Learning:** Pretrain on canonical systems, fine-tune to application-specific variants
6. **Real-Time Control:** Integration into feedback control systems for manufacturing

## Conclusion

This work demonstrates that physics-guided neural networks can serve as accurate, stable, and efficient surrogates for PDE systems. By encoding conservation laws and physics principles through careful loss function design, the model achieves both high accuracy and physical consistency. The Cahn-Hilliard application provides a canonical test case validating the approach, but the methodology generalizes to other systems with conserved kinetics. This research advances the frontier of scientific machine learning, enabling practical acceleration of expensive simulations while maintaining physical validity—a critical requirement for real-world scientific and engineering applications.
