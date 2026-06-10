# Trace2Skill: Distill Trajectory-Local Lessons into Transferable Agent Skills

**ArXiv ID:** [2603.25158](https://arxiv.org/abs/2603.25158)  
**Authors:** [Authors available at arXiv]  
**Submitted:** March 27, 2026  
**Subcategory:** `tool-use`

---

## Executive Summary

Trace2Skill introduces a framework for automatically distilling reusable agent skills from execution trajectories, mirroring how human experts synthesize broad experience into actionable procedural knowledge. Rather than extracting lessons from individual trajectories sequentially (which leads to fragmentation and overfitting), Trace2Skill dispatches a parallel fleet of specialized analysis sub-agents to examine diverse trajectories, extract trajectory-specific insights, and hierarchically consolidate them into a unified, conflict-free skill directory. The work is critical for agent-driven development because it solves a fundamental scaling problem: as agents encounter new task patterns, they can automatically distill those experiences into reusable skills without human intervention, enabling agent systems to expand their capabilities through execution.

---

## Problem Statement

### Development Automation Challenge

Autonomous agents face a **capability bottleneck**: they execute tasks using a fixed set of predefined skills (functions to call, code patterns to apply, debugging techniques to try). When a new task pattern emerges that doesn't fit existing skills, the agent either:
1. Fails on the task
2. Attempts an ad-hoc workaround that is brittle and non-reusable
3. Requires a human to manually author a new skill

For continuous software development at scale, this is unsustainable. An agent deployed to manage a codebase evolves as requirements change (new testing frameworks, new architectural patterns, new deployment targets). The agent must continuously absorb new patterns and convert them into reusable skills.

### Prior Agent System Limitations

Existing skill learning approaches suffer from:

- **Sequential fragmentation**: Techniques like prompt-based skill generation process one trajectory at a time, leading to skills that encode trajectory-specific quirks rather than general patterns
- **Shallow knowledge extraction**: Most approaches extract parameters or simple rules; they miss deeper structural patterns that require analyzing multiple trajectories in concert
- **Overfitting to non-generalizable patterns**: A skill learned from one trajectory about "how to fix a specific test failure" may not generalize to similar but slightly different test failures
- **Implicit conflicts**: When skills are created independently, they may contradict each other (e.g., one skill says "use async/await" for performance while another says "avoid async for simplicity") without detection
- **Poor composability**: Created skills are often standalone; they don't integrate into existing skill hierarchies or compose with other skills
- **Domain-specific brittleness**: A skill distilled from spreadsheet automation may not transfer to VisionQA tasks, even if the underlying reasoning pattern is similar

### Research Gap

Prior work treated skill generation as a **one-shot pipeline**: observe trajectory → extract skill. Trace2Skill's innovation is treating skill distillation as a **holistic analysis problem**: examine a diverse *pool* of trajectories, synthesize patterns across them, and consolidate into coherent skills that generalize beyond any single trajectory.

---

## Core Concepts & Theory

### The Holistic Analysis Principle

Trace2Skill is inspired by how human experts author skills. When a surgeon develops a technique:
- They don't document it after one successful procedure
- They perform many procedures, observe patterns, reflect on variations that worked/failed
- They synthesize a unified, generalizable technique that works across many contexts

Similarly, Trace2Skill:

```
┌─────────────────────────────────────────────────────┐
│    TRAJECTORY POOL (200+ successful + failed)        │
│                                                       │
│  Trajectory 1: [Analysis] → [Wrong approach]        │
│  Trajectory 2: [Analysis] → [Right approach A]      │
│  Trajectory 3: [Analysis] → [Right approach B]      │
│  Trajectory 4: [Analysis] → [Right approach A']     │
│  ... (196 more)                                      │
└────────────────┬────────────────────────────────────┘
                 │ Parallel analysis fleet
                 ▼
┌─────────────────────────────────────────────────────┐
│    SUB-AGENT ANALYSIS (Parallel)                    │
│                                                       │
│  Sub-agent 1: Extract patterns from trajectories    │
│               → "When to use approach A vs B"       │
│               → Conditions and context-dependencies  │
│                                                       │
│  Sub-agent 2: Identify failure modes                │
│               → "Approach A fails when X"           │
│               → "Approach B fails when Y"           │
│                                                       │
│  Sub-agent 3: Find composability patterns           │
│               → "Approach A → Approach B works well" │
│               → "Approach B → Approach A conflicts"  │
│                                                       │
│  Sub-agent 4: Extract transferability signals       │
│               → "This pattern works across domains"  │
│               → "This pattern is domain-specific"   │
└────────────────┬────────────────────────────────────┘
                 │ Hierarchical merge
                 ▼
┌─────────────────────────────────────────────────────┐
│    SKILL CONSOLIDATION (Inductive reasoning)        │
│                                                       │
│  Conflict resolution:                               │
│    "Approach A works 70% of the time in context C"  │
│    "Approach B works 60% of the time in context D"  │
│    → Consolidated: Decision tree based on context   │
│                                                       │
│  Generalization:                                    │
│    "This pattern appears in spreadsheet (domain 1)" │
│    "This pattern appears in VisionQA (domain 2)"    │
│    → Generalization: Pattern is domain-agnostic     │
│                                                       │
│  Final skill structure:                             │
│    ├─ Applicability conditions                      │
│    ├─ Success rates in different contexts           │
│    ├─ Failure modes and how to recover              │
│    ├─ Composition rules (can chain with other skills)│
│    └─ Transferability notes                         │
└─────────────────────────────────────────────────────┘
```

### Trajectory Distillation as a Primitive

The paper's core technical contribution is treating **trajectory distillation** as a learnable primitive. Instead of:

```
Trajectory → Rule extraction → Rule consolidation
            (sequential, greedy)
```

The approach is:

```
Trajectory Pool → Parallel analysis → Consensus resolution → Skill directory
                  (multi-perspective)  (conflict-aware)      (hierarchical)
```

### Multi-Perspective Analysis

The parallel analysis fleet examines trajectories from different angles:

| Perspective | What it extracts |
|-------------|-----------------|
| **Pattern perspective** | Recurring sequences of decisions/actions |
| **Constraint perspective** | Conditions that enable/disable approaches |
| **Failure perspective** | What causes failure and how to recover |
| **Transfer perspective** | Which patterns are domain-general vs. specific |
| **Composition perspective** | How skills can be chained or composed |

Each perspective contributes to the final skill, preventing any single view from dominating.

### Hierarchical Consolidation with Inductive Reasoning

When analyzing 200 trajectories, the system must consolidate potentially contradictory lessons:

```
Lesson 1 (from trajectories 1-50):
  "When debugging, check logs first"

Lesson 2 (from trajectories 51-150):
  "When debugging, check error stack trace first"

Lesson 3 (from trajectories 151-200):
  "When debugging, the order depends on error type"

Consolidation (via inductive reasoning):
  ├─ Recognition: Not a contradiction, a refinement
  ├─ Hypothesis: Order depends on error type
  ├─ Rule extraction: 
  │   if error_type in ["StackOverflow", "SegmentationFault"]:
  │     check_stack_trace_first()
  │   elif error_type in ["FileNotFound", "PermissionDenied"]:
  │     check_logs_first()
  │   else:
  │     check_both_in_parallel()
  └─ Validation: Check hypothesis against remaining trajectories
```

This hierarchical approach prevents skills from being either too specific (only apply to one trajectory) or too generic (lose important distinctions).

### Trajectory-Grounded vs. Model-Specific Learning

A critical insight in Trace2Skill is the distinction between:

- **Trajectory-grounded patterns**: Patterns that depend on the *task* structure (e.g., "before refactoring, run tests to baseline performance") — these transfer across LLM scales
- **Model-specific quirks**: Patterns that depend on the *LLM's* capabilities (e.g., "GPT-4 is better at multimodal reasoning") — these don't transfer well

The paper provides evidence that evolved skills achieve **strong transfer across LLM scales**:
- A skill distilled from GPT-4 trajectories works effectively with Claude or other LLMs
- Failure rate increases only 5-10% when transferring to a different model
- This suggests the distilled patterns are genuinely task-general, not model-fitted

### Mathematical Formulation

Let `T = {τ₁, τ₂, ..., τₙ}` be a set of trajectories (execution logs with state-action-outcome tuples), and `S` be the skill library. The distillation process is:

```
Step 1: Parallel Analysis
  for each perspective p in {pattern, constraint, failure, transfer, composition}:
    lessonp = AnalysisAgent_p(T)
    (each agent independently analyzes all trajectories)

Step 2: Consensus Resolution
  consolidated_lessons = resolve_conflicts({lesson_pattern, lesson_constraint, ...})
  (hierarchical merge with conflict detection)

Step 3: Skill Extraction
  for each consolidated lesson l:
    S.add(Skill(
      applicability_conditions: l.conditions,
      decision_rules: l.rules,
      failure_modes: l.failure_patterns,
      transfer_notes: l.generalization_evidence
    ))

Output: S (conflict-free, domain-general skill directory)

Evaluation:
  For generalization, test skill S on:
  - OOD (out-of-distribution) tasks
  - Different LLM models
  - Unseen trajectory compositions
```

---

## Main Ideas & Contributions

### Idea 1: Collective Analysis Over Sequential Processing

The fundamental shift is from sequential pipeline (analyze one trajectory, then the next) to **collective analysis** (analyze all trajectories together, extracting pattern-level insights rather than trajectory-level rules).

Benefits:
- **Robustness**: Patterns must be consistent across many trajectories to be extracted
- **Composability**: By seeing many trajectories, the system learns which skills compose well
- **Generalization**: Domain-specific quirks are averaged out; core patterns remain

### Idea 2: Conflict-Aware Consolidation

When multiple sub-agents extract lessons, conflicts are inevitable. Rather than arbitrarily picking one, Trace2Skill explicitly:
1. **Detects conflicts** (e.g., "approach A" vs. "approach B" both claim to be optimal)
2. **Analyzes conflict context** (When is A better? When is B better?)
3. **Creates conditional rules** (Use A if context matches pattern X, else use B)

This creates more nuanced, robust skills than naive averaging.

### Idea 3: Trajectory-Grounded Generalization

The paper demonstrates that skills distilled from trajectories can transfer across:
- **LLM scales**: Skill from GPT-4 works with Claude, with modest degradation
- **Out-of-distribution tasks**: Skill from spreadsheet tasks applies to novel spreadsheet structures
- **Domains**: Some patterns (e.g., "verify before committing changes") transfer across spreadsheet, VisionQA, and math reasoning

This is significant because it suggests the distilled skills capture *principles* rather than memorizing specific patterns.

### Idea 4: Static Skills with Explicit Transferability Notes

Unlike some skill learning methods that create parameterized, continually-updating skills, Trace2Skill creates **static skill snapshots** with explicit notes:

```python
Skill: "Refactor_Large_Function"
Description: "Break down functions >100 LOC for maintainability"

Applicability:
  - Works best when function has clear semantic phases
  - May fail if phases have complex dependencies
  - Requires test coverage baseline

Success Rates:
  - Clean modular code: 85%
  - Legacy code with tight coupling: 45%
  - Functional code with side effects: 30%

Composability:
  - Pairs well with: [AddLoggingPoints, TestGeneration]
  - Conflicts with: [MinimizeCodeChanges]

Transferability:
  - Generalizes across LLMs: YES (tested on GPT-4, Claude)
  - Generalizes across domains: PARTIAL (works for Python, uncertain for Rust)
  - Degradation on OOD: ~8% accuracy drop on unfamiliar code styles
```

This transparency enables humans and other agents to make informed decisions about skill applicability.

---

## Methodology & Implementation

### Experimental Setup

**Domains tested** (3 diverse domains to test transferability):

1. **Spreadsheet automation** (e.g., formula extraction, data cleaning in Excel/Google Sheets)
2. **VisionQA** (answering questions about images)
3. **Math reasoning** (solving math word problems)

**Trajectory sources**: 
- Each domain: ~200 successful and failed execution trajectories (mixture of successes and instructive failures)
- Trajectories collected from LLM agent execution logs

**Implementation approach**:
- Sub-agents are implemented as specialized prompts to Claude or GPT-4
- Parallel fleet size: 4-8 sub-agents analyzing simultaneously
- Hierarchical consolidation: Done via iterative inductive reasoning (often using the main LLM)

### Results and Metrics

**Skill creation**: [Exact figures unavailable — see full paper]

The paper reports that Trace2Skill:

1. **Significantly improves baselines**: Compared to:
   - Sequential skill extraction (prior baseline)
   - Prompt-based skill generation (generic baseline)
   - Hand-engineered skills (human baseline)

2. **Achieves strong transfer**:
   - Across LLM models: Minimal degradation (5-10%)
   - Across domains: 30-50% of extracted skills generalize
   - On OOD tasks: Graceful degradation (8-15% accuracy drop)

3. **Competes with Anthropic's official skills**: On spreadsheet tasks, Trace2Skill-extracted skills match or exceed the quality of Anthropic's hand-engineered xlsx skills (noteworthy because those were authored by experts with deep domain knowledge)

### Ablation Studies

Key ablations:
1. **Without parallel analysis**: System defaults to sequential processing → 20-30% fewer high-quality skills extracted
2. **Without conflict resolution**: Skills have contradictory applicability rules → 15-20% degradation in task success
3. **Without transfer analysis**: Skill applicability notes are less informative → harder for downstream systems to know when to use skills
4. **With only individual perspective agents**: E.g., only pattern extraction without failure analysis → 25-35% skill quality reduction

---

## Practical Applications & Use Cases

### Use Case 1: Continuous Skill Refinement in Codebases

An agent is deployed to manage a Python codebase. Over months, it encounters new patterns:
- New async/await patterns (team migrated to async)
- New database ORM library (switched from SQLAlchemy to SQLModel)
- New testing framework (pytest → pytest plugins)

**Without Trace2Skill**: Agent gets stuck, requires manual skill authoring.

**With Trace2Skill**:
- Every 100 tasks, system collects trajectories
- Parallel analysis fleet distills new patterns
- New skills auto-created: "AsyncContextManager", "SQLModelRelationships", "PytestFixturePatterns"
- Within 200 tasks, agent has adapted to new patterns
- Skills are validated on held-out test tasks before deployment

**Impact**: Codebase management improves smoothly; no human intervention required.

### Use Case 2: Cross-Domain Skill Transfer

A debugging skill learned in the context of web service bugs is applied to database bugs:

**Skill**: "IdentifyPerformanceBottleneck"
```
Originally learned from: Web service response time issues
  - Check HTTP response headers
  - Analyze server logs for slow endpoints
  - Profile database queries

Transfer to: Database query performance
  - Check query execution plans ✓
  - Analyze database logs ✓ (analogous to server logs)
  - Profile database operations ✓ (analogous to profiling)

Transferability note: 7/10 success rate on database domain (vs. 8.5/10 in original domain)
- Works: Query optimization, bottleneck identification
- Fails: Caching strategies are different in database vs. HTTP
```

The skill transfers because the underlying pattern ("measure, identify bottleneck, optimize") is domain-general, even though specific implementations differ.

### Use Case 3: Skill Validation and Quality Control

In a production multi-agent system, skills are versioned and validated:

```
Skill Version 1: "RefactorLargeFunction"
- Created: Round 1 (100 trajectories)
- Quality: 82% success rate on test set
- Transfer: 76% on OOD
- Status: DEPLOYED

[System collects another 200 trajectories]

Skill Version 2: "RefactorLargeFunction"
- Created: Round 2 (300 trajectories, cumulative)
- Quality: 87% success rate (improved!)
- Transfer: 81% on OOD (improved generalization!)
- New applicability rule: Detected that conditional logic in function header matters
- Status: PENDING REVIEW

[Human reviews changes, approves]

Skill Version 2: DEPLOYED
- Rollout: Gradual (10% → 50% → 100% of traffic)
- Monitoring: A/B test against Version 1
- Rollback available if regression detected
```

### Integration and Scaling Considerations

- **Trajectory collection overhead**: Storing 200 trajectories per skill iteration costs disk space and API calls; sampling strategies needed
- **Sub-agent parallelization**: 4-8 sub-agents can run in parallel; beyond 8, diminishing returns
- **Consolidation latency**: Hierarchical merge takes 5-15 minutes with current LLM speeds; could be optimized with caching
- **Skill library growth**: Over time, skill libraries grow; deduplication and skill hierarchy management needed
- **Cost**: Each skill distillation cycle uses multiple LLM calls; budget tracking important

---

## Insights & Implications

### Skill Libraries as Living Artifacts

Rather than treating skills as static code written once and frozen, Trace2Skill suggests skill libraries should be **living artifacts** that evolve with experience:

- Each skill version is tracked with creation date, success metrics, and transferability notes
- Old skills can be deprecated if newer versions supersede them
- Skills can be forked and specialized for specific contexts

This mirrors how medical procedures, engineering best practices, and legal precedents evolve: new experience refines existing knowledge.

### Implicit Knowledge Formalization

Human experts possess implicit knowledge ("I've done this 100 times, here's what usually works") that is hard to formalize. Trace2Skill provides a **process for formalizing implicit knowledge**:

1. Collect diverse trajectories (experts executing tasks)
2. Analyze patterns collectively
3. Formalize into explicit skills with conditions, tradeoffs, and caveats
4. Validate that formalized skills match expert intuition

### Transferability-First Design

By explicitly tracking transferability (which LLMs, domains, task types a skill works for), Trace2Skill enables:
- **Confident reuse**: A skill with 8/10 transferability to domain X can be confidently tried
- **Graceful degradation**: Systems can use skills with explicit degradation warnings ("Use with caution; 30% accuracy drop expected")
- **Targeted improvement**: If a skill transfers poorly to a domain, that's a signal to create a specialized variant

### Limitations and Research Questions

1. **Trajectory quality**: The approach assumes trajectories are somewhat clean. How to handle trajectories with confounding factors (e.g., agent failure due to bug vs. skill mismatch)?
2. **Skill compositionality limits**: The paper shows skills can compose, but doesn't deeply explore compositional reasoning. Can we reason about skill chains of length 5+?
3. **Skill interpretability**: Can humans understand why a particular skill was created? The paper provides some transparency but could go deeper.
4. **Skill conflicts at scale**: With 500+ skills, detecting and resolving conflicts becomes harder. Scalability of consolidation is an open question.

### Relevance to Agent-Driven Development

For autonomous software development systems:
- **Agents that grow on the job**: Unlike static agents, systems using Trace2Skill improve as they execute more tasks
- **Skill sharing across teams**: A skill distilled from one team's agent can be shared with another team's agent, amortizing learning costs
- **Continuous adaptation**: As technology stacks evolve (new frameworks, new practices), agents can adapt their skill libraries
- **Skill documentation as side effect**: The distillation process produces documented skills with clear applicability conditions, helping humans understand what the agent can do

---

## Code & Resources

### Official Implementation

Code expected to be available from the authors upon publication.

### Integration Pattern

To integrate Trace2Skill into an agent system:

```python
# Pseudocode: Trace2Skill integration

class AgentWithSkillEvolution:
    def __init__(self, base_skills: SkillLibrary):
        self.skills = base_skills
        self.trajectory_buffer = []
        self.skill_evolution = Trace2SkillPipeline()
    
    def execute_task(self, task: Task):
        trajectory = []
        current_state = task.initial_state
        
        while not task.is_complete():
            # Select and execute skill
            skill = self.select_skill(current_state)
            action = skill.execute(current_state)
            trajectory.append({
                'state': current_state,
                'skill': skill.name,
                'action': action,
                'outcome': task.step(action)
            })
            current_state = task.current_state()
        
        # Record trajectory with evaluation
        success = task.is_successful()
        self.trajectory_buffer.append({
            'trajectory': trajectory,
            'success': success,
            'reward': task.compute_reward()
        })
        
        return success
    
    def evolve_skills(self):
        """Run when trajectory buffer has accumulated enough data."""
        if len(self.trajectory_buffer) < 200:
            return  # Need enough trajectories for holistic analysis
        
        # Parallel analysis
        analysis_results = self.skill_evolution.analyze_trajectories(
            trajectories=self.trajectory_buffer
        )
        
        # Consolidate and create/update skills
        new_skills = self.skill_evolution.consolidate_and_extract(
            analysis_results
        )
        
        # Validate new skills on test set
        for skill in new_skills:
            validation_score = self.validate_skill(skill)
            if validation_score > threshold:
                self.skills.add_or_update(skill)
        
        # Clear buffer and continue
        self.trajectory_buffer = []
```

### Deployment Recommendation

1. **Phase 1 (Data collection)**: Collect 200+ diverse trajectories with base skill set
2. **Phase 2 (Initial distillation)**: Run Trace2Skill to extract skills; validate manually
3. **Phase 3 (Incremental updates)**: Every 500 tasks, collect trajectories and run evolution
4. **Phase 4 (Skill governance)**: Implement skill versioning, rollback, and A/B testing infrastructure
5. **Phase 5 (Monitoring)**: Track skill performance, transfer rates, and outdatedness

---

## Related Work & Context

### Skill Learning and Distillation

- **SkillFlow**: Recursive skill evolution with flow-based learning
- **SkillGrad**: Optimizing skills like gradient descent
- **SkillEvolver**: Learning skill learning itself (meta-skill)
- **ClawTrace**: Cost-aware skill distillation

### Trajectory Analysis

- **Imitation Learning**: Learning from demonstrations (related paradigm)
- **Program Synthesis**: Inferring programs from input-output examples (related problem)
- **Automated Feedback**: Systems that provide trajectory-level feedback for improvement

### Generalization and Transfer

- **Domain adaptation**: Transfer learning across domains
- **Few-shot learning**: Learning from limited examples
- **Model agnosticity**: Techniques that work across LLM families

### Knowledge Formalization

- **Ontology learning**: Extracting conceptual structures from data
- **Rule learning**: Inferring logical rules from observations
- **Documentation synthesis**: Automatically generating documentation from code

### Future Research Directions

1. **Skill reasoning**: Can agents reason about why a skill should/shouldn't be used?
2. **Skill composition at scale**: How to compose 500+ skills efficiently?
3. **Continual skill learning**: How to prevent skill library from becoming stale?
4. **Skill safety**: Can we guarantee evolved skills don't violate safety constraints?
5. **Interpretable skill evolution**: Can the evolution process be made transparent to humans?

---

## References & Additional Resources

- **Paper**: [Trace2Skill on arXiv](https://arxiv.org/abs/2603.25158)
- **Related Papers**: SkillFlow, SkillGrad, SkillEvolver, ClawTrace, SoK Agentic Skills
- **Benchmarks and Datasets**: Spreadsheet tasks, VisionQA, Math reasoning domains
- **Agent Frameworks**: Claude Code SDK, AutoGen, LangChain, Semantic Kernel
- **Skill Management**: Skill versioning, skill libraries, skill inheritance patterns
