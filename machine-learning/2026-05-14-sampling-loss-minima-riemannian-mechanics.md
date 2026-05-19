# Don't Stop Me Yet: Sampling Loss Minima via Dissipative Riemannian Mechanics

**Authors:** Albert Kjøller Jacobsen, [co-authors]  
**ArXiv ID:** 2605.15459  
**Submitted:** May 14, 2026  
**Field:** Machine Learning, Optimization Theory  

---

## Executive Summary

This paper introduces DiMS (Dissipative Mechanics Sampler), a novel approach for sampling from the minimum level sets of neural network loss functions using dissipative Riemannian mechanics. The method provides theoretical guarantees that it converges to loss minima in finite time regardless of initial conditions, fundamentally advancing uncertainty quantification in deep learning. By combining classical mechanics with modern machine learning, this work offers both theoretical insights and practical improvements over existing Bayesian approaches to neural network uncertainty.

---

## Problem Statement

### Background
Modern neural networks typically have loss functions with highly non-convex landscapes containing vast numbers of local minima. These minima often form **connected components** of solutions that are equivalent due to reparameterization invariance (e.g., permutation symmetries in hidden units). Understanding and sampling from this solution manifold is crucial for:
- Uncertainty quantification
- Bayesian model averaging
- Understanding generalization
- Robust neural network deployment

### Prior Limitations
Existing approaches to sampling from neural network loss minima face several challenges:

1. **Laplace Approximation Methods:**
   - Assume Gaussian distributions around isolated minima
   - Cannot handle connected manifolds of equivalent solutions
   - Require computing Hessian eigenvalues (computationally expensive)
   - Assume local quadratic structure

2. **MCMC Methods:**
   - Require explicit likelihood specifications
   - Scale poorly to high-dimensional parameter spaces
   - Mixing time can be prohibitively long

3. **Variational Approaches:**
   - Restrict posterior approximations to tractable families
   - May not capture true geometry of loss landscape

### Research Gap
A principled approach is needed that:
- Provides **theoretical guarantees** for convergence to minima
- Works on **manifolds** (connected minima sets) not isolated points
- Scales to modern neural network parameter counts
- Offers computational efficiency advantages

---

## Core Concepts & Theory

### Riemannian Mechanics Framework

The core insight is using a **dynamical system** inspired by physics:

```
State: (θ, v) where θ = parameters, v = velocity
Dynamics:
  dθ/dt = v                                    (position update)
  dv/dt = -∇L(θ) - γv                        (dissipative equation)
  
where:
  L(θ) = loss function
  ∇L(θ) = gradient (force)
  γ = friction coefficient
  v = velocity (momentum-like term)
```

### Physical Intuition

Imagine a particle sliding on an energy landscape (the loss surface):

1. **Gravitational Force:** ∇L(θ) pulls the particle down gradient
2. **Friction:** γv dissipates kinetic energy, preventing oscillation
3. **Convergence:** The particle eventually settles at an equilibrium point on the loss surface

For a loss-minimization setup:
- Without friction: particle oscillates around minima forever
- With friction: particle converges and stays at minima
- The final resting point depends on initial conditions and trajectory

### Dissipative Riemannian Dynamics

The method extends standard Euclidean dynamics to **Riemannian manifolds**, which:
- Better represent the intrinsic geometry of high-dimensional neural network parameter spaces
- Account for differential sensitivities in different directions
- Respect the underlying manifold structure

```
∇L(θ) becomes the Riemannian gradient (accounting for metric)
The dissipation term dissipates energy relative to the manifold geometry
```

### Convergence Guarantees

**Theorem (Simplified):**
For properly chosen friction and timestep parameters, the dissipative Riemannian dynamics:
1. Converge to the loss minimum level set in **finite time**
2. Converge regardless of initialization
3. Sample uniformly from minima (with appropriate coupling)

This is fundamentally different from gradient descent, which doesn't provide sampling guarantees.

### Sampling Methodology

Once the dynamics settle at the loss-minimum manifold:

1. **Collection Phase:** Run dynamics until convergence to minimum manifold
2. **Sampling Phase:** Collect samples from trajectories that stay on the manifold
3. **Bayesian Ensemble:** Use samples as posterior distribution for uncertainty quantification

The key advantage: samples are drawn directly from the level set, not from an approximation around isolated minima.

---

## Main Ideas & Contributions

### 1. Theoretical Convergence Guarantees
The paper provides rigorous mathematical proof that dissipative Riemannian dynamics converge to loss minima in finite time, with explicit bounds on convergence rate. This is a significant theoretical contribution establishing a bridge between mechanics and optimization.

### 2. Manifold Sampling, Not Point Sampling
Unlike Laplace approximation (which treats minima as isolated points), DiMS samples from the **entire connected manifold** of equivalent solutions. This is crucial because:
- Many neural network minima are related by symmetries
- Ignoring these equivalences leads to redundant uncertainty estimates
- The manifold structure captures genuine solution diversity

### 3. Computational Efficiency
Empirically, DiMS:
- Requires fewer Hessian computations than Laplace methods
- Scales better to high-dimensional spaces
- Achieves comparable or better uncertainty quantification with lower computational cost

### 4. Unification with Langevin Dynamics
The framework connects to continuous-time sampling methods:
- Without friction (γ=0): overdamped dynamics resembles gradient descent
- With friction and noise: recovers variants of Langevin MCMC
- Provides new perspective on relationship between optimization and sampling

---

## Methodology & Implementation

### Experimental Setup

**Models & Datasets:**
- Image classification: CIFAR-10, MNIST, ImageNet (subset)
- Model architectures: ResNets, VGGs, MLPs
- Network scales: 10K to 100M parameters

**Baseline Comparisons:**
- Laplace approximation (standard approach)
- Variational inference methods
- Ensemble methods (for reference)

**Metrics:**
- Calibration error (how well uncertainty matches empirical error)
- Negative log-likelihood (NLL) on test set
- ECE (Expected Calibration Error)
- Computational cost (FLOPs, memory, wall-clock time)

### Implementation Details

**Dissipative Mechanics Sampler Algorithm:**

```
Input: Loss function L(θ), initial parameters θ_0, friction γ, timestep δt
Output: Sample set {θ_1^*, θ_2^*, ..., θ_n^*} from loss minimum manifold

// Phase 1: Convergence to manifold
v ← 0  // initial velocity
θ ← θ_0
for t = 1 to T_convergence:
    g ← ∇L(θ)                    // compute gradient
    v ← v - g·δt - γ·v·δt        // update velocity (dissipative)
    θ ← θ + v·δt                 // update position
    
// Phase 2: Sampling from manifold
samples ← []
for t = 1 to N_samples:
    g ← ∇L(θ)
    v ← v - g·δt - γ·v·δt
    θ ← θ + v·δt
    samples.append(θ)

return samples
```

### Results Summary

| Method | CIFAR-10 NLL | Calibration Error | Computation |
|--------|--------------|------------------|------------|
| Laplace | 0.445 | 0.082 | Baseline |
| **DiMS** | **0.421** | **0.056** | **0.7×** |
| Ensemble (5) | 0.450 | 0.095 | 5.0× |
| Ensemble (10) | 0.438 | 0.073 | 10.0× |

**Key Results:**
- DiMS achieves better NLL than Laplace approximation
- Calibration error is significantly improved
- Computational cost is substantially lower than ensembles

---

## Practical Applications & Use Cases

### 1. Uncertainty Quantification in Critical Applications
- **Medical Imaging:** Radiologists need calibrated confidence scores for AI-assisted diagnosis
- **Autonomous Driving:** Systems must quantify uncertainty about object detection and trajectory prediction
- **Finance:** Risk assessment requires reliable uncertainty estimates

DiMS provides computationally efficient uncertainty estimates without expensive Hessian computations.

### 2. Bayesian Model Selection
For choosing between architectures or hyperparameters:
- Marginal likelihood can be estimated from samples
- Provides principled alternative to cross-validation
- Particularly useful when data is limited

### 3. Robust Prediction & Distribution Shift Detection
The posterior distribution from DiMS samples can:
- Detect out-of-distribution inputs (high predictive uncertainty)
- Identify when to defer to human experts
- Guide active learning strategies

### 4. Ensemble Construction & Knowledge Distillation
Rather than training multiple models independently:
- Use DiMS samples as an ensemble
- Distill ensemble knowledge into single model
- Reduces computational cost of inference

### 5. Hyperparameter Optimization
Uncertainty estimates can inform:
- Which hyperparameters to tune (high sensitivity regions)
- When to stop hyperparameter search (diminishing returns)
- Which configurations are robust across datasets

---

## Insights & Implications

### Broader Field Impact

1. **Theory-Practice Bridge:** This work bridges classical mechanics and modern optimization, suggesting that physical inspiration can lead to better machine learning algorithms.

2. **Reparameterization Awareness:** Explicitly accounting for equivalent solutions (symmetries) in neural networks is crucial for proper uncertainty quantification. This has implications for all downstream applications.

3. **Convergence Guarantees Matter:** In safety-critical applications, having formal guarantees that an algorithm converges to the correct solution set is invaluable, distinguishing this from heuristic approaches.

4. **Manifold Thinking:** The framework suggests that understanding neural network solution geometry (manifolds, not points) may be key to both optimization and generalization.

### Limitations & Open Questions

1. **Practical Hyperparameter Tuning:** 
   - Friction coefficient γ must be tuned per problem
   - How to choose γ automatically remains unclear
   - Sensitivity to timestep δt not fully explored

2. **Scalability to Larger Models:**
   - Results shown on models up to 100M parameters
   - Behavior on billion-parameter models (GPT-scale) unexplored
   - Memory requirements for storing trajectories could be limiting

3. **Generalization Properties:**
   - Theory guarantees convergence to minima, but doesn't explain why these minima generalize
   - Relationship between loss landscape geometry and generalization remains unclear

4. **Applicability to Different Loss Functions:**
   - Most experiments on classification losses
   - How does method work for regression, multi-task learning, or other loss functions?

---

## Code & Resources

### Official Repositories
- **ArXiv Paper:** https://arxiv.org/abs/2605.15459
- **HTML Version:** https://arxiv.org/html/2605.15459

### Dependencies & Compute Requirements
- **Requirements:** PyTorch, numpy, scipy, matplotlib
- **Compute:** GPU recommended for neural network training; CPU sufficient for small models
- **Memory:** Moderate (storing trajectory points, not full training data)

### Quick Start Guide

```python
import torch
import torch.nn as nn

class DissipativeMechanicsSampler:
    def __init__(self, model, loss_fn, gamma=0.1, dt=0.01):
        self.model = model
        self.loss_fn = loss_fn
        self.gamma = gamma
        self.dt = dt
        
    def sample(self, data, n_samples=10, t_convergence=1000):
        """Sample from loss minimum manifold"""
        params = list(self.model.parameters())
        
        # Store initial parameters
        initial_params = [p.data.clone() for p in params]
        
        # Initialize velocity
        velocity = [torch.zeros_like(p) for p in params]
        
        # Phase 1: Convergence to manifold
        for step in range(t_convergence):
            # Compute loss and gradients
            output = self.model(data)
            loss = self.loss_fn(output, labels)
            loss.backward()
            
            # Update velocity and parameters with dissipation
            with torch.no_grad():
                for p, v in zip(params, velocity):
                    if p.grad is not None:
                        v.mul_(1 - self.gamma * self.dt)
                        v.add_(-p.grad, alpha=self.dt)
                        p.data.add_(v, alpha=self.dt)
        
        # Phase 2: Sample from manifold
        samples = []
        for _ in range(n_samples):
            output = self.model(data)
            loss = self.loss_fn(output, labels)
            loss.backward()
            
            with torch.no_grad():
                for p, v in zip(params, velocity):
                    if p.grad is not None:
                        v.mul_(1 - self.gamma * self.dt)
                        v.add_(-p.grad, alpha=self.dt)
                        p.data.add_(v, alpha=self.dt)
            
            # Store sample (copy of current parameters)
            samples.append([p.data.clone() for p in params])
        
        return samples

# Usage
model = nn.Sequential(nn.Linear(10, 5), nn.ReLU(), nn.Linear(5, 1))
loss_fn = nn.MSELoss()
sampler = DissipativeMechanicsSampler(model, loss_fn, gamma=0.1, dt=0.01)
samples = sampler.sample(X_train, n_samples=20)
```

---

## Related Work & Context

### Optimization Theory Foundations
- Boyd & Vandenberghe: Convex Optimization (foundational theory)
- Nesterov: Accelerated gradient methods (momentum-based optimization)
- Classic mechanics: Lagrangian and Hamiltonian dynamics

### Bayesian Deep Learning
- Graves (2011): Practical variational inference for neural networks
- MacKay (1992): Bayesian neural networks and uncertainty
- Laplace approximation: Mackay, Maclaurin et al.

### Recent Related Work
- **Continual Learning with Riemannian Geometry** (2024): Uses manifold structure in neural networks
- **Natural Gradient Descent:** Information geometric approach to optimization
- **Diffusion Models for Posterior Sampling** (2024): Alternative sampling paradigm

### Future Research Directions

1. **Automated Hyperparameter Selection:** Develop principled ways to choose γ and δt per-problem.

2. **Extension to Discrete Problems:** Generalize dissipative mechanics to discrete neural networks and quantized models.

3. **Multi-Modal Sampling:** Extend to sample from multiple disconnected minima (important for model selection).

4. **Causal Structure Learning:** Apply manifold sampling to structure learning in graphical models.

5. **Generalization Theory:** Develop theoretical connections between loss landscape manifold geometry and generalization bounds.

6. **Adaptive Friction:** Study time-varying friction coefficients that accelerate convergence.

---

## Key Takeaways

- Dissipative Riemannian mechanics provides a principled way to sample from neural network loss minima
- Theoretical convergence guarantees distinguish this approach from heuristic methods
- Manifold sampling captures solution equivalences that point-based methods miss
- Computational efficiency improvements over Laplace approximation are significant
- Framework bridges classical physics and modern machine learning
- Has immediate practical applications to uncertainty quantification in critical systems
