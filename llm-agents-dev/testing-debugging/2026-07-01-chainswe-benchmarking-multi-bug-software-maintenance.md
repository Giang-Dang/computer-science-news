# ChainSWE: Benchmarking Coding Agents on Multi-Bug Software Maintenance

**Authors:** Qirui Jin, Yihao Sun, Yixuan Weng, Hao Wu, Xiaoli Deng, Honglei Zhang, and 15+ co-authors

**ArXiv ID:** 2607.02606

**Submission Date:** July 1, 2026

---

## Executive Summary

ChainSWE introduces the first benchmark for evaluating software engineering agents on sequential, dependent bug fixes within a shared codebase. While current LLM-based agents perform well on isolated tasks, real-world software maintenance involves continuous workflows where fixing one bug creates dependencies for the next. This research reveals a critical performance drop of up to 70% as agents navigate chain-dependent bug fixes, establishing a new evaluation paradigm for real-world software maintenance automation.

## Problem Statement

### Development Automation Challenge

Existing software engineering benchmarks (SWE-bench family) evaluate coding agents on isolated, independent tasks where:
- Each task begins with a fresh repository snapshot
- Bugs are treated as standalone issues
- The cumulative context and dependencies of real-world maintenance are collapsed

However, real software maintenance follows a continuous maintenance workflow:
- Developers fix related defects in sequence
- Earlier fixes influence the context and complexity of subsequent fixes
- Bugs often have interdependencies in shared code components
- Context carried from one fix to the next affects decision-making and code quality

### Research Gap

No existing benchmark captures sequential, dependent bug-fixing scenarios that reflect actual continuous software development. The performance degradation observed under chained maintenance scenarios is undocumented and unmeasured.

## Core Concepts & Theory

### Sequential Bug-Fixing Workflows

ChainSWE models software maintenance as a sequence of causally related fixes:

```
Repository State 0 (initial)
         ↓
Fix Bug 1 → Repository State 1
         ↓
Fix Bug 2 → Repository State 2
         ↓
Fix Bug 3 → Repository State 3
         ...
```

### Chain Composition

**Dataset Statistics:**
- Chronologically ordered chains of 304 issues
- Spans 54 Python projects
- Mined from SWE-bench-family datasets (SWE-bench, SWE-bench Verified, SWE-bench Pro)
- Chain lengths: varying from 2-15 sequential bug fixes per chain

### Agent Evaluation Framework

Agents are evaluated on their ability to:
1. **Fix Sequential Issues:** Resolve bugs while preserving previous fixes
2. **Maintain Context:** Carry forward understanding from earlier bugs to later ones
3. **Avoid Regression:** Ensure earlier fixes remain valid after new modifications
4. **Handle Interdependencies:** Navigate implicit dependencies between related bugs

### Key Metrics

**Primary Metric: Chain Completion Rate**
- Percentage of chains where all sequential bugs are successfully fixed
- Measured across varying chain lengths

**Performance Degradation Analysis**
- Isolated bug resolution: baseline performance (100%)
- Chain-2 (two sequential bugs): intermediate drop
- Chain-3+ (three or more bugs): cumulative degradation
- Observed degradation: up to 70% performance loss with chain progression

## Main Ideas & Contributions

### Novel Benchmark Design

1. **Chronologically Organized Chains:** Bugs mined and sequenced temporally to reflect real maintenance workflows
2. **Shared Codebase Context:** All fixes applied to the same evolving repository, creating natural interdependencies
3. **Realistic Task Distribution:** 304 chains across 54 projects, ensuring diversity in programming patterns and domain-specific contexts

### Key Findings

**Performance Degradation Pattern:**
- Single-bug resolution (baseline): agents achieve their best performance
- Chain-length 2: initial performance drop observed
- Chain-length 3+: increasingly severe degradation
- Maximum observed loss: ~70% on longest chains

**Failure Mode Categories:**
1. **Context Confusion:** Agents lose track of earlier fixes when processing later bugs
2. **Regression Introduction:** New fixes accidentally break previously fixed issues
3. **Cumulative Complexity:** Agent reasoning quality degrades as the edit history grows

### Implications for Agentic Development

- **Single-Task Bias:** Current agent evaluation overestimates real-world performance
- **Stateful Development:** Agents must maintain coherent state across multiple edits
- **Dependency Awareness:** Future agent systems need explicit mechanisms to track fix interdependencies

## Methodology & Implementation

### Dataset Construction

**Source:** Six SWE-bench-family datasets
- SWE-bench (full open-source baseline)
- SWE-bench Verified (human-validated fixes)
- SWE-bench Pro (challenging, repository-level issues)

**Filtering & Sequencing:**
1. Extract all issues chronologically by date
2. Group issues by project
3. Create chains of 2-15 sequential issues within the same project
4. Validate that each chain is solvable independently and sequentially

### Experimental Setup

**Agents Evaluated:**
- Claude Opus (Anthropic)
- GPT-4 Turbo (OpenAI)
- Open-source agents (CodeLlama, WizardCoder)
- Specialized SWE agents (SWE-Agent, etc.)

**Evaluation Protocol:**
- For each chain: reset repository to initial state
- Apply agents sequentially to each bug in chain order
- Record success/failure at each step
- Track whether chain completion is achieved

### Key Results

**Aggregate Performance Metrics:**

| Chain Length | Success Rate (%) | Relative Drop (%) |
|-------------|------------------|-------------------|
| Single (baseline) | 100 | — |
| 2 bugs | 65-75 | 25-35 |
| 3 bugs | 40-50 | 50-60 |
| 4+ bugs | 20-35 | 65-80 |

**Model-Specific Results:**
- Claude Opus: most stable performance across chain lengths, ~40% success on 3-bug chains
- GPT-4 Turbo: initial strength but sharper degradation curve
- Open-source models: more severe degradation starting at chain-length 2

**Failure Analysis:**
- Context loss: 35-40% of failures
- Regression (breaking prior fixes): 30-35% of failures
- Incomplete/incorrect fix: 25-30% of failures

## Practical Applications & Use Cases

### Real-World Software Maintenance Scenarios

1. **Bug Triage Systems:** Systems that queue dependent bugs must account for agent degradation
2. **CI/CD Agent Integration:** Continuous bug-fixing agents in pipelines need state management mechanisms
3. **Large-Scale Codebase Maintenance:** Organizations using agents for ongoing maintenance need chain-aware evaluation

### Concrete Example Workflow

```
Time T=1: Bug #1001 reported (file A, function foo())
         → Agent fixes foo() with change set X
         → Repository state updated

Time T=2: Bug #1002 reported (file A, function bar())
         → Agent must understand foo() change context
         → Risk of regression if changes interact
         → Success rate: 60-70%

Time T=3: Bug #1003 reported (file B, function baz())
         → Agent sees cumulative edits from #1001, #1002
         → Context window filling with historical changes
         → Success rate: 35-50%
```

### Integration Challenges

- **State Management:** Tracking which code changes belong to which fix
- **Test Suite Evolution:** Tests added/modified for each fix may conflict
- **Performance Overhead:** Longer chains mean more tokens consumed per task
- **Agent Confusion:** Larger edit histories increase LLM token limits and reasoning complexity

## Insights & Implications

### Impact on Agent-Driven Development

1. **Single-Task Evaluation Limitations:** Current benchmarks (SWE-bench, HumanEval) significantly overestimate real-world agent effectiveness

2. **Need for Stateful Agents:** Future agent frameworks must:
   - Explicitly track fix dependencies
   - Maintain coherent context across sequential tasks
   - Implement mechanisms to prevent regression

3. **Cumulative Degradation:** Agent performance follows a power-law degradation curve—early fixes are easier but later fixes become exponentially harder

### Limitations & Open Questions

1. **Language Generalization:** ChainSWE focuses on Python; results may differ for Java, C++, Go
2. **Chain Length Boundaries:** No clear guidance on maximum practical chain length
3. **Agent Architecture:** Which agent components (planning, execution, verification) are most affected by context growth?

### Future Research Directions

1. **Regression Prevention Mechanisms:** Develop techniques to ensure agent fixes don't break prior changes
2. **Hierarchical Task Decomposition:** Can agents plan multi-step fixes more effectively with explicit decomposition?
3. **Context Compression:** How can agents maintain effective context across long chains without token overflow?
4. **Hybrid Workflows:** Can human-agent collaboration mitigate degradation in long maintenance chains?

## Code & Resources

### Official Repository

- **GitHub:** [https://github.com/qjin2016/ChainSWE](https://github.com/qjin2016/ChainSWE) (Expected publication)
- **Dataset:** ChainSWE benchmark with 304 chronologically ordered bug-fix chains

### Dependencies

- Python 3.10+
- LLM APIs: OpenAI, Anthropic, or open-source model hosting
- SWE-bench family datasets (reference for issue mining)
- Test execution framework (pytest, unittest)

### Quick-Start Integration Guide

1. **Load ChainSWE benchmark:** Download the dataset of 304 bug chains
2. **Prepare agent harness:** Implement sequential bug-fix loop that maintains repository state
3. **Run evaluation:** For each chain, apply agent fixes in order and record completion rate
4. **Analyze degradation:** Compare isolated vs. chained performance metrics

```python
# Pseudocode: Chain-based evaluation
for chain in chainswe_benchmark:
    repo = initialize_repo(chain.project)
    successes = 0
    for bug in chain.bugs:
        fix = agent.generate_fix(repo, bug)
        if validate_fix(fix, repo):
            successes += 1
            apply_fix(repo, fix)
    chain_success_rate = successes / len(chain.bugs)
    results.append(chain_success_rate)
```

## Related Work & Context

### Prior Software Engineering Benchmarks

- **SWE-bench (2024):** Introduced repository-level bug-fixing evaluation but treats each task independently
- **SWE-bench Verified (2024):** Human-validated fixes, improved reliability but maintains isolation assumption
- **SWE-bench Pro (2025):** More complex issues but still isolated task evaluation

### Foundational Agent & Code Generation Work

- **SWE-Agent (OpenAI):** Agentic framework for software engineering; ChainSWE tests this on sequential tasks
- **AutoCodeRover:** Multi-agent orchestration for code understanding
- **Repository-level reasoning:** Prior work on understanding full codebase context

### Related Evaluation Paradigms

- **Long-horizon task evaluation:** ChainSWE applies principles from long-horizon RL benchmarks to code generation
- **Continuous integration testing:** Analogous to sequential test execution in CI/CD pipelines
- **Multi-step reasoning:** Related to chain-of-thought prompting but for code actions

### Possible Extensions

1. **Cross-Repository Chains:** Do agent errors in one project affect performance on related projects?
2. **Chain Statistics:** What properties of chains (edit complexity, interdependency distance) predict degradation?
3. **Agent Self-Repair:** Can agents detect and fix their own regressions within chains?
4. **Optimized Chain Scheduling:** Can agents pre-process chains to identify optimal fix ordering?

---

## Summary

ChainSWE establishes a new evaluation paradigm for software engineering agents that reflects real-world maintenance workflows. The benchmark reveals a critical performance degradation (up to 70%) as agents tackle sequential, dependent bug fixes—a scenario absent from existing isolated-task benchmarks. This work highlights the gap between current agent capabilities and production-scale software maintenance requirements, motivating future research into stateful agent design, regression prevention, and hierarchical task orchestration.
