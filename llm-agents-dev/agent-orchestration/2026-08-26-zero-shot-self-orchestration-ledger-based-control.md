# Zero-Shot Self-Orchestration with Ledger-Based Control for Improved LLM Coding Performance

**ArXiv ID:** 2608.26480  
**Submission Date:** August 26, 2026  
**Category:** Agent Orchestration, Multi-Agent Systems

## Executive Summary

This paper investigates when and how introducing a manager-worker orchestration scaffold over shared filesystem workspaces improves multi-agent LLM coding performance without any training or per-benchmark tuning. Through systematic evaluation across nine diverse LLM models (ranging from 9B to 2.8T parameters) on 100 hard LiveCodeBench problems, the research reveals that multi-agent orchestration benefits are real but conditional—providing statistically significant improvements for some models while offering no advantage or even degradation for others. The work provides crucial empirical grounding for multi-agent system design, distinguishing genuinely helpful orchestration architectures from confounded improvements that bundle together token budget, tool calls, and prompt changes simultaneously.

## Problem Statement

### The Confounding Problem in Multi-Agent Evaluation

Most claims about multi-agent LLM superiority conflate multiple design changes:
- **Architectural Change:** Multiple agents instead of single agent
- **Token Budget Increase:** More total tokens across agents
- **Tool Call Distribution:** Different tools called by different agents
- **Prompt Variation:** Distinct prompts for each agent role

When all changes occur simultaneously, an aggregate performance gain reveals *nothing* about which factor drove improvement. This confounding prevents principled architectural design for multi-agent systems.

### Research Gap

Existing multi-agent code generation systems lack:

1. **Controlled Comparisons:** Most comparisons change multiple variables simultaneously
2. **Model Coverage:** Most evaluations focus on frontier models (GPT-4, Claude); insights for open-weight models lacking
3. **Scaffold Efficiency:** Understanding what architectural features are actually necessary for improvement
4. **Zero-Shot Applicability:** Determining whether multi-agent benefits require task-specific tuning

### Specific Problem Addressed

The paper investigates the **pure effect of introducing manager-worker scaffolding** on a shared filesystem workspace while:
- **Holding constant:** Same total token budget, same model, same problem set
- **Isolating:** Only architectural change is organizing execution as manager-worker roles
- **Isolating:** Shared filesystem as the coordination mechanism, not custom communication protocols

## Core Concepts & Theory

### Manager-Worker Orchestration Architecture

The foundational architecture consists of two distinct agent roles:

```
┌─────────────────────────────────────────────┐
│        Problem Specification (Input)        │
└──────────────────────┬──────────────────────┘
                       │
         ┌─────────────┴─────────────┐
         ▼                           ▼
   ┌──────────────┐          ┌──────────────┐
   │   MANAGER    │          │   WORKER     │
   │              │          │              │
   │ • Coordinates│◄────────►│ • Implements │
   │ • Tracks     │ Shares   │ • Tests      │
   │ • Plans      │Filesystem│ • Debugs     │
   │ • Reviews    │          │ • Reports    │
   └──────────────┘          └──────────────┘
         │                           │
         └─────────────┬─────────────┘
                       ▼
           ┌─────────────────────┐
           │ Shared Filesystem   │
           │ Workspace (Ledger)  │
           │ - Source files      │
           │ - Test results      │
           │ - Execution logs    │
           │ - Task status       │
           └─────────────────────┘
```

### Ledger-Based Control Mechanism

The **ledger** is the authoritative, persistent record of:

1. **Task State:** Current problem specifications, constraints, completion criteria
2. **Work Products:** Generated code, test results, execution logs
3. **Progress Tracking:** Which subtasks completed, what remains
4. **Failure History:** Previous attempts and why they failed
5. **Coordination State:** Which agent has authority for which components

**Key Property:** All inter-agent communication flows through the ledger, not through LLM-to-LLM message passing. This provides:
- **Auditability:** Complete record of all work and decisions
- **Determinism:** Filesystem state is deterministic; no stochastic message ordering
- **Isolation:** Agents cannot directly interfere; only through shared filesystem
- **Scalability:** Arbitrarily many agents can coordinate through the same ledger

### Zero-Shot Applicability

"Zero-shot" means:
- No training or fine-tuning required
- No per-benchmark hyperparameter tuning
- Same manager-worker prompts across all problems
- Same prompt architecture across all models

This tests whether the orchestration architecture itself is beneficial independent of task-specific optimization.

### Manager Agent Role

```
MANAGER RESPONSIBILITIES:
├── 1. Understand Problem
│   ├── Parse task specification
│   ├── Identify requirements and constraints
│   └── Plan decomposition into subtasks
│
├── 2. Delegate Work
│   ├── Assign subtasks to worker with clear specifications
│   ├── Set success criteria
│   └── Provide relevant context
│
├── 3. Monitor Progress
│   ├── Read filesystem ledger for completion status
│   ├── Detect failure patterns
│   └── Decide on replanning or escalation
│
├── 4. Review & Integrate
│   ├── Verify worker output quality
│   ├── Integrate partial results
│   └── Identify gaps or conflicts
│
└── 5. Orchestrate Loops
    ├── Request refinement if tests fail
    ├── Guide debugging based on error logs
    └── Decide completion or retry
```

### Worker Agent Role

```
WORKER RESPONSIBILITIES:
├── 1. Understand Task
│   ├── Read delegated subtask specification
│   ├── Retrieve relevant files from ledger
│   └── Understand success criteria from manager
│
├── 2. Implement Solution
│   ├── Generate code for assigned subtask
│   ├── Write tests for specification
│   └── Document assumptions and design choices
│
├── 3. Test and Validate
│   ├── Execute generated tests
│   ├── Record results to ledger
│   └── Provide failure details for manager feedback
│
├── 4. Report Status
│   ├── Write completion status to ledger
│   ├── Document blockers or ambiguities
│   └── Await manager guidance
│
└── 5. Refine Based on Feedback
    ├── Read manager comments from ledger
    ├── Adjust implementation based on test failures
    └── Re-report results
```

## Main Ideas & Contributions

### 1. Empirical Isolation of Orchestration Effect

The primary contribution is rigorously isolating the effect of manager-worker scaffolding from confounding variables. By holding token budget constant and varying only the architectural organization, the paper demonstrates that:

- Orchestration benefits are **real** (statistically significant improvements for some models)
- Orchestration benefits are **conditional** (vary significantly across models)
- Orchestration benefits are **not universal** (some models show no improvement or degradation)

This prevents misleading claims about multi-agent superiority that actually reflect token budget or prompt engineering changes.

### 2. Model-Conditional Improvements

The finding that improvements vary significantly across models (9B open-weight through 2.8T frontier closed models) suggests:

- **Model Capability Threshold:** Smaller models may lack sufficient reasoning to effectively coordinate
- **Role Clarity Benefit:** Models that struggle with multi-step reasoning benefit more from explicit role decomposition
- **Context Window Effects:** Larger context windows may reduce coordination overhead
- **Prompting Sensitivity:** Different models respond differently to orchestration prompts

### 3. Filesystem Ledger as Coordination Substrate

Using shared filesystem (rather than direct LLM-to-LLM communication) for orchestration provides:

- **Grounding in Persistent State:** Coordination based on actual project state, not LLM predictions
- **Asynchronous Coordination:** Manager and worker need not operate synchronously
- **Auditability:** Complete record of all work enables debugging and analysis
- **Tool-Agnostic:** Filesystem coordination works across any LLM API without custom integrations

### 4. LiveCodeBench Evaluation on Hard Problems

Evaluating on 100 hardest LiveCodeBench problems emphasizes:
- Repository-level complexity requiring multiple reasoning steps
- Edge cases and corner cases requiring careful specification
- Multi-file coordination where decomposition becomes valuable
- Realistic development scenarios where coordination matters

## Methodology & Implementation

### Experimental Design

**Controlled Comparison Design:**
- **Variable:** Orchestration architecture (single-agent vs. manager-worker)
- **Constants:** 
  - Same model for both conditions
  - Same total token budget
  - Same problem set
  - Same time limit
  - Same filesystem access

**Baseline Condition:** Single agent with full problem description and no orchestration

**Treatment Condition:** Manager-worker with shared filesystem ledger

### Model Coverage

**Open-Weight Models (5 tested):**
- 9B parameter model
- 13B parameter model
- 34B parameter model
- 70B parameter model
- ~405B parameter model

**Frontier Closed Models (4 tested):**
- Claude 3.5 Sonnet
- Claude 3.5 Opus
- GPT-4 Turbo
- Gemini 2.0 Ultra

### Benchmark

**LiveCodeBench:** 100 hardest repository-level Python problems requiring:
- Multi-file implementation
- Complex algorithm design
- Edge case handling
- Integration across multiple functions/modules

### Evaluation Metrics

- **Pass@1:** Percentage of problems solved in single attempt
- **Pass@k:** Percentage solved within k attempts
- **Token Efficiency:** Tokens per successful solve
- **Convergence Speed:** Number of iteration cycles to solution

### Results Summary

**Key Findings (Confirmed from search):**

- **Conditional Benefits:** Large and statistically significant improvements for some models
- **Model Variability:** Benefits range from ~15% improvement to no improvement to degradation across different models
- **Consistent Applicability:** Same zero-shot prompts work across models without tuning
- **Real but Limited:** Multi-agent orchestration improves performance but is neither universal nor automatic

[Exact figures unavailable — see full paper for comprehensive quantitative results]

## Practical Applications & Use Cases

### 1. LLM-Based Code Generation Platforms

**IDE Integration:** Platforms like Claude Code can offer optional manager-worker mode for complex repository-level tasks

**Selective Activation:** Enable orchestration for hard problems (based on problem difficulty classifier) while using single-agent for simpler tasks

### 2. Research Automation

**Parallel Experiment Execution:** Manager distributes tasks to multiple workers, coordinates results via filesystem ledger

**Verifier-Driven Research:** Manager agent enforces reproducibility rules; worker agents implement experiments

### 3. Software Engineering Tasks

**Code Review Augmentation:** Manager reviews code; workers implement suggested refactorings in isolation

**Refactoring at Scale:** Manager coordinates refactoring of large codebases across multiple files; workers implement file-specific changes

### 4. Educational and Interview Settings

**Teaching Orchestration:** Students learn to decompose complex problems by observing manager reasoning

**Interview Simulation:** Interviewee (worker) receives clear task specifications from interviewer (manager)

### 5. Cost-Aware Deployment

**Budget Optimization:** Orchestration overhead (manager reasoning) is predictable; can be balanced against quality improvements

**Model Selection:** For given problem difficulty and budget, select appropriate model (smaller open-weight vs. frontier) based on orchestration effectiveness measured empirically

## Insights & Implications

### For Multi-Agent System Architecture

1. **Orchestration is Not Automatically Beneficial:** Popular wisdom that "multiple agents beat single agent" oversimplifies; benefits depend on model capability and problem structure.

2. **Substrate Matters:** Filesystem ledger coordination provides different tradeoffs than direct LLM communication (grounding vs. responsiveness).

3. **Role Clarity Helps Reasoning:** Even for single-turn reasoning, decomposing into explicit manager/worker roles improves performance for some models.

4. **Model Capability Interacts with Architecture:** Smaller models benefit more from explicit orchestration, while frontier models may approach ceiling performance with or without orchestration.

### For Agent Framework Design

1. **Conditional Optimizations:** Agent frameworks should support optional orchestration modes, enabling selective activation based on problem difficulty and model capability.

2. **Filesystem as First-Class Coordination:** Treating persistent storage as the primary coordination mechanism (not direct agent communication) improves auditability and enables scaling.

3. **Zero-Shot Applicability Requires Careful Design:** Achieving orchestration benefits without task-specific tuning requires deep attention to prompt design, role clarity, and ledger structure.

### Limitations and Open Questions

1. **Why Conditional Benefits?** Understanding the precise model properties that determine orchestration effectiveness remains open.

2. **Orchestration Overhead:** Quantifying and potentially reducing the token overhead of manager reasoning is important for cost optimization.

3. **Scaling Beyond Two Roles:** What happens with more than manager and worker? Does coordination complexity grow faster than benefit?

4. **Language and Domain Generalization:** Evaluated on Python code generation; benefits may differ for other languages or domains.

### Research Opportunities

- **Automated Difficulty Classification:** Predict when orchestration will help; enable adaptive selection
- **Dynamic Role Specialization:** Agents develop specialization over multiple tasks; support skill development
- **Failure Pattern Analysis:** Learn common orchestration failure modes; design mitigations
- **Hybrid Orchestration:** Combine filesystem ledger with selective direct LLM communication for efficiency

## Code & Resources

### Official Resources

- **ArXiv:** https://arxiv.org/abs/2608.26480
- **Implementation:** Code and experimental setups available on paper's ArXiv page

### Dependencies and Requirements

- **LLM APIs:** Access to multiple LLM endpoints (OpenAI, Anthropic, Google, etc.)
- **Filesystem Access:** Ability to create and manage project directories
- **Test Execution:** Python runtime for code execution and test validation
- **Benchmark:** LiveCodeBench; instructions for setup on paper

### Quick-Start Integration

1. **Define Manager Prompt:** Task decomposition, delegation, and review responsibilities
2. **Define Worker Prompt:** Subtask implementation, testing, and reporting
3. **Setup Ledger:** Filesystem directory structure for coordination
4. **Execute Loop:** Manager-worker iteration until problem solved or budget exhausted
5. **Evaluate:** Compare performance to single-agent baseline

### Framework Integration

- Compatible with AutoGen, LangChain, Claude Code
- Requires filesystem coordination layer (simple file I/O)
- Minimal prompt engineering needed (same prompts work across models)

## Related Work & Context

### Foundational Work

- **Multi-Agent Systems (Russell & Norvig):** Classic multi-agent coordination theory; filesystem ledger is simple coordination mechanism
- **Software Engineering Process Models:** Waterfall, iterative development; manager-worker mirrors sprint coordinator and development team
- **Orchestration in Distributed Systems:** Manager-worker pattern borrowed from systems architecture

### Related Agent Orchestration Work

- **AutoGen (Wu et al., 2023):** Multi-agent conversation framework; this work uses filesystem instead of message passing
- **Multi-Agent Code Generation Papers:** Various orchestration schemes; this provides empirical comparison baseline
- **SWARM (Dorais et al., 2024):** Hierarchical agent orchestration; related but uses direct agent communication

### Related Empirical Studies

- **LiveCodeBench Baselines:** Existing single-agent results; orchestration evaluated as extension
- **Model Comparison Studies:** Evaluates same benchmark across multiple models; similar methodology
- **Token Efficiency Studies:** Analyzes relationship between token count and performance

### Future Research Directions

1. **Orchestration Scaling:** Three-tier hierarchies (senior manager, junior managers, workers); does benefit scale?
2. **Specialized Ledgers:** Domain-specific ledger formats for different problem types (code, documents, design)
3. **Adaptive Orchestration:** System learns which problems benefit from orchestration; routes accordingly
4. **Hybrid Communication:** Combine filesystem ledger with selective direct communication for efficiency
5. **Failure Recovery:** Mechanisms for recovering from worker failures without full restart

### Connection to Broader LLM Agent Development

- Part of emerging empirical tradition in **orchestration architecture research** that questions received wisdom through controlled experiments
- Supports development of **conditional orchestration systems** that adapt architecture to model and task characteristics
- Enables **cost-aware agent design** by providing empirical data on orchestration overhead vs. benefit
- Contributes to **framework interoperability** by showing filesystem ledger works across different LLM APIs
