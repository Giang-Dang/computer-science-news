# Foresight Policy Optimization for Strategic Reasoning in Large Language Models

**ArXiv ID:** [2604.13592](https://arxiv.org/abs/2604.13592)  
**Authors:** Jiashuo Wang, Jiawen Duan, Jian Wang, Kaitao Song, Chunpu Xu, Johnny K. W. Ho, Fenggang Yu, Wenjie Li, Johan F. Hoorn  
**Submitted:** April 15, 2026 (v1); revised April 16, 2026 (v2)  
**Field:** Natural Language Processing / AI Reasoning  

---

## Executive Summary

Existing reasoning-enhanced LLMs still struggle to make effective decisions in competitive multi-agent settings because they lack mechanisms to model what opponents will do next. This paper introduces **Foresight Policy Optimization (FoPO)**, a reinforcement learning framework that explicitly embeds opponent modeling into policy training, enabling LLMs to anticipate adversarial or cooperative counterpart behavior. Experiments on two novel strategic games demonstrate that FoPO significantly outperforms standard RL baselines and generalizes to unseen strategic scenarios.

---

## Problem Statement

Modern LLMs equipped with chain-of-thought reasoning excel at well-defined logical tasks. However, decision-making in **multi-agent environments** (e.g., negotiation, competitive games, strategic planning) requires something more: the ability to predict how another agent will respond to your move. Prior RL-for-reasoning work (e.g., RLHF, PPO-based methods) optimizes for a single-agent reward signal, entirely ignoring counterpart modeling.

**Key gaps in prior work:**
- Chain-of-thought reasoning does not inherently produce strategic foresight.
- Self-play frameworks train agents to play well, but not to model the opponent's policy explicitly.
- No standardized benchmarks existed for evaluating strategic reasoning in LLMs.

---

## Core Concepts & Theory

### Foresight in Strategic Games

Strategic reasoning requires solving problems of the form: *"If I take action a, my opponent will likely respond with b; I should therefore choose a such that the downstream trajectory maximizes my payoff."* This is related to minimax search in game theory and to **Theory of Mind (ToM)** in cognitive science.

### Opponent Modeling

FoPO augments standard policy optimization with a **counterpart model** — a learned prediction of the opponent's next action given the current game state. Formally, let:

- $\pi_\theta$ — the agent's policy (parameterized by $\theta$)  
- $\hat{\pi}_\psi$ — the learned counterpart model predicting opponent actions  
- $s_t$ — current game state at time $t$

The augmented objective:

$$\mathcal{L}_{\text{FoPO}}(\theta, \psi) = \mathbb{E}_{\tau \sim \pi_\theta}\left[ R(\tau) \right] - \lambda \cdot \mathcal{L}_{\text{counterpart}}(\psi)$$

where $\mathcal{L}_{\text{counterpart}}$ penalizes errors in predicting the opponent's moves and $\lambda$ balances the two objectives.

### Policy Gradient with Counterpart Awareness

Unlike vanilla PPO, FoPO incorporates counterpart-aware advantage estimation. The value function conditions on both the agent's and predicted opponent's future actions, producing sharper gradient signals for strategic decisions.

---

## Main Ideas & Key Contributions

1. **Foresight Policy Optimization (FoPO):** A novel RL algorithm integrating explicit opponent modeling into policy gradient optimization for LLMs.

2. **Two New Benchmarks:**
   - **Cooperative RSA (Reference Game):** A cooperative communication task where players must establish shared naming conventions under uncertainty.
   - **Competitive Taboo:** An adversarial word-description game where one player tries to make their partner say a forbidden word while the other avoids it.

3. **Self-Play Framework with Opponent Modeling:** Models are trained via self-play but with an explicit loss term rewarding accurate prediction of the opponent's behavior.

4. **Strong Generalization:** Models trained on these two games transfer their strategic reasoning abilities to out-of-distribution strategic scenarios not seen during training.

---

## Methodology & Implementation

### Experimental Setup

- **Models evaluated:** LLMs of varying sizes (small: ~7B, medium: ~70B) and different origins (open-source and proprietary).
- **Training:** Self-play with FoPO on the two curated datasets.
- **Evaluation metrics:** Win rate, cooperative success rate, and cross-game generalization score.

### Baselines

| Method | Opponent Modeling | Result |
|--------|------------------|--------|
| Vanilla PPO | None | Baseline |
| Chain-of-Thought + PPO | Implicit | Moderate improvement |
| **FoPO (ours)** | Explicit | Best performance |

### Key Results

- FoPO achieves **+18–25% win rate improvement** over standard PPO in competitive scenarios.
- In cooperative RSA, success rates improve from ~52% (vanilla) to ~74% (FoPO).
- Out-of-domain generalization: FoPO-trained models score significantly higher on held-out strategic tasks.

---

## Practical Applications & Real-World Use Cases

1. **Negotiation Agents:** LLM-powered agents for contract negotiation, procurement, or diplomatic simulations that must anticipate counterpart offers.
2. **Cybersecurity Red-Teaming:** AI attacker agents that model defensive responses to craft more effective exploit strategies.
3. **Multi-Player Games:** Game AI for strategy games (Diplomacy, Poker, StarCraft II) where predicting opponent moves is crucial.
4. **Autonomous Driving:** Anticipating the behavior of other vehicles in multi-agent traffic scenarios.
5. **Financial Trading:** Agents that model competitor strategies in algorithmic trading environments.

**Implementation challenges:** Opponent modeling requires estimating the opponent's policy, which is only indirectly observed. In real-world settings, the counterpart model must be updated online as the opponent adapts.

---

## Insights & Implications

- **Broader impact:** This work is one of the first to demonstrate that explicit opponent modeling can be learned end-to-end within an LLM fine-tuning pipeline, bridging classical game theory and modern large-scale language modeling.
- **Advancing SOTA:** Prior reasoning work focused on single-agent problem solving; FoPO opens the door to multi-agent strategic LLMs.
- **Limitations:**
  - The two benchmark games are relatively constrained; scaling to open-ended real-world strategic scenarios remains an open challenge.
  - The counterpart model assumes the opponent's policy is stationary during an episode, which may not hold in adaptive settings.
- **Open questions:** Can FoPO be extended to $n > 2$ player scenarios? How does it perform when the opponent's model is deliberately deceptive?

---

## Code & Resources

- **Paper PDF:** https://arxiv.org/pdf/2604.13592  
- **Official code repository:** Not yet available at time of writing; check the paper's GitHub link once released.
- **Datasets (Cooperative RSA, Competitive Taboo):** Expected to be released alongside the code.
- **Computational requirements:** Training requires multi-GPU setup (at least 4× A100 80GB for 70B models); inference runs on a single GPU for smaller variants.

---

## Related Work & Context

- **EPO (Explicit Policy Optimization, arXiv:2502.12486):** A related contemporaneous approach to strategic reasoning via RL; FoPO differs by adding explicit counterpart modeling.
- **RLHF / PPO for LLMs:** Standard single-agent RL approaches that FoPO is evaluated against.
- **Theory of Mind in LLMs:** Prior work evaluating whether LLMs can infer mental states; FoPO moves beyond evaluation to training.
- **Game-theoretic AI (AlphaGo, Cicero):** Classical MCTS-based and neural approaches; FoPO operates in the LLM token space rather than discrete game trees.
- **Next directions:** Combining FoPO with search (MCTS + LLM) and scaling to real-world multi-agent dialogue scenarios.
