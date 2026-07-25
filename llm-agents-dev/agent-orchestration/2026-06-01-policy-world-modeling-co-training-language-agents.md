# Policy and World Modeling Co-Training for Language Agents

**Authors:** Ning Lu, Baijiong Lin, Shengcai Liu, and collaborators

**ArXiv ID:** 2606.02388

**Date:** June 1, 2026

**Categories:** LLM Agents, Reinforcement Learning, World Models, Agent Training

## Executive Summary

This paper presents PaW (Policy and World modeling co-training), a framework that jointly trains policy learning and world modeling within a single RL training process for language agents. Rather than requiring separate simulators or additional inference stages, PaW leverages the supervision already present in on-policy RL rollouts: each interaction step provides both policy supervision (from action and advantage) and dynamics supervision (from resulting observation). This elegant co-training approach enables language agents to learn both what actions lead to high rewards and what those actions do to the environment, without additional computational overhead.

## Problem Statement

Reinforcement learning improves large language model agents by teaching which actions lead to high rewards, but provides little information about what those actions do to the environment. World modeling—understanding how the environment evolves in response to actions—could address this gap, yet existing approaches face critical limitations:

1. **Separate Simulators Required:** Traditional world modeling requires training separate environment models, adding complexity and computational cost
2. **Additional Training Stages:** Existing approaches often require pre-training world models before or alongside policy training
3. **Inference Overhead:** Some world model approaches require explicit simulation steps during agent inference
4. **Wasted Supervision:** On-policy RL rollouts contain rich environment dynamics information that goes unused for world modeling

The core challenge is efficiently incorporating world modeling supervision into RL training without incurring the traditional costs of separate simulators or additional training infrastructure.

## Core Concepts & Theory

### World Modeling for Language Agents

World models learn how environments evolve: given current state and action, predict next state observation. For language agents, this means learning to predict how tool calls or API interactions modify the environment state.

**Types of World Modeling:**
1. **Forward Models:** State + Action → Next State
2. **Inverse Models:** State Pair → Action that caused transition
3. **Latent Models:** Learning in latent representation space

**Why World Models Matter:**
- Enable better long-horizon planning
- Provide richer learning signals than reward alone
- Support learning in simulation before real execution

### On-Policy RL Rollout Structure

Every on-policy RL trajectory provides natural supervision:

```
RL Rollout: S₀ -[a₁]-> S₁ -[a₂]-> S₂ -[a₃]-> ... -[aₙ]-> Sₙ

Policy Supervision:
- Each (Sₜ, aₜ) pair with advantage R-V(S) guides policy improvement

World Modeling Supervision (PaW insight):
- Each (Sₜ, aₜ, Sₜ₊₁) triple provides dynamics training signal
- Already collected; zero additional cost
```

### Co-Training Framework

The key innovation is recognizing that policy training and world modeling can share:
1. **Same collected rollouts** (no separate data required)
2. **Same model parameters** (single model instance)
3. **Same training loop** (augmented RL objective)

## Main Ideas & Contributions

### PaW Framework Architecture

**1. Unified Model Architecture**
- Single language model with dual output heads:
  - **Policy Head:** Predicts next action token
  - **World Model Head:** Predicts next observation representation
- Both heads operate on same shared representation
- Enables parameter sharing and efficient joint training

**2. Co-Training Objective**

The training objective combines:
- **RL Loss (L_policy):** Standard policy gradient on action selection
  - Improves which actions agent chooses
  - Supervised by rewards and advantages
  
- **World Modeling Loss (L_wm):** Auxiliary objective for next-observation prediction
  - Trains dynamics understanding
  - Supervised by actual next observations from rollouts
  
- **Joint Objective:** L_total = L_policy + α × L_wm

Where α is an adaptive coefficient based on reward signal strength.

### Data-Centric Design Choices

**Action-Entropy-Based Selection:**
- Filters rollout transitions before world modeling training
- Focuses WM supervision on high-value decisions
- Prevents learning from agent's own indecision

**Robust Observation Prediction:**
- Uses clipped MAE (Mean Absolute Error) loss
- Handles prediction errors gracefully
- Prevents WM loss from dominating RL training

**Reward-Adaptive Coefficient:**
- Dynamically adjusts α based on reward signal
- When rewards are clear, weight WM appropriately
- When rewards are noisy, down-weight WM supervision
- Prevents reward signal dilution

## Methodology & Implementation

### Experimental Setup

**Target Domains:**
- Interactive agent tasks (language agents performing tool-use)
- Environments with observable state transitions
- Both discrete action spaces and continuous control

**Baseline Comparisons:**
- Standard RL without world modeling
- World modeling trained separately with additional data
- RL + world modeling with separate training pipeline
- State-of-the-art agent training methods

### Training Protocol

**On-Policy Collection:**
1. Run agent policy to generate trajectories
2. Collect (State, Action, Reward, Next State) tuples
3. Compute advantages from collected rewards

**Co-Training Loop:**
For each collected trajectory:
- Compute policy loss from action and advantage
- Compute WM loss from (State, Action, Next State) prediction
- Backprop joint loss through shared parameters
- Update both policy and world model simultaneously

**Reward-Adaptive Scheduling:**
- Monitor reward signal variance
- Adjust α dynamically based on signal quality
- Increase α when rewards are clear
- Decrease α when rewards are noisy

### Evaluation Metrics

**Agent Performance:**
- Task success rate
- Sample efficiency (learning curve)
- Planning horizon length achievable

**World Modeling Quality:**
- Next-observation prediction accuracy
- Latent representation quality
- Dynamics understanding transferred to planning

[Exact performance figures unavailable — see full paper]

### Key Results

The PaW framework demonstrates:
1. **Competitive Policy Performance:** Policy training matches or exceeds RL-only baselines
2. **Improved Generalization:** World modeling improves agent generalization to new scenarios
3. **Sample Efficiency:** Joint training achieves better sample efficiency than separate pipelines
4. **Zero Overhead:** Co-training adds minimal computational cost vs. policy-only training

## Practical Applications & Use Cases

### Interactive Language Agents

1. **Web Agents:** Learning how web APIs and interfaces respond to actions
2. **Code Generation:** Understanding how code modifications affect program state
3. **Database Agents:** Learning environment dynamics of SQL query execution

### Long-Horizon Planning

1. **Multi-Step Tasks:** World models enable better long-horizon planning
2. **Tool-Use Chains:** Understanding how tool outputs become inputs to subsequent tools
3. **Complex Workflows:** Modeling complex sequences of interactions

### Transfer and Adaptation

1. **Domain Generalization:** World model learned in one domain aids transfer to similar domains
2. **Rapid Adaptation:** Pre-learned dynamics accelerate learning in new tasks
3. **Simulation-to-Reality Transfer:** Learned world models can bridge sim-to-real gaps

## Insights & Implications

### Training Philosophy

**Reuse Over Redundancy:**
The central insight is that on-policy RL already generates the supervision needed for world modeling. Rather than collecting separate data or training separate models, PaW reuses existing supervision for joint improvement.

**Efficiency Through Alignment:**
By aligning policy training and world modeling objectives (both trained on same rollouts), the framework achieves computational efficiency that separate approaches cannot match.

### State-of-the-Art Advancement

PaW contributes to understanding:
- How to efficiently incorporate world models into RL training
- The value of joint learning compared to separate pipelines
- Practical design choices (clipped MAE, adaptive coefficients) that work well

### Broader Field Impact

This work influences:
- **Agent Research:** Shows integrated world modeling is feasible and beneficial
- **RL Design:** Suggests value of auxiliary tasks aligned with primary objectives
- **Training Efficiency:** Demonstrates computational benefits of co-training

## Limitations and Open Questions

1. **Observation Predictability:** Assumes environment states are largely predictable; may struggle with stochastic environments
2. **Scalability:** Unclear how well approach scales to very long horizons where errors compound
3. **Model Capacity:** Joint training on dual objectives may compete for limited model capacity
4. **Offline Evaluation:** Most results likely from online RL; offline RL performance unclear
5. **Generalization:** How well do learned dynamics transfer between significantly different domains?

## Code & Resources

**Official Repository:** Not specified in abstract; likely available from authors

**Paper Link:** https://arxiv.org/abs/2606.02388

**Dependencies:**
- Language model fine-tuning infrastructure
- Environment simulation (ALFWorld, WebShop, or similar)
- RL training framework (PPO, GRPO, or similar)
- Optional: Separate world model baselines for comparison

**Quick-Start Implementation:**

```python
# Pseudocode structure
for rollout in collect_trajectories():
    # Standard RL loss
    policy_loss = compute_rl_loss(rollout.actions, rollout.rewards)
    
    # Auxiliary WM loss
    predicted_next_obs = world_model_head(rollout.state, rollout.action)
    wm_loss = clipped_mae(predicted_next_obs, rollout.next_state)
    
    # Joint optimization
    adaptive_alpha = compute_reward_based_alpha(rollout.rewards)
    total_loss = policy_loss + adaptive_alpha * wm_loss
    
    optimizer.backward(total_loss)
```

## Related Work & Context

### Prior World Modeling Research

**Separate World Model Training:**
- Model-based RL approaches requiring explicit simulators
- Latent world models trained independently
- Planning with learned dynamics

**Agent Learning Methods:**
- Reinforcement learning for language agents
- Policy gradient and actor-critic methods
- Experience replay and prioritization

### Comparison with Related Approaches

**vs. Pure RL:** Adds interpretability and generalization via world modeling
**vs. Separate WM Training:** More efficient, no extra data or training stages needed
**vs. End-to-End Multi-Task Learning:** Cleaner separation of objectives through auxiliary head design

### Future Research Directions

1. **Stochastic Environments:** Extending to environments with non-deterministic dynamics
2. **Inverse Models:** Incorporating inverse modeling (action prediction from state pairs)
3. **Long-Horizon Planning:** Using learned world models for explicit planning steps
4. **Multi-Agent Scenarios:** Co-training with world models for multi-agent environments
5. **Theory and Analysis:** Formal analysis of why co-training improves sample efficiency
6. **Adaptive Architecture:** Dynamically allocating capacity between policy and world modeling heads based on task characteristics

## Discussion Questions

1. How would this approach perform in highly stochastic environments?
2. Could the world model be used explicitly during inference for improved planning?
3. How does performance scale with increasing horizon length?
4. What's the optimal balance between policy and world modeling capacity?
5. Could this framework extend to multi-agent or competitive settings?
6. How sensitive is performance to the reward-adaptive coefficient scheduling strategy?

---

## Papers Referenced in This Summary

- [Policy and World Modeling Co-Training for Language Agents](https://arxiv.org/abs/2606.02388) (2606.02388)
- [World Models: A Comprehensive Survey](https://arxiv.org/abs/2606.00133) — foundational world modeling overview
- [Reinforcement Learning for Language Agents](https://arxiv.org/abs/2604.27859) — agent RL paradigms
