# MOSS: Self-Evolution through Source-Level Rewriting in Autonomous Agent Systems

**ArXiv ID:** 2605.22794  
**Submitted:** May 21, 2026  
**Authors:** Qianshu Cai, Yonggang Zhang, Xianzhang Jia, Wei Xue, Jun Song, Xinmei Tian, Yike Guo  
**Institution:** University of Science and Technology of China, Alibaba Group

## Executive Summary

MOSS introduces a paradigm-shifting approach to self-evolving autonomous agents by enabling source-level code adaptation rather than limiting evolution to configuration files and prompts. Unlike prior self-evolving systems that only modify text artifacts (skill files, memory schemas), MOSS performs deterministic structural modifications directly at the source code level, making it the first system to achieve Turing-complete self-adaptation in production agentic substrates. This work addresses a critical limitation: recurring failures in deployed agents can now be autonomously fixed through code evolution, improving mean grader scores from 0.25 to 0.61 in single adaptation cycles without human intervention.

## Problem Statement

### Problem Addressed
Autonomous agentic systems deployed in production are largely static and cannot learn from user interactions. When failures occur, they persist until human developers manually identify, fix, and redeploy updated code. Existing self-evolving agent approaches (text-level evolution) only modify mutable artifacts like prompts and configuration files, leaving the core agent infrastructure—routing logic, hook ordering, state invariants, and dispatch mechanisms—untouchable.

### Prior Limitations
Previous self-evolution systems operate at the text layer through:
- Prompt optimization: limited expressiveness, subject to long-context drift
- Configuration file modification: cannot change structural behavior
- Memory schema updates: cannot fix fundamental logic errors

These approaches form a "text ceiling" where fundamental architectural issues cannot be resolved without human intervention.

### Research Gap
The research gap lies in the gap between what can be modified (text artifacts) and what needs to be modified (source code structure). No existing system enables deterministic, safe, and effective source-code-level adaptation for production agents.

## Core Concepts & Theory

### Fundamental Concepts

#### 1. Source-Level Adaptation vs. Text-Level Evolution
- **Text-level:** Modifies prompts, configurations, memory → high-level, non-deterministic, model-dependent
- **Source-level:** Modifies code structure, routing, hooks → low-level, deterministic, universally applicable

#### 2. Turing-Completeness of Adaptation
Source-level modifications enable Turing-complete transformations:
- Text-level modifications form a strict subset of possible source modifications
- Code changes take effect deterministically (no model compliance issues)
- Structural changes don't erode under long-context drift

#### 3. Production Agentic Substrates
The agent harness comprises:
- **Router:** Dispatches to skills based on input
- **Hooks:** Pre/post-processing steps (logging, validation, state management)
- **State Invariants:** Constraints maintained across agent execution
- **Dispatch Mechanisms:** How skills are invoked and composed

### Mathematical Framework

The self-evolution problem can be formalized as:

```
minimize: F(agent_instance) = ∑ failures in trajectory

subject to:
  - Code modifications preserve safety invariants
  - Changes take effect deterministically
  - Adaptation occurs online during production use
```

### Comparison with Existing Approaches

| Approach | Text Artifacts | Code Structure | Deterministic | Turing-Complete |
|----------|---|---|---|---|
| Prompt Optimization | ✓ | ✗ | ✗ | ✗ |
| Configuration Tuning | ✓ | ✗ | ✓ | ✗ |
| Workflow Graphs | ✓ | ✗ | ✓ | ✗ |
| **MOSS (Source-Level)** | ✓ | **✓** | **✓** | **✓** |

## Main Ideas & Contributions

### Novel Techniques

#### 1. Source-Level Code Rewriting
MOSS generates syntactically correct modifications to agent source code:
- Analyzes failure traces to identify problematic code paths
- Proposes targeted modifications to routing, hooks, or dispatch logic
- Validates changes against safety constraints before deployment

#### 2. Deterministic Execution Model
Unlike text-level approaches that depend on model interpretation:
- Code changes execute deterministically on every invocation
- No model compliance issues or degradation over time
- Structural improvements persist across all future interactions

#### 3. Safety-Aware Adaptation
- Maintains invariant preservation through constraint checking
- Implements rollback mechanisms for failing modifications
- Validates changes in sandboxed environments before production deployment

### Technical Contributions

1. **Identification of Agent Harness Components:** Defines the distinct layers where modifications can occur (routing, hooks, state, dispatch)

2. **Symbolic Analysis Pipeline:** Traces failures to root causes in agent code and proposes repairs

3. **Staged Deployment Strategy:** Tests modifications incrementally before full adoption

## Methodology & Implementation

### System Architecture

```
Agent Execution
    ↓
Failure Detection
    ↓
Trace Analysis (symbolic execution)
    ↓
Source Code Modification Generation
    ↓
Validation (invariant checking + sandbox testing)
    ↓
Staged Rollout
    ↓
Production Deployment
```

### Experimental Setup

**Dataset:** OpenClaw benchmark with 4 complex reasoning tasks requiring multi-step agent reasoning

**Metrics:**
- Mean grader score (task success rate)
- Adaptation cycle time
- Code complexity growth
- Safety constraint violations

**Baseline Comparisons:**
- Static agent (no adaptation): 0.25 mean score
- Text-level evolution (prompts): 0.42 mean score
- Workflow graph modification: 0.48 mean score
- MOSS (source-level): 0.61 mean score

### Implementation Details

MOSS operates on production-ready agent substrates written in Python:

```python
# Example: Routing Logic Modification
# Original: routes all queries to single skill
if query_type == "reasoning":
    result = skill_reasoning(query)
else:
    result = skill_default(query)

# MOSS-evolved: adds specialized routing for complex queries
if query_complexity > THRESHOLD and query_type == "reasoning":
    result = skill_advanced_reasoning(query)  # newly added path
elif query_type == "reasoning":
    result = skill_reasoning(query)
else:
    result = skill_default(query)
```

### Evaluation Metrics

- **Success Rate:** Percentage of tasks completed without human intervention
- **Grader Score Improvement:** Mean increase in performance metrics (0.25 → 0.61)
- **Adaptation Speed:** Time to generate and validate modifications
- **Code Quality:** Lines of code added, cyclomatic complexity

## Practical Applications & Use Cases

### Applicable Domains

1. **Autonomous Coding Agents**
   - Real-world: GitHub Copilot-like systems that learn from code review failures
   - Challenge: Handling diverse programming languages and edge cases
   - Solution: Source-level modifications to routing and validation hooks

2. **Intelligent Task Automation**
   - Real-world: RPA (Robotic Process Automation) systems in enterprises
   - Challenge: Adapting to workflow changes without redeployment
   - Solution: Runtime modification of task dispatch logic

3. **Conversational AI Systems**
   - Real-world: Customer service chatbots operating 24/7
   - Challenge: Improving response quality from failure patterns
   - Solution: Evolving response filtering and ranking logic

4. **Robotics and Control Systems**
   - Real-world: Autonomous vehicles making safety-critical decisions
   - Challenge: Adapting to edge cases detected in deployment
   - Solution: Modifying decision-making and safety constraint logic

### Concrete Examples

**Example 1: Coding Assistant Evolution**
- Initial failure: Agent generates syntactically incorrect code
- Analysis: Identifies missing validation in code generation hook
- Adaptation: Adds syntax checking before code emission
- Result: Error rate drops from 15% to 3%

**Example 2: Task Automation Workflow**
- Initial failure: Agent routes complex tasks to wrong automation path
- Analysis: Discovers insufficient complexity detection
- Adaptation: Adds cost/complexity estimation to routing logic
- Result: Task success rate improves from 65% to 92%

## Insights & Implications

### Broader Field Impact

1. **Shift from Static to Adaptive Agents:** MOSS enables agents to become truly "alive"—learning and improving from operational experience rather than remaining frozen until human updates.

2. **Reduced Operational Cost:** By eliminating the human-in-the-loop update cycle, MOSS reduces time-to-fix from weeks to minutes.

3. **Safety Concerns Addressed:** Deterministic code changes and constraint validation provide stronger safety guarantees than probabilistic text-level evolution.

### State-of-the-Art Advancement

MOSS represents the first production-grade self-evolving agent system that:
- Operates at the source-code level (Turing-complete expressiveness)
- Maintains deterministic execution semantics
- Preserves safety invariants automatically
- Demonstrates significant performance improvements (0.25→0.61)

### Limitations and Open Questions

1. **Scaling to Complex Agents:** Current evaluation on 4-task benchmark; larger systems may exhibit emergent behaviors difficult to predict

2. **Representation of Constraints:** Safety invariants must be explicitly specified; discovering invariants automatically remains an open problem

3. **Theoretical Guarantees:** While empirical results are strong, formal verification of modification safety is not yet provided

4. **Cross-Language Support:** Current implementation targets Python; extending to polyglot agent systems is non-trivial

## Code & Resources

### Official Repository
- **GitHub:** [https://github.com/dav-joy-thon/MOSS](https://github.com/dav-joy-thon/MOSS)
- **Paper:** https://arxiv.org/abs/2605.22794
- **License:** MIT

### Dependencies
- Python 3.10+
- Agent framework (compatible with LangChain, AutoGen)
- AST manipulation libraries (ast, astor)
- Symbolic execution engine (optional: Manticore or similar)

### Compute Requirements
- GPU: Not strictly required (most work is symbolic, not neural)
- Memory: 8GB+ for large agent codebases
- Latency: ~5-10s per adaptation cycle (including validation)

### Quick Start

```python
from moss import SelfEvolvingAgent

# Initialize agent with failure monitoring
agent = SelfEvolvingAgent(
    agent_code="path/to/agent.py",
    safety_constraints="path/to/constraints.json",
    evolution_enabled=True
)

# Run agent with automatic adaptation
result = agent.execute(
    task="complex reasoning task",
    auto_evolve=True,
    max_adaptations=3
)

print(f"Task result: {result}")
print(f"Adaptations applied: {agent.evolution_history}")
```

## Related Work & Context

### Prior Work Foundations

1. **Self-Improving Systems:** Early work on self-modification (Lenat's Cyc, genetic programming)
   - MOSS advances: Applies to modern agent architectures, production-grade safety

2. **Prompt Optimization:** Recent work on in-context learning and prompt engineering
   - MOSS comparison: Source-level is more expressive and deterministic than text-level

3. **Program Synthesis:** Automated code generation and repair
   - MOSS contribution: Focuses on agent-specific modifications, not general code synthesis

4. **Multi-Agent Systems:** Collaborative agent evolution
   - MOSS extension: Could enable distributed adaptation across agent fleets

### Recent Related Papers

- "Code as Agent Harness" (2605.18747): Defines the conceptual framework MOSS builds upon
- "AutoHarness" (2603.03329): Earlier work on automatic harness synthesis
- "Agentic AI Orchestration Should be Bayes-consistent" (related work): Discusses principled agent design

### Future Research Directions

1. **Automated Invariant Discovery:** Learn safety constraints from operational data rather than manual specification

2. **Multi-Agent Co-Evolution:** Enable agents to learn from each other's adaptations

3. **Formal Verification:** Provide mathematical proofs of safety for evolved code

4. **Transfer Learning for Adaptations:** Apply modifications learned in one agent to structurally similar agents

---

**Paper Link:** https://arxiv.org/abs/2605.22794
