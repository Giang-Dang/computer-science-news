# Recursive Multi-Agent Systems (RecursiveMAS)

**Paper**: [arXiv:2604.25917](https://arxiv.org/abs/2604.25917)  
**Authors**: Xiyuan Yang, Jiaru Zou, Rui Pan, Ruizhong Qiu, Pan Lu, Shizhe Diao, Jindong Jiang, Hanghang Tong, Tong Zhang, Markus J. Buehler, Jingrui He, James Zou  
**Project Page**: [https://recursivemas.github.io/](https://recursivemas.github.io/)  
**Submitted**: April 2026  
**Field**: Machine Learning / Multi-Agent Systems  

---

## Executive Summary

RecursiveMAS introduces a novel framework for multi-agent AI systems that replaces token-level text communication between agents with **continuous latent-space state transfer**. Inspired by recursive computation principles (which enable single models to loop over their own representations), RecursiveMAS extends this idea to networks of heterogeneous agents, connecting them into a unified recursive loop via a lightweight two-layer module called **RecursiveLink**. Evaluated across 9 benchmarks spanning mathematics, science, medicine, search, and coding, RecursiveMAS achieves an average **8.3% accuracy improvement**, **1.2–2.4× inference speedup**, and **34.6–75.6% reduction in token usage** compared to state-of-the-art text-based multi-agent systems — fundamentally rethinking how AI agents should communicate.

---

## Problem Statement

### The Token Communication Bottleneck in Multi-Agent Systems

Current multi-agent LLM systems communicate exclusively through natural language text. One agent generates a response, its tokens are decoded to a string, and that string is then tokenized again as the next agent's input. This text-in, text-out interface has several critical limitations:

**1. Information Bottleneck**: A language model's internal reasoning exists as rich, high-dimensional hidden states (residual stream activations, attention patterns, layer-wise representations). When the model converts this internal state to output text, it is forced to *compress* its thinking into the discrete vocabulary of natural language. Nuanced intermediate reasoning steps, uncertainty estimates, and sub-symbolic patterns are irreversibly lost in this discretization.

**2. Computational Redundancy**: Each agent in a pipeline re-tokenizes and re-encodes the text from the previous agent. This is equivalent to converting a floating-point computation result to a string and then parsing that string back into a number — a lossy and wasteful round-trip. In practice, much of the early-layer processing in agent N is redundant re-encoding of information that agent N-1 already computed.

**3. Vocabulary Mismatch and Semantic Drift**: Different agents may use different phrasings for the same concept. Text normalization, paraphrasing overhead, and potential semantic shifts all accumulate as information passes through a multi-agent pipeline.

**4. Token Budget Pressure**: Explicit text communication consumes context window tokens. In long-horizon multi-step reasoning tasks, each agent's verbose explanation consumes space that could otherwise be used for additional computation or task-relevant information.

### Limitations of Prior Multi-Agent Architectures

- **Chain-of-Thought Pipelines (AutoGPT, BabyAGI)**: Entirely text-based; agents have no direct access to each other's internal states.
- **Mixture-of-Experts (MoE) routing**: Routes different tokens to different expert networks, but experts don't communicate — they operate independently on separate input fragments.
- **Recursive Language Models (RLM, arXiv:2512.24601)**: Apply recursion to *single* models — the model loops over its own hidden states. RecursiveMAS extends this to *multi-agent* settings with heterogeneous models.
- **Speculative Decoding / Draft Models**: Use a small model to predict tokens for a large model, but communication is still at the token level.

---

## Core Concepts & Theory

### Recursive Computation in Single Models

Before understanding RecursiveMAS, it helps to understand the single-model case. Recursive Language Models (RLMs) allow a model to feed its own hidden states back as inputs across multiple "rounds," enabling iterative refinement in continuous space:

```
Round 1: Input_tokens → [LLM] → Hidden_states_1 → Output_1
Round 2: Inner_RecursiveLink(Hidden_states_1) → [LLM] → Hidden_states_2 → Output_2
...
```

The RecursiveLink module maps the model's last-layer hidden states back into the input embedding space, allowing the next round to start from where the previous round's *internal state* left off — not from a tokenized string.

### Extending to Multi-Agent Systems

RecursiveMAS generalizes this idea to a system of $K$ heterogeneous agents $\{M_1, M_2, \ldots, M_K\}$ (which may have different architectures, sizes, and specializations):

```
Agent M_1: Input → [Inner Loop: latent thoughts] → [Outer RecursiveLink] → M_2
Agent M_2: Latent input from M_1 → [Inner Loop: latent thoughts] → [Outer RecursiveLink] → M_3
...
Agent M_K: Latent input from M_{K-1} → [Inner Loop: latent thoughts] → [Outer RecursiveLink] → M_1
    ↑_______________________________________________________________|  (recursive loop)
```

The entire system forms a **closed recursive loop** in latent space. No text is generated and passed between agents — only hidden state tensors are transferred.

### The RecursiveLink Module

RecursiveLink is the core component enabling latent-space communication. It is a **small two-layer residual network**:

```
RecursiveLink(h) = h + MLP(LayerNorm(h))
```

where $h$ is a hidden state vector of dimension $d$. The residual branch (the "$+h$" term) is crucial: it preserves the original latent semantics, so the module only needs to learn the *distributional shift* between two agents' latent spaces — not a full transformation from scratch. This makes training more stable and efficient.

**Two instantiations**:

1. **Inner RecursiveLink** (within a single agent): Maps the agent's own last-layer hidden states back to its input embedding space, enabling multiple rounds of latent refinement before generating output. This implements in-agent "latent thinking."

2. **Outer RecursiveLink** (between agents): Maps agent $M_i$'s last-layer hidden states into agent $M_{i+1}$'s input embedding space, transferring the internal state across heterogeneous architectures. The challenge here is the domain gap — $M_i$ and $M_{i+1}$ may have different embedding dimensions, vocabulary sizes, and learned feature distributions.

**Handling heterogeneous agents**: For cross-architecture transfer (e.g., from a 7B to a 70B model), the outer RecursiveLink includes an optional linear dimension adapter before the residual block:

```
h_adapted = W_adapt · h    (if dimensions differ)
RecursiveLink(h_adapted) = h_adapted + MLP(LayerNorm(h_adapted))
```

### Inner-Outer Loop Learning Algorithm

Training RecursiveMAS involves optimizing both the agent weights and the RecursiveLink weights jointly. The authors develop a **nested optimization** strategy:

**Inner Loop** (per-agent latent refinement):
- For each agent $M_i$ and each recursion round $r$, compute the forward pass through the inner RecursiveLink and the agent backbone.
- Accumulate gradients from the task loss back through all rounds.

**Outer Loop** (cross-agent co-optimization):
- After each agent finishes its inner-loop computation, pass the resulting latent state through the outer RecursiveLink to the next agent.
- Gradients flow through the outer RecursiveLink back to the previous agent, enabling cross-agent credit assignment.

This means RecursiveMAS supports **end-to-end gradient backpropagation through the entire multi-agent pipeline** — something impossible with text-based communication, where the tokenization step breaks the gradient graph.

**Theoretical properties** (proved in the paper):
- **Runtime complexity**: RecursiveMAS is more computationally efficient than standard text-based MAS at equal task performance.
- **Gradient stability**: The residual design of RecursiveLink ensures stable gradients even through many recursion rounds.

---

## Main Ideas & Key Contributions

### Contribution 1: The RecursiveMAS Framework

A general framework for converting any set of LLM agents into a recursively-communicating latent-space system. The framework is modular — it can be instantiated with any combination of agent types.

### Contribution 2: The RecursiveLink Module

A minimal, trainable bridge module that transfers latent states across:
- Multiple rounds within a single agent (inner RecursiveLink)
- Different agents in the multi-agent loop (outer RecursiveLink)

The key design insight: using a residual architecture so the module only needs to learn distributional shifts, not complete transformations.

### Contribution 3: Four Agent Collaboration Patterns

The paper instantiates RecursiveMAS under four representative collaboration patterns:

| Pattern | Description | Use Case |
|---|---|---|
| **Sequential** | Agents in a chain, each refining the previous agent's output | Multi-step reasoning pipelines |
| **Parallel** | Multiple agents process the same input, outputs merged | Ensemble reasoning |
| **Hierarchical** | Manager agent delegates to specialized worker agents | Complex task decomposition |
| **Iterative Refinement** | Same agent(s) loop multiple times | Self-correction and polish |

### Contribution 4: Inner-Outer Loop Learning

An end-to-end training algorithm that enables gradient flow across agent boundaries — something fundamentally impossible in text-based multi-agent systems.

### Contribution 5: Theoretical Analysis

Formal proofs of RecursiveMAS's computational efficiency and gradient stability properties, grounding the empirical results in theory.

---

## Methodology & Implementation

### Experimental Setup

**Agents used**: RecursiveMAS is evaluated with combinations of LLMs of various sizes (1B to 70B parameters), including both homogeneous setups (all agents are the same model) and heterogeneous setups (different model architectures).

**Collaboration patterns**: All 4 patterns above are evaluated.

**Benchmarks (9 total)**:
- **Mathematics**: GSM8K, MATH
- **Science**: ARC-Challenge, GPQA-Diamond
- **Medicine**: MedQA, PubMedQA
- **Search**: HotpotQA, 2WikiMultiHopQA
- **Code**: HumanEval, MBPP

### Baselines Compared

- Text-based multi-agent systems (standard pipeline)
- Single-agent models with chain-of-thought
- Recursive single-agent models (RLM)
- Advanced prompting baselines (self-consistency, majority voting)

### Results

| Metric | RecursiveMAS vs. Text-Based MAS |
|---|---|
| Average accuracy improvement | +8.3% |
| Inference speedup | 1.2× – 2.4× |
| Token usage reduction | 34.6% – 75.6% |

**Key finding**: The speedup comes from two sources:
1. Fewer tokens need to be generated per agent (since detailed reasoning is done in latent space, not serialized to text).
2. Subsequent agents don't need to re-encode information the previous agent already processed.

**Heterogeneous agents**: RecursiveMAS works across different model sizes and architectures with minimal performance degradation from the cross-architecture transfer.

### Implementation Details

- RecursiveLink adds ~2–5% additional parameters relative to the base agent models
- Training adds ~10–20% overhead relative to training individual agents independently
- Inference overhead from RecursiveLink is negligible (a 2-layer MLP over hidden states)

---

## Practical Applications & Real-World Use Cases

### 1. Scalable AI Reasoning Pipelines

Enterprise AI applications that currently chain multiple LLM calls (query → retrieval → reasoning → synthesis → response) can adopt RecursiveMAS to reduce latency and cost by 34–75% on token usage while improving accuracy.

### 2. Scientific Discovery Workflows

In multi-step scientific reasoning (hypothesis generation → literature search → experiment design → result interpretation), latent communication allows intermediate reasoning to remain richer and more nuanced than natural language serialization.

### 3. Code Generation and Debugging Systems

A pipeline where one agent generates code, a second agent reviews it for correctness, and a third suggests optimizations can benefit dramatically from latent communication — the reviewer gets direct access to the generator's uncertainty signals, not just its text output.

### 4. Multi-Modal Reasoning Chains

When text agents need to hand off context to vision agents (or vice versa), latent transfer could reduce the lossy conversion between modalities. RecursiveMAS provides a principled framework for doing this.

### 5. Agentic Search and Retrieval

Multi-hop question answering systems that alternate between reasoning and search can use RecursiveMAS to carry reasoning context across search iterations without ballooning context windows.

### Implementation Challenges

- **Requires joint training**: RecursiveMAS needs agents to be fine-tuned together to learn the RecursiveLink connections. Off-the-shelf pretrained models cannot be dropped in without fine-tuning.
- **Gradient explosion risk**: Despite the residual design mitigation, training very deep recursive loops (many agents, many rounds) can still exhibit instability without careful learning rate scheduling.
- **Deployment complexity**: Serving RecursiveMAS requires holding multiple agent models in GPU memory simultaneously and managing the latent state tensors between them.

---

## Insights & Implications

### Broader Implications for the Field

RecursiveMAS represents a paradigm shift in how we think about multi-agent coordination:

1. **Language is not the only or best medium for agent communication**. Agents are neural networks that think in high-dimensional continuous space — forcing them to communicate through natural language is an unnecessary constraint inherited from human communication conventions.

2. **End-to-end training across agent boundaries is feasible and beneficial**. The ability to backpropagate gradients through multiple agents enables a form of distributed credit assignment that text-based systems cannot achieve.

3. **Multi-agent systems can be treated as unified computational graphs**, not just orchestrated sequences of independent model calls.

### How This Advances State-of-the-Art

- First work to demonstrate systematic efficiency gains (both accuracy and compute) from latent-space multi-agent communication
- Proves that heterogeneous agents (different sizes and architectures) can be linked in latent space without catastrophic performance degradation
- Provides a theoretical framework connecting recursive computation literature to multi-agent systems

### Limitations

- **Training cost**: Requires fine-tuning all agents jointly; cannot use existing zero-shot models out of the box.
- **Interpretability**: Latent communication is less interpretable than text communication — debugging "what did agent A tell agent B?" becomes harder.
- **Context window constraints**: The paper doesn't fully address how RecursiveMAS handles very long context tasks where KV-cache management across agents becomes complex.
- **Generalization to new agents**: Adding a new agent to an existing RecursiveMAS setup requires retraining the outer RecursiveLink modules connecting to it.

### Open Questions

- Can RecursiveMAS be extended to asynchronous/parallel agent execution?
- How does the latent communication degrade when agents are updated independently post-deployment?
- Can RecursiveLink be learned in a few-shot or zero-shot manner to enable plug-and-play agent composition?

---

## Code & Resources

- **Official GitHub**: [https://github.com/RecursiveMAS/RecursiveMAS](https://github.com/RecursiveMAS/RecursiveMAS)
- **Project Page**: [https://recursivemas.github.io/](https://recursivemas.github.io/)
- **ArXiv Paper**: [https://arxiv.org/abs/2604.25917](https://arxiv.org/abs/2604.25917)
- **HuggingFace Paper Page**: [https://huggingface.co/papers/2604.25917](https://huggingface.co/papers/2604.25917)

### Quick Start

```python
# From the official RecursiveMAS repo
from recursivemas import RecursiveMAS, Agent, RecursiveLink

# Define agents (can be different models)
agents = [
    Agent(model="meta-llama/Llama-3.1-8B-Instruct", role="generator"),
    Agent(model="meta-llama/Llama-3.1-70B-Instruct", role="critic"),
    Agent(model="meta-llama/Llama-3.1-8B-Instruct", role="synthesizer"),
]

# Initialize RecursiveMAS with sequential collaboration
mas = RecursiveMAS(
    agents=agents,
    pattern="sequential",
    inner_rounds=3,     # latent thought rounds per agent
    outer_rounds=2,     # full system recursion rounds
)

# Forward pass (returns final output + latent states)
output = mas.forward(input_text="Solve this multi-step problem: ...")
```

### Computational Requirements

- Training: Multi-GPU setup with enough memory to hold all agent models simultaneously (e.g., 4×A100 80GB for 3 agents of 7B each)
- Inference: Single or dual A100 for smaller model configurations; larger setups for 70B+ models

---

## Related Work & Context

### Builds Upon

- **Recursive Language Models** (arXiv:2512.24601, December 2025): Introduces recursive computation for single models; RecursiveMAS is the multi-agent generalization.
- **Society of Mind** (Minsky, 1986): Philosophical precursor — intelligence as emergent from many interacting agents. RecursiveMAS provides a concrete ML implementation.
- **Mixture-of-Experts**: Related in spirit (multiple specialized components), but MoE routing is static and non-communicating; RecursiveMAS features dynamic, iterative cross-agent communication.
- **Graph Neural Networks**: The cross-agent latent communication in RecursiveMAS resembles message passing in GNNs — agents are nodes, RecursiveLinks are edges.

### Related Contemporary Work

- **StePPO / StePo (credit assignment in RL for LLM agents)**: Addresses a related problem of multi-step credit assignment for LLM agents but in the RL rather than supervised/distillation setting.
- **AgentGL** (already in this repo): Explores graph-based learning for LLM agent systems; RecursiveMAS provides a complementary view of multi-agent architectures.
- **STEPPO** (already in this repo): Step-aligned policy optimization for agentic RL; RecursiveMAS's inner-outer learning algorithm shares conceptual similarities.

### Where This Research Leads

- **Specialized agent networks**: Large ecosystems of fine-grained specialist agents that communicate in latent space, orchestrated by a router.
- **Latent communication protocols**: Developing standardized latent transfer formats that allow pre-trained agents to communicate without joint training.
- **Neural architecture search for agent topologies**: Learning the optimal agent graph structure (who communicates with whom) end-to-end.
