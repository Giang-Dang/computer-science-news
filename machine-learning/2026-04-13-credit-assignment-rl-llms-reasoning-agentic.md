# From Reasoning to Agentic: Credit Assignment in Reinforcement Learning for Large Language Models

**ArXiv ID:** [2604.09459](https://arxiv.org/abs/2604.09459)  
**Author:** Chenchen Zhang (Independent Researcher)  
**Submitted:** April 13, 2026  
**Field:** Machine Learning / Reinforcement Learning / Large Language Models

---

## Executive Summary

This paper presents the first comprehensive survey of **credit assignment (CA)** methods for reinforcement learning with large language models, covering 47 techniques published between 2024 and early 2026. It introduces a unifying two-dimensional taxonomy organized by assignment granularity (token → segment → step → turn → multi-agent) and methodology (Monte Carlo, temporal difference, model-based, game-theoretic), revealing key structural differences between *reasoning RL* (single long-form generation) and *agentic RL* (multi-turn environment interaction). The survey is essential reading for anyone working on RLHF, GRPO, PPO-based LLM training, or building agentic AI systems, as it systematically maps what works, what fails, and what remains unsolved in the credit assignment landscape.

---

## Problem Statement

### The Sparse Reward Problem in LLM Training

Modern LLM training increasingly relies on reinforcement learning from outcome-level feedback. In RLHF, a reward model scores a complete response. In math reasoning, a verifier checks only the final answer. In coding, a test harness judges the final program. These are all **sparse, outcome-level rewards** — the reward signal arrives at the very end of a long generation, providing no guidance about which intermediate decisions were good or bad.

This creates the **credit assignment problem**: given a trajectory $\tau = (s_0, a_0, s_1, a_1, \ldots, s_T, a_T)$ and a terminal reward $R_T$, how do we determine how much each action $a_t$ at each step $t$ contributed to $R_T$?

### Two Regimes of Credit Assignment

The paper identifies two fundamentally different settings where CA problems arise:

**Regime 1 — Reasoning RL:**
- A single chain-of-thought (CoT) response: 500–30,000+ tokens
- Actions = individual tokens or reasoning steps
- Single episode, no external environment
- Challenge: the causal chain from intermediate token choices to final answer quality is dense and entangled

**Regime 2 — Agentic RL:**
- Multi-turn interaction with external environment (tools, web, code interpreter, other agents)
- 100–1,000+ interaction turns, trajectories of 100K–1M tokens
- Stochastic transitions, partial observability, delayed feedback
- Challenge: environment noise makes it hard to isolate the agent's contribution from environmental luck

### Why This Matters

The choice of CA method directly determines:
- **Training efficiency:** Poor CA leads to gradient noise and slow convergence
- **Policy quality:** Methods that misattribute credit create systematic biases
- **Safety:** Incorrectly attributing harmful outputs makes alignment training less reliable
- **Scalability:** As LLMs become longer-context and more agentic, CA complexity grows super-linearly

---

## Core Concepts & Theory

### Formalization

The RL problem for LLMs is formalized as a Markov Decision Process (MDP):
- **State** $s_t$: current context (prompt + tokens generated so far)
- **Action** $a_t$: next token (vocabulary size ~100K)
- **Policy** $\pi_\theta$: the LLM parameterized by $\theta$
- **Reward** $R_t$: typically 0 for all intermediate steps, $R_T \neq 0$ at the end
- **Value function** $V^\pi(s_t) = \mathbb{E}_\pi\left[\sum_{k=t}^T \gamma^{k-t} R_k \mid s_t\right]$

### The Policy Gradient Theorem

The fundamental training signal in policy gradient methods is:
$$\nabla_\theta J(\theta) = \mathbb{E}_\tau\left[\sum_{t=0}^T \nabla_\theta \log \pi_\theta(a_t \mid s_t) \cdot \Psi_t\right]$$

where $\Psi_t$ is the **credit signal** for action $a_t$. Different choices of $\Psi_t$ define different CA methods:

| Method | $\Psi_t$ | Properties |
|--------|-----------|------------|
| REINFORCE | $G_t = \sum_{k=t}^T \gamma^{k-t} R_k$ | High variance, unbiased |
| PPO | $A_t = G_t - V(s_t)$ | Lower variance, needs value fn |
| GRPO | $A_t = R_T - \bar{R}$ (group mean) | No value fn, simple |
| DAPO | Token-level KL-clipped advantage | Fine-grained, stable |
| Process RM | $A_t = r_\text{PRM}(s_t, a_t) - V(s_t)$ | Dense rewards via PRM |

### Granularity Levels

The paper's primary axis of organization is the **granularity** at which credit is assigned:

**Token-level CA:**
- Each generated token receives an individual credit signal
- Finest granularity, highest computation cost
- Methods: token-wise advantage normalization, per-token KL penalties

**Segment-level CA:**
- Credit assigned to semantic segments (sentences, reasoning steps, tool calls)
- Balance between granularity and tractability
- Methods: step-wise reward models, process reward models (PRM)

**Step-level CA (in agentic settings):**
- One action = one agent turn (a full tool call or response)
- Natural boundary for multi-turn credit
- Methods: MCTS-based value estimation, turn-level advantage

**Multi-agent CA:**
- Credit must be distributed across agents in collaborative/competitive settings
- Methods: counterfactual reasoning, Shapley values, decentralized critics

### Methodological Categories

**Monte Carlo methods:** Sample full trajectories to estimate $G_t$. Simple but high variance. REINFORCE, GRPO.

**Temporal Difference (TD) methods:** Bootstrap from learned value function. Lower variance but needs accurate $V^\pi$. PPO, actor-critic variants.

**Model-based methods:** Learn a world model to simulate counterfactual trajectories. Most powerful but most compute-intensive. MCTS-guided CA, Dreamer-LLM approaches.

**Game-theoretic methods:** Model multi-agent credit assignment as cooperative game theory problems. Shapley value attribution for agent teams.

---

## Main Ideas & Key Contributions

### 1. Unified Two-Dimensional Taxonomy

The paper's central contribution is a **47-method taxonomy** that classifies every significant CA approach along:
- **X-axis:** Granularity (token → segment → step → turn → multi-agent)
- **Y-axis:** Methodology (MC → TD → model-based → game-theoretic)

This allows practitioners to navigate the literature systematically and identify the right CA method for their setting.

### 2. The Reasoning–Agentic Distinction

Prior surveys treat LLM RL as a monolithic problem. This paper argues that **reasoning RL and agentic RL have fundamentally different CA challenges**:

- Reasoning RL: the MDP is dense and deterministic (no external environment), so token-level or step-level CA is tractable
- Agentic RL: the MDP has stochastic transitions (environment responses are random), long horizons, and partial observability — requiring turn-level or higher CA with uncertainty quantification

### 3. Identification of Three Research Gaps

1. **The bootstrapping gap:** Most reasoning RL methods use episode-level reward without step-level feedback. PRMs (Process Reward Models) partially address this but require expensive human annotation.

2. **The agentic horizon gap:** At 100+ turns, even TD methods struggle with long-range dependencies. Transformer-based critics are emerging as a solution but are understudied.

3. **The multi-agent CA gap:** For systems with multiple interacting LLM agents (debate, coding assistants, multi-model pipelines), CA across agents is almost entirely unsolved.

### 4. Survey of Emerging Counterfactual Methods

Three independent papers appearing in a single week (HCAPO, C3, CCPO) all converge on **counterfactual credit assignment**:
- Model each turn's action as a treatment in a structural causal model
- The credit for turn $t$ is the **average treatment effect (ATE)** of taking action $a_t$ vs. counterfactual alternatives
- CCPO (2026) provides the most rigorous causal formalization

This convergence signals community consensus that counterfactual reasoning is the right framework for agentic CA.

---

## Methodology & Implementation

### Survey Scope and Selection

- **Coverage:** 47 core methods + 6 "adjacent enablers" (methods not directly CA but enabling it, e.g., PRM training techniques)
- **Period:** January 2024 – March 2026
- **Sources:** ArXiv, NeurIPS/ICML/ICLR/ACL/EMNLP proceedings, technical reports from major labs
- **Exclusions:** Methods predating LLM-scale RL, pure RLHF without CA focus

### Empirical Comparison (Where Available)

The survey compiles results across several benchmarks:

**Math reasoning (Reasoning RL):**

| Method | MATH-500 | GSM8K | Tokens/Grad |
|--------|----------|-------|-------------|
| GRPO | 78.2% | 94.1% | 8K |
| PPO | 79.8% | 94.6% | 12K |
| DAPO | 82.1% | 95.3% | 10K |
| Process RM | 84.7% | 96.2% | 15K |

**Agentic coding (Agentic RL):**

| Method | SWE-bench | Turns/Ep | Training Cost |
|--------|-----------|----------|---------------|
| GRPO (episode) | 18.3% | 12 | 1× |
| StePPO | 23.7% | 15 | 2.1× |
| CCPO | 26.4% | 18 | 3.4× |

### Key Findings on Method Effectiveness

1. **Token-level CA rarely helps in reasoning RL:** The benefit of going from episode to step-level credit is large (~5pp MATH); step to token-level yields marginal gains (<1pp) at much higher cost
2. **Value function training is the bottleneck in agentic RL:** At 100+ turns, learned value functions have high error, making TD methods unstable; MC methods are more reliable despite higher variance
3. **Process Reward Models are underutilized:** PRMs provide the richest training signal but are expensive to collect; synthetic PRMs (LLM-as-judge) are emerging as a cost-effective alternative

---

## Practical Applications & Real-World Use Cases

### 1. LLM Training at Scale

The survey directly informs practitioners at AI labs about which CA method to use for different training scenarios:
- For math/code reasoning fine-tuning: DAPO or Process RM-guided CA
- For web agent training: Turn-level CCPO or MC with hindsight relabeling
- For multi-agent systems: Shapley-value CA (emerging, not yet mature)

### 2. RLHF System Design

Alignment teams can use the taxonomy to diagnose pathologies in RLHF training:
- If the model is reward-hacking (gaming terminal reward without actually improving): use finer-grained CA (step-level)
- If training is unstable: switch from TD to MC methods with baseline normalization

### 3. Agentic Product Development

Companies building LLM agent products (coding copilots, customer support bots, research assistants) can use this work to:
- Select appropriate CA for their specific agent loop topology
- Understand sample efficiency vs. computation tradeoffs
- Anticipate failure modes of standard RLHF when applied naively to multi-turn settings

### 4. Benchmarking and Evaluation

The survey provides a structured evaluation framework for comparing CA methods on a common ground, useful for academic benchmarking papers.

---

## Insights & Implications

### Paradigm Shift: From Episode to Process

The field is clearly moving from **episode-level** (REINFORCE/GRPO: treat the whole response as a single unit) to **process-level** credit assignment (reward intermediate steps). This shift mirrors a decade-long evolution in classical RL from episode returns to step-wise TD, adapted to the unique structure of language generation.

### The Scaling Laws of Credit Assignment

An emerging pattern: as models get larger and trajectories get longer, the *relative benefit* of finer-grained CA increases, but so does the cost. There may exist an optimal CA granularity that scales with model capability — a "credit assignment scaling law" that remains uncharacterized.

### Limitations of the Survey

1. **Empirical breadth:** Many results cannot be directly compared because different papers use different base models, evaluation splits, and hyperparameters
2. **Post-training bias:** The survey focuses exclusively on RL fine-tuning; CA during pre-training (credit for which tokens to predict next) is not covered
3. **Rapid obsolescence:** The field moves so fast that some methods discussed may already be superseded

### Open Questions

- Can CA methods be designed to be compute-adaptive (more granular credit for harder examples)?
- Is there a unifying theoretical framework that encompasses both reasoning and agentic RL under a single CA formulation?
- How do CA errors propagate in multi-stage training pipelines (SFT → RM → RL)?

---

## Code & Resources

- **ArXiv Paper:** [https://arxiv.org/abs/2604.09459](https://arxiv.org/abs/2604.09459)
- **HTML Full Text:** [https://arxiv.org/html/2604.09459](https://arxiv.org/html/2604.09459)

### Key Referenced Implementations

| Method | Repository |
|--------|-----------|
| PPO for LLMs | [OpenRLHF](https://github.com/OpenRLHF/OpenRLHF) |
| GRPO | [verl](https://github.com/volcengine/verl) |
| DAPO | [ByteDance/DAPO](https://github.com/ByteDance-Seed/Seed-Thinking-v1.5) |
| Process Reward Models | [Math-Shepherd](https://github.com/OFA-Sys/Math-Shepherd) |

### Relevant Libraries

```bash
pip install trl           # HuggingFace RL for LLMs (PPO, GRPO)
pip install openrlhf      # Full PPO pipeline for LLMs
pip install verl          # GRPO, distributed RL training
```

---

## Related Work & Context

### Building On

- **Williams (1992):** Original REINFORCE algorithm
- **PPO (Schulman et al., 2017):** Foundation for most LLM RL training
- **InstructGPT (Ouyang et al., 2022):** First large-scale RLHF application
- **GRPO (DeepSeek-R1, 2025):** Simplified group relative policy optimization without value function

### Key 2025–2026 Methods Surveyed

- **StePPO (2604.xxxxx):** Step-aligned PPO, already in this repo
- **DAPO:** Token-level advantage with dual-clip and KL control
- **CCPO:** Counterfactual credit policy optimization via causal inference
- **Process RM:** PRM-guided dense reward for reasoning chains

### Where This Leads

1. **Unified reasoning + agentic training:** A single CA framework that handles both short reasoning and long agent trajectories
2. **Causal RL for LLMs:** Full integration of causal inference with LLM policy optimization
3. **Multi-agent alignment:** CA as the foundation for aligning networks of LLM agents rather than individual models
