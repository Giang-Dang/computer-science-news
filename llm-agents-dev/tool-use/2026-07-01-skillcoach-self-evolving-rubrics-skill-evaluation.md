# SkillCoach: Self-Evolving Rubrics for Evaluating and Enhancing Agentic Skill-Use

**Authors:** HKUST(GZ) and JD.COM researchers  
**ArXiv ID:** 2607.01874  
**Submission Date:** July 1, 2026  
**Paper Link:** https://arxiv.org/abs/2607.01874

---

## Executive Summary

SkillCoach addresses a critical gap in agent evaluation frameworks by introducing **process-level skill-quality assessment** rather than relying solely on final outcome metrics. The framework evolves per-task rubrics that evaluate four trajectory dimensions—skill selection, skill following, skill composition, and skill-grounded reflection—enabling agents to diagnose and improve their procedural competency in complex, overlapping skill repositories. Empirical results show 2-3x accuracy improvements (8.0→24.0 for Qwen 3.5-4B, 14.0→32.0 for 3.5-9B) when rubric-filtered supervised fine-tuning is applied, making this work essential for building reliable agent systems in production environments where skill libraries are inherently overlapping and reuse is critical.

---

## Problem Statement

### Challenge
In realistic skill repositories, agents face **overlapping skills** that blur decision boundaries. Unlike synthetic benchmarks with cleanly separated tasks, production skill libraries contain:
- Multiple skills solving similar problems with different trade-offs
- Skills that share common subtasks (requiring correct composition)
- Skills with complex preconditions and state dependencies
- Validation steps that must not be skipped

**Existing Gap:** Final-outcome metrics (pass/fail) are too coarse-grained to diagnose skill-use failures. Agents may:
- Select distractor skills (look at skill definitions but pick wrong one)
- Skip required procedural steps
- Compose skill workflows incorrectly (wrong order, missing transitions)
- Omit final validation or sanity checks

This masks the root causes of failures, preventing targeted improvement.

### Research Question
Can fine-grained, process-level assessment rubrics help distinguish between different failure modes and enable more targeted training interventions than binary outcome signals?

---

## Core Concepts & Theory

### Skill-Grounded Rubrics
SkillCoach extends classical educational rubric design to agent evaluation by creating **per-task rubrics** that score trajectories along four distinct dimensions:

1. **Skill Selection:** Did the agent identify and choose the correct skill for this task?
   - Evaluates initial decision-making (not prompt engineering)
   - Distinguishes between "looked at wrong skill" vs. "considered but rejected correct skill"

2. **Skill Following:** Does the agent correctly invoke the selected skill and follow its specification?
   - Traces step-by-step adherence to skill SOP (Standard Operating Procedure)
   - Identifies skipped prerequisites or incorrect parameter binding

3. **Skill Composition:** When multiple skills are chained, are dependencies and handoffs correct?
   - Evaluates data flow between skills (output→input matching)
   - Detects composition errors: wrong order, missing transitions, state inconsistencies

4. **Skill-Grounded Reflection:** Does the agent validate outcomes and reflect on correctness?
   - Checks for sanity checks, error detection, and recovery attempts
   - Distinguishes between blind execution vs. monitoring-aware execution

### Rubric Evolution
Rather than hand-authored rubrics, SkillCoach **automatically derives rubrics from real rollouts**:
- Extract trajectories from curated rollouts (both successes and failures)
- Identify discriminative signal patterns for each dimension
- Evolve rubric scoring functions to maximize predictive power for skill-quality diagnosis

### Theoretical Foundation
Builds on:
- **Educational rubric design:** Criterion-referenced scoring separating process quality from outcome
- **Behavioral cloning + outcome-signal decoupling:** Process quality (rubric) remains independent from final outcome (verifier), preventing outcome-noise from corrupting process learning
- **Trajectory segmentation:** Process breakdown into distinct, independently assessable phases

### Agent Topology Connection
SkillCoach fits into multi-agent skill orchestration as the **per-skill quality-assurance layer**:
```
Task Input
   ↓
[Agent Planner] → decompose into skill calls
   ↓
[Skill Selection Module] ← scores via SkillCoach rubric
   ↓
[Skill Executor] → invoke selected skill
   ↓
[Composition Validator] ← SkillCoach checks transitions
   ↓
[Reflection Module] ← SkillCoach scores self-monitoring
   ↓
[Outcome Verifier] → final pass/fail
```

---

## Main Ideas & Contributions

### 1. Rubric-Based Process Evaluation
**Innovation:** Separates **process quality** (how skills are used) from **outcome quality** (whether task succeeds), allowing:
- Diagnosis of procedural errors even when final verification fails
- Training signals that guide skill-use improvement without waiting for rare positive outcomes
- Interpretable error analysis: "agent picked wrong skill" vs. "agent skipped validation step"

**Why it matters:** In overlapping skill repositories (the real-world norm), outcome-only training conflates multiple failure modes, making it hard to know what to fix.

### 2. Four-Dimensional Trajectory Scoring
Rather than monolithic "quality" score, SkillCoach produces a **4-tuple (selection_score, following_score, composition_score, reflection_score)**, enabling:
- Targeted interventions: "fix skill selection" vs. "fix composition"
- Interpretable diagnostics: which agent capability is breaking down?
- Curriculum learning: train on "easy" dimensions (selection) before "hard" ones (composition)

### 3. Rubric Evolution from Rollouts
**Technical contribution:** Automated rubric derivation rather than hand-authoring:
- Collect rollouts (successes and failures) with curated outcomes
- Extract feature patterns discriminative of skill-use quality
- Evolve scoring functions via supervised learning over trajectory segments
- Result: rubrics that adapt to task-specific skill overlaps

### 4. Rubric-Filtered Supervised Fine-Tuning
**Integration with training pipeline:**
```
Real Rollouts (curated)
   ↓
[Rubric Scorer] → per-trajectory dimension scores
   ↓
[Rubric Filter] → keep only high-quality trajectories
   ↓
[SFT] → train on filtered subset
   ↓
Result: +200% accuracy (from 8% → 24% on Qwen 3.5-4B)
```

The key insight: filtering for skill-use quality during training achieves larger gains than outcome-only filtering, because it removes "accidentally correct" trajectories that use wrong procedures.

---

## Methodology & Implementation

### Experimental Setup
- **Models:** Qwen 3.5-4B, Qwen 3.5-9B
- **Benchmark:** Realistic skill repositories with intentional task-skill overlap
- **Baseline:** Standard supervised fine-tuning (no rubric filtering)
- **Curated rollouts:** Both successes and failures, annotated with ground-truth task labels

### Rubric Construction Pipeline

**Phase 1: Trajectory Extraction**
- Collect rollouts: agent attempts task using skill library
- Segment trajectories into {skill selection → invocation → composition → reflection → outcome}
- Label each segment with ground-truth skill correctness

**Phase 2: Feature Engineering**
- Extract discriminative features for each dimension:
  - **Selection:** attention to correct skill, token positions of skill names, decision logits
  - **Following:** adherence to SOP sequence, parameter correctness, precondition satisfaction
  - **Composition:** output-input type matching, state consistency checks, error propagation
  - **Reflection:** self-monitoring triggers, error detection attempts, recovery attempts

**Phase 3: Rubric Learning**
- Train scoring functions: $\text{score}_i(trajectory_segment) \in [0, 1]$ for $i \in \{\text{select}, \text{follow}, \text{compose}, \text{reflect}\}$
- Use logistic regression or lightweight classifiers to avoid overfitting
- Validate on held-out task-skill pairs to ensure generalization

**Phase 4: Quality Filtering & Training**
- Filter trajectories: keep only those with $\text{average}(score_1, score_2, score_3, score_4) > \tau$ (threshold)
- Apply SFT on filtered subset to produce improved policy

### Datasets & Benchmarks
- Evaluated on **realistic skill repositories** where multiple skills solve the same class of problems
- Tested across 4B and 9B model scales to assess generalization
- Compared against:
  - No filtering (raw outcome-based SFT)
  - Outcome-only filtering (keep only successful rollouts)
  - Rubric-based filtering (proposed)

### Metrics
- **Primary:** Task accuracy (pass@1) on held-out test set
- **Secondary:** 
  - Per-dimension performance (selection accuracy, following accuracy, etc.)
  - Rubric inter-rater reliability (consistency across models)
  - Efficiency: SFT data efficiency (accuracy gain per training example)

### Results

**Main Finding: 2-3x Accuracy Improvements via Rubric-Filtered SFT**

| Model | No Filter | Outcome Filter | Rubric Filter | Gain |
|-------|-----------|--------|-----------|--------|
| Qwen 3.5-4B | 8.0% | 11.0% | 24.0% | +200% |
| Qwen 3.5-9B | 14.0% | 18.0% | 32.0% | +128% |

**Interpretation:**
- Outcome-only filtering achieves modest gains (3pp, 4pp) by removing obviously wrong rollouts
- Rubric filtering nearly 3x larger gains because it removes "accidentally correct" trajectories using wrong procedures
- Suggests most skill-repository confusion involves selecting wrong skill that partially solves task

**Per-Dimension Analysis:**
- Skill selection improves most (+14pp for 4B) → main failure mode in overlapping repositories
- Skill composition improves moderately (+4pp) → occurs less frequently but high impact
- Skill following stable → less error-prone than selection/composition
- Reflection improves (+2pp) → less developed agent capability

**Rubric Quality Metrics:**
- Rubric-difficulty correlation: 0.73 (rubrics correctly identify genuinely hard tasks)
- Cross-model consistency: 0.81 (rubric scores transfer between model sizes)
- Feature importance: skill-selection features dominate (68% weight), composition features secondary (19%)

---

## Practical Applications & Use Cases

### 1. Skill Repository Management
**Scenario:** Enterprise AI system with 50+ overlapping skills (e.g., CRM queries, data extraction, report generation).

**Application:**
- Deploy SkillCoach rubrics to audit agent skill-use quality
- Identify skills being confused with each other
- Merge confusing skills or add disambiguating context
- Result: improve agent reliability without model changes

### 2. Skill Training & Onboarding
**Scenario:** Organization adds new skill to library, agents start selecting wrong skill.

**Application:**
- Use SkillCoach's selection dimension to detect confusion
- Curate hard negative examples (contrasting new skill with confusers)
- Train agent on rubric-filtered trajectories focused on selection
- Result: agent learns distinguishing features faster

### 3. Quality Assurance & Monitoring
**Scenario:** Agent system in production; accuracy drops after new skills added.

**Application:**
- Run SkillCoach on production failures
- Diagnose whether failures are skill-selection, composition, or reflection issues
- Route failures to appropriate remediation:
  - Selection issues → update skill descriptions or add examples
  - Composition issues → add inter-skill dependencies or validation rules
  - Reflection issues → add verifier feedback loops
- Result: targeted debugging rather than retraining entire agent

### 4. Multi-Agent Coordination
**Scenario:** Hierarchical agent system with coordinator selecting specialist agents.

**Application:**
- Coordinator uses SkillCoach rubrics to score its own agent-selection decisions
- Identifies categories of tasks where selection is weak
- Trains coordinator on rubric-filtered trajectories
- Result: improves agent-selection accuracy in hierarchical orchestration

### Scalability & Cost Considerations
- **Rubric computation:** Lightweight (logistic regression per trajectory segment), O(n) in trajectory length
- **Storage:** Rubric models < 1MB each, no model download required at inference
- **Latency:** Rubric scoring ~5-10ms per trajectory (negligible compared to agent execution)
- **Training cost:** Curating rollouts (most expensive) ~2x manual annotation effort; SFT training same cost as baseline

---

## Insights & Implications

### Key Takeaways

1. **Process Matters More Than Outcome in Overlapping Environments**
   - Outcome-only evaluation is insufficient when multiple skills can (partially) solve tasks
   - Fine-grained process assessment reveals hidden failures masked by occasional success
   - Implication: agent evaluation frameworks must decompose trajectories into interpretable dimensions

2. **Skill Selection is the Primary Bottleneck**
   - 68% of rubric discrimination power comes from selection dimension
   - 2x larger gains from fixing selection than fixing composition or reflection
   - Implication: future work should focus on improving skill-selection mechanisms (e.g., skill description design, disambiguation prompts)

3. **Rubric-Filtered Training is Superior to Outcome-Filtered Training**
   - Removing "accidentally correct" trajectories is as important as removing failures
   - Suggests agents learn procedural correctness (when) and outcome optimization (whether) through different mechanisms
   - Implication: training data curation should target process quality, not just outcome

4. **Rubric Evolution Enables Automatic Adaptation**
   - Hand-authored rubrics would be brittle; automated derivation from rollouts is generalizable
   - Rubrics automatically capture task-specific skill overlaps
   - Implication: rubric frameworks can scale to new domains without domain-expert annotation

### Limitations & Open Questions

1. **Rubric Design Space:** Current rubrics focus on procedural correctness; extension to efficiency, safety, or ethical dimensions unexplored
2. **Partial Failures:** Rubrics score full trajectories; fine-grained token-level or step-level diagnosis not yet developed
3. **Cross-Task Transfer:** Rubrics trained on one task category; generalization to new task domains not studied
4. **Multi-Modal Integration:** Current work assumes text-based trajectories; extending to multimodal agent traces (e.g., vision + code) open

### Relevance to Agent-Driven Development

- **For skill frameworks:** SkillCoach provides the per-skill QA infrastructure missing from existing frameworks
- **For agent orchestration:** Rubrics enable feedback-driven coordinator learning in hierarchical multi-agent systems
- **For autonomous coding:** Can be extended to debugging (procedural correctness of agent's reasoning steps) and testing (coverage of edge cases)
- **For prompt engineering:** Rubric dimensions suggest key features of effective skill descriptions (clarity, disambiguation, precondition specification)

---

## Code & Resources

### Official Repository
- **GitHub:** Expected publication linked from ArXiv paper (check arxiv.org/abs/2607.01874 for links)
- **Author Affiliations:** HKUST(GZ) + JD.COM research teams

### Dependencies & Requirements
- **Base LLM:** Qwen 3.5-4B/9B (or other foundation models for evaluation)
- **Skill Library:** Requires domain-specific skill definitions and rollout data
- **Framework Integration:** Designed to integrate with:
  - Agent orchestration frameworks (e.g., LangChain, AutoGen, ALMAS)
  - Skill management systems (e.g., SkillFlow, CODESKILL)
  - LLM fine-tuning stacks (HuggingFace Transformers, vLLM)

### Quick-Start Integration Guide

**Step 1: Collect Rollouts**
```
Agent interacts with skill library on curated tasks
→ capture full trajectories {task, selected_skill, invocation, outcome}
→ annotate ground-truth correct skill for each task
```

**Step 2: Extract Rubric Features**
```python
# Pseudocode
rubrics = learn_rubrics(trajectories=[curated rollouts])
# Returns: {select_rubric, follow_rubric, compose_rubric, reflect_rubric}
```

**Step 3: Score & Filter**
```python
scores = [
    rubrics['select'](trajectory),
    rubrics['follow'](trajectory),
    rubrics['compose'](trajectory),
    rubrics['reflect'](trajectory)
]
quality = mean(scores)
if quality > threshold:
    include_in_training_set(trajectory)
```

**Step 4: Fine-Tune Agent**
```python
sft_dataset = filter_trajectories(all_rollouts, threshold=0.7)
agent = train_sft(base_model, dataset=sft_dataset)
# Expected: 2-3x accuracy improvement over outcome-filtered baseline
```

### Integration with Existing Tools
- **SkillFlow compatible:** Can wrap SkillCoach rubrics as skill-evolution feedback signals
- **ABSTRAL compatible:** Rubric scores can guide automated skill search in multi-agent system design
- **ALMAS compatible:** Deploy rubrics in ALMAS workflow for continuous skill-quality monitoring

---

## Related Work & Context

### Foundational Work on Skill Learning
- **SoK: Agentic Skills -- Beyond Tool Use** (2026-02-24): Defines skill taxonomy; SkillCoach operationalizes skill-quality assessment
- **AutoSkill: Experience-Driven Lifelong Learning** (2026-03-01): Agent learns skills over time; SkillCoach provides per-skill feedback signal
- **CODESKILL: Learning Self-Evolving Skills** (2026-05-25): Skills evolve; SkillCoach provides evolution guidance via rubric feedback

### Related Work on Agent Evaluation
- **Beyond Resolution Rates: Behavioral Drivers of Coding Agent Success** (2026-04-02): Analyzes behavioral failure modes; SkillCoach provides structured diagnosis framework
- **Debugging the Debuggers: Failure-Anchored Structured Recovery** (2026-05-09): Recovery from failures; SkillCoach identifies failure types enabling targeted recovery
- **Agent Skills for Large Language Models: Architecture, Acquisition, Security** (2026-06-11): Comprehensive survey; SkillCoach addresses acquisition & evaluation dimensions

### Related Work on Trajectory Evaluation
- **Code as Agent Harness: Toward Executable, Verifiable, Stateful Agent Systems** (2026-05-18): Emphasizes trajectory verification; SkillCoach formalizes verification rubrics
- **TDD Governance for Multi-Agent Code Generation** (2026-05-27): Uses test-driven development for agent governance; SkillCoach is complementary process-quality assessment

### Future Extensions
1. **Reward Modeling:** Use rubric scores as reward signals for RL-based agent training (complementing SFT approach)
2. **Multi-Agent Rubrics:** Extend to evaluate composition/coordination quality in multi-agent trajectories
3. **Safety & Efficiency Rubrics:** Add dimensions for safe reasoning, computational efficiency, and interpretability
4. **Cross-Domain Transfer:** Study rubric transfer across task domains and skill libraries
5. **Interactive Rubric Design:** Explore human-in-the-loop rubric refinement for specialized domains

---

## References

- ArXiv Paper: https://arxiv.org/abs/2607.01874
- HKUST(GZ) Agentic AI Group
- JD.COM AI Research

---

**Keywords:** skill evaluation, rubrics, multi-agent orchestration, skill repositories, process quality, supervised fine-tuning, agentic skill-use, trajectory assessment

**Citation:**
```bibtex
@article{skillcoach2026,
  title={SkillCoach: Self-Evolving Rubrics for Evaluating and Enhancing Agentic Skill-Use},
  author={[HKUST(GZ) and JD.COM researchers]},
  journal={arXiv preprint arXiv:2607.01874},
  year={2026}
}
```
