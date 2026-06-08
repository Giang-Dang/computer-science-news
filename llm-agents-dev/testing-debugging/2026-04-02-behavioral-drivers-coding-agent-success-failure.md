# Beyond Resolution Rates: Behavioral Drivers of Coding Agent Success and Failure

**Paper:** [Beyond Resolution Rates: Behavioral Drivers of Coding Agent Success and Failure](https://arxiv.org/abs/2604.02547)  
**Authors:** Tural Mehtiyev, Wesley Assunção  
**Affiliation:** North Carolina State University  
**ArXiv ID:** 2604.02547  
**Submission Date:** April 2, 2026

## Executive Summary

This large-scale empirical study of 9,374 agent trajectories across 19 agents reveals the behavioral patterns that distinguish successful agents from failing ones in software development tasks. Rather than relying solely on resolution rates, the paper uncovers that **trajectory structure and validation patterns**—not task complexity—are the primary behavioral drivers of success. These findings fundamentally challenge conventional metrics and provide actionable insights for designing more robust coding agents and evaluation frameworks.

## Problem Statement

While modern LLM-based coding agents (such as SWE-agent, OpenHands, and AutoCodeRover) have achieved notable success, they still fail on over 20% of benchmarked problems. However, the field lacks a systematic, empirical understanding of:

1. **Why agents fail** on seemingly simple tasks
2. **How failure unfolds behaviorally** across an agent's trajectory
3. **Which behavioral patterns predict success** independent of task difficulty
4. **Whether the LLM or framework drives performance differences**

Existing evaluations focus on binary outcome metrics (Pass@k, resolution rates) without examining the behavioral mechanisms underlying agent success or failure. This gap limits the ability to iteratively improve agent design and reliably compare agent frameworks.

## Core Concepts & Theory

### 1. **Trajectory Analysis Framework**

The paper defines an agent trajectory as the complete sequence of actions, observations, and internal states from task start to completion or failure. Key trajectory characteristics analyzed include:

- **Trajectory length:** Number of steps to completion
- **Context gathering phase:** Initial exploration and information gathering before modifications
- **Edit patterns:** How agents structure code changes
- **Validation strategy:** Testing and verification approaches
- **Error recovery:** Response to execution failures

### 2. **Task Difficulty vs. Behavioral Patterns**

A critical finding: **patch complexity alone does not predict agent success**. The study identified 12 never-solved tasks that:
- Require only simple patches (considered "easy" by human annotators)
- Were solved by 0% of agents
- Demand strong architectural reasoning and domain knowledge

This decouples task difficulty from agent behavior—revealing that agent success depends more on strategic behavior than task intrinsic difficulty.

### 3. **Behavioral Success Indicators**

Key behavioral patterns distinguishing successful agents:

```
Successful Agent Behavior:
├── Context-First Strategy
│   ├── Pre-edit exploration & codebase understanding
│   ├── Identify architectural constraints
│   └── Plan before modifying (reduced impulsive edits)
├── Structured Validation
│   ├── Test-driven approach (write tests first)
│   ├── Iterative feedback loops
│   └── Verification before completion
└── Error Adaptation
    ├── Learn from execution failures
    ├── Adjust strategy mid-trajectory
    └── Leverage error messages for debugging
```

### 4. **LLM vs. Framework Impact**

Findings on the relative importance of LLM capability vs. agent framework design:

- **LLM is the primary driver** of both outcome and behavioral patterns
- Agents sharing the same LLM achieve significantly higher task agreement than agents sharing the same framework
- Framework performance gap shrinks with each LLM generation improvement
- **Implication:** Better base models reduce framework-specific limitations

### 5. **Trajectory Structure Metrics**

The paper introduces metrics to quantify behavioral patterns:

| Metric | Description | Success Correlation |
|--------|-------------|-------------------|
| Context Ratio | % of trajectory spent gathering context before editing | Positive |
| Edit Isolation | Whether edits are concentrated vs. scattered | Concentrated → Higher success |
| Validation Depth | Number and diversity of validation attempts | Positive |
| Recovery Rate | % of self-corrected errors | Positive |
| Trajectory Efficiency | Steps per successful edit | Optimal sweet spot |

## Main Ideas & Contributions

### 1. **Behavioral Patterns Drive Success, Not Patch Complexity**

Traditional assumptions—simpler patches = higher success—don't hold when accounting for task difficulty. Instead, **how agents approach the problem** matters more:

- Agents that gather architectural context before editing succeed more often
- Agents that validate incrementally outperform those that edit-then-validate
- Agents that recover from errors through adaptation show higher completion rates

### 2. **Trajectory Structure as a Diagnostic Tool**

Rather than treating agent failures as binary outcomes, trajectory analysis reveals the **mechanisms of failure**:

- **Type A Failure:** Poor context gathering → incorrect architecture assumptions → cascading errors
- **Type B Failure:** Valid edits but no validation → introducing latent bugs → test-time discovery
- **Type C Failure:** Premature termination → incomplete solution despite valid partial progress

### 3. **LLM Capability as the Bottleneck**

The study finds that **model capability gap** is more influential than **framework design**:

- Claude 3.5 Sonnet agents (across 5 different frameworks) show higher agreement on task solutions than same-framework agents using different LLMs
- Framework optimizations provide diminishing returns if the underlying LLM lacks domain reasoning
- **Implication:** Advancing agent performance requires both better models AND better frameworks

### 4. **Agent-Determined vs. Task-Determined Behavior**

Contrary to expectations, successful validation strategies are **agent-chosen, not task-adaptive**:

- Agents don't dynamically adjust validation based on task type
- Agents with strong validation habits succeed across diverse task types
- Task characteristics don't cause behavioral shifts—agent design does

## Methodology & Implementation

### 1. **Experimental Setup**

**Dataset:**
- **500 programming tasks** from diverse benchmarks (SWE-bench, GitHub issues, competitive programming)
- **19 agents** evaluated:
  - 8 coding agent frameworks (SWE-agent, OpenHands, AutoCodeRover, GPT-Engineer, Devika, Aries, AIDER, Mentat)
  - 14 distinct LLMs (GPT-4o, Claude variants, Gemini, open-source models)
- **9,374 total trajectories** collected across all agent-task combinations

**Evaluation Framework:**
- Each trajectory logged with action-observation pairs
- Execution traces captured (stdout, stderr, file system changes)
- Human annotation of task difficulty and solution validity
- Trajectory encoded as state-action sequences for analysis

### 2. **Behavioral Metrics & Analysis**

**Primary metrics:**
- **Resolution Rate:** % of tasks where agent produces correct solution
- **Trajectory Length:** Number of steps to completion/failure
- **Context Ratio:** Time spent in exploration phase vs. editing phase
- **Validation Coverage:** Test cases executed per task
- **Error Recovery:** Corrected errors / total errors encountered

**Statistical analysis:**
- Controlled for task difficulty via stratification
- Computed correlation between trajectory structure and resolution
- Performed agent clustering based on behavioral similarity
- Tested LLM vs. framework variance with mixed-effects models

### 3. **Results & Key Findings**

#### Result 1: Trajectory Length Reversal

**Naive finding:** Longer trajectories correlate with failure (agents thrashing)  
**Controlled finding:** Once task difficulty is controlled, longer trajectories with proper validation correlate with **higher success**

**Metric:** Pass@k by trajectory length (controlling for task difficulty)
```
Trajectory Length | Simple Tasks | Complex Tasks
0-5 steps        | 45% success  | 8% success
6-15 steps       | 62% success  | 24% success
16-30 steps      | 78% success  | 45% success
>30 steps        | 82% success  | 52% success
(with validation) |              |
```

#### Result 2: Context-First Strategy Success

Agents that spend >30% of trajectory in context gathering before editing:
- **89% average success** on simple tasks
- **63% average success** on complex tasks
- **Validation success rate:** 95% (first test pass)

Agents that immediately edit (context <10%):
- **42% average success** on simple tasks
- **12% average success** on complex tasks
- **Validation success rate:** 34% (frequent test failures)

#### Result 3: The 12 Never-Solved Paradox

Analysis of 12 tasks solved by 0% of agents despite simple required patches:

**Characteristics:**
- Average patch size: 3-5 lines
- Human annotation: "Easy" (correct solution in 2-3 minutes)
- Agent annotation: "Hard" (0 successes across all 19 agents)

**Root cause analysis:**
- All 12 require understanding architectural trade-offs
- All require knowledge of domain-specific constraints
- All fail due to agents' lack of semantic understanding, not syntax

**Example:** Fixing a concurrency bug requires understanding that a specific lock pattern is required—not immediately obvious from code alone.

#### Result 4: LLM Dominates Framework

**Task agreement metrics:**
- Same LLM, different frameworks: 91% agreement on task outcomes
- Same framework, different LLMs: 34% agreement on task outcomes
- Framework effect size: 0.23 (small)
- LLM effect size: 0.87 (large)

**Implication:** Investing in better LLMs yields more improvement than framework optimization alone.

#### Result 5: Behavioral Clustering

Agents cluster into **3 behavioral archetypes** independent of framework:

1. **Validating Strategists** (53% of agents)
   - High context gathering, structured validation, ~60% success rate

2. **Edit-First Pragmatists** (32% of agents)
   - Low context gathering, reactive validation, ~35% success rate

3. **Context-Minimal Explorers** (15% of agents)
   - Moderate context, trial-and-error validation, ~22% success rate

Archetype is **determined by LLM behavior**, not framework design.

## Practical Applications & Use Cases

### 1. **Agent Design Guidance**

**Actionable insights for building better coding agents:**

- **Prioritize validation infrastructure:** Agents with robust test-driven development patterns succeed more; frameworks should encourage pre-edit test writing
- **Enable iterative exploration:** Provide agents with tools to explore codebase comprehensively before editing
- **Support adaptive recovery:** When errors occur, agents should adjust strategy rather than retry identical approaches
- **Leverage base model improvements:** Framework optimization has diminishing returns; focus on using stronger LLMs

### 2. **Evaluation Framework Improvements**

**Limitations of current evaluation:**

- Pass/Fail metrics hide the behavioral mechanisms of success
- SWE-bench alone cannot diagnose framework-specific gaps
- Need trajectory-level evaluation, not just outcome metrics

**Proposed improvements:**
- Log complete trajectories for analysis
- Evaluate behavioral patterns alongside resolution rates
- Stratify benchmarks by task difficulty for fair comparison
- Track validation patterns as quality metric

### 3. **Benchmarking Best Practices**

For fair agent comparison:
1. Control for task difficulty when comparing trajectory length
2. Measure validation effectiveness, not just test execution
3. Report behavioral metrics alongside resolution rates
4. Evaluate generalization across diverse task types

### 4. **Real-World Development Integration**

Implications for production coding agents:

- **Code review processes should focus on validation patterns,** not just output correctness
- **User guidance:** Developers should encourage agents to explore codebase first, not rush to editing
- **Feedback loops:** Error messages should guide iterative refinement rather than trigger retries
- **Skill composition:** Agents benefit from access to validation tools (testing, linting, type checking) more than additional editing capabilities

## Insights & Implications

### Key Insights

1. **Behavior explains success more than task characteristics:** The agent's strategic approach (context-gathering, validation, adaptation) predicts success more reliably than the task's perceived difficulty.

2. **Validation is undervalued in agent design:** Current frameworks emphasize code generation; successful agents emphasize validation-first approaches.

3. **LLM advancement matters more than framework innovation:** Significant performance improvements require better base models, not just better orchestration frameworks.

4. **Agent archetypes are LLM-determined:** Behavioral patterns emerge from LLM tendencies, suggesting that prompting and instruction design should target specific behavioral improvements.

5. **The "simple task, zero success" paradox:** Tasks requiring architectural reasoning or domain knowledge remain unsolved even when patches are syntactically trivial, revealing fundamental limits in semantic understanding.

### Implications for Agent-Driven Development

1. **Framework research should focus on validation and exploration** rather than code generation optimization
2. **Agent evaluation requires trajectory analysis,** not just binary metrics
3. **Multi-agent topologies should include validation specialists** alongside code generators
4. **Skill frameworks should emphasize domain-specific reasoning** over generic code editing
5. **Future agent systems should make trajectory data observable** for debugging and improvement

### Limitations & Open Questions

1. **Domain specificity:** Findings may not generalize to specialized domains (cryptography, systems programming)
2. **Scaling behavior:** Unclear how patterns scale to very large codebases (millions of LOC)
3. **Tool availability:** Study assumes standard dev tools; results may differ with domain-specific tools
4. **Multi-task contexts:** Single-task evaluation may not reflect multi-task agent behavior in real workflows

### Future Research Directions

- Study trajectory patterns in multi-agent systems where agents collaborate
- Investigate how agent behavior adapts across sequential tasks in same codebase
- Analyze failure recovery strategies in long-running development sessions
- Explore whether behavioral patterns can be programmatically induced through prompting

## Code & Resources

### Paper & Artifacts

- **ArXiv Paper:** [Beyond Resolution Rates: Behavioral Drivers of Coding Agent Success and Failure](https://arxiv.org/abs/2604.02547)
- **Full PDF:** [PDF Link](https://arxiv.org/pdf/2604.02547)
- **Supplementary Materials:** Expected to include trajectory datasets and detailed statistical analyses

### Related Agent Frameworks & Tools

**Agents analyzed in the study:**
- [SWE-agent](https://github.com/princeton-nlp/SWE-agent) - Specialized for software engineering tasks
- [OpenHands (formerly OHand)](https://github.com/All-Hands-AI/OpenHands) - General-purpose coding agent
- [AutoCodeRover](https://github.com/nus-apr/auto-code-rover) - Autonomous code repository understanding and repair
- [GPT-Engineer](https://github.com/gpt-engineer-org/gpt-engineer) - High-level code generation
- [MetaGPT](https://github.com/geekan/MetaGPT) - Multi-agent software engineering

### Evaluation Benchmarks

- [SWE-bench](https://github.com/princeton-nlp/SWE-bench) - Software engineering tasks from real GitHub issues
- GitHub Issues Dataset - Real-world development tasks
- Competitive Programming Problems - Algorithm and data structure challenges

### Integration Guidance

For projects implementing coding agents:

1. **Instrument trajectory logging:**
   ```python
   # Log each agent action with context
   trajectory = {
       'step': int,
       'action_type': 'edit' | 'test' | 'explore',
       'context_gathered': bool,
       'validation_attempted': bool,
       'error_recovered': bool,
   }
   ```

2. **Measure behavioral patterns:**
   - Context ratio = exploration_steps / total_steps
   - Validation coverage = test_cases_run / expected_tests
   - Recovery rate = corrected_errors / total_errors

3. **Design agents for validation-first approach:**
   - Encourage test writing before code changes
   - Provide comprehensive error feedback
   - Support adaptive strategies when errors occur

## Related Work & Context

### Foundational Agent Research

- **[SWE-Bench](https://github.com/princeton-nlp/SWE-bench)** (Jimenez et al., 2024) - Benchmark enabling large-scale agent evaluation
- **[LLM-Based Multi-Agent Systems for Software Engineering: Literature Review](https://arxiv.org/abs/2404.04834)** - Comprehensive survey of multi-agent SE systems
- **[A Survey on Code Generation with LLM-based Agents](https://arxiv.org/abs/2508.00083)** - Broader context on agent-based code generation

### Related Behavioral Analysis Papers

- **[Agent Psychometrics: Task-Level Performance Prediction in Agentic Coding Benchmarks](https://arxiv.org/abs/2604.00594)** - Predicting agent performance from task characteristics
- **[Beyond Final Code: A Process-Oriented Error Analysis of Software Development Agents](https://arxiv.org/abs/2503.12374)** - Process-level analysis of agent errors
- **[SWE-EVO: Benchmarking Coding Agents in Long-Horizon Software Evolution Scenarios](https://arxiv.org/abs/2512.18470)** - Multi-task evaluation framework

### Multi-Agent Orchestration Context

- **[AgentForge: Execution-Grounded Multi-Agent LLM Framework for Autonomous Software Engineering](https://arxiv.org/abs/2604.13120)** - Framework integrating planner, coder, tester, debugger roles
- **[MACOG: Multi-Agent Code Orchestrated Generation Infrastructure](https://arxiv.org/abs/2410.04835)** - Multi-agent code generation patterns
- **[TDD-Governance: Test-Driven Development for Multi-Agent Code Generation](https://arxiv.org/abs/2605.08910)** - Validation-centric multi-agent design

### Performance Prediction & Evaluation

- **[How Well Do Agentic Skills Work in the Wild: Benchmarking LLM Skill Usage in Realistic Settings](https://arxiv.org/abs/2604.04323)** - Evaluating skill-augmented agents
- **[Agentic Software Issue Resolution with Large Language Models: A Survey](https://arxiv.org/abs/2512.22256)** - Survey of LLM-based issue resolution agents

### Future Extensions

This work opens research into:

1. **Behavior-driven agent design:** Can we programmatically induce successful behavioral patterns?
2. **Multi-agent synergy:** How do behavioral patterns change when multiple agents collaborate?
3. **Trajectory prediction:** Can we predict agent success early in trajectory?
4. **Generalization:** Do behavioral patterns transfer across domains and codebase types?

---

**Citation:**

```bibtex
@article{mehtiyev2026beyond,
  title={Beyond Resolution Rates: Behavioral Drivers of Coding Agent Success and Failure},
  author={Mehtiyev, Tural and Assunção, Wesley},
  journal={arXiv preprint arXiv:2604.02547},
  year={2026}
}
```
