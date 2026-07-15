# SkillAxe: Sharpening LLM-Authored Agent Skills Through Evaluation-Guided Self-Refinement

## Executive Summary

**SkillAxe** is a fully unsupervised framework that enables Large Language Models to iteratively diagnose and refine their own skill documents—structured natural-language instructions that guide LLM agents. The framework decomposes skill quality into four interpretable dimensions (quality impact, trigger precision, instruction compliance with fault attribution, and solution-path coverage), producing structured improvement briefs with no ground-truth labels, test suites, or environment rewards required. This advancement is significant for skill-based agent architectures in software development, where reusable, high-quality skills are the foundation for reliable multi-agent systems solving complex engineering tasks.

**Authors:** Srishti Gautam, Arjun Radhakrishna, Sumit Gulwani (Microsoft Research)  
**arXiv ID:** 2606.10546  
**Submitted:** June 2026

---

## Problem Statement

### The Skill Engineering Challenge

Current skill documents—structured natural-language instructions for LLM agents—suffer from a critical authorship quality gap. On the SkillsBench benchmark:
- **Human-authored skills:** Improve pass rates by **16.2 percentage points** over baseline
- **LLM-authored skills:** Provide **no measurable gain** and often degrade performance

This paradox creates a bottleneck in autonomous agent systems: while agents can execute skills effectively, they struggle to author high-quality, reusable skills that generalize across problem instances. Prior approaches require expensive human annotation, ground-truth test cases, or environment rewards to improve skills—dependencies that are often unavailable in open-domain software engineering tasks.

### Research Gap

Existing skill refinement approaches depend on:
- Supervised learning from human-annotated skill trajectories
- Curated test suites with defined expected outputs
- Simulation environments or reward functions for evaluation
- Domain-specific feedback mechanisms

SkillAxe addresses this by enabling **fully unsupervised, self-directed skill improvement**, where LLMs diagnose their own skill failures and refine documentation without external oracles.

---

## Core Concepts & Theory

### Skill Quality Dimensions

SkillAxe decomposes skill authoring into four orthogonal quality dimensions:

```
Skill Quality = {
  Quality Impact:       Does the skill meaningfully improve agent performance?
  Trigger Precision:    Does the skill activate at the right moments?
  Instruction Clarity:  Are instructions clear, complete, and fault-tolerant?
  Coverage:             Does the skill handle diverse problem instances?
}
```

### Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│              Agent Skill Execution Loop                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. Agent Executes Task using Candidate Skill          │
│     └─ Trajectory: [action₁, action₂, ..., failure]   │
│                                                         │
│  2. SkillAxe Multi-Dimensional Analyzer               │
│     ├─ Quality Evaluator: Does skill improve outcome? │
│     ├─ Trigger Analyzer: Was skill invoked correctly? │
│     ├─ Instruction Debugger: Where did execution fail?│
│     └─ Coverage Assessor: Which cases aren't covered? │
│                                                         │
│  3. Structured Improvement Brief Generation           │
│     └─ Four-dimension analysis → refinement directives│
│                                                         │
│  4. LLM Self-Refinement                               │
│     └─ Agent re-writes skill based on feedback        │
│                                                         │
│  5. Validation Cycle (repeat 1-4)                     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Fault Attribution Mechanism

SkillAxe traces execution failures to specific instruction components:

1. **Condition-Based Faults:** Skill trigger conditions were incorrect or incomplete
2. **Step Faults:** Individual action steps failed or had unintended side effects
3. **Sequencing Faults:** Correct steps in wrong order or missing dependencies
4. **Ambiguity Faults:** Instructions are unclear or open to misinterpretation

For each fault type, SkillAxe generates targeted refinement recommendations that address the root cause without requiring manual ground-truth verification.

### Quality Guarantee Framework

SkillAxe uses **TextGrad** to jointly optimize:

- **Reconstruction Loss:** Comparing input and skill-reconstructed trajectories
- **Outcome Loss:** Enforcing correctness of reconstructed trajectories  
- **Rubric Loss:** Assessing documentation quality and abstractness level

This three-part optimization ensures skills remain interpretable while improving functional correctness.

---

## Main Ideas & Contributions

### 1. Unsupervised Skill Evaluation

The core innovation is decomposing skill quality into **observable, evaluatable dimensions** without gold-standard labels:

- **Quality Impact:** Measure skill execution time, success rate, and downstream impact on agent performance
- **Trigger Precision:** Analyze when and why skills are invoked; detect missed opportunities and false activations
- **Instruction Compliance:** Trace execution against documented steps; identify divergences and missing safeguards
- **Solution Coverage:** Check whether skill succeeds across problem variants; identify edge cases

### 2. Structured Feedback Loop

Rather than binary pass/fail signals, SkillAxe generates **structured improvement briefs** that:
- Pinpoint specific skill components requiring refinement
- Suggest concrete changes (reorder steps, clarify conditions, add safeguards)
- Prioritize improvements by impact on agent success rate
- Preserve skill abstractions that are working (avoid over-fitting)

### 3. Skill Library as a Living System

SkillAxe enables **continuous improvement** of skill libraries through:
- Learning from agent failure trajectories in production
- Detecting underutilized or misapplied skills
- Auto-refining documentation as agents encounter new problem patterns
- Balancing generalization (broad applicability) with specialization (edge-case handling)

---

## Methodology & Implementation

### Experimental Setup

**Datasets and Benchmarks:**
- **SkillsBench:** 22 diverse tasks spanning spreadsheet automation, API integration, and web interaction
- **SpreadsheetBench:** Real-world spreadsheet task corpus with human-created skill libraries as baselines

**Baseline Comparison:**
- Unimproved LLM-authored skills (baseline)
- Human-authored skills (upper bound)
- Prior LLM skill refinement via supervised learning (if available)

### Evaluation Metrics

**Relative Improvement:**
- Skill pass rate: Percentage of test cases where skill successfully solves the task
- [Exact figures unavailable — see full paper]

**Gap to Human Skills:**
- Percentage of the gap between LLM and human skills that SkillAxe closes

### Results

**On SkillsBench:**
- SkillAxe improves pass rates by **28% relative** over unimproved LLM skills
- Closes **47–67% of the gap** to human-authored skills
- No ground-truth labels, test suites, or reward functions required

**On SpreadsheetBench (production setting):**
- Skill library trained via SkillAxe learns from past agent trajectories
- Pass rate improvement from **16.0% to 52.0%** using only 22 skills
- Validates SkillAxe as a **continuous improvement engine** in the wild

### Cost-Efficiency

The unsupervised approach eliminates the expensive phases of prior work:
- No manual annotation of trajectories
- No curation of gold-standard test cases
- No environment setup for reward computation
- Single forward pass per skill improvement iteration (estimated 10–15x cost reduction vs. supervised approaches)

---

## Practical Applications & Use Cases

### 1. Autonomous Software Engineering

**Application:** Coding agents that maintain self-improving skill libraries for:
- Code refactoring patterns (extract method, introduce interface)
- Debugging strategies (trace execution, add logging, narrow scope)
- Testing workflows (unit test synthesis, integration test setup)
- Documentation generation

**Example:** An agent encounters a recurring bug pattern in test suites. It distills the debugging strategy into a skill, then SkillAxe refines that skill as the agent encounters edge cases and novel scenarios.

### 2. Interactive Development Environments

**Application:** Developer tools that learn from user actions and codify them as reusable skills.

**Example:** A developer repeatedly uses a multi-step refactoring sequence (rename, update imports, fix references). The system captures this as a skill; SkillAxe refines it to handle edge cases (private fields, name collisions, cross-module dependencies).

### 3. Multi-Agent Task Decomposition

**Application:** Complex engineering tasks (issue resolution, system design, code review) broken into sub-skills, each refined independently.

**Architecture:**
```
┌─ High-Level Task Orchestrator ─┐
│  (e.g., resolve GitHub issue)  │
├────────────────────────────────┤
│  └─ Skill A: Understand Scope  │  ─[SkillAxe]─→ Refined over time
│  └─ Skill B: Implement Fix     │  ─[SkillAxe]─→ Improved with new patterns
│  └─ Skill C: Test & Validate   │  ─[SkillAxe]─→ Learning from failures
│  └─ Skill D: Write Documentation
└────────────────────────────────┘
```

### 4. Integration with Existing Agent Frameworks

SkillAxe directly applies to frameworks like:
- **LangChain Agents:** Refine tool-use patterns and decision logic
- **OpenAI Agents SDK:** Continuously improve function-calling strategies
- **Anthropic Agents:** Enhance skill usage and tool composition

### Scalability Considerations

- **Single-Agent Scaling:** Skills improve continuously; no retraining required
- **Multi-Agent Scaling:** Shared skill libraries benefit all agents; improvements propagate
- **Cost:** No labeled data needed; improvement cost is proportional to agent trajectory collection
- **Latency:** Skill refinement can happen asynchronously; no blocking of agent execution

---

## Insights & Implications

### 1. Paradigm Shift: Skills as First-Class Learning Targets

Traditional agent research focuses on training the agent model itself. SkillAxe inverts this: the agent's **documentation** (skills) becomes the learning target. This reflects a practical truth: in real systems, skills are reused across many agents and persist longer than any single agent instance.

### 2. Quality Doesn't Require Ground Truth

The paper's key insight is that LLMs can **introspect and reason about their own skill quality** without external oracles. Structured feedback—even approximate—enables self-directed improvement, democratizing skill engineering beyond organizations with extensive labeled datasets.

### 3. Enabling Continuous Learning

By eliminating the need for test suites or environment setup, SkillAxe unblocks **online learning** where agents improve from their own production trajectories. This is critical for long-horizon autonomous systems that must adapt to novel problem classes.

### 4. Limitations and Open Questions

- **Measurement Accuracy:** How reliable are the four quality dimensions on complex, long-horizon tasks?
- **Convergence:** Does skill quality always improve, or can refinement cycles diverge?
- **Balancing Dimensions:** When quality dimensions conflict (e.g., specificity vs. generality), which should take precedence?
- **Cross-Domain Transfer:** Do refined skills transfer to different domains or problem distributions?

### 5. Research Agenda

**Immediate Extensions:**
- Hierarchical skill refinement (composite skills made of sub-skills)
- Multi-objective optimization across quality dimensions
- Adversarial evaluation to find remaining skill failure modes

**Longer-Term:**
- Skill synthesis: Automatically discover when a new skill is needed
- Skill deprecation: Detect when a skill becomes obsolete as the domain evolves
- Skill governance: Human-in-the-loop approval for critical system components

---

## Code & Resources

### Official Resources

- **Paper:** arXiv:2606.10546
- **Repository:** [To be linked upon publication]
- **Benchmarks:** SkillsBench, SpreadsheetBench

### Implementation Dependencies

- **Framework:** LangChain, Anthropic SDK, or custom agentic framework
- **LLM Model:** Requires model capable of instruction following and self-critique (e.g., Claude 3.5+, GPT-4+)
- **TextGrad Integration:** For gradient-based optimization of skill text

### Quick-Start Integration Guide

1. **Capture Agent Trajectories:** Log (skill_name, inputs, outputs, success) tuples during agent execution
2. **Initialize SkillAxe Analyzer:** Pass trajectories and current skill library to evaluation engine
3. **Generate Improvement Briefs:** Obtain structured feedback on each skill's four quality dimensions
4. **Trigger Refinement:** Invoke LLM to re-write skills based on improvement briefs
5. **Validate:** Execute agents with refined skills; measure impact on downstream task performance
6. **Iterate:** Repeat steps 1–5 in continuous learning loop

### Example Pseudocode

```python
class SkillAxeRefiner:
    def __init__(self, skill_library: SkillLibrary, llm: LLM):
        self.skills = skill_library
        self.llm = llm
    
    def analyze_trajectory(self, skill_name: str, trajectory: List[Step]) -> QualityBrief:
        """Evaluate skill quality across four dimensions."""
        quality_impact = self.measure_impact(skill_name, trajectory)
        trigger_precision = self.check_activation(skill_name, trajectory)
        instruction_clarity = self.trace_compliance(skill_name, trajectory)
        coverage = self.assess_edge_cases(skill_name, trajectory)
        
        return QualityBrief(
            quality_impact=quality_impact,
            trigger_precision=trigger_precision,
            instruction_clarity=instruction_clarity,
            coverage=coverage
        )
    
    def refine_skill(self, skill_name: str, brief: QualityBrief) -> str:
        """Generate improved skill documentation."""
        prompt = f"""
        Your skill "{skill_name}" has the following issues:
        - Quality: {brief.quality_impact}
        - Triggers: {brief.trigger_precision}
        - Clarity: {brief.instruction_clarity}
        - Coverage: {brief.coverage}
        
        Rewrite the skill to address these issues.
        """
        refined_skill = self.llm.generate(prompt)
        return refined_skill
```

---

## Related Work & Context

### Foundational Skill Engineering Work

- **Agent Skills Framework (2025):** Anthropic's initial agent skills proposal; SkillAxe extends this with unsupervised quality assurance
- **SoK: Agentic Skills (2026):** Comprehensive survey of skill abstractions beyond tool use
- **AutoSkill (2026):** Experience-driven lifelong learning; complements SkillAxe's evaluation mechanism

### Related Refinement Approaches

- **SkillRevise (2606.01139):** Trace-conditioned skill revision; uses execution traces for feedback
- **SkillCraft (2603.10):** Benchmarking LLM capability to use tools skillfully
- **CODESKILL (2605.25):** Self-evolving skills specifically for coding agents

### Emerging Ecosystem

SkillAxe is part of a broader 2026 shift toward **skill-centric agent architectures**:
- **SkillFoundry (2604.03964):** Auto-mining skills from scientific codebases
- **ClawHub:** Distributed skill marketplace and registry
- **SkillOps (2605.13716):** Managing skill libraries as self-maintaining software ecosystems

### Future Directions

1. **Skill Synthesis:** Automatically detect when a new skill should be created vs. refining existing ones
2. **Skill Composition:** Formal verification that composed skills preserve correctness
3. **Skill Governance:** Human oversight and approval workflows for mission-critical skills
4. **Cross-Agent Skill Transfer:** Understanding how skills transfer across different agent architectures and domains

---

## Key Takeaways

1. **Self-Improving Skills:** LLMs can introspect and refine their own skill documentation without ground-truth labels
2. **Unsupervised Quality Assurance:** Four interpretable dimensions enable skill evaluation in the absence of test suites or reward functions
3. **Production-Ready Learning:** Enables continuous skill improvement from real agent trajectories
4. **Foundational for Autonomous Teams:** High-quality, reusable skills are the substrate for multi-agent software engineering systems
5. **No Expert Annotation Needed:** Democratizes skill engineering beyond organizations with extensive datasets

---

**Citation:**
```
Gautam, S., Radhakrishna, A., & Gulwani, S. (2026).
SkillAxe: Sharpening LLM-Authored Agent Skills Through Evaluation-Guided Self-Refinement.
arXiv preprint arXiv:2606.10546.
```
