# Beyond Function Calling: Benchmarking Tool-Using Agents under Tool-Environment Unreliability

**Authors:** Yang Tian, Zhengpeng Shi, Yu Zhou, Bo Zhao  
**ArXiv ID:** [2606.25819](https://arxiv.org/abs/2606.25819)  
**Published:** June 24, 2026  
**Subject Areas:** Software Engineering (cs.SE), Artificial Intelligence (cs.AI), Machine Learning (cs.LG)

## Executive Summary

This paper addresses the critical gap between ideal tool-use benchmarks and real-world deployment scenarios. While recent agent benchmarks assume clean, reliable tool environments, production systems face cascading failures from tool unreliability. The authors introduce **ToolBench-X**, a comprehensive benchmark that evaluates LLM agents under five realistic tool-environment hazard types, revealing that current agents remain fragile under uncertainty but can be significantly hardened through structured guidance and recovery strategies. This work is essential for building production-grade autonomous agents for software development, where tool reliability directly impacts code quality and development velocity.

## Problem Statement

Large language models deployed as autonomous agents depend critically on external tool calls to execute real-world actions. However, evaluation frameworks have consistently lagged behind production realities:

- **Ideal-world assumption:** Current benchmarks assume perfect tool specifications, reliable execution, and deterministic outputs
- **Production reality:** Real tools exhibit specification drift, transient failures, corrupted outputs, and conflicting results across sources
- **Reliability gap:** Agents that perform well on clean benchmarks often catastrophically fail when tools become unreliable
- **Missing recovery patterns:** Existing benchmarks don't teach agents recovery strategies (retry, fallback, cross-verification)

This gap is particularly acute for software development automation, where tools (compilation, testing, package management, version control) frequently fail or return ambiguous results. The paper bridges this gap by introducing structured hazard types that agents must handle to be production-ready.

## Core Concepts & Theory

### Tool Reliability Hazard Categories

**ToolBench-X** defines five orthogonal, recoverable hazard types:

1. **Specification Drift**
   - Tool specification changes after initial learning
   - Agent must adapt to updated parameter schemas or return types
   - Recovery: Re-reading specification, parameter validation

2. **Invocation Error**
   - Transient failures in function calls (malformed requests, resource exhaustion)
   - Agent receives error responses rather than successful outputs
   - Recovery: Retry logic, parameter debugging, fallback to alternative tools

3. **Execution Failure**
   - Tool execution times out or crashes mid-operation
   - Partial or missing results despite correct invocation
   - Recovery: Timeout handling, checkpoint restart, state reconstruction

4. **Output Drift**
   - Tool returns results that don't match specification
   - Output format violations, semantic inconsistencies
   - Recovery: Output validation, schema checking, fallback parsing

5. **Cross-Source Conflict**
   - Multiple tools return conflicting results for the same query
   - Agent must resolve ambiguity and decide on trust boundaries
   - Recovery: Cross-verification, source ranking, consensus building

### Benchmark Architecture

```
ToolBench-X Structure
├── Task Dataset (executable multi-step tasks)
├── Tool Environment (deterministic, contract-based)
├── Hazard Injection Layer (five structured types)
├── Recovery Mechanisms (retry, fallback, verify, cross-check)
└── Evaluation Framework (canonical answers, automatic scoring)

Workflow Types:
├── Sequential: Task A → B → C
├── Parallel: A, B, C executed concurrently
└── Mixed: Some sequential, some parallel dependencies
```

### Evaluation Methodology

Each task has:
- **Canonical answer:** Ground truth for automatic evaluation
- **Multiple workflows:** Testing different composition patterns
- **Injected hazards:** 1-5 hazard instances per task
- **Recovery paths:** ≥1 valid recovery strategy per hazard
- **Deterministic execution:** Same task, same conditions → same results

## Main Ideas & Contributions

### 1. Reliability Gap Discovery

**Key Finding:** Agents show dramatic performance degradation under tool unreliability

- Agents performing well on standard function-calling benchmarks fail 60-80% of the time under structured hazards
- This gap is wider for open-source models, making deployment riskier for smaller organizations
- Hazard types are not equally difficult; some (e.g., Invocation Error) agents already handle better than others

### 2. Structured Recovery Mechanisms

The paper identifies and validates four recovery patterns:

- **Retry Logic:** Simple exponential backoff for transient failures
- **Fallback Strategy:** Switching to alternative tools when primary fails
- **Verification Protocol:** Cross-checking outputs against specifications
- **Consensus Building:** Querying multiple sources and ranking by reliability

### 3. Agent Guidance Strategies

Test-time guidance substantially improves performance:

- **Explicit recovery instructions:** "If the tool fails, try X before falling back"
- **Specification injection:** Providing updated tool specs to agents
- **Confidence scoring:** Agents learn to flag low-confidence results
- **Error categorization:** Teaching agents to distinguish failure types

### 4. Task Completion vs. Function-Call Accuracy

**Critical distinction:** Standard function-calling metrics (accuracy of individual calls) ≠ task completion

- An agent can make perfect function calls but fail to recover from hazards
- ToolBench-X emphasizes end-to-end task success under adversity
- This aligns with real-world metrics: developer time saved, bugs fixed, features shipped

## Methodology & Implementation

### Dataset Construction

**Data Sources:**
- Diverse domains: software development, finance, e-commerce, content management
- Task types: sequential workflows (code compilation → testing → deployment), parallel execution (testing multiple branches), mixed patterns
- Baseline benchmark: 500+ executable tasks with deterministic ground truth

**Hazard Injection Strategy:**

1. Start with clean task execution (establish baseline)
2. Inject 1-5 hazard instances per task
3. Vary hazard timing (early, middle, late in workflow)
4. Ensure ≥1 recovery path per injected hazard
5. Validate recovered outputs match canonical answer

### Experimental Setup

**Models Evaluated:** 19 models across:
- Closed-source: GPT-4, GPT-4o, Gemini, Qwen-max, Kimi K2
- Open-source: Llama 3, Mistral, etc. (various parameter sizes)

**Metrics:**

| Metric | Definition | Relevance to Dev Tasks |
|--------|-----------|----------------------|
| Task Completion Rate | % tasks solved end-to-end | Direct proxy for developer productivity |
| Function-Call Accuracy | % individual calls correct | Traditional benchmark metric (insufficient) |
| Recovery Success Rate | % hazards handled without manual intervention | Autonomy level in dev workflows |
| Time-to-Recovery | Steps/tokens to recover from hazard | Cost and latency impact |
| Fallback Effectiveness | How often fallback solutions work | Graceful degradation capability |

**Baseline Comparisons:**

- Standard ToolBench (clean environment): agents achieve 85-95% accuracy
- ToolBench-X (with hazards): same agents drop to 20-40% task completion
- With guidance: recovery to 60-75% (substantial but not perfect)

### Results

[Exact figures unavailable — see full paper for detailed result tables]

**Key Findings:**

1. **Fragility is widespread:** Across all 19 models tested, performance on clean tasks (>90%) drops dramatically to <50% with hazards
2. **Hazard difficulty varies:** Specification Drift is easier to handle; Cross-source Conflict is hardest
3. **Guidance helps significantly:** Structured recovery instructions improve completion by 15-30pp
4. **Open-source models lag:** Open-source models show larger degradation than proprietary models
5. **Recovery strategies are learnable:** Agents can be trained to recognize hazard types and apply appropriate recovery patterns

## Practical Applications & Use Cases

### Software Development Automation

**Real-world scenario:** Autonomous agent fixing a GitHub issue

```
Workflow:
1. Clone repository (tool: git)
   → Hazard: Clone times out
   → Recovery: Retry with specific branch
2. Analyze failing tests (tool: pytest)
   → Hazard: Test output truncated
   → Recovery: Re-run with verbose logging
3. Generate fix (tool: code editor + linter)
   → Hazard: Linter output format changed (drift)
   → Recovery: Parse new format, validate syntax
4. Submit PR (tool: git, GitHub API)
   → Hazard: API rate limit hit
   → Recovery: Wait, retry with exponential backoff
5. Verify CI passes
   → Hazard: CI results conflict (flaky test)
   → Recovery: Cross-check with local runner
```

Agent must handle each hazard and complete the full workflow.

### CI/CD Pipeline Orchestration

Agents coordinating multi-tool pipelines:
- Build tools (Docker, Make) fail → fallback to alternative build strategy
- Test frameworks report conflicting results → consensus protocol
- Deployment tools timeout → retry with checkpointing
- Monitoring tools give inconsistent health signals → verification layer

### Autonomous Debugging

Tool reliability critical for reasoning about code:
- Debugger outputs may be incomplete → cross-check with logging
- Profilers may have transient errors → retry with sampling
- Symbol resolution may fail → fallback to pattern matching

## Insights & Implications

### For Agent System Design

1. **Reliability is non-negotiable:** Tool-using agents for production must be benchmarked under realistic hazards, not clean environments
2. **Recovery strategies matter more than individual accuracy:** Teaching agents when and how to recover outweighs perfect first-call accuracy
3. **Guidance scales benefits:** Small prompting changes (recovery instructions) yield 15-30pp gains
4. **Fallback architectures enable resilience:** Multi-tool strategies and graceful degradation are essential

### For Development Automation

1. **Tool stability is a prerequisite:** Agents can handle some unreliability, but require >70% stable execution as baseline
2. **Transparency improves controllability:** Agents that explain recovery decisions are easier to debug and improve
3. **Monitoring adds overhead:** Real-time tool monitoring and validation doubles agent reasoning cost but is often necessary

### Limitations & Open Questions

1. **Recovery strategies are task-specific:** General recovery principles don't transfer well across domains
2. **Cascading failures:** Hazards early in workflow amplify failures downstream (not fully explored)
3. **Human-in-the-loop:** Some failures require human intervention; paper doesn't optimize for escalation points
4. **Trade-off between cost and reliability:** Verification/cross-check strategies increase token usage significantly

## Code & Resources

**Official Repository:** GitHub link not provided in available search results; check arXiv PDF for implementation details

**Dependencies:**
- Standard Python tooling for benchmark construction
- Multi-version tool environments for injecting hazards
- Deterministic execution framework for reproducibility

**Quick-Start Integration:**

1. Evaluate your agent on ToolBench-X (clean tasks first)
2. Analyze failure patterns on hazard-injected tasks
3. Add recovery strategies: retry logic, fallback tools, verification
4. Re-evaluate with guidance (updated system prompts with recovery instructions)
5. Measure improvement in task completion rate

## Related Work & Context

### Foundations

- **Tool-use benchmarks:** API-Bank, ToolBench, ToolLLM (focus on accuracy, not reliability)
- **Agent robustness:** Prior work on adversarial examples, but limited to static perturbations
- **Multi-step reasoning:** ReAct, Reflexion (foundational for recovery loops)

### Related Papers

- "UniToolCall: Unifying Tool-Use Representation, Data, and Evaluation for LLM Agents" (standardization of tool-use evaluation)
- "FAMA: Failure-Aware Meta-Agentic Framework" (handling failures in open-source models)
- "AsyncTool: Evaluating the Asynchronous Function Calling Capability" (multi-task tool use under latency)

### Future Directions

1. **Learned recovery strategies:** Train agents to discover optimal recovery patterns via RL
2. **Tool adaptation:** Agents that learn new tool specifications on-the-fly
3. **Cascading failure analysis:** Understanding how early failures propagate downstream
4. **Human-agent collaboration:** Designing intervention points for human oversight

---

**Citation:**
```
@article{tian2026beyond,
  title={Beyond Function Calling: Benchmarking Tool-Using Agents under Tool-Environment Unreliability},
  author={Tian, Yang and Shi, Zhengpeng and Zhou, Yu and Zhao, Bo},
  journal={arXiv preprint arXiv:2606.25819},
  year={2026}
}
```
