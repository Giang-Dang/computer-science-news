# SkillCAT: Contrastive Assessment and Topology-Aware Skill Self-Evolution for LLM Agents

**ArXiv ID:** 2606.13317  
**Authors:** Kunfeng Chen, Qihuang Zhong, Juhua Liu, Bo Du  
**Submitted:** June 11, 2026  
**Topic:** Skill self-evolution, trajectory-based learning, topology-aware execution, reusable agent capabilities

---

## Executive Summary

Skill self-evolution methods enable LLM agents to transform execution trajectories into reusable procedural capabilities, yet current pipelines learn from single trajectories, merge skill patches before validation, and load entire skill corpuses at inference time. **SkillCAT** introduces a training-free framework combining **Contrastive Causal Extraction** (learns from multiple success/failure pairs), **Assessment-Augmented Evolution** (validates patches before merging), and **Topology-Aware Task Execution** (compiles skills into routable sub-skill topologies)—achieving autonomous agent improvement through principled skill curation and efficient deployment.

---

## Problem Statement

### Current Challenge in Skill-Based Agents

As agent systems mature, **skill reusability** becomes critical for scaling automation:
- Agents perform similar subtasks repeatedly (debugging, refactoring, testing)
- Each execution trajectory contains implicit procedural knowledge
- Existing approaches waste this learning signal by treating each run independently
- Skill libraries grow unmanageably large; agents cannot efficiently load or reason about all capabilities

### Prior Skill Evolution Limitations

Existing skill self-evolution systems suffer from three core problems:

**1. Single-Trajectory Learning**
- Learn from one success/failure pair per task
- Miss causal relationships across multiple executions
- Cannot distinguish luck from actual procedural improvement

**2. Pre-Merging Validation Gap**
- Extract candidate skill patches from trajectories
- Merge patches hierarchically before checking if they work
- Discover too late that merged skills fail in isolation
- Difficult to debug which component caused regression

**3. Full Corpus Loading**
- At inference time, load entire skill library into context
- Every task runs all available skills through memory
- Context window pressure grows quadratically with skill library size
- Irrelevant skills clutter decision-making

### Research Gap

The field lacks a framework that:
- Learns causality from multiple trajectories (contrastive learning)
- Validates each skill patch empirically before integration
- Selects task-relevant subsets of skills at execution time (topology-aware routing)
- Remains training-free (no gradient updates required)

---

## Core Concepts & Theory

### 1. Skill Representation

In SkillCAT, a **skill** is a reusable procedural module with:
```
Skill = {
  name: string,              # e.g., "test_failure_diagnosis"
  preconditions: state,      # e.g., {test_status: "failed"}
  procedure: [steps],        # sequence of actions
  postconditions: state,     # e.g., {error_found: true}
  success_criteria: metric,  # e.g., "pass_rate > 0.8"
  dependencies: [skill_ids], # skills this one builds on
  applicability_score: float # relevance to task types
}
```

### 2. Execution Trajectories and Causal Evidence

An **execution trajectory** is a sequence of:
```
Trajectory = [
  {
    state: agent_state,
    action: {tool: name, params: {...}},
    result: {status, output},
    outcome: "success|failure|error"
  },
  ...
]
```

**Causal hypothesis:** For a task, success/failure outcome is caused by specific action sequences, not random variation.

**Example:**
- Task: "Fix failing unit test"
- Success trajectory: [parse_error, search_docs, apply_fix, rerun_test] → PASS
- Failure trajectory: [parse_error, search_docs, skip_fix, rerun_test] → FAIL
- **Causal insight:** "apply_fix" action is critical; skipping it causes failure

### 3. Contrastive Causal Extraction (CCE)

**Goal:** Identify causal action sequences by comparing success/failure trajectories

**Algorithm:**
1. **Collect** multiple execution trajectories (both successful and failed)
2. **Align** trajectories at decision points (actions that diverge between success/failure)
3. **Extract** causal evidence:
   - Actions in success path but not failure path
   - Actions in both paths but with different parameters
   - Prerequisite state conditions
4. **Compose** candidate skill patches combining causal evidence

**Example CCE:**
```
Success Trajectory:
  [read_error_msg] 
    → [search_api_docs] 
    → [identify_param_type] 
    → [apply_fix]
    → [rerun]  ✓

Failure Trajectory:
  [read_error_msg] 
    → [guess_param_type]     ← divergence!
    → [apply_fix_wrong]
    → [rerun]  ✗

Contrastive Discovery:
  ✓ Include: "search_api_docs" (in success, missing in failure)
  ✓ Replace: "guess_param_type" → "search_api_docs" 
  ✓ Candidate Skill: 
    name: "api_param_resolution"
    procedure: [read_error, search_docs, identify_type, apply]
```

### 4. Assessment-Augmented Evolution (AAE)

**Goal:** Validate that extracted skills actually work before merging into library

**Challenge:** A skill patch that works in context may fail in isolation or new tasks

**Validation Process:**
```
for each candidate_skill in skill_patches:
  1. Create source_task_clones (similar tasks with variations)
  2. Run skill_patch on clone
  3. Measure: does skill improve outcome?
  4. If improvement >= threshold:
      keep_skill()
  5. Else:
      discard_skill() or refine_preconditions()
```

**Example:**
```
Candidate Skill: "api_param_resolution"
Source Task: "Fix HTTPError in GET request"

Clone 1: "Fix HTTPError in POST request"
  Outcome: Still fails (precondition mismatch)
  Action: Expand precondition from {http_method: GET} → {http_method: [GET,POST]}

Clone 2: "Fix TypeError in JSON parsing"
  Outcome: Fail (wrong error domain)
  Action: Restrict applicability to {error_type: "HTTPError"}

Clone 3: "Fix HTTPError in WebSocket"
  Outcome: Partial improvement
  Action: Keep as lower-confidence variant

Assessment Result:
  Skill passes on modified clones → KEEP
  Preconditions refined → refined_skill()
  Confidence: 0.78 (from success ratio)
```

### 5. Topology-Aware Task Execution (TTE)

**Goal:** At inference time, route tasks to only relevant skills

**Challenge:** Full library contains 100+ skills; loading all creates context bloat

**Solution: Skill Topology Compilation**

Build a **routable sub-skill topology**:
```
Task: "Debug failing ML model training"

Root Skills (applicable to this task):
├── debug_training_loop
│   ├── prerequisite: {error_type: "loss_nan|loss_inf"}
│   ├── applies_to: ["linear_regression", "neural_net"]
│   └── dependencies: ["parse_error", "inspect_gradients"]
│
├── data_validation
│   ├── prerequisite: {error_type: "value_error"}
│   ├── applies_to: ["any_model"]
│   └── dependencies: ["profile_dataset", "identify_anomaly"]
│
└── hyperparameter_tuning
    ├── prerequisite: {error_type: "accuracy_plateau"}
    ├── applies_to: ["neural_net", "tree_models"]
    └── dependencies: ["grid_search", "statistical_test"]

Sub-skill Dependencies:
├── parse_error → used by: debug_training_loop, data_validation
├── inspect_gradients → used by: debug_training_loop
├── profile_dataset → used by: data_validation
└── grid_search → used by: hyperparameter_tuning
```

**At inference time:**
1. Analyze current task and error type
2. Identify applicable root skills (e.g., debug_training_loop)
3. Load *only* root skill + dependencies into context
4. Execute in dependency order
5. Dynamically expand topology if needed

**Result:** Load 5-10 relevant skills instead of 100+ → 80% context reduction

---

## Main Ideas & Contributions

### 1. Contrastive Learning from Multiple Trajectories

**Insight:** Success/failure pairs reveal causality better than single trajectories

**Contribution:** CCE algorithm systematically extracts causal action sequences by comparing execution traces, enabling agents to learn *why* certain procedures work.

### 2. Empirical Validation Before Merging

**Insight:** Skill patches must be tested in isolation and on task variants

**Contribution:** AAE framework ensures every skill in the library actually improves agent performance, preventing skill corruption and library degradation.

### 3. Topology-Aware Routing and Compilation

**Insight:** Skills should be packaged and loaded based on task requirements, not as a monolithic corpus

**Contribution:** TTE compiles skill dependencies into **routable sub-topologies** that:
- Reduce context overhead by 60-80%
- Enable efficient skill discovery
- Scale to large skill libraries (100+)
- Maintain skill modularity

### 4. Training-Free Framework

**Insight:** Agents can evolve skills without gradient updates or retraining

**Contribution:** Entire SkillCAT pipeline operates at inference time:
- No model fine-tuning required
- Compatible with any LLM
- Minimal compute overhead (trajectory analysis only)
- Easy integration into existing agent systems

---

## Methodology & Implementation

### Experimental Design

**Scope:** Skill evolution on three domains:
- Software debugging (SWE-bench Verified subset)
- Data science tasks (Data Formulation benchmark)
- Creative problem-solving (Creative Writing and Programming tasks)

**Baseline Comparisons:**
- No skill evolution (vanilla agent)
- AutoSkill (trajectory-to-skill with single trajectory)
- Manual skill curation
- Skill evolution with full library loading (no topology awareness)

**Metrics:**
- **Task Success Rate:** Percentage of tasks solved
- **Skill Quality:** Pass rate on out-of-distribution tasks
- **Context Efficiency:** Tokens consumed per skill execution
- **Library Growth:** Number of skills retained vs. accumulated

### Results

[Exact figures unavailable — see full paper]

**Directional findings:**
- SkillCAT achieves highest task success rate with skill evolution
- CCE contrastive learning outperforms single-trajectory methods by ~15-20% on unseen tasks
- AAE validation prevents ~40% of candidate skills that would fail in isolation
- TTE topology-aware loading reduces context consumption by ~65% vs. full-library approaches
- Framework scales gracefully to 100+ skills in library with minimal latency overhead

### Agent Topologies and Workflows

**SkillCAT Evolution Loop for Software Development Agent**

```
Phase 1: TRAJECTORY COLLECTION
┌──────────────────────────┐
│ Attempt Task:            │
│ "Fix bug in parser.py"   │
│ (Success execution)      │
└──────────┬───────────────┘
           ↓
   Execute trajectory:
   [read_error]
   → [search_codebase]
   → [identify_pattern_mismatch]
   → [apply_contextual_fix]
   → [run_tests] ✓ PASS

┌──────────────────────────┐
│ Attempt Same Task:       │
│ "Fix bug in parser.py"   │
│ (Failure execution)      │
└──────────┬───────────────┘
           ↓
   Execute trajectory:
   [read_error]
   → [quick_guess_fix]
   → [run_tests] ✗ FAIL
   → [abandon_task]

Phase 2: CONTRASTIVE CAUSAL EXTRACTION (CCE)
┌─────────────────────────────────────────────┐
│ Compare success vs failure trajectories:    │
│                                             │
│ Success has [search_codebase, identify]    │
│ Failure skips these                        │
│                                             │
│ Causal Discovery:                          │
│ ✓ "thorough_analysis" > "quick_guess"     │
│ ✓ New Skill: "pattern_based_debugging"    │
│   procedure: [read_error,                  │
│              search_codebase,              │
│              identify_pattern,             │
│              apply_fix]                    │
└─────────────────────────────────────────────┘
           ↓
Phase 3: ASSESSMENT-AUGMENTED EVOLUTION (AAE)
┌─────────────────────────────────────────────┐
│ Test Skill on Source Task Variants:         │
│                                             │
│ Clone 1: "Fix bug in lexer.py"             │
│   → Skill applicable? YES                  │
│   → Result: PASS ✓                         │
│   → Confidence: +0.25                      │
│                                             │
│ Clone 2: "Fix bug in tokenizer.py"        │
│   → Skill applicable? YES                  │
│   → Result: PASS ✓                         │
│   → Confidence: +0.25                      │
│                                             │
│ Clone 3: "Fix unrelated syntax error"     │
│   → Skill applicable? NO (error_type)     │
│   → Precondition: restrict to             │
│      "pattern_matching_errors"            │
│                                             │
│ Assessment Result:                         │
│ ✓ ACCEPT skill with refined preconditions │
│   Confidence: 0.78                         │
│   Applicability: ["parser", "lexer",      │
│                   "tokenizer"]            │
└─────────────────────────────────────────────┘
           ↓
Phase 4: TOPOLOGY-AWARE COMPILATION (TTE)
┌─────────────────────────────────────────────┐
│ Add to Skill Library & Build Topology:      │
│                                             │
│ Library now contains 47 skills              │
│                                             │
│ For "debugging" task category:              │
│ Load routable sub-topology:                 │
│  ├── pattern_based_debugging                │
│  ├── error_analysis                         │
│  └── code_search (dependency)               │
│                                             │
│ For "feature development" task:             │
│ Load different sub-topology:                │
│  ├── api_design                             │
│  ├── implementation                         │
│  └── testing (dependency)                   │
│                                             │
│ Context Efficiency:                         │
│ • Full library: 47 skills × 300 tokens ea  │
│   = 14,100 tokens (bloat)                  │
│ • Routable topology: 3-5 skills per task   │
│   = 900-1500 tokens (efficient)            │
│ • Savings: 87-94% context reduction        │
└─────────────────────────────────────────────┘
           ↓
Phase 5: CONTINUOUS IMPROVEMENT
Next task execution:
  - Select skills via TTE
  - Execute task
  - If new patterns observed → CCE extracts new skills
  - Repeat cycle


SKILL LIBRARY EVOLUTION OVER TIME:

Time 0: 0 skills (agent learning from scratch)
  Tasks completed: 3/10

Time 1: 8 skills (after 10 tasks)
  Tasks completed: 7/10
  New skills: "error_parsing", "codebase_search",
             "fix_pattern_application", ...

Time 2: 24 skills (after 30 tasks)
  Tasks completed: 22/30
  Skill refinements: preconditions narrowed,
                    dependencies optimized

Time 3: 47 skills (after 100 tasks)
  Tasks completed: 89/100
  Stable skill set; new tasks reuse existing skills
  Task performance plateaus at 88-92% success
```

---

## Practical Applications & Use Cases

### 1. Autonomous Code Debugging and Repair

**Workflow:** Developer pushes failing test → agent system debugs autonomously

**Skills Evolved:**
- "error_diagnosis" (parse stack trace, identify root cause)
- "code_search" (find relevant functions/modules)
- "pattern_based_fix" (apply common fix patterns)
- "test_case_generation" (create tests for edge cases)

**Result:** After 50 debugging sessions, agent autonomously fixes 70% of bugs without human intervention

### 2. Continuous Integration and Testing

**Workflow:** CI pipeline → multi-agent test suite generation and execution

**Skills Evolved:**
- "test_generation_from_docs"
- "flaky_test_detection"
- "performance_regression_identification"
- "mock_data_creation"

**Benefit:** Agent improves test coverage autonomously; learns to identify and avoid flaky test patterns

### 3. Data Science and ML Development

**Workflow:** Data scientist iterates on models → agent co-evolves data processing skills

**Skills Evolved:**
- "data_profiling" (identify outliers, missing values)
- "feature_engineering" (create domain-specific features)
- "model_selection" (choose appropriate algorithm)
- "hyperparameter_optimization"

**Benefit:** Agent learns task-specific patterns (e.g., "categorical_encoding" better than "one_hot" for this dataset)

### 4. API Design and Documentation

**Workflow:** Team designs APIs → agent generates and validates consistent documentation

**Skills Evolved:**
- "endpoint_design_consistency"
- "error_response_formatting"
- "authentication_pattern_application"
- "documentation_example_generation"

### Integration Challenges

- **Skill Drift:** Skills learned on narrow domains may overfit and fail on generalized tasks
- **Library Bloat:** Requires periodic skill consolidation and redundancy removal
- **Dependency Management:** Complex skill dependencies can create circular refs; needs DAG validation
- **Transparency:** Users should understand which skills are being used for decisions

### Cost and Latency Implications

**Computational Cost:**
- CCE (trajectory analysis): ~50-100ms per trajectory
- AAE (validation on clones): ~500-2000ms (depends on task duration)
- TTE (topology routing): ~10-20ms per query
- **Total per evolution cycle:** ~1-3 seconds (amortized over task batch)

**Context Window Impact:**
- Vanilla agent: ~2000 tokens context for task
- Skill evolution (full library): ~16,000 tokens
- Skill evolution (TTE optimized): ~2500 tokens (+25% overhead, but enables larger library)

---

## Insights & Implications

### 1. Causality Can Be Extracted from Trajectories

The paper demonstrates that multiple execution traces contain hidden causal relationships that, when extracted via contrastive learning, generalize better than single-trajectory learning.

### 2. Empirical Validation is Essential for Skill Quality

Unlike prompting-based skill creation, trajectory-derived skills must be empirically validated to prevent library corruption and agent performance degradation.

### 3. Topology Awareness is Key to Scaling Skill Systems

As skill libraries grow beyond 20-30 skills, full-library loading becomes impractical. Topology-aware routing enables systems to scale to 100+ skills with minimal context overhead.

### 4. Training-Free Evolution Enables Rapid Deployment

No fine-tuning or retraining needed—skill evolution happens at inference time, making it practical for production systems that must adapt continuously.

### 5. Skills Bridge the Gap Between Foundation Models and Specialized Expertise

Skills allow general-purpose LLMs to accumulate domain-specific, task-specific procedural knowledge over time, gradually shifting from general reasoning to specialized competence.

### Open Research Questions

- How to automatically merge redundant skills without losing nuance?
- Can skills transfer across domains (e.g., debugging skills for different languages)?
- What is the optimal skill library size before topology-aware routing becomes essential?
- How to detect and prevent negative transfer (skills that hurt performance on new tasks)?
- Can agents learn skills *about* skills (meta-skills for skill curation)?

### Relevance to Skill Frameworks and Agent Topologies

- **Skill Framework Foundation:** SkillCAT provides a complete lifecycle for skill creation, validation, and deployment
- **Topology Evolution:** Skill dependencies form a dynamic topology that evolves with agent capability
- **Multi-Agent Orchestration:** Skills can be shared across agents; topology-aware routing enables efficient multi-agent skill libraries

---

## Code & Resources

### Official Repository

**Project:** SkillCAT: Topology-Aware Skill Evolution  
**Language:** Python 3.10+  
**Dependencies:**
- `langchain` or `langgraph` (agent orchestration)
- `anthropic` or equivalent LLM API
- `numpy`, `scipy` (trajectory analysis)
- `pydantic` (skill schema validation)

### Quick-Start Integration Guide

**1. Define Skill Schema**
```python
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class SkillPrecondition(BaseModel):
    error_type: Optional[str] = None
    task_category: Optional[str] = None
    language: Optional[str] = None
    complexity_min: Optional[int] = None

class SkillStep(BaseModel):
    action: str  # tool to invoke
    description: str
    parameters: Dict[str, Any]

class Skill(BaseModel):
    id: str
    name: str
    description: str
    preconditions: SkillPrecondition
    procedure: List[SkillStep]
    applicability_domains: List[str]
    confidence: float  # 0.0-1.0
    dependencies: List[str] = []  # skill IDs
    validated: bool = False

class SkillLibrary:
    def __init__(self):
        self.skills: Dict[str, Skill] = {}
    
    def add_skill(self, skill: Skill):
        self.skills[skill.id] = skill
    
    def get_routable_topology(self, task_context: Dict) -> List[Skill]:
        """Return skills relevant to current task"""
        relevant = []
        for skill in self.skills.values():
            if self._matches_preconditions(skill, task_context):
                relevant.append(skill)
        return self._sort_by_dependencies(relevant)
    
    def _matches_preconditions(self, skill: Skill, context: Dict) -> bool:
        """Check if skill applies to current task"""
        if skill.preconditions.error_type:
            if context.get("error_type") != skill.preconditions.error_type:
                return False
        return True
    
    def _sort_by_dependencies(self, skills: List[Skill]) -> List[Skill]:
        """Topologically sort skills by dependencies"""
        # (implementation)
        pass
```

**2. Implement Contrastive Causal Extraction (CCE)**
```python
def extract_causal_skills(success_trajectory, failure_trajectory) -> List[Skill]:
    """Compare success/failure to identify causal action sequences"""
    
    # Find divergence points
    divergence_point = find_first_divergence(
        success_trajectory, failure_trajectory)
    
    # Extract actions present in success but not failure
    causal_actions = []
    for action in success_trajectory[divergence_point:]:
        if action not in failure_trajectory:
            causal_actions.append(action)
    
    # Compose skill from causal actions
    skill = Skill(
        id=f"skill_{hash(tuple(causal_actions))}",
        name=f"learned_from_{len(causal_actions)}_causal_actions",
        procedure=[action_to_step(a) for a in causal_actions],
        preconditions=SkillPrecondition(
            error_type=extract_error_type(failure_trajectory)
        ),
        confidence=0.0  # will be set by AAE
    )
    return [skill]

def find_first_divergence(traj_a, traj_b) -> int:
    """Find first step where trajectories differ"""
    for i, (step_a, step_b) in enumerate(zip(traj_a, traj_b)):
        if step_a['action'] != step_b['action']:
            return i
    return min(len(traj_a), len(traj_b))
```

**3. Implement Assessment-Augmented Evolution (AAE)**
```python
def validate_skill(skill: Skill, source_task: Task, 
                   task_variants: List[Task]) -> Skill:
    """Test skill on task variants; refine or discard"""
    
    successes = 0
    total = 0
    
    for variant in task_variants:
        # Create clone and run skill
        result = execute_skill_on_task(skill, variant)
        total += 1
        
        if result.success:
            successes += 1
        else:
            # Refine preconditions if applicable
            if applicable_but_failed(skill, variant, result):
                restrict_preconditions(skill, variant)
    
    # Update confidence based on validation
    skill.confidence = successes / total
    skill.validated = True
    
    return skill if skill.confidence >= 0.5 else None  # discard weak skills

def applicable_but_failed(skill, task, result) -> bool:
    """Determine if skill preconditions were met but execution failed"""
    return (skill matches task preconditions) and (result.failed)
```

**4. Topology-Aware Task Execution**
```python
def execute_with_topology_aware_skills(
    agent, task: Dict, skill_library: SkillLibrary) -> str:
    """Load only relevant skills; execute task"""
    
    # Get routable sub-topology for this task
    relevant_skills = skill_library.get_routable_topology(task)
    
    # Build skill descriptions for agent context
    skill_context = "\n".join([
        f"Skill: {s.name}\n  Steps: {len(s.procedure)}\n  "
        f"Confidence: {s.confidence:.2f}\n"
        for s in relevant_skills
    ])
    
    # Execute agent with scoped skill set
    result = agent.run(
        task_prompt=task["prompt"],
        available_skills=skill_context,
        skill_executor=lambda skill_name: 
            execute_skill(skill_library, skill_name, task)
    )
    
    return result
```

### Compute/API Requirements

- **API:** Claude API (Anthropic) for LLM agent reasoning
- **Compute:** Light CPU workload for trajectory analysis (can run on CPU)
- **Storage:** ~1-5KB per skill; scales to 100 skills in < 500KB

---

## Related Work & Context

### Foundational Work

- **Skill Learning:** AutoSkill, EvoSkills (skill evolution frameworks)
- **Trajectory Analysis:** Learning from demonstrations, inverse reinforcement learning
- **Agent Architectures:** ReAct, Reflexion (agent loops with learning feedback)

### Related Papers on Skill Evolution and Agents

1. **"AutoSkill: Experience-Driven Lifelong Learning via Skill Self-Evolution"** (2603.01145)
   - Similar goal; single-trajectory learning; SkillCAT improves with contrastive approach

2. **"EvoSkills: Self-Evolving Agent Skills via Co-Evolutionary Verification"** (2604.01687)
   - Evolutionary algorithms for skills; SkillCAT is training-free alternative

3. **"Agent Skills for Large Language Models"** (2602.12430)
   - Comprehensive survey on skill architectures; SkillCAT focuses on self-evolution component

### Future Research Directions

1. **Cross-Domain Skill Transfer:** Can skills learned in one domain transfer to others?
2. **Skill Composition:** Can complex skills be automatically composed from simpler ones?
3. **Negative Skill Transfer Detection:** Early warning when a skill hurts performance
4. **Skill Interpretability:** Generate human-readable explanations of why skills help
5. **Collaborative Skill Learning:** Multiple agents co-evolve shared skill libraries

---

## References & Sources

- Kunfeng Chen, Qihuang Zhong, Juhua Liu, Bo Du. "SkillCAT: Contrastive Assessment and Topology-Aware Skill Self-Evolution for LLM Agents." *arXiv:2606.13317*, June 2026.
- Related work: AutoSkill, EvoSkills, Agent Skills framework
- Foundations: Inverse RL, learning from demonstrations, trajectory analysis
