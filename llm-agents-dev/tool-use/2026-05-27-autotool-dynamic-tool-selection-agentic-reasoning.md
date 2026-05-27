# AutoTool: Dynamic Tool Selection and Integration for Agentic Reasoning

**ArXiv ID:** 2512.13278  
**Authors:** (Research team focusing on adaptive agent tool use)  
**Date:** December 2025  
**Award:** Best Paper Award, ICCV 2025 Workshop on Multi-Modal Reasoning for Agentic Intelligence  
**Relevance:** Dynamic tool selection via ranking, RL optimization, and tool generalization for agent reasoning

---

## Executive Summary

AutoTool addresses a fundamental limitation in agentic systems: existing frameworks assume a **fixed inventory of tools**, but real-world development environments have evolving, domain-specific toolsets. AutoTool introduces a framework that enables LLM agents to dynamically select and integrate tools throughout reasoning trajectories, adapting to new or unseen tools at inference time. The system is built on a 200k dataset with explicit tool-selection rationales across 1,000+ tools and 100+ tasks (mathematics, science, code generation, multimodal reasoning). AutoTool employs a dual-phase optimization: (i) trajectory stabilization via supervised and reinforcement learning, and (ii) **KL-regularized Plackett-Luce ranking** to learn consistent multi-step tool selection policies. Results show average improvements of 6.4% (math & science), 4.5% (search QA), 7.7% (code generation), and 6.9% (multimodal tasks) over advanced LLM agents and prior tool-integration methods, with notably superior generalization to unseen tools.

---

## Problem Statement

### Development Automation Challenge

Autonomous agents for software development rely on external tools to expand reasoning capabilities:
- **Code generation** agents use interpreters, linters, type checkers, documentation systems
- **Debugging** agents invoke profilers, log analyzers, version control tools
- **Testing** agents call test runners, coverage analyzers, mocking libraries
- **Refactoring** agents use AST parsers, code formatters, complexity analyzers

Current agent frameworks either:
1. Hardcode tool inventories (e.g., "always use Python interpreter for code, always use grep for search")
2. Allow agents to call any tool, leading to inefficient or incorrect tool chains
3. Assume tools are static; fail when encountering unfamiliar tools in new domains

### Prior Agent System Limitations

Existing approaches (ReAct, Chain-of-Thought with tools, Function Calling) use simplistic tool selection strategies:
- **Greedy routing:** Pick the tool that seems most relevant; no ranking or optimization
- **Sequential chaining:** One tool's output deterministically feeds the next; no backtracking or alternative paths
- **Fixed tool sets:** Training assumes tools won't change; inference fails gracefully on unseen tools
- **No explicit learning:** Tool selection is emergent from LLM base behavior, not a learned policy

These limitations compound on long reasoning trajectories where early tool misselection cascades into later failures.

### Research Gap

How can agents learn a **ranking-based tool selection policy** that:
- Operates across 1,000+ diverse tools (not dozens)
- Generalizes to unseen tools at inference time (out-of-distribution tool sets)
- Integrates with reinforcement learning to optimize end-to-end task success
- Remains efficient (fewer wasted tool calls)

---

## Core Concepts & Theory

### Tool-Chaining and Multi-Step Reasoning

LLM agents perform agentic reasoning by interleaving thought steps with tool invocations:

```
Thought Step 1 → Tool Call 1 → Observe Result 1
                      ↓
Thought Step 2 (uses Result 1) → Tool Call 2 → Observe Result 2
                      ↓
Thought Step 3 (uses Results 1&2) → Tool Call 3 → Observe Result 3
                      ↓
... (continued until task complete or max steps)
```

**Tool selection problem:** At each thought step, the agent must decide which tool (if any) to call next. With 1,000+ tools, the action space is enormous, and poor selection early in reasoning cascades.

### Plackett-Luce Ranking for Tool Ordering

AutoTool frames tool selection as a **ranking problem** using the **Plackett-Luce (PL) ranking model:**

**Definition:** Given a set of tools T = {t₁, t₂, ..., tₙ}, the Plackett-Luce model assigns a probability to every permutation of tools based on learned utilities:

$$P(\text{permutation}) = \prod_{i=1}^{n} \frac{u_{\pi(i)}}{\sum_{j=i}^{n} u_{\pi(j)}}$$

where:
- π(i) is the i-th tool in the ranking
- u(t) is the utility (learned value) of tool t
- Higher utility tools are prioritized earlier

**Intuition:** Instead of binary "use/don't use" decisions, Plackett-Luce ranks all available tools. The top-ranked tool is selected first; if it fails or is suboptimal, the agent can backtrack or explore the next-ranked tool.

**Connection to Agentic Reasoning:**
- Each thought step induces a new ranking over available tools
- Tools with high predicted value (based on current context and problem) are explored first
- Failed tool explorations are "deprioritized" in subsequent rounds

### Dual-Phase Optimization Pipeline

#### Phase 1: Trajectory Stabilization

**Goal:** Ensure the agent follows a coherent reasoning trajectory with consistent tool selections.

**Supervised Learning:**
- Train on 200k trajectories with explicit tool-selection rationales
- Learn to predict which tool to select given context (problem, prior observations, available tools)
- Use teacher forcing to stabilize early training

**Reinforcement Learning:**
- Fine-tune with RL using task completion (pass/fail) as reward signal
- Optimize for end-to-end task success, not intermediate tool correctness
- Use policy gradient methods to learn robust selection policies

#### Phase 2: Ranking Refinement

**Goal:** Optimize tool-selection rankings using Plackett-Luce semantics.

**KL-Regularized Optimization:**
- Define a **Plackett-Luce policy** that converts model logits into tool rankings
- Optimize with **policy-level cross-entropy (CE) loss** to maximize likelihood of high-reward trajectories
- Add **KL divergence regularization** to prevent overfitting to specific tool inventories
  - Regularization: $L = -\log P(\text{trajectory}) + \lambda \cdot KL(P_{\text{new}} || P_{\text{old}})$
  - Benefit: Encourages the new ranking policy to remain close to prior knowledge, improving generalization to unseen tools

**Why Plackett-Luce + KL-Regularization?**
- **Ranking formalism:** Handles tool sets of varying sizes without retraining
- **KL-Regularization:** Prevents the model from becoming overly confident in specific tools, improving robustness when tools are unavailable or new tools are added

### Agent Topologies for Tool Selection

```
                        Agent Reasoning Loop
                              │
                              ▼
                    ┌──────────────────────┐
                    │ Current State:       │
                    │ - Problem context    │
                    │ - Prior observations │
                    │ - Available tools    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Tool Ranking Module  │ ◄─── Plackett-Luce Policy
                    │ (Learned Utilities)  │      (trained via RL + KL-reg)
                    └──────────┬───────────┘
                               │
                    Utility scores over
                    all available tools
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Top-K Tool Selection │ ◄─── Select from N tools
                    │ (e.g., Top-5)        │      in order of utility
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
         ┌─────────┐      ┌─────────┐      ┌─────────┐
         │ Tool 1  │      │ Tool 2  │      │ Tool 3  │
         │ (Python │      │ (Search │      │ (Docs   │
         │Interpret)      │ Engine) │      │ Lookup) │
         └────┬────┘      └────┬────┘      └────┬────┘
              │                │                │
         Execution Results (shared observations)
              │                │                │
              └────────────────┼────────────────┘
                               │
                    Integrate result + update state
                               │
                    Repeat: back to Reasoning Loop
```

---

## Main Ideas & Contributions

### 1. Unified Tool-Selection Policy via Ranking

**Problem:** Existing agents use heuristic, ad-hoc tool selection (e.g., "if parsing JSON, use JSON parser"). These rules don't generalize and break when tools change.

**Solution:** Learn a **unified ranking policy** that works across diverse domains and tool sets. The policy outputs utilities for each available tool, enabling Plackett-Luce ranking.

**Benefit:**
- Single model handles 1,000+ tools, not dozens
- Tool utilities are learned from task success, not hand-crafted
- Ranking allows graceful degradation if preferred tool is unavailable

### 2. Scalable Training on Tool-Selection Rationales

**Innovation:** The 200k training dataset includes **explicit rationales** for why specific tools were selected at each step:

Example trajectory:
```
Problem: "Compute the factorial of 100 and check if it's prime."

Step 1: Use Python Interpreter (rationale: "Need to compute large integer arithmetic")
Step 2: Use Math Proof Assistant (rationale: "Primality testing for large numbers requires mathematical reasoning")
Step 3: (Back-up) Use Python Math Library (rationale: "Fallback if proof assistant insufficient")
```

**Why rationales matter:**
- Teach the model not just which tool, but *why* (generalizable to new tasks)
- Enable curriculum learning: easy tasks → harder tasks
- Facilitate debugging when tool selection fails

### 3. RL + Ranking = Efficient Exploration

**Standard RL limitation:** If agents have 1,000 tool choices, the action space is huge, and exploration is inefficient (many random tool calls).

**AutoTool solution:** Use **Plackett-Luce ranking to constrain the action space:**
- Instead of exploring uniformly over 1,000 tools, prioritize top-ranked tools
- RL learns to improve ranking utilities, not individual tool policies
- This **reduces variance** in RL gradient estimates

**Result:** Faster convergence and better sample efficiency compared to naive RL over large action spaces.

### 4. Generalization to Unseen Tools

**Key Challenge:** At test time, new tools may be available (not seen during training).

**AutoTool approach:**
- Tools are represented via their descriptions/names (learned embeddings)
- Ranking utility is computed over tool embeddings, not discrete tool IDs
- New tools → new embeddings → participate in ranking automatically

**KL-Regularization ensures:**
- Ranking doesn't overfit to training tools
- Remains generalizable when tool inventory changes
- Robustness to tool removal or substitution

---

## Methodology & Implementation

### Dataset Construction

**200k Training Trajectories** across 100+ tasks:

| Domain | #Tools | #Tasks | Trajectory Count | Characteristics |
|--------|--------|--------|------------------|-----------------|
| Mathematics | ~250 | 25 | 50k | Integration, calculus, number theory, optimization |
| Science (Physics/Chemistry) | ~200 | 20 | 40k | Simulations, equation solving, unit conversions |
| Code Generation | ~350 | 30 | 70k | Interpreters, linters, profilers, debuggers, documentation |
| Search & QA | ~150 | 15 | 25k | Web search, document retrieval, ranking, synthesis |
| Multimodal Reasoning | ~200 | 10 | 15k | Image/video processing, OCR, visual reasoning |

**Rationale Annotation:** Human annotators and/or LLM-generated (Claude/GPT-4) explanations for tool selections.

### Dual-Phase Training

#### Phase 1: Trajectory Stabilization

```
Input Batch: {(problem, trajectory, tool_selections, rationales)}

Supervised Learning:
  For each step in trajectory:
    - Encode context (problem, observations, available tools)
    - Train to predict next tool (cross-entropy loss)
    - Validation: Does predicted trajectory match ground truth?

Reinforcement Learning (Policy Gradient):
  For each sampled trajectory:
    - Encode context and generate tool selections (with exploration)
    - Execute trajectory, collect reward (binary: task_success)
    - Compute policy gradient: ∇ log P(trajectory) * reward
    - Backprop to improve likelihood of successful trajectories
```

#### Phase 2: Ranking Refinement

```
Input: Stabilized agent + task reward signal

KL-Regularized Plackett-Luce Optimization:
  1. Compute tool utilities from model (current policy)
  2. Generate Plackett-Luce ranking distribution
  3. Compute policy-level CE loss:
     Loss = -log P_PL(high_reward_trajectories)
  4. Add KL regularization:
     Loss += λ * KL(P_new || P_old)
  5. Backprop and update tool utilities

Hyperparameter:
  λ (KL weight): Balance between fitting data (λ=0) and staying close to original (λ→∞)
  Tuned on validation set
```

### Evaluation

#### Benchmarks and Metrics

| Domain | Benchmark | Metric | Baseline | AutoTool | Improvement |
|--------|-----------|--------|----------|----------|-------------|
| **Math & Science** | GSM8K, MATH, Science Olympiad | pass@1 | 72.0% | 78.4% | +6.4% |
| **Search QA** | Natural Questions, HotpotQA | F1 / EM | 68.0% | 72.5% | +4.5% |
| **Code Generation** | MBPP, HumanEval | pass@1 | 68.0% | 75.7% | +7.7% |
| **Multimodal Reasoning** | MMVP, ScienceQA | Accuracy | 62.0% | 68.9% | +6.9% |

#### Out-of-Distribution (OOD) Evaluation

**Scenario:** At test time, 30% of tools are unseen (not in training set).

| Tool Presence | Seen Tools | Unseen Tools | Drop |
|---|---|---|---|
| All tools seen (baseline) | 75.7% | - | - |
| 70% tools seen, 30% unseen | 73.2% | 71.8% | -1.4% (minimal) |
| 50% tools seen, 50% unseen | 71.9% | 69.5% | -3.8% (graceful degradation) |

**Insight:** AutoTool generalizes to unseen tools because:
- Ranking learned from rationales applies broadly
- KL-regularization prevents overfitting to specific tools
- Tool embeddings enable OOD extrapolation

#### Efficiency Analysis

**Average Tool Calls per Task:**

| Method | Avg Calls | Task Success |
|--------|-----------|--------------|
| Greedy (Random selection) | 8.2 | 64% |
| Chain-of-Thought (Fixed routing) | 6.1 | 70% |
| ReAct (LLM chooses tool) | 5.8 | 73% |
| **AutoTool (Learned ranking)** | **4.9** | **75.7%** |

**Interpretation:** AutoTool achieves better task success with fewer tool calls, indicating more efficient reasoning trajectories.

---

## Practical Applications & Use Cases

### 1. IDE-Integrated Code Generation

**Scenario:** Developer in VS Code requests code completion for an algorithm problem.

```
Tool Availability: 
  - Python Interpreter, Type Checker, Linter, AST Parser,
    Stack Overflow Search, Code Formatter, Profiler, (1000+ total)

Agent Reasoning with AutoTool:
  Step 1: Rank tools by utility
    1. Interpreter (u=0.95) - "Need execution to validate"
    2. Type Checker (u=0.92) - "Type-driven development"
    3. Search (u=0.80) - "Find similar solutions"
    ... (remaining 997 tools)
  
  Step 2: Select Interpreter → Execute code → Observe result
  Step 3: Error in type system → Re-rank (Type Checker utility ↑)
  Step 4: Select Type Checker → Fix types
  Step 5: Code complete, rank Search lower (not needed)
```

**Benefit:** Efficient exploration of large tool spaces; graceful degradation if tools unavailable.

### 2. Continuous Integration and Automated Testing

**Scenario:** CI/CD pipeline has 200+ test-related tools (linters, formatters, security scanners, coverage analyzers).

- **Problem:** Which tools to run? In what order? (Each run costs time/resources)
- **AutoTool Solution:** Learn ranking of tools by their bug-detection effectiveness and speed
- **Result:** Run most impactful tools first; fail fast if critical issues found

### 3. Multi-Domain Problem Solving (Research/Education)

**Scenario:** Math researcher tackling a cross-disciplinary problem requiring calculus, numerics, and symbolic reasoning.

```
Available Tools:
  - Symbolic algebra system (SymPy, Mathematica)
  - Numerical solver (SciPy, MATLAB)
  - Visualization (Matplotlib, Wolfram Alpha)
  - Literature search (arXiv, Google Scholar API)
  - Formal proof system (Coq, Lean)

AutoTool Ranking:
  Problem: "Prove existence of solutions to PDEs"
  1. Formal proof system (u=0.98) - "Rigor required"
  2. Symbolic algebra (u=0.90) - "Symbolic manipulation"
  3. Numerical solver (u=0.75) - "Verify with examples"
  4. Visualization (u=0.60) - "Post-hoc analysis"
```

**Benefit:** Researchers don't manually decide tool order; agent learns from domain expertise.

### 4. Large Codebase Refactoring

**Scenario:** Refactoring million-line codebase requires: dependency analyzers, refactoring tools, testing frameworks, performance profilers.

- Tools are domain-specific (e.g., tools for C++ differ from Python)
- AutoTool learns tool utility in context of refactoring goals (e.g., "minimize breaking changes")
- Generalizes across programming languages via learned representations

### Integration Challenges & Scalability

**Challenges:**

1. **Tool API Changes:** If tools update their interfaces, agent must adapt. Solution: Version-aware tool embeddings.

2. **Tool Error Handling:** Bad tool calls (e.g., invalid Python) must be caught and ranked lower. Solution: Include error logs in training data.

3. **Dependency Between Tools:** Some tools require output from prior tools. Solution: Constraint-aware ranking (model learns dependencies).

4. **Compute Overhead:** Ranking 1,000+ tools at each step is expensive. Solution: Approximate ranking (compute top-K, not full ranking).

**Scalability to Many Tools:**
- For N tools, Plackett-Luce ranking is O(N log N) (sorting)
- Can be approximated to O(K log K) where K << N
- Tested up to 1,000 tools without significant slowdown

---

## Insights & Implications

### Impact on Agent-Driven Development Systems

1. **Scalable Tool Integration:**
   - Current agent frameworks add tools ad-hoc; AutoTool enables systems with 1,000+ tools
   - Suggests future for "tool marketplaces" where agents dynamically compose solutions from diverse tool ecosystems

2. **Learned Coordination:**
   - Tool ranking is learned from data, not hand-crafted
   - Opens path for **continual learning**: as new tools arrive, agent can retrain on their effectiveness
   - Decouples agent logic from tool inventory

3. **Robustness and Generalization:**
   - KL-regularization shows that "staying close to prior knowledge" improves generalization
   - Pattern applicable to other agent systems: prompts, policies, model updates

### Advancement in Autonomous Code Generation and Testing

- **Efficiency:** 4.9 avg tool calls vs. 5.8 for ReAct demonstrates smart tool selection saves compute
- **Reliability:** 75.7% pass@1 on code generation surpasses simple chaining, suggesting learned ranking captures domain expertise
- **Multimodal:** 6.9% improvement on multimodal tasks shows ranking generalizes across modalities

### Limitations and Open Research Questions

1. **Representation Learning for Tools:**
   - How should tool descriptions/APIs be encoded for generalization?
   - Current: embedded descriptions; future: semantic tool graphs?

2. **Skill Acquisition and Tool Learning:**
   - Can agents *learn how to use* new tools from documentation alone?
   - AutoTool ranks tools but assumes agents know *how to call them*

3. **Causal Understanding of Tool Effects:**
   - Plackett-Luce assumes tool utilities are independent; what about causal tool dependencies?
   - Example: "Run linter, then formatter"—order matters

4. **Tool Interaction and Conflict:**
   - What if two tools produce conflicting results (e.g., different refactoring recommendations)?
   - How does ranking handle tool consensus or majority voting?

### Relevance to Skill Frameworks and Agent Topologies

- **Skill Framework:** Tool selection is a meta-skill. AutoTool demonstrates a **ranking-based skill** that coordinates diverse sub-skills (tools).
- **Hierarchical Agents:** Ranking policy could be learned at the orchestrator level; tool-selection logic factored out from individual agents
- **Adaptive Topologies:** As tools change, agent topology (which tools to call) adapts via re-ranking, without retraining agents themselves

---

## Code & Resources

### Official Resources

- **ArXiv Paper:** https://arxiv.org/abs/2512.13278
- **Paper PDF:** https://arxiv.org/pdf/2512.13278
- **Award:** Best Paper Award, ICCV 2025 Workshop on Multi-Modal Reasoning for Agentic Intelligence
- **Code Availability:** [To be confirmed; check arXiv page for GitHub links]

### Dependencies and Compute Requirements

- **Python:** ≥3.10 (for type hints, match statements)
- **ML Frameworks:**
  - PyTorch or TensorFlow for RL training
  - Transformers library (HuggingFace) for LLM backbone
- **Tool APIs:** Depends on tools integrated (Python, Search APIs, Math libraries, etc.)
- **Compute:**
  - Training: GPU cluster (8× A100 or equivalent) for 200k trajectories
  - Inference: Single GPU (V100+) or CPU (slower)
  - Estimated cost: $10k–$50k for full training (varies by cloud provider)

### Integration Guide

**Pseudocode for Plackett-Luce Tool Selection:**

```python
import torch
from torch.nn import Softmax

def select_tool_via_ranking(context, available_tools, utility_model):
    """
    Use learned utilities and Plackett-Luce ranking to select a tool.
    
    Args:
      context: dict with {problem, observations, prior_tools_used}
      available_tools: list of Tool objects
      utility_model: trained neural network predicting tool utilities
    
    Returns:
      ranked_tools: list of tools sorted by utility (highest first)
    """
    # Encode context
    context_embedding = encode_context(context)
    
    # Predict utilities for all tools
    utilities = []
    for tool in available_tools:
        tool_embedding = tool.embed(tool.description, tool.signature)
        combined = torch.cat([context_embedding, tool_embedding])
        utility = utility_model(combined)
        utilities.append(utility)
    
    utilities = torch.tensor(utilities)
    
    # Apply Plackett-Luce ranking
    # P(ranking) ∝ ∏ u[rank_i] / (sum of remaining utilities)
    probabilities = plackett_luce_ranking(utilities)
    
    # Sort tools by utility (descending)
    ranked_indices = torch.argsort(utilities, descending=True)
    ranked_tools = [available_tools[i] for i in ranked_indices]
    
    return ranked_tools

def plackett_luce_ranking(utilities):
    """
    Compute Plackett-Luce probabilities for a ranking of items.
    """
    n = len(utilities)
    log_probs = []
    
    for i in range(n):
        # Probability that item i is selected first among remaining items
        remaining_utilities = utilities[i:]
        softmax = Softmax(dim=0)
        normalized = softmax(remaining_utilities)
        log_prob = torch.log(normalized[0])
        log_probs.append(log_prob)
    
    return torch.exp(torch.stack(log_probs))  # Joint probability
```

### Quick-Start Integration Steps

1. **Collect tool-selection data:**
   - Run agents on diverse tasks (200k+ trajectories)
   - Annotate which tools were selected and why (rationales)

2. **Train utility model:**
   - Supervised: predict tool at each step (cross-entropy loss)
   - RL: optimize for end-to-end task success (policy gradient)

3. **Add KL-regularization:**
   - Compute Plackett-Luce ranking distribution
   - Minimize: CE loss + λ * KL(new || old)

4. **Deploy ranking policy:**
   - At inference, encode context
   - Compute utilities for available tools
   - Select top-ranked tool; execute and observe
   - Repeat until task complete

5. **Evaluate generalization:**
   - Test on unseen tools (OOD evaluation)
   - Measure task success and tool-call efficiency

---

## Related Work & Context

### Related Papers on Tool Use and Agent Reasoning

- **ReAct** (Yao et al., 2023): Reasoning + Acting framework; pioneering work on interleaving thought and tool calls
  - Limitation: Ad-hoc tool selection, assumes fixed tool inventory
  
- **Gorilla** (Patil et al., 2023): LLM for tool-use; models tool APIs as text
  - Difference: Gorilla focuses on *how to call* tools; AutoTool focuses on *which* tool to select
  
- **ToolFormer** (Schick et al., 2023): Fine-tune LLM to decide when to use tools
  - Limitation: Doesn't handle 1000+ tools or generalize to unseen tools
  
- **API-BLEND** (Li et al., 2024): Blend multiple APIs for task solving
  - Difference: Static API inventories; AutoTool learns dynamic ranking

### Foundational Work on Ranking and Preference Learning

- **Plackett-Luce Model** (Luce, 1959; Plackett, 1975): Statistical model for rankings; classical in econometrics
  - Application: Choice modeling, recommendation systems, ranking learning
  
- **Learning to Rank** (Liu, 2009): Comprehensive survey of ranking ML methods
  - Related: LambdaMART, pairwise ranking, pointwise ranking
  
- **Preference Learning** (Fürnkranz & Hüllermeier, 2011): Learning from preference judgments
  - Connection: Tool-selection rationales are preference signals (why one tool over others)

### Reinforcement Learning for Agent Control

- **Policy Gradient Methods** (Sutton et al., 2000): Foundation for RL agent training
- **KL-Regularized RL** (Abdolmaleki et al., 2018): Theory and practice of KL constraints in policy learning
  - Application: AutoTool uses KL-regularized CE loss to prevent overfitting

### Future Research Directions

1. **Hierarchical Tool Selection:** Learn both *which tool* and *how to use* it (current: assumes agents know how)
2. **Tool Composition:** Learn when to chain tools vs. use them independently
3. **Causal Tool Dependencies:** Model causal relationships (e.g., "linter must run before formatter")
4. **Adaptive Tool Learning:** Continually update ranking as new tools are added (online learning)
5. **Cross-Domain Transfer:** Train on one domain, apply ranking to new domains without retraining

---

## Author and Citation

**Citation Format (BibTeX):**

```bibtex
@article{autotool2025,
  title={AutoTool: Dynamic Tool Selection and Integration for Agentic Reasoning},
  year={2025},
  arxiv={2512.13278},
  journal={arXiv preprint},
  note={Best Paper Award, ICCV 2025 Workshop on Multi-Modal Reasoning for Agentic Intelligence}
}
```

---

## Document Metadata

- **Lecture Created:** 2026-05-27
- **Last Updated:** 2026-05-27
- **Relevance Score:** 9/10 (Highly relevant to tool-use, agent reasoning, and adaptive orchestration)
- **Recommended for:** Developers building agent frameworks with diverse tool ecosystems, researchers on agent generalization, builders of autonomous development environments
