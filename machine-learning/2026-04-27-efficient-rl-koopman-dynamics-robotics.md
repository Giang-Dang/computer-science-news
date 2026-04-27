# Efficient Reinforcement Learning using Linear Koopman Dynamics for Nonlinear Robotic Systems

**ArXiv ID:** [2604.19980](https://arxiv.org/abs/2604.19980)  
**Authors:** Wenjian Hao, Yuxuan Fang, Zehui Lu, Shaoshuai Mou  
**Submitted:** April 2026  
**Field:** Machine Learning / Reinforcement Learning / Robotics  

---

## Executive Summary

Model-based reinforcement learning (MBRL) for robotic control is hampered by the nonlinearity of physical systems — learned dynamics models are complex, hard to optimize over, and prone to compounding rollout errors. This paper exploits **Koopman operator theory** to learn a *linear* representation of nonlinear dynamics in a high-dimensional feature space, then integrates this linear model into an actor-critic RL framework. Policy gradients are estimated using one-step (not multi-step) model predictions, dramatically reducing computation and rollout error accumulation. The approach is validated on simulated benchmarks and two real-world platforms: a Kinova Gen3 robotic arm and a Unitree Go1 quadruped.

---

## Problem Statement

**Standard model-based RL** learns a neural dynamics model $\hat{f}(s_t, a_t)$ and uses it for policy optimization, but faces three challenges:

1. **Nonlinearity:** Physical systems (robotic joints, quadruped locomotion) are highly nonlinear, requiring complex and data-hungry models.
2. **Rollout errors:** Multi-step trajectory simulation accumulates errors exponentially, causing policy optimization to diverge from real-world behavior.
3. **Computational cost:** Planning or differentiating through multi-step nonlinear dynamics is expensive.

**Koopman operator theory** offers a principled solution: every nonlinear dynamical system can be exactly represented by a *linear* operator in an (infinite-dimensional) function space. In practice, a finite-dimensional approximation is learned from data, providing a linear model that captures nonlinear dynamics.

---

## Core Concepts & Theory

### Koopman Operator Theory

The **Koopman operator** $\mathcal{K}$ acts on *observable functions* $g: \mathcal{S} \rightarrow \mathbb{R}^d$ of the state space:

$$\mathcal{K} g(s) = g(f(s))$$

where $f$ is the nonlinear dynamics. Key property: while $f$ is nonlinear in state space, $\mathcal{K}$ is a *linear* operator in the space of observables. This means:

$$g(s_{t+1}) = K \cdot g(s_t) + B \cdot a_t$$

for some matrices $K, B$ in the lifted space, where $g: \mathcal{S} \rightarrow \mathbb{R}^N$ is a learned lifting function (implemented as a neural network).

### Learning the Lifting Function

The lifting function $g_\phi$ and linear dynamics matrices $(K, B)$ are learned jointly from interaction data by minimizing:

$$\mathcal{L}_{\text{Koopman}} = \sum_t \| g_\phi(s_{t+1}) - K \cdot g_\phi(s_t) - B \cdot a_t \|^2$$

This is a **spectral decomposition** problem in disguise: the learning process finds the dominant Koopman eigenfunctions that best capture the system's dynamics.

### One-Step Policy Gradient Estimation

Standard MBRL differentiates through multi-step rollouts $s_0 \rightarrow s_1 \rightarrow \cdots \rightarrow s_H$, accumulating errors. This paper's key innovation: **one-step policy gradients** using the learned Koopman model:

$$\nabla_\theta J(\pi_\theta) \approx \mathbb{E}_{(s_t, a_t) \sim \mathcal{D}} \left[ \nabla_\theta \pi_\theta(a_t|s_t) \cdot \nabla_a Q(s_t, a_t) \Big|_{a_t = \pi_\theta(s_t)} \right]$$

where $Q$ is estimated using the linear Koopman model for one-step prediction only. This:
- Eliminates multi-step rollout error accumulation.
- Makes gradient computation cheap (one linear prediction vs. multi-step neural rollout).
- Enables online mini-batch learning from streamed real interaction data.

### Actor-Critic Architecture

- **Actor (Policy):** Standard neural network $\pi_\theta(a|s)$, takes raw state as input.
- **Critic (Value function):** Operates in Koopman lifted space, exploiting linearity for efficient optimization.
- **Dynamics model:** Linear Koopman model $(K, B)$ used only for one-step gradient estimation.

---

## Main Ideas & Key Contributions

1. **Koopman-lifted actor-critic:** Integrates linear Koopman dynamics into an actor-critic framework, combining global structure from Koopman theory with local gradient efficiency.

2. **One-step policy gradients:** Avoids multi-step model rollouts entirely, eliminating compounding errors and reducing computation.

3. **Online mini-batch framework:** Supports continuous learning from streaming robot data without storing large replay buffers.

4. **Real-world validation:** Demonstrated on Kinova Gen3 arm and Unitree Go1 quadruped — not just simulated benchmarks.

---

## Methodology & Implementation

### Simulated Benchmarks

| Environment | Task | MBRL Baseline | Koopman-RL (ours) |
|-------------|------|---------------|-------------------|
| Pendulum | Stabilization | 78% success | 94% success |
| HalfCheetah | Locomotion | 4,200 reward | 5,100 reward |
| Reacher | Goal reaching | 85% success | 96% success |

### Real-World Results

- **Kinova Gen3 arm:** Achieves sub-centimeter precision on pick-and-place tasks after 30 minutes of online training (vs. 2+ hours for model-free SAC baseline).
- **Unitree Go1 quadruped:** Stable locomotion at 1.5 m/s on varied terrain after 45 minutes of online adaptation.

### Sample Efficiency

Koopman-RL achieves convergence with **3–5× fewer environment interactions** compared to model-free SAC and model-based PETS, due to the efficient linear dynamics model.

---

## Practical Applications & Real-World Use Cases

1. **Industrial robot arms:** Fast online adaptation to new payloads or end-effectors without retraining from scratch.
2. **Legged robotics:** Rapid terrain adaptation for quadrupeds and bipeds in unstructured environments.
3. **Drone control:** Koopman's linear structure enables efficient model predictive control (MPC) for UAV stabilization.
4. **Medical robotics:** Safety-critical systems benefit from interpretable linear dynamics models with stability guarantees.

**Feasibility:** The Koopman lifting function adds moderate overhead (~20ms per step for a 7-DOF arm); real-time control at 50–100 Hz is achievable.

---

## Insights & Implications

- **Key insight:** Koopman theory provides a principled way to obtain a *linear* model for nonlinear systems without sacrificing accuracy, bridging classical control theory and modern RL.
- **Advancing SOTA:** One of the first works to combine Koopman operator theory with actor-critic RL and validate on real hardware.
- **Limitations:**
  - Koopman approximation quality depends on the richness of the lifting function; very high-dimensional chaotic systems require very large lifting spaces.
  - Linear approximation may be insufficient for highly discontinuous dynamics (e.g., contact-rich manipulation).
  - Online learning assumes slowly changing dynamics; sudden environment changes can temporarily degrade performance.
- **Open questions:** Can Koopman representations be shared across tasks (meta-learning Koopman operators)? How does performance scale to whole-body humanoid control?

---

## Code & Resources

- **Paper PDF:** https://arxiv.org/pdf/2604.19980  
- **Related prior work:** [Koopman Operators in Robot Learning (arXiv:2408.04200)](https://arxiv.org/abs/2408.04200)
- **Dependencies:** PyTorch, MuJoCo (simulation), ROS 2 (real-robot interface), `numpy`, `scipy` for linear algebra.
- **Hardware:** Kinova Gen3 7-DOF arm, Unitree Go1 quadruped (or simulators thereof).

---

## Related Work & Context

- **PETS (Chua et al., 2018):** Probabilistic ensemble MBRL; Koopman-RL avoids multi-step rollouts that PETS requires.
- **Koopman-Assisted RL (arXiv:2403.02290):** Related approach; this paper extends it to online streaming learning and validates on real hardware.
- **iLQR/MPC with learned dynamics:** Classical trajectory optimization; Koopman's linear structure makes MPC particularly efficient.
- **Continual Learning of Koopman Dynamics for Legged Robots (arXiv:2411.14321):** Extends Koopman to lifelong learning; complementary direction.
- **Future directions:** Combining Koopman dynamics with diffusion-based policy generation for more expressive controllers.
