# TDD Governance for Multi-Agent Code Generation via Prompt Engineering

**ArXiv ID:** [2604.26615](https://arxiv.org/abs/2604.26615)  
**Authors:** Tarlan Hasanli, Shahbaz Siddeeq, Bishwash Khanal, Pyry Kotilainen, Tommi Mikkonen, Pekka Abrahamsson  
**Submitted:** April 29, 2026  
**Venue:** The 30th International Conference on Evaluation and Assessment in Software Engineering (EASE 2026)  
**Subcategory:** `agent-orchestration`

---

## Executive Summary

This paper introduces an AI-native Test-Driven Development (TDD) governance framework that operationalizes classical TDD principles as structured prompt-level and workflow-level constraints within a multi-agent code generation pipeline. Rather than treating tests as optional auxiliary inputs, the system enforces a Red-Green-Refactor discipline as a binding governance layer through which LLM agents must operate, significantly improving stability and reproducibility of generated code. The work is highly significant for agent-driven development because it demonstrates how well-established software engineering processes can be formalized into machine-readable governance manifests that constrain and direct agent behavior at runtime.

---

## Problem Statement

### Development Automation Challenge

Multi-agent LLM systems for code generation face a fundamental reliability problem: when multiple specialized agents collaborate on code tasks, small logic errors at one stage propagate downstream and compound through the pipeline. Without enforceable process constraints, agents may generate syntactically valid but semantically incorrect code, with no principled mechanism for detecting and correcting failures before they cascade.

### Prior Agent System Limitations

Existing LLM-based code generation approaches typically use test cases as auxiliary signals at best — they check for pass/fail but do not embed the TDD discipline into the agent workflow itself. These approaches suffer from:

- **Ad hoc prompting**: Agents receive unstructured instructions without formal phase boundaries
- **Unbounded repair loops**: Agents may attempt unlimited revision cycles with no convergence guarantee
- **Model-as-authority**: LLMs make state mutations without deterministic engine oversight
- **No atomic mutation control**: Multiple agents may modify shared code state concurrently, causing inconsistencies

### Research Gap

There was no prior work that treated TDD's Red-Green-Refactor cycle as a *governance mechanism* — a machine-enforced workflow structure binding on all agents in the pipeline. Prior systems used TDD tests as data, not as a process invariant.

---

## Core Concepts & Theory

### Test-Driven Development as Governance

Classical TDD prescribes three phases:

1. **Red**: Write a failing test that specifies desired behavior
2. **Green**: Write the minimal code to make the test pass
3. **Refactor**: Improve code structure while keeping tests passing

This paper re-interprets these phases not as a programmer's personal discipline but as **workflow-level governance constraints** enforced by a deterministic execution engine separate from the LLM agents.

### The Machine-Readable TDD Manifesto

The core innovation is extracting TDD principles into a formal, machine-readable **governance manifesto** — a structured specification document that:

- Defines which agent actions are permitted in each phase
- Specifies transition conditions between phases (e.g., all tests must pass before entering Refactor)
- Establishes validation gates that must be satisfied before state progression
- Encodes bounded repair loop constraints (maximum retry counts per phase)

This manifesto is distributed to each agent in the pipeline as part of its prompt context, making governance rules explicit rather than implicit.

### Layered Architecture: Proposal vs. Authority

A key theoretical contribution is the clean separation between two layers:

```
┌─────────────────────────────────────────────┐
│              PROPOSAL LAYER                 │
│  ┌────────────┐  ┌──────────┐  ┌─────────┐ │
│  │  Planning  │  │  Code    │  │  Repair │ │
│  │   Agent    │  │   Gen    │  │  Agent  │ │
│  │            │  │  Agent   │  │         │ │
│  └─────┬──────┘  └────┬─────┘  └────┬────┘ │
│        │              │             │       │
└────────┼──────────────┼─────────────┼───────┘
         │              │             │
         ▼              ▼             ▼
┌─────────────────────────────────────────────┐
│           DETERMINISTIC ENGINE              │
│         (Governance Authority)              │
│                                             │
│  Phase Ordering │ Validation Gates          │
│  Bounded Loops  │ Atomic Mutation Control   │
│  State Machine  │ TDD Manifesto Enforcement │
└─────────────────────────────────────────────┘
```

**LLMs act as proposal generators** — they suggest code, test cases, repair patches, and plans. **The deterministic engine acts as the authority** — it decides whether proposals satisfy governance constraints and controls all state mutations.

### Coordination Mechanisms

The framework enforces four specific governance mechanisms:

| Mechanism | Description |
|-----------|-------------|
| **Phase Ordering** | Agents cannot skip phases; Red must precede Green must precede Refactor |
| **Bounded Repair Loops** | Each phase has a maximum iteration budget; failure exhausts budget and signals error |
| **Validation Gates** | Phase transitions require passing deterministic checks (test suite, lint, type check) |
| **Atomic Mutation Control** | Only the engine may commit changes to the code state; agents propose, engine commits |

### Mathematical Foundation

Let `S` be the set of system states, `P` be the set of phases `{Red, Green, Refactor}`, and `T: S × P → S` be the transition function. The governance constraint is:

```
∀ transition (s, p) → s':
  1. p must be the next valid phase given current phase(s)
  2. ValidationGate(s', p) = True
  3. RepairBudget(p) > 0
  4. Δ(s, s') is proposed by LLM but committed only by engine
```

This formalization ensures the TDD cycle is a strict directed graph with no backward edges until a repair loop is explicitly permitted.

---

## Main Ideas & Contributions

### Novel Agent Orchestration Pattern

The paper's primary contribution is the **governance layer pattern**: a thin, deterministic middleware layer that sits between the orchestrator and specialized agents, enforcing process invariants without restricting the creativity of individual agents within their phase.

### Prompt-Level Governance Distribution

TDD principles are encoded into each agent's system prompt through the manifesto. This is distinct from simple prompt engineering — the manifesto is structured data (not free text) that agents parse and reference when generating proposals:

```
Pseudocode: Manifesto Distribution

MANIFESTO = {
  "current_phase": "GREEN",
  "allowed_operations": ["code_generation", "import_addition"],
  "forbidden_operations": ["test_modification", "refactoring"],
  "validation_requirements": ["all_tests_pass", "no_syntax_errors"],
  "repair_budget_remaining": 3,
  "phase_transitions": {
    "GREEN -> REFACTOR": ["all_tests_pass", "no_new_failures"]
  }
}

agent_prompt = base_prompt + format_manifesto(MANIFESTO)
proposal = llm.generate(agent_prompt)
if engine.validate(proposal, MANIFESTO):
    engine.commit(proposal)
else:
    engine.increment_repair_count()
    if repair_count >= MANIFESTO["repair_budget_remaining"]:
        raise GovernanceError("Phase budget exhausted")
```

### Sub-Agent Specialization

The framework decomposes the development pipeline into specialized sub-agents:

- **Planning Agent**: Interprets requirements and writes failing test specifications (Red phase)
- **Code Generation Agent**: Implements minimal code to satisfy tests (Green phase)
- **Repair Agent**: Diagnoses failures and proposes targeted patches within bounded loops
- **Refactoring Agent**: Improves code structure while ensuring all tests remain green (Refactor phase)
- **Validation Agent**: Runs deterministic checks and reports gate results to the engine

### Intuition Behind Design

The key insight is that classical TDD's value comes not from the tests themselves but from the *discipline* of following the cycle. LLMs are creative and can generate plausible-looking but incorrect code; the governance framework channels that creativity through proven engineering constraints.

---

## Methodology & Implementation

### Experimental Setup

The framework was evaluated on software engineering benchmarks covering:
- **Functional correctness**: Pass@k metrics on test suite execution
- **Stability**: Variance in outcomes across multiple runs (reproducibility)
- **Convergence**: Rate at which repair loops terminate within the bounded budget

### Agent Architecture Workflow

```
INPUT: Requirements / User Story
          │
          ▼
┌─────────────────────────┐
│    PLANNING AGENT       │  ← RED PHASE
│  Writes failing tests   │
│  (TDD manifesto loaded) │
└────────────┬────────────┘
             │ Tests committed by Engine
             ▼
┌─────────────────────────┐
│   CODE GEN AGENT        │  ← GREEN PHASE
│  Generates minimal impl │
│  Proposals → Engine     │
└────────────┬────────────┘
             │ Engine runs tests
             ├─── FAIL ──→ REPAIR AGENT (budget: N)
             │                    │
             │            ┌───────┘
             │            │ Patch proposed
             │            ▼
             │    Engine re-runs tests
             │            │
             │            ├── PASS → continue
             │            └── FAIL → decrement budget
             │
             ▼ (all tests pass)
┌─────────────────────────┐
│  REFACTORING AGENT      │  ← REFACTOR PHASE
│  Structural improvement │
│  Tests must stay green  │
└────────────┬────────────┘
             │
             ▼
         OUTPUT: Governed, tested, refactored code
```

### Metrics and Evaluation

| Metric | Description |
|--------|-------------|
| Pass@1 | Fraction of tasks where first generated solution passes all tests |
| Pass@k | Fraction of tasks passing within k repair attempts |
| Budget Utilization | Average repair iterations consumed per task |
| Reproducibility | Standard deviation of outcomes across 5 independent runs |
| Governance Compliance | Rate at which agents respect phase boundaries without violations |

### Results

The governance framework demonstrates improvement in:
- **Reproducibility**: Significantly reduced variance compared to unconstrained multi-agent systems
- **Repair Convergence**: Bounded loops terminate predictably, with most tasks resolving within the budget
- **Phase Compliance**: Agents operating under the manifesto respect governance constraints consistently
- **Code Quality**: Enforced Refactor phase produces structurally cleaner code than ad hoc generation

---

## Practical Applications & Use Cases

### Direct Software Development Applications

1. **CI/CD Pipeline Integration**: The governance engine can be embedded as a CI gate — code changes must pass TDD governance before merging
2. **Automated Feature Development**: Given a user story, agents produce tested, refactored code following TDD discipline
3. **Bug Fix Automation**: The repair agent operates within bounded loops to patch failing tests without regression
4. **Code Review Automation**: The Validation Agent's gate reports serve as machine-generated review feedback

### Concrete Multi-Agent Workflow Example

```
User: "Add authentication to the API"

1. Planning Agent (Red):
   - Generates failing tests:
     test_login_returns_token()
     test_invalid_credentials_rejected()
     test_token_expires_after_ttl()
   
   Engine: Commits tests, runs them → all FAIL ✓ (expected Red)
   
2. Code Gen Agent (Green):
   - Proposes JWT auth implementation
   Engine: Runs tests → 2/3 PASS

3. Repair Agent (bounded: 3 attempts):
   Attempt 1: Patches token expiry logic
   Engine: All 3 tests PASS ✓
   
4. Engine: Transitions to Refactor phase
   
5. Refactoring Agent:
   - Extracts auth middleware
   - DRYs token logic
   Engine: Tests still pass ✓ → commits refactored code

Output: Clean, tested auth implementation
```

### Integration Challenges

- **LLM Non-determinism**: Agents may generate different proposals each run; governance compensates by enforcing structural consistency
- **Budget Tuning**: Repair loop budgets must be empirically calibrated per task complexity domain
- **Phase Boundary Ambiguity**: Some refactoring changes inadvertently affect behavior; the engine must handle edge cases

### Cost and Latency

- Governance adds overhead through validation gate checks and engine coordination
- However, bounded repair loops *reduce* worst-case latency by preventing runaway repair cycles
- Net effect: more predictable latency distribution compared to unconstrained systems

---

## Insights & Implications

### Impact on Agent-Driven Development

This paper establishes that **process methodologies from traditional software engineering are directly translatable into agent governance mechanisms**. The TDD manifesto pattern could be extended to other methodologies (BDD, DDD, Clean Architecture principles) as governance layers for different agent orchestration contexts.

### Advancement in Autonomous Coding

The key advance is separating *creativity* (LLM proposals) from *authority* (engine governance). This is analogous to how traditional software teams separate developer freedom from CI/CD enforcement — the LLMs are like developers who can write whatever code they want, but the governance engine is the CI system that decides what gets merged.

### Limitations

- The framework assumes well-specified test requirements in the planning phase; ambiguous requirements degrade governance effectiveness
- Deterministic validation gates may not cover all correctness criteria (e.g., performance, security)
- The manifesto format is not yet standardized — interoperability between different agent frameworks requires custom integration work

### Open Research Questions

- Can governance manifests be learned from existing codebases rather than manually specified?
- How do governance constraints interact with tool-use in agents (e.g., database access during testing)?
- Can the framework generalize to non-code artifacts (documentation, API schemas)?

### Relevance to Skill Frameworks

The manifesto-based governance pattern directly maps to **skill frameworks**: each agent's allowed operations per phase are essentially a constrained skill set. A skill framework could implement TDD governance by restricting which skills are callable in each phase, providing a natural integration point.

---

## Code & Resources

- **ArXiv Paper:** https://arxiv.org/abs/2604.26615
- **Related Framework (TDFlow):** https://github.com/toughhou/TDFlow
- **Venue:** EASE 2026 (30th International Conference on Evaluation and Assessment in Software Engineering)

### Dependencies and Compute Requirements

- Any LLM capable of instruction-following (GPT-4, Claude, Gemini, Llama series)
- A deterministic test runner (pytest, Jest, JUnit, etc.) as the governance engine
- The manifesto is a lightweight JSON/YAML structure with negligible overhead

### Quick-Start Integration Guide

```python
from tdd_governance import GovernanceEngine, TDDManifesto, AgentPipeline

# Define governance manifesto
manifesto = TDDManifesto(
    repair_budget=3,
    validation_gates=["test_suite", "lint", "type_check"],
    phase_order=["RED", "GREEN", "REFACTOR"]
)

# Initialize agents
pipeline = AgentPipeline(
    planning_agent=PlanningAgent(llm="claude-sonnet-4-6"),
    codegen_agent=CodeGenAgent(llm="claude-sonnet-4-6"),
    repair_agent=RepairAgent(llm="claude-sonnet-4-6"),
    refactor_agent=RefactorAgent(llm="claude-sonnet-4-6"),
)

# Initialize governance engine
engine = GovernanceEngine(manifesto=manifesto, pipeline=pipeline)

# Run governed development
result = engine.run(requirements="Add user authentication to REST API")
```

---

## Related Work & Context

### Related Papers

- **TDFlow: Agentic Workflows for Test Driven Software Engineering** ([arXiv:2510.23761](https://arxiv.org/abs/2510.23761)): Predecessor work that decomposes TDD into sub-agents for patching, debugging, and revising; this paper extends the governance framing
- **AgentCoder: Multi-Agent-based Code Generation with Iterative Testing** ([arXiv:2312.13010](https://arxiv.org/abs/2312.13010)): Uses test designer + executor agents without formal governance
- **From Governance Norms to Enforceable Controls** ([arXiv:2604.05229](https://arxiv.org/abs/2604.05229)): Complementary work on runtime guardrails for agentic AI systems

### Prior Foundational Work

- **Classical TDD**: Beck, K. (2002). *Test-Driven Development by Example*. The intellectual foundation for the governance approach
- **SWE-Bench**: The canonical benchmark for LLM software engineering agents, motivating the need for process governance
- **Devin (Cognition AI)**: Commercial system demonstrating autonomous development agents, against which governance frameworks must compete

### Future Research Directions

- **Adaptive governance**: Manifests that evolve based on project type, complexity, and historical performance
- **Multi-methodology governance**: Combining TDD governance with other process models (BDD, Domain-Driven Design)
- **Cross-agent governance**: Extending the framework to distributed agent networks where governance must be consensus-based
- **Empirical calibration**: Learning optimal repair budgets and phase boundaries from historical project data
