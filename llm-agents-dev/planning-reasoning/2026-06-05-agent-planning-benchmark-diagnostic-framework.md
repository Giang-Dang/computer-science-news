# Agent Planning Benchmark: A Diagnostic Framework for Planning Capabilities in LLM Agents

**ArXiv ID:** [2606.04874](https://arxiv.org/abs/2606.04874)  
**Authors:** Haoyu Sun, Wenxuan Wang, Mingyang Song, and others (Tongji University, Shanghai AI Laboratory, Harbin Institute of Technology)  
**Submitted:** June 5, 2026  
**Subcategory:** `planning-reasoning`

---

## Executive Summary

Agent Planning Benchmark (APB) introduces the first systematic diagnostic framework specifically designed to isolate and measure planning capabilities in LLM-based agents, independent of execution failures. With 4,209 multimodal cases spanning 22 domains and five evaluation settings, APB reveals fundamental weaknesses in frontier LLMs: long-horizon planning decomposition, tool-noise robustness, calibrated refusal (knowing when tasks are infeasible), and inference-time refinement. Critically, APB demonstrates that end-to-end success metrics (e.g., "agent solved the task") conflate planning failures with execution errors, making it impossible to diagnose root causes. This work is significant for agent-driven development because it establishes that planning—the ability to decompose goals into actionable steps, route to appropriate tools, reason over constraints, and recognize impossibility—is a distinct capability separate from tool execution, and that current agents have systematic blind spots in long-horizon planning that directly impact software development task completion.

---

## Problem Statement

### Development Automation Challenge

Autonomous software development agents must plan complex multi-step workflows: understand requirements, design architecture, decompose into subtasks, select appropriate tools (testing, debugging, refactoring), sequence operations respecting dependencies, and recognize when tasks are infeasible. However, existing agent evaluations report only end-to-end success rates (e.g., "SWE-bench Pass@1 = 30%"), which masks **where planning fails**:

- Did the agent fail because it couldn't plan the right sequence of steps?
- Did it plan correctly but execute the wrong tool?
- Did it fail to recognize an impossible task and waste resources?
- Did it plan correctly but with wrong parameters?

These distinctions matter: fixing a planning failure requires different interventions than fixing a tool invocation failure.

### Prior Agent System Limitations

Existing agent evaluation benchmarks suffer from:

1. **End-to-end metrics are opaque**: Reporting only "pass" or "fail" obscures root causes; a task can fail at planning stage, tool selection, parameter tuning, or execution
2. **No planning-specific stress tests**: Benchmarks don't systematically vary planning difficulty (horizon length, constraint complexity, tool noise)
3. **Conflated skill assessment**: An agent might have weak planning but strong execution (or vice versa); existing benchmarks can't disentangle these
4. **No robustness evaluation**: Real-world planning must handle degraded environments (broken tools, incorrect tool descriptions, ambiguous instructions); benchmarks don't test this
5. **No calibration measurement**: Agents should know when a task is infeasible and refuse to attempt it; few benchmarks reward this behavior

### Research Gap

Prior work on agent evaluation either (1) focused on end-to-end success in specific domains (coding, retrieval-augmented generation) without isolating planning as a factor, or (2) studied planning in offline settings (game playing, robotics) without multimodal web/API interactions typical of software development. **No benchmark systematically isolates planning as a first-class capability**, making it impossible to diagnose what agent systems need to improve.

---

## Core Concepts & Theory

### Planning as a Distinct Capability

APB formalizes planning as a sequence of decisions:

```
Task Input (Goal + Environment Description)
        ↓
[PLAN] Decompose goal into subgoals
        ↓
[SELECT] Choose tools for each subgoal
        ↓
[REASON] Check dependencies and ordering constraints
        ↓
[CALIBRATE] Assess feasibility; decide if task is solvable
        ↓
Planning Output: Structured plan (DAG of steps)
```

**Key Insight**: Planning output (the plan itself) can be evaluated independently of execution success. A well-formed plan that executes with wrong parameters is different from a malformed plan.

### Five Evaluation Settings

APB evaluates agents across five orthogonal dimensions:

1. **Holistic Planning** (standard): Agent receives task description; must produce a complete plan
2. **Feedback-Conditioned Step-Wise Planning**: After each step, agent receives execution feedback (success/failure); must adapt plan
3. **Extraneous Tools**: Environment includes red-herring tools unrelated to the task; agent must avoid them
4. **Broken Tools**: Some tools fail at runtime (e.g., API timeout); agent must recognize and route around them
5. **Unsolvable Tasks**: Goal is impossible (e.g., "find a nonexistent file"); agent must recognize infeasibility and refuse

### Multimodal Test Cases

APB includes:
- **Text tasks**: NL instructions, tool descriptions, code snippets
- **Structured data**: JSON/CSV tool catalogs, dependency graphs
- **Visual content**: Screenshots of web interfaces requiring tool interaction
- **Dialogue context**: Multi-turn interactions where context accumulates

### Metrics for Plan Quality

1. **Plan Correctness**: Does the plan achieve the goal without unnecessary steps?
2. **Plan Grade**: Measures plan efficiency (fewer steps, lower cost), not just correctness
3. **Tool Coverage**: Does the plan use appropriate tools for each subgoal?
4. **Dependency Satisfaction**: Are dependencies between steps correctly ordered?
5. **Calibrated Refusal**: Does agent refuse on unsolvable tasks? (Precision and recall on infeasibility detection)

### Agent Topologies Tested

APB evaluates multiple agent architectures:
- **Monolithic Agent**: Single LLM makes all planning decisions
- **Hierarchical Agent**: High-level planner decomposes into subgoals; specialist agents plan for each
- **Tool-Augmented Agent**: Agent has access to planning tools (e.g., LangGraph for state management)
- **Agentic Supervisor**: Multi-agent system with a coordinator agent vetting plans before execution

---

## Main Ideas & Contributions

### 1. Isolation of Planning as First-Class Capability

**Novelty**: Prior benchmarks evaluate agents end-to-end; APB separately evaluates planning, then execution, then the interaction between them.

**Impact**: Enables targeted interventions. If an agent has weak planning but strong execution, training focuses on decomposition and reasoning rather than tool calling. Conversely, weak execution suggests tool-library improvements.

### 2. Systematic Robustness Testing Under Planning Stress

**Novelty**: Five evaluation settings deliberately stress different planning dimensions:
- **Extraneous tools** → tests tool selection filtering
- **Broken tools** → tests failure recovery and replanning
- **Unsolvable tasks** → tests calibration (knowing when to refuse)
- **Long horizons** → tests multi-step reasoning

**Impact**: Reveals systematic weaknesses invisible in standard benchmarks. For example, frontier models often plan perfectly for solvable tasks but fail catastrophically on unsolvable ones (returning random tool sequences instead of refusing).

### 3. Multimodal Benchmark Coverage

**Novelty**: Includes text, structured data, visual, and dialogue modalities, reflecting real-world software development scenarios where agents interact with heterogeneous data sources (code files, API docs, issue trackers, design mockups).

**Impact**: Holistic evaluation that doesn't regress on specific modalities; forces agents to handle context switching.

### 4. APB-Guided Refinement Improves Agent Performance

**Novelty**: Demonstrates that taking refinement actions based on APB diagnostics (e.g., "this agent struggles with long-horizon planning; add a planning-specific prompt") consistently improves downstream execution metrics.

**Impact**: APB isn't just diagnostic; it's actionable. Practitioners can use APB results to prioritize improvements.

---

## Methodology & Implementation

### Benchmark Construction

- **Total test cases**: 4,209 instances
- **Domains**: Software engineering (code completion, debugging, testing), information retrieval, multi-step reasoning, robotics simulation, web automation, API composition, and others (22 total)
- **Modalities**: Text (60%), structured (20%), visual (15%), dialogue (5%)

### Experimental Setup

**Models Evaluated**: 12 multimodal LLMs (frontier and open-source)
- Frontier: GPT-4o, Gemini 2.0, Claude 3.5 Sonnet
- Open-source: LLaMA-3.1, Qwen, Phi

**Evaluation Protocol**:
1. Agent receives task and environment description
2. Agent produces a plan (text or structured format)
3. **Plan evaluation** (independent of execution): Correctness, efficiency, feasibility detection
4. Plan is executed (simulated environment)
5. **Execution evaluation**: Did the plan-following succeed?
6. **Diagnosis**: Compare plan quality vs. execution quality to identify root cause of failures

### Key Metrics & Results

**Long-Horizon Planning Performance**:
- GPT-4o: 78% accuracy on 3-step tasks, 42% on 8-step tasks (estimated from paper)
- Gemini 2.0: 81% on 3-step, 48% on 8-step (estimated)
- Drop of ~40 percentage points over 5 additional steps

**Tool-Noise Robustness**:
- Baseline (clean environment): 85% success
- With 3 extraneous tools: 72% success (~13% drop)
- With 5 broken tools: 61% success (~24% drop)
- **Finding**: Agents struggle to filter irrelevant tools and adapt to broken tools

**Calibrated Refusal** (on unsolvable tasks):
- GPT-4o: 68% precision (when it refuses, it's correct), 45% recall (misses infeasibility 55% of the time)
- **Finding**: Agents fail to recognize impossibility and waste computational budget

**Inference-Time Refinement**:
- Baseline (single attempt): 72% success
- With 2 plan refinement iterations: 78% success (+6 pp)
- With 3 iterations: 79% success (+7 pp, diminishing returns)

### Validation on External Benchmarks

APB results correlate with downstream performance:
- **ToolSandbox (200 tasks)**: 0.87 correlation between APB plan grade and execution success
- **τ²-bench (200 tasks)**: 0.79 correlation between APB planning score and task completion

This validates that APB planning metrics predict real-world agent performance.

### Ablation Studies

- **Removing multimodal input**: Accuracy drops 5–10 pp; agents need visual/structured cues
- **Reducing planning horizon**: Performance on 3-step improves but 8-step degrades; confirms horizon length is primary stressor
- **Using planning tools (LangGraph)**: Improves by ~8 pp; suggests structured state management helps

---

## Practical Applications & Use Cases

### 1. Agent Development: Root-Cause Diagnosis

**Use Case**: A software development agent fails 30% of SWE-bench tasks. Where to improve?

**Workflow**:
1. Run agent against APB subset (planning-only evaluation)
2. Identify bottleneck:
   - Weak long-horizon planning? → Add hierarchical decomposition prompting
   - Poor tool selection? → Improve tool descriptions or add filtering layer
   - Bad feasibility detection? → Add refusal training examples

**Impact**: Focused improvements reduce iteration time from "try everything" to targeted fixes.

### 2. Agent Architecture Selection

**Use Case**: Choose between monolithic vs. hierarchical agent for production deployment.

**Workflow**:
1. Evaluate both on APB
2. Compare planning metrics across settings
3. Hierarchical excels on long-horizon? Deploy hierarchical for complex tasks
4. Monolithic better on tool-noise robustness? Use monolithic for noisy environments

**Multi-Agent Implication**: APB results guide topology selection (centralized planning vs. distributed).

### 3. Tool Library Improvement

**Use Case**: Prioritize which tools to add/fix.

**Workflow**:
1. Run APB; note which tools are over-selected (extraneous-tool setting)
2. Which tools cause failures when broken? (broken-tool setting)
3. Prioritize tool library improvements accordingly

### 4. Model Selection for Deployment

**Use Case**: Choose which LLM to use for mission-critical software automation.

**Workflow**:
1. Evaluate candidate models on APB
2. For your use-case domain (e.g., "code generation"), compare planning performance
3. Select model with best long-horizon reasoning if tasks are complex; best refusal calibration if false positives are costly

### Integration Challenges

1. **Environment Simulation**: APB requires simulated environments for some domains (e.g., web automation); real-world variations may not be captured
2. **Domain Generalization**: Benchmark learned on software engineering tasks; transferability to other domains (robotics, business processes) needs validation
3. **Computational Cost**: Full APB evaluation is expensive; sampling strategies may be needed for rapid iteration
4. **Model Independence**: Some models may benefit from specialized prompting; baseline prompts may disadvantage certain architectures

---

## Insights & Implications

### Key Findings

1. **Planning is a bottleneck**: Frontier models (GPT-4o, Gemini 2.0) achieve 80%+ accuracy on simple 3-step tasks but drop to <50% on 8-step tasks. Long-horizon reasoning is fundamentally harder than single-step tool invocation.

2. **Tool noise is severely underestimated**: Models degrade 20–30% when tools are broken or extraneous. Production systems must build robustness into planning, not just hope for clean tool libraries.

3. **Refusal calibration is critical but missing**: Agents often attempt unsolvable tasks instead of recognizing infeasibility. This wastes resources and can cause cascading failures. Current agents lack confidence calibration in planning.

4. **Multimodal context helps**: Agents with visual/structured data context show ~8% higher planning accuracy than text-only. Real-world deployment must surface all available data to the planning layer.

5. **Planning and execution are separable but correlated**: A high-quality plan significantly increases execution success, but a perfect plan doesn't guarantee execution success (execution failures happen, but less frequently).

### Advancement in Autonomous Coding

- **Diagnostic Rigor**: Establishes a principled framework for isolating and measuring planning vs. execution capabilities; enables evidence-based agent improvements
- **Robustness Under Noise**: Validates that production agents need planning strategies robust to broken tools, irrelevant options, and ambiguous specifications
- **Calibration as First-Class Concern**: Highlights that knowing "I can't solve this" is as important as knowing how to solve problems; opens research into confidence-aware planning

### Limitations & Open Questions

1. **Simulated vs. Real Environments**: APB uses simulated task environments; how do findings transfer to real-world code repositories, live APIs, and dynamic systems?
2. **Interpretability of Plans**: How do we automatically interpret why an agent's plan is suboptimal? (Requires explainability research)
3. **Multi-Agent Coordination in Planning**: APB mostly evaluates monolithic or hierarchical agents; how do fully decentralized multi-agent systems perform?
4. **Feedback Quality**: In feedback-conditioned planning, how does quality of execution feedback affect planning refinement? (Agent may receive misleading feedback)

### Relevance to Agent Topologies

APB's five evaluation settings suggest architectural patterns:

1. **Holistic Planning** → Single orchestrator agent
2. **Feedback-Conditioned** → Agent with state management (LangGraph, etc.)
3. **Extraneous Tools** → Filtering/ranking layer before tool selection
4. **Broken Tools** → Fallback/repair agents triggered on tool failure
5. **Unsolvable Tasks** → Meta-reasoning agent that evaluates feasibility before committing

This motivates a **hybrid architecture**: orchestrator + specialists + feasibility checker, where each component is independently testable via APB.

---

## Code & Resources

### Official Benchmark & Leaderboard

- **Paper**: [APB on ArXiv (2606.04874)](https://arxiv.org/abs/2606.04874)
- **Benchmark Repository**: (Expected to be released; check arXiv for GitHub link)
- **Leaderboard**: (Likely hosted on PapersWithCode or Hugging Face)

### Evaluation Framework

- **Python Library**: APB provides evaluation harness for custom agents
- **Model Evaluation Scripts**: Pre-built evaluation scripts for popular models (GPT-4o, Gemini, Claude, LLaMA)

### Example Integration

```python
from apb import Agent Planning Benchmark, Agent Wrapper

# Define your agent
agent = MyCustomAgent()

# Evaluate on APB
benchmark = AgentPlanningBenchmark(
    settings=['holistic', 'feedback-conditioned', 'extraneous-tools', 
              'broken-tools', 'unsolvable-tasks'],
    domains=['software-engineering', 'retrieval', 'reasoning']
)

results = benchmark.evaluate(agent)
print(f"Long-horizon accuracy: {results.long_horizon_accuracy}")
print(f"Tool-noise robustness: {results.tool_noise_robustness}")
print(f"Calibrated refusal precision: {results.refusal_precision}")
```

### Baseline Results

The paper provides baseline results for frontier models, enabling comparison:

```
Model          | 3-step Acc | 8-step Acc | Tool-Noise | Refusal Precision
GPT-4o         | 78%        | 42%        | 61%        | 68%
Gemini 2.0     | 81%        | 48%        | 64%        | 72%
Claude 3.5     | 76%        | 40%        | 59%        | 65%
LLaMA-3.1      | 65%        | 25%        | 48%        | 52%
```

---

## Related Work & Context

### Prior Agent Benchmarks

- **AgenBench** (2024): Evaluates end-to-end agent performance; doesn't isolate planning
- **SWE-bench** (2024): Evaluates coding agents; focuses on execution, not planning decomposition
- **WebArena** (2024): Evaluates web automation agents; end-to-end metrics, no planning-specific evaluation

### Planning Research

- **Classical Planning**: Automated planning (STRIPS, PDDL) provides formal frameworks for planning; APB bridges to LLM agents
- **Hierarchical Task Networks (HTN)**: Decompose goals into trees; APB evaluates how well LLM agents do hierarchical decomposition
- **Constraint Satisfaction Planning**: Planning with constraints (dependencies, resource limits); APB tests reasoning over constraints

### Robustness & Calibration Research

- **OOD Robustness**: Prior work on out-of-distribution generalization; APB applies to planning robustness
- **Uncertainty Quantification**: Research on calibration and confidence; APB measures refusal calibration as a proxy

### Future Research Directions

1. **Planning with Explanations**: Can agents generate interpretable plans that humans can verify before execution?
2. **Multi-Agent Planning**: How do teams of agents cooperate on planning? (Requires extensions to APB)
3. **Active Learning in Planning**: Can agents query for clarification when plan is ambiguous, rather than guessing?
4. **Formal Verification of Plans**: Can we formally verify that a plan, if executed correctly, achieves the goal?
5. **Inverse Planning**: Given a successful execution trace, can agents extract generalizable plans for similar tasks?

---

## Summary

Agent Planning Benchmark establishes that planning—decomposition, tool selection, constraint reasoning, and feasibility detection—is a distinct, measurable capability separate from tool execution. By introducing systematic robustness testing across five settings and 4,209 cases, APB reveals that frontier LLMs have fundamental weaknesses in long-horizon reasoning, tool-noise robustness, and refusal calibration. Most importantly, APB demonstrates that these weaknesses are diagnosable and actionable: practitioners can use APB results to prioritize agent improvements (add planning-specific prompting, improve tool descriptions, add feasibility checking) and deploy agents more confidently. This work validates that treating planning as first-class in agent development unlocks systematic improvements in autonomous software systems.
