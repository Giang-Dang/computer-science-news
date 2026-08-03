# AgentDebugX: An Open-Source Toolkit for Failure Observability, Attribution, and Recovery in LLM Agents

**ArXiv ID:** 2607.18754  
**Authors:** Kunlun Zhu, Xuyan Ye, Zhiguang Han, Yuchen Zhao, Bingxuan Li, Weijia Zhang, Muxin Tian, Xiangru Tang, Pan Lu, James Zou, Jiaxuan You, Heng Ji  
**Institutions:** University of Illinois Urbana-Champaign, University of Toronto, Google, Stanford University  
**Submission Date:** July 21, 2026  
**Status:** Open-source toolkit

---

## Executive Summary

AgentDebugX is a comprehensive debugging framework that addresses a critical gap in LLM agent reliability: the challenge of diagnosing and recovering from failures that manifest far from their root causes. The toolkit implements a closed-loop debugging cycle (Detect-Attribute-Recover-Rerun) with a core multi-turn diagnosis engine (DeepDebug) that achieves 28.8% root-cause attribution accuracy and repairs 13 out of 73 failed tasks in benchmarks. This work is foundational for enabling production-grade LLM agent systems by providing systematic observability infrastructure.

---

## Problem Statement

LLM agent failures present a unique debugging challenge distinct from traditional software systems:

1. **Root Cause Localization Problem:** Execution errors frequently manifest steps or turns after their origin. When an agent fails at step N, the actual failure might have originated from step 3 due to cascading effects through the reasoning trajectory.

2. **Error Attribution Difficulty:** Existing tools offer trace replay capabilities but lack mechanisms to identify which component in the agent's pipeline (memory, reasoning, tool invocation, environment model) caused the failure.

3. **Gap Between Diagnosis and Recovery:** Knowing that an error occurred and knowing how to recover from it are separate challenges. Current debugging tools focus on the former but provide little guidance on the latter.

4. **Production Observability Gap:** LLM agent frameworks lack the instrumentation and closed-loop feedback mechanisms necessary for operational reliability, in contrast to traditional software systems where crashes serve as reliable failure signals.

---

## Core Concepts & Theory

### Debugging as a Closed-Loop Process

AgentDebugX organizes agent debugging as a four-phase cycle:

```
Detect → Attribute → Recover → Rerun
  ↑_____________________↓
```

**Phase 1 - Detect:** Identifies the step or turn in an agent's execution trajectory where observable failure occurs (exception, unexpected output, blocked action).

**Phase 2 - Attribute:** Traces backward through the trajectory to identify the root cause—the agent decision, memory state, or tool call that initiated the failure cascade.

**Phase 3 - Recover:** Proposes ranked fixes based on the diagnosed root cause, considering multiple remediation strategies.

**Phase 4 - Rerun:** Re-executes the agent trajectory with the proposed fix, regenerating outputs from the recovery point forward to validate the fix.

### Multi-Turn Root-Cause Diagnosis (DeepDebug)

The core innovation is DeepDebug, which performs attribution through three complementary strategies:

1. **Global Trajectory Understanding:** Analyzes the complete execution history rather than isolated steps, recognizing that agent failures are emergent properties of sequential decisions.

2. **Structure-Guided Investigation:** Leverages the structural properties of agent systems (distinct reasoning, action, reflection phases) to guide diagnostic queries, focusing investigation on components most likely to be causal.

3. **Cross-Examination:** Performs multi-turn questioning to triangulate the root cause, asking the model to explain why certain decisions were made and how alternative paths might have prevented the failure.

### Error Taxonomy and Classification

AgentDebugX introduces a failure-mode taxonomy categorizing agent errors into:

- **Memory Errors:** Loss or corruption of context, forgotten state, hallucinated history
- **Reflection Errors:** Incorrect self-assessment, failure to recognize mistakes, flawed post-hoc analysis
- **Planning Errors:** Goal misalignment, suboptimal decomposition, constraint violations
- **Action Errors:** Incorrect API invocation, parameter mismatches, sequencing violations
- **System-Level Errors:** Environment model mismatches, permission issues, resource exhaustion

This taxonomy enables systematic classification of agent failures and supports building institutional knowledge of failure patterns.

### Error Hub: Shareable Failure Knowledge

A key architectural component is the Error Hub—a cross-team corpus of diagnosed failures and associated fixes. This enables:

- Accumulation of organizational knowledge about agent failure modes
- Cross-team sharing of diagnostic patterns (with privacy controls for scrubbing sensitive data)
- Detection of recurring failure patterns across different agent deployments
- Machine learning on failure-diagnosis-repair bundles for automated recovery

---

## Main Ideas & Contributions

### 1. Closed-Loop Debugging Framework

The core contribution is formalizing agent debugging as an integrated cycle where diagnosis directly informs recovery, and recovery outcomes feed back into the knowledge base.

**Key Innovation:** Rather than treating debugging as a post-hoc inspection tool, AgentDebugX makes debugging an integral part of agent execution, enabling both human engineers and autonomous agents to learn from failures.

### 2. DeepDebug Multi-Turn Diagnosis Engine

A sophisticated diagnosis system that moves beyond simple trace analysis to multi-turn reasoning about root causes.

**Key Innovation:** Using the agent's own reasoning capabilities to diagnose agent failures creates a meta-level loop where agents help debug agents, improving both immediate recovery and long-term learning.

### 3. Error Taxonomy and Fault Localization

Systematic classification of agent failure modes enables targeted debugging strategies and prevents treatment of symptoms rather than root causes.

**Key Innovation:** The taxonomy grounds debugging in the actual architectural components of LLM agents (memory, reasoning, planning) rather than generic software error categories.

### 4. Multiple Interface Abstractions

AgentDebugX provides debugging access through multiple interfaces:

- **Python Library:** Programmatic access for integration into agent frameworks
- **Command-Line Interface:** "ingest / diagnose / inspect / act" workflow for interactive debugging
- **Web Console:** Visual debugging interface for examining trajectories and diagnostic reasoning
- **Agentic Skill:** Debuggable as an autonomous capability that agents can invoke on themselves

**Key Innovation:** Enabling agents to self-debug through an agentic skill creates opportunities for autonomous error recovery and continuous improvement.

### 5. Error Hub for Institutional Knowledge

A shareable corpus of diagnosed failures and solutions enables cross-team learning and pattern recognition at scale.

**Key Innovation:** Treating failure data as a valuable organizational asset (with privacy protections) accelerates learning across multiple agent deployments and teams.

---

## Methodology & Implementation

### Detect Phase

The detection phase identifies observable failures in agent execution:

1. **Exception Capture:** Standard try-catch mechanisms capture runtime exceptions
2. **Behavioral Anomaly Detection:** Recognizes non-exception failures (unexpected outputs, state inconsistencies)
3. **Step-Level Indexing:** Marks the specific step in the execution trajectory where failure became observable

**Implementation:** Integrated with popular agent frameworks (LangChain, LlamaIndex, etc.) through instrumentation hooks.

### Attribute Phase

The attribution phase performs root-cause localization:

1. **Multi-Turn Diagnosis:** DeepDebug engages in multiple turns of questioning, iteratively refining the hypothesized root cause
2. **Trajectory Segmentation:** Divides the execution history into logical phases to focus investigation
3. **Cross-Examination:** Asks targeted questions about decision points, assumptions, and alternative paths

**Algorithm Sketch:**
```
diagnosis_state = {}
trajectory = agent_execution_history
for turn in range(max_turns):
    question = generate_diagnostic_question(trajectory, diagnosis_state)
    response = model(question)
    diagnosis_state = update_diagnosis(response)
    if confidence(diagnosis_state) > threshold:
        break
return root_cause_attribution(diagnosis_state)
```

### Recover Phase

The recovery phase proposes fixes based on diagnosed root causes:

1. **Recovery Strategy Generation:** Based on the error type and root cause, generates candidate fixes
2. **Ranking:** Prioritizes fixes by likelihood of success and implementation cost
3. **Fix Validation:** Checks proposed fixes for semantic validity before recommending to users

**Recovery Strategies by Error Type:**
- Memory Errors: Refresh context, inject corrected state, rebuild memory
- Planning Errors: Revise goal decomposition, relax constraints, restart planning
- Action Errors: Correct API invocations, fix parameter types, reorder operations
- System-Level Errors: Adjust environment model, request elevated permissions, allocate additional resources

### Rerun Phase

The rerun phase validates fixes by re-executing the agent trajectory:

1. **Trajectory Truncation:** Re-executes from the recovery point forward
2. **Output Validation:** Checks whether the fixed trajectory achieves the original goal
3. **Feedback Recording:** Captures both successful and unsuccessful recovery attempts in the Error Hub

### Experimental Setup

**Benchmarks Used:**
- **Who & When Benchmark:** Attribution accuracy benchmark designed to test root-cause localization
- **GAIA Benchmark:** General-purpose agent task completion with measured recovery rates

**Models Evaluated:**
- Qwen3.5-9B (lightweight, deployment-friendly)
- Larger models for comparative analysis

**Evaluation Methodology:**
- Measure strict agent-and-step attribution accuracy (did the diagnosis correctly identify root cause and step?)
- Measure repair success rates (did the proposed recovery fix the problem?)
- Compare against self-correction and other baseline approaches

---

## Results and Evaluation

### Quantitative Results

#### Root-Cause Attribution Performance

| Benchmark | Metric | AgentDebugX (Qwen3.5-9B) | Best Baseline | Improvement |
|-----------|--------|------------------------|---------------|------------|
| Who & When | Strict Agent-and-Step Accuracy | 28.8% | 21.7% | +7.1pp |
| Who & When | Root-Cause Accuracy | 42.1% | 35.4% | +6.7pp |

#### Task Repair Performance on GAIA

| Scenario | AgentDebugX | Self-Correction Baseline | Improvement |
|----------|------------|------------------------|------------|
| Failed Task Repairs (Single Rerun) | 13 of 73 tasks | 4-6 tasks | 2.2x - 3.25x |
| Overall Accuracy Before Repair | 55.8% | 55.8% | Baseline |
| Overall Accuracy After Repair | 63.6% | 59.2% | +4.4pp |
| Net Accuracy Gain | +7.8pp | +3.4pp | +4.4pp improvement |

### Qualitative Analysis

The paper includes case studies demonstrating typical failure patterns and how AgentDebugX handles them:

1. **Memory Degradation Case:** Agent correctly reasons through steps 1-3 but gradually loses context, causing step 5 to use outdated information. DeepDebug attributes to step 4's inadequate context refreshing.

2. **Planning Mismatch Case:** Agent's high-level plan assumes tool X is available, but tool invocation fails in step 7. Root cause identified in step 2's faulty environment model assumption.

3. **Action Sequencing Case:** Agent invokes correct operations but in wrong order, causing state inconsistency. Diagnosed as planning error in step 3 rather than action error in step 7.

### Insights from Error Analysis

- **Latency Between Failure Origin and Manifestation:** On average, root causes occur 3.2 steps before the failure is observable, highlighting why naive trace-based debugging is insufficient.

- **Memory and Planning Errors Dominate:** Across the benchmark, memory-related and planning-related errors account for 68% of failures, suggesting these are the highest-value targets for improvement.

- **Cascading Failure Chains:** Single errors often cause multiple downstream failures. Fixing the root cause stops the entire cascade.

---

## Practical Applications & Use Cases

### 1. Production Agent Debugging and Incident Response

When an LLM agent deployed in production encounters a failure:

1. The Detect phase captures the error and full trajectory
2. The Attribute phase runs automatically, generating a diagnostic report
3. Engineers review the diagnosis and approve or modify proposed fixes
4. The Recover phase generates candidate repairs
5. The Rerun phase validates the fix on historical data

**Impact:** Reduce mean-time-to-recovery (MTTR) for agent failures from hours to minutes.

### 2. Continuous Error Learning and Improvement

The Error Hub accumulates diagnosed failures across all agent deployments:

1. Pattern recognition identifies recurring failure types
2. Extracted patterns feed into agent training and prompt engineering
3. Organization learns systematic responses to common failure modes

**Impact:** Build institutional knowledge of agent failure modes and recovery strategies.

### 3. Agent Self-Healing and Autonomous Recovery

By exposing debugging as an agentic skill, agents can self-diagnose and attempt recovery:

1. Agent detects its own failure (via validation checks)
2. Invokes AgentDebugX as a tool/skill
3. Receives diagnosis and proposed fixes
4. Attempts recovery and validates success
5. Reports results for human oversight

**Impact:** Agents become more robust and resilient without requiring human intervention for every failure.

### 4. Multi-Agent Debugging and Coordination Issues

In multi-agent systems, failures in one agent can cascade through the system. AgentDebugX can:

1. Identify whether failure is in agent A or caused by incorrect input from agent B
2. Trace responsibility chains through multi-agent workflows
3. Diagnose coordination issues in agent teams

**Impact:** Enable debugging of complex multi-agent workflows by identifying precisely which agent or interaction caused the failure.

### 5. Agent Framework Development and Testing

Framework developers use AgentDebugX to:

1. Understand how framework features contribute to agent failures
2. Identify framework bugs vs application bugs
3. Improve framework design based on failure patterns

**Impact:** Improve agent framework quality by grounding development in real failure data.

---

## Insights & Implications

### 1. Debugging is Distinct from Error Correction

AgentDebugX's innovation is not in proposing fixes, but in reliably identifying root causes. This separation of concerns means:

- Diagnosis infrastructure can be independent of recovery mechanisms
- Multiple recovery strategies can be applied to the same diagnosed root cause
- Diagnosis can inform human decision-making even when automated recovery is not used

**Implication:** Future work can focus on improving diagnosis accuracy and recovery strategy quality independently.

### 2. Failures in LLM Agents Require New Primitives

Traditional software debugging relies on crashes and exception stack traces as failure signals. LLM agents fail silently (producing wrong outputs) or in ways that don't pin to a single line of code.

**Implication:** New debugging paradigms are needed, centered on trajectory analysis rather than crash analysis.

### 3. Agent Failures are Emergent Properties

Because agent decisions cascade through execution, root causes emerge from interaction of multiple decisions rather than single-point failures.

**Implication:** Debugging must operate at the trajectory level (multiple steps) rather than the action level (single step).

### 4. Error Knowledge is Shareable and Reusable

Diagnosed failures and their fixes generalize across different agent deployments and models, enabling organizational learning.

**Implication:** Error Hub infrastructure creates new opportunities for knowledge management and cross-team collaboration in agent systems.

### 5. Self-Debugging Enables Agent Autonomy

By enabling agents to debug themselves, we move toward truly autonomous systems that can improve their own reliability.

**Implication:** Self-improvement mechanisms in agents may outpace human-driven debugging and optimization.

---

## Code & Resources

### Official Repository and Release

- **GitHub:** Open-source toolkit available (check academic repositories and agent framework integrations)
- **Installation:** Python package with pip/conda installation
- **Interfaces:** Python API, CLI, web console, agentic skill

### Dependencies and Requirements

- **Framework Support:** LangChain, LlamaIndex, CrewAI, and other popular agent frameworks
- **Language Model:** Works with both small models (Qwen3.5-9B) and larger models, though accuracy improves with larger models
- **Compute:** Multi-turn diagnosis requires LLM inference capability

### Quick-Start Integration Guide

```python
from agentdebugx import AgentDebugX, DebugSession

# Initialize the debugger
debugger = AgentDebugX()

# Run agent with automatic failure detection
session = debugger.run_agent_with_observability(
    agent=my_agent,
    task=task_description,
    auto_detect_failures=True
)

# If failure occurs, perform diagnosis
if session.failed:
    diagnosis = session.attribute_root_cause()
    fixes = session.generate_recovery_strategies()
    
    # Attempt rerun with best fix
    recovery_result = session.rerun_with_fix(fixes[0])
    
    # Store in Error Hub for organizational learning
    session.publish_to_error_hub(scrub_sensitive=True)
```

### Agentic Skill Usage

```python
# Expose AgentDebugX as a tool agents can invoke
from agentdebugx.skills import DebugSkill

agent_toolkit.add_skill(
    DebugSkill(
        allow_self_invocation=True,
        error_hub_access=True,
        autonomous_recovery=False  # Require human approval
    )
)

# Agents can now call debugging on their own failures:
# "I encountered an error. Let me diagnose it using the debug_agent skill..."
```

---

## Related Work & Context

### Related Papers on Agent Debugging and Reliability

1. **Agent Observability:** Papers addressing logging, tracing, and visualization of agent execution
2. **Error Correction in LLMs:** Prior work on self-correction and feedback mechanisms
3. **Program Synthesis Debugging:** Techniques for understanding why generated programs fail

### Foundational Work

- **Software Debugging:** Traditional debugging techniques (stack traces, breakpoints, interactive debugging)
- **Agent Systems:** Agent architectures, reasoning loops, tool use frameworks
- **Machine Learning Debugging:** Techniques for understanding ML model failures

### Positioning in the Ecosystem

AgentDebugX addresses a critical gap in the agent infrastructure stack:

- **Level 1 (Framework):** LangChain, LlamaIndex provide basic agent execution
- **Level 2 (Testing):** LogicHunter provides framework-level testing and validation
- **Level 3 (Debugging):** AgentDebugX provides runtime debugging and observability
- **Level 4 (Optimization):** Future work on automated agent improvement and self-evolution

### Future Research Directions

1. **Automated Recovery:** Can agents automatically apply fixes without human approval?
2. **Predictive Diagnosis:** Can we diagnose failures before they manifest?
3. **Cross-Agent Debugging:** How do we debug failures in multi-agent systems?
4. **Continuous Improvement:** How can Error Hub data drive automated agent refinement?
5. **Explainability Integration:** Can debugging provide explanations for agent decisions?

---

## Key Takeaways

AgentDebugX represents a paradigm shift in how we approach LLM agent reliability:

- **Systematic Debugging:** Moves from ad-hoc debugging to systematic closed-loop diagnosis and recovery
- **Root-Cause Focus:** Prioritizes identifying why failures happen over documenting that they happened
- **Organizational Learning:** Error Hub enables knowledge accumulation and sharing across teams
- **Autonomous Capability:** By exposing debugging as a skill, enables agents to improve their own reliability
- **Production Ready:** Provides practical tooling for deploying LLM agents in production environments

This work is foundational for enabling a new generation of autonomous, self-improving agent systems in software development and beyond.
