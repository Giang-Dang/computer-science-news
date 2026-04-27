# Diffusion Sequence Models for Generative In-Context Meta-Learning of Robot Dynamics

**ArXiv ID:** [2604.13366](https://arxiv.org/abs/2604.13366)  
**Published:** April 15, 2026  
**Authors:** Angelo Moroncelli, Matteo Rufolo, Gunes Cagin Aydin, Asad Ali Shahid, Loris Roveda  
**Institution:** SUPSI (Scuola Universitaria Professionale della Svizzera Italiana)  
**Field:** Machine Learning / Robotics / Generative Models  

---

## Executive Summary

This paper introduces a novel framework for robot system identification—estimating a robot's dynamics model from observed behavior—by formulating it as a **generative in-context meta-learning problem**. Rather than learning a fixed dynamics model for each robot configuration, the approach trains a meta-model that, given a few context observations of a robot's behavior, can predict future robot states without parameter updates. Two diffusion-based approaches are introduced and compared against deterministic Transformer baselines: **Diffuser** (inpainting diffusion over joint input-observation distributions) and **conditioned diffusion** (generating future observations conditioned on control inputs). The generative formulation enables modeling uncertainty in dynamics predictions—crucial for safe robot control.

---

## Problem Statement

Accurate robot dynamics modeling is essential for model-based control: model predictive control (MPC), trajectory optimization, and safe constraint satisfaction all rely on accurate predictions of how a robot will respond to control inputs.

Traditional approaches to system identification require:
1. **Data collection**: Running experiments on each specific robot configuration
2. **Model fitting**: Fitting physics-based or learned models to the collected data
3. **Re-identification**: Repeating the process when the robot's configuration changes (different payloads, worn joints, new end-effectors)

This is **prohibitively expensive** in deployment:
- Industrial robots frequently change end-effectors for different tasks
- Hardware wear gradually changes joint dynamics
- Environmental factors (temperature, humidity) affect robot behavior

**In-context meta-learning** offers a solution: instead of re-training for each configuration, a meta-learned model can adapt its predictions based on a few context observations of the current configuration—at inference time, with no gradient updates.

### Why Generative (Diffusion) Models?

Deterministic dynamics models make a single prediction: "given input u, the next state will be x." But robot dynamics are often **uncertain** due to:
- Unmodeled physical effects (friction, compliance)
- Sensor noise
- Unknown payloads or tool dynamics

A **generative diffusion model** can instead produce a *distribution* of predictions, enabling:
- Uncertainty-aware control (plan for the worst-case trajectory, not just the mean)
- Risk-sensitive decision making
- Better calibration for safety-critical applications

---

## Core Concepts & Theory

### In-Context Meta-Learning

In-context meta-learning (also called in-context learning) is a paradigm where a model is trained to adapt its behavior based on a few examples provided at inference time, without gradient updates:

```
Meta-training: Train on many (task, context, query) triplets
  where context = [(u_1, x_1), ..., (u_K, x_K)] (K context examples)
  and query = u_{K+1} (next control input)
  and target = x_{K+1} (next state)

Meta-inference (new robot, no gradient updates):
  Given context of NEW robot: [(u_1, x_1), ..., (u_K, x_K)]
  Predict: x_{K+1} = model(context, u_{K+1})
```

The key is that training on diverse robot configurations teaches the model a general understanding of robot dynamics, enabling rapid adaptation to new configurations via context.

### Transformer-Based Meta-Model (Baseline)

The deterministic baseline uses a **Transformer** to encode the context sequence and predict future states:

```
z_context = TransformerEncoder([(u_1, x_1), ..., (u_K, x_K)])
x̂_{K+1} = TransformerDecoder(z_context, u_{K+1})
```

This is similar to how GPT processes context to predict the next token, but applied to robot state sequences.

### Diffusion Approach 1: Inpainting Diffusion (Diffuser)

The **Diffuser** approach treats the entire sequence of (input, observation) pairs as a joint distribution and uses diffusion to model this joint:

```
Full sequence: S = [(u_1, x_1), u_2, x_2, ..., u_K, x_K, u_{K+1}, ?]
                                                               ↑
                                                    This is the masked/inpainted part

Diffuser: p(x_{K+1} | S_observed) = ∫ p(x_{K+1}, S) dS_masked
```

Training uses standard DDPM with masking on the prediction target. At inference, the observed context is held fixed while the masked future state is denoised.

### Diffusion Approach 2: Conditioned Diffusion (CNN / Transformer)

The **conditioned diffusion** approach uses the context to condition a standard diffusion model:

```
z_context = ContextEncoder([(u_1, x_1), ..., (u_K, x_K)])  # CNN or Transformer

x̂_{K+1} ~ DiffusionModel(u_{K+1}, z_context)
         = Denoise(noise, conditioning = (u_{K+1}, z_context))
```

Two variants are tested:
- **CNN encoder**: Local temporal patterns in context
- **Transformer encoder**: Long-range dependencies in context

---

## Main Ideas & Key Contributions

### 1. Formulation of Robot System ID as In-Context Meta-Learning

Reframing system identification as meta-learning enables zero-shot adaptation to new robot configurations using only inference-time context—no re-training required.

### 2. Generative Diffusion Models for Dynamics Uncertainty

By using diffusion models instead of deterministic predictors, the framework captures **aleatoric uncertainty** (inherent stochasticity in dynamics) and **epistemic uncertainty** (uncertainty due to limited context). This is crucial for safety-critical robot applications.

### 3. Comparative Study of Approaches

The paper provides a rigorous comparison between:
- Deterministic Transformer (strong baseline)
- Inpainting Diffusion (Diffuser)
- CNN-conditioned Diffusion
- Transformer-conditioned Diffusion

This ablation provides the community with a clear understanding of where diffusion adds value over deterministic approaches.

### 4. Real-Time Constraint Analysis

The paper explicitly addresses the real-time constraint of robot control: dynamics models must produce predictions at control loop frequency (typically 100-1000 Hz). Diffusion models are typically slow due to iterative denoising. The paper analyzes the trade-off between prediction accuracy and inference speed.

---

## Methodology & Implementation

### Robot Dynamics Model

Robot dynamics are modeled as:
```
x_{t+1} = f(x_t, u_t) + ε
```

Where:
- `x_t` = robot state (joint positions, velocities, torques)
- `u_t` = control input (commanded torques/velocities)
- `f` = unknown dynamics function (what we're modeling)
- `ε` = noise/disturbances

### Dataset Collection

Experiments are conducted on:
- **Simulated robot arm**: 6-DOF manipulator with varying payloads (0.5 - 5 kg)
- **Real robot**: Physical robot arm with different end-effectors
- Training: 50+ robot configurations × 10K trajectories
- Test (new configurations): 10 held-out configurations

### Context Window

`K = 10-50` context observations are sufficient for reliable adaptation in most configurations. Larger K generally improves performance but increases inference cost.

### Evaluation Metrics

| Metric | Description |
|--------|-------------|
| RMSE | Root mean squared prediction error |
| NLL | Negative log-likelihood (measures calibration of uncertainty estimates) |
| Coverage | % of ground-truth states within predicted 95% CI |
| Inference latency | Time per prediction step |

### Results Summary

- **Transformer-conditioned Diffusion** achieves the best RMSE among diffusion models
- **Deterministic Transformer** baseline is competitive on RMSE but cannot provide uncertainty estimates
- Diffusion models show better **calibration** (coverage closer to 95%) than deterministic models
- Inference: diffusion models require 10-50ms per prediction vs. <1ms for deterministic; DDIM acceleration reduces this to 5-10ms

---

## Practical Applications & Real-World Use Cases

### 1. Flexible Manufacturing

Assembly lines with frequently changing tasks (different parts, tools, configurations) would benefit enormously from robots that can adapt their dynamics models on the fly. Instead of re-calibrating after every tool change, an operator provides 10-50 observations and the robot's control policy updates automatically.

### 2. Field Robotics

Robots operating in outdoor environments (search and rescue, agriculture, disaster response) face highly variable terrain and payload conditions. In-context dynamics adaptation ensures control policies remain effective as conditions change.

### 3. Medical Robotics

Surgical robots must adapt to patient anatomy and tissue properties that vary between patients and even within a procedure. Uncertainty-aware dynamics models are especially valuable here: knowing the predicted state with quantified uncertainty is essential for safe surgical planning.

### 4. Space Robotics

Robotic systems in space (Lunar rovers, orbital maintenance robots) cannot be re-trained after deployment. In-context meta-learning allows these systems to adapt to new configurations (e.g., after a hardware modification) without ground control re-training.

---

## Insights & Implications

### The Value of Generative Modeling for Control

The paper's most important insight for the robotics community is that **uncertainty quantification is not optional** for safe robot control—it is fundamental. Diffusion models provide a principled and elegant way to model dynamics uncertainty, and the accuracy-uncertainty tradeoff is manageable with modern efficient diffusion methods.

### In-Context Learning Beyond Language

In-context meta-learning has shown transformative results in language (GPT's few-shot capabilities). This paper demonstrates that the same paradigm transfers to physical system modeling, suggesting that **sequence modeling with in-context adaptation** is a general and powerful learning paradigm.

### The Deterministic vs. Generative Tradeoff

For many robotics tasks where computational speed is paramount and dynamics are well-understood, deterministic Transformers may be sufficient. For safety-critical or high-uncertainty tasks, the overhead of diffusion-based uncertainty estimation is justified.

### Limitations

- **Multi-step prediction**: Performance degrades for longer prediction horizons as errors accumulate
- **Out-of-distribution dynamics**: If the test configuration is very different from training configurations, in-context adaptation may fail
- **Latency**: Even with DDIM acceleration, diffusion models may be too slow for very fast control loops (>500 Hz)

---

## Code & Resources

- **Paper (arXiv)**: [https://arxiv.org/abs/2604.13366](https://arxiv.org/abs/2604.13366)

**Dependencies**:
- PyTorch, HuggingFace diffusers
- Robotics: PyBullet or MuJoCo for simulation
- Data: RoboMimic or custom robot trajectory datasets

**Quick Start (Conceptual)**:
```python
# Train meta-model on diverse robot configurations
meta_model = DiffusionContextTransformer(state_dim=12, action_dim=6)
meta_model.train(robot_trajectories)  # diverse configs

# At inference: new robot configuration
context = [(u1, x1), ..., (u10, x10)]  # 10 observations from new robot
predicted_distribution = meta_model(context, next_control_input)

# Sample predictions for uncertainty-aware control
samples = predicted_distribution.sample(N=100)  # 100 possible next states
safe_control = mpc_with_uncertainty(samples)
```

---

## Related Work & Context

### Prior Meta-Learning for Dynamics
- **MAML**: Model-Agnostic Meta-Learning (gradient-based, requires fine-tuning)
- **PEARL**: Posterior-based meta-RL with latent variable inference
- **RoboMorph** (2409.11815): In-context meta-learning for diverse robot morphologies

### Diffusion in Robotics
- **Diffusion Policy**: Using diffusion for action generation in imitation learning
- **DIAMOND**: Diffusion world model for RL environments
- **AnchorVLA**: Diffusion-based VLA for manipulation

### Future Directions
- Combining in-context dynamics models with model predictive path integral (MPPI) control
- Multi-robot transfer: can context from one robot inform dynamics estimation of a different robot type?
- Integration with foundation models for robotics (RoboVLMs)
