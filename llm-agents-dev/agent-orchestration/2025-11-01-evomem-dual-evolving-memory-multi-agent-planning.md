# EvoMem: Improving Multi-Agent Planning with Dual-Evolving Memory

**Authors:** [Metadata from arXiv:2511.01912]  
**Submitted:** November 1, 2025  
**ArXiv ID:** [2511.01912](https://arxiv.org/abs/2511.01912)

## Executive Summary

EvoMem introduces a cognitive psychology-inspired multi-agent planning framework built on dual-evolving memory mechanisms. The system decomposes complex planning tasks across three specialized agents (Constraint Extractor, Verifier, Actor) supported by two complementary memory modules: Constraint Memory (CMem) which evolves across queries to store task-specific rules, and Query-feedback Memory (QMem) which evolves within a single query by accumulating iterative refinement feedback. This novel orchestration pattern demonstrates 2-11% performance gains across diverse planning domains including trip planning, calendar scheduling, and meeting coordination, while providing a principled framework for managing agent knowledge and reducing redundant reasoning.

## Problem Statement

### Multi-Agent Planning Challenges

Current multi-agent orchestration systems face fundamental limitations in information management:

1. **Static Knowledge:** Agents either memorize task-specific knowledge once or regenerate it repeatedly across queries, creating inefficiency
2. **Feedback Isolation:** Iterative refinement feedback from one agent cycle is often lost or not leveraged in subsequent attempts
3. **Role Confusion:** Agents lack clear separation between understanding constraints (architecture) and refining solutions (iteration)
4. **Cross-Query Learning:** Knowledge learned from one query is typically discarded rather than generalized for future queries

### Cognitive Gap

Human planning experts naturally maintain two types of memory:
- **Long-term structural knowledge:** Rules, constraints, and best practices that apply across similar tasks
- **Working memory:** Current task-specific details and iterative refinement notes

Existing multi-agent systems lack this distinction, forcing agents to either memorize everything or remember nothing.

## Core Concepts & Theory

### The Cognitive Psychology Foundation

EvoMem draws inspiration from Baddeley's Model of Working Memory:

```
Human Cognitive Planning:
├── Long-Term Memory (Task-Independent)
│   ├── Domain knowledge
│   ├── Constraint patterns
│   └── Best practices
└── Working Memory (Task-Dependent)
    ├── Current task details
    ├── Temporary workspace
    └── Iterative refinement notes
```

### Dual-Evolving Memory Architecture

The system implements two complementary memory mechanisms:

#### 1. Constraint Memory (CMem)

**Evolution Pattern:** Across queries (query-level evolution)

```
CMem Lifecycle:
├── Initialization (Query Start)
│   ├── Constraint Extractor analyzes new query
│   └── Extracts task-specific rules and constraints
├── Stable State (Query Execution)
│   ├── CMem remains fixed during query
│   ├── Anchors Actor's solution generation
│   └── Prevents off-topic solutions
└── Update (Next Query)
    ├── CMem is refreshed with new constraints
    └── Generalizable knowledge is retained
```

**Key Properties:**
- Fixed within a query (provides stable anchor)
- Updated only between queries (captures generalization)
- Task-specific but reusable across similar tasks
- Examples: business rules, domain constraints, architectural patterns

#### 2. Query-Feedback Memory (QMem)

**Evolution Pattern:** Within a single query (iteration-level evolution)

```
QMem Lifecycle:
├── Task Start (Empty)
│   └── No prior feedback on current task
├── Iteration N
│   ├── Verifier evaluates current solution
│   ├── Identifies improvement opportunities
│   └── Feedback stored in QMem
├── Iteration N+1
│   ├── Actor reads QMem feedback
│   ├── Refines solution considering feedback
│   └── New feedback added to QMem
└── Convergence
    ├── Solution reaches acceptable quality
    └── QMem discarded (task-specific, not reusable)
```

**Key Properties:**
- Evolves within task execution
- Accumulates iterative refinement insights
- Task-specific and discarded after task completion
- Examples: "Avoid booking hotels after 9pm", "Include 30-minute travel buffers"

### Agent Roles in EvoMem

**1. Constraint Extractor Agent**
- Responsibility: Identify and formalize task-specific constraints
- Inputs: Task description, domain context
- Output: Structured constraint set for CMem
- Triggered: Once per query

**2. Verifier Agent**
- Responsibility: Evaluate Actor's output against constraints
- Inputs: Proposed solution, CMem, QMem
- Output: Evaluation and improvement suggestions
- Triggered: After each Actor iteration

**3. Actor Agent**
- Responsibility: Generate and refine solutions
- Inputs: Task description, CMem, QMem
- Output: Solution attempt
- Triggered: Once initially, then after each Verifier feedback

### Information Flow Topology

```
Multi-Agent Communication Pattern in EvoMem:

Query Initialization:
  Task ──> Constraint Extractor ──> CMem

Iterative Refinement Loop:
  CMem ──> Actor ──> Solution Attempt
            ▲
            │
  QMem ◄────┘
            │
            └──> Verifier ──> Feedback
                    ▲
                    │
              QMem ─┘

Between Queries:
  CMem is refreshed
  QMem is cleared
```

## Main Ideas & Contributions

### 1. Cognitive-Inspired Architecture

Translating cognitive psychology research into agent orchestration:
- Separates query-independent knowledge (CMem) from query-dependent knowledge (QMem)
- Leverages stability properties: CMem anchors reasoning, QMem enables iteration
- Natural mapping to agent roles with clear responsibilities

### 2. Dual-Level Evolution Mechanism

Two independent evolution timescales enabling efficient knowledge management:
- **Cross-Query Learning:** CMem evolves to capture generalizable patterns
- **Within-Query Refinement:** QMem accumulates task-specific improvements
- **Clean Separation:** No mixing of long-term and short-term knowledge

### 3. Provable Agent Coordination Pattern

The architecture provides formal properties:
- **Non-interference:** CMem stability ensures consistent actor anchoring
- **Convergence:** QMem accumulation provides monotonic solution improvement
- **Scalability:** Memory footprint independent of query complexity (only stores constraint patterns)

### 4. Practical Integration Points

The system design enables:
- **Modular integration:** Each agent can use different LLM backends independently
- **Incremental deployment:** Can be integrated into existing multi-agent systems
- **Transparent memory:** Constraints and feedback are human-readable and editable

## Methodology & Implementation

### Experimental Setup

- **Domains Tested:** 
  - Trip planning (multi-city itinerary optimization)
  - Calendar scheduling (meeting scheduling with constraints)
  - Meeting planning (participant coordination and logistics)

- **LLM Backbones:** Gemini-1.5-Pro (primary), DeepSeek V3, GPT-4.1-mini

- **Baselines:** 
  - Single-agent planning
  - Multi-agent without memory
  - Multi-agent with static memory
  - Iterative single-agent refinement

### Agent Workflow with EvoMem

```
Pseudocode Execution Flow:

procedure EvoMem(task, max_iterations):
  // Initialization
  CMem = ConstraintExtractor.extract(task)
  QMem = {}
  
  // Iterative refinement loop
  for iteration = 1 to max_iterations:
    // Generation
    solution = Actor.generate(task, CMem, QMem)
    
    // Verification and feedback
    feedback = Verifier.evaluate(solution, CMem, QMem)
    
    // Update QMem
    QMem.add(feedback)
    
    // Check convergence
    if solution_satisfies_constraints(solution, CMem):
      return solution
  
  return best_solution_found

procedure UpdateCMem(new_task, old_CMem):
  // Between queries
  current_constraints = ConstraintExtractor.extract(new_task)
  generalized = extract_patterns(current_constraints)
  CMem = current_constraints  // Updated but may retain generalizations
```

### Experimental Results and Performance

**Performance Improvements:**

| Domain | Improvement | Metric |
|--------|-------------|--------|
| Trip Planning | +11.17% | Solution quality/feasibility |
| Calendar Scheduling | +2.56% | Schedule conflict-free rate |
| Meeting Planning | +3.76% | Participant satisfaction |

**Model Consistency:**

Results validated across multiple LLM backends:
- **Gemini-1.5-Pro:** Baseline performance, used for primary evaluation
- **DeepSeek V3:** Consistent improvements, 8-10% gains
- **GPT-4.1-mini:** Robust performance, 2-5% improvements (smaller model baseline)

**Key Metrics:**

- Solution quality (constraint satisfaction)
- Convergence speed (iterations to solution)
- Feedback effectiveness (improvement per iteration)
- Memory efficiency (CMem footprint, QMem growth rate)

[Complete statistical significance testing and ablation studies in full paper]

## Practical Applications & Use Cases

### 1. Enterprise Scheduling Systems

**Application:** Calendar management, meeting coordination, resource allocation

```
Enterprise Scheduling Flow:
├── Organization Constraints (CMem)
│   ├── Working hours policies
│   ├── Resource availability rules
│   ├── Cross-timezone considerations
│   └── Project priority levels
└── Meeting-Specific Planning (QMem)
    ├── Participant time zone preferences
    ├── Equipment requirements
    ├── Prior failed slots
    └── Iterative refinement feedback
```

Benefits:
- Reuse organizational policies across thousands of meetings
- Rapid convergence on per-meeting solutions
- Clear audit trail of scheduling decisions

### 2. Travel and Logistics Planning

**Application:** Trip planning, itinerary generation, transportation coordination

- Trip-level constraints (CMem): Budget limits, visa requirements, flight times
- Day-level planning (QMem): Activity preferences, travel buffers, meal timing
- Significant efficiency gains with iterative refinement

### 3. Project Planning and Task Coordination

**Application:** Sprint planning, task assignment, resource allocation

- Project constraints (CMem): Team availability, skill requirements, dependencies
- Sprint-specific planning (QMem): Priority adjustments, resource conflicts, progress tracking
- Enables responsive planning without re-learning project structure

### 4. Legal and Compliance Documentation

**Application:** Contract review, compliance checking, regulatory approval workflows

- Regulatory constraints (CMem): Industry regulations, company policies
- Document-specific planning (QMem): Specific clause review feedback, revision history
- Maintains compliance consistency while enabling document customization

### Integration Challenges

- **CMem Update Frequency:** Determining optimal timing for constraint updates
- **QMem Size Management:** Preventing QMem from becoming too large in long iterative processes
- **Cross-Domain Generalization:** Adapting CMem patterns from similar but distinct domains
- **Human Oversight:** Integrating human feedback into both CMem and QMem

## Insights & Implications

### Impact on Multi-Agent Orchestration

1. **Cognitive Alignment:** Demonstrates value of aligning agent architectures with human cognitive models
2. **Memory as Architecture:** Treats memory evolution as first-class design concern, not afterthought
3. **Separation of Concerns:** Clear distinction between architectural (CMem) and operational (QMem) knowledge
4. **Reusability Framework:** Enables systematic knowledge reuse across similar tasks

### Advancement in Agent System Design

- Shows feasibility of stability-focused (CMem) vs. flexibility-focused (QMem) dual mechanisms
- Provides template for other dual-memory applications (hypothesis generation, hypothesis testing)
- Demonstrates measurable benefits of psychology-inspired agent coordination

### Limitations and Open Questions

- **CMem Generalization:** How well do extracted constraints transfer to different task variants?
- **Scalability:** Does performance scale with very large constraint sets or deep iterative chains?
- **Domain Adaptation:** Which domain characteristics predict effectiveness of EvoMem?
- **Human Collaboration:** How to effectively integrate human feedback into CMem/QMem updates?
- **Computational Cost:** What is the inference cost of multiple agent rounds?

## Code & Resources

### Official Implementation

- **Source Code:** [Implementation details from paper]
- **Framework Integration:** Compatible with LangChain, CrewAI, and other multi-agent frameworks
- **Dependencies:**
  - LLM API access (Gemini, OpenAI, DeepSeek, or compatible)
  - JSON parsing and validation libraries
  - Optional: Constraint solver for verification (Z3, OR-Tools)

### Quick-Start Integration

```python
from evomem import EvoMemOrchestrator, Agents

# Initialize orchestrator
orchestrator = EvoMemOrchestrator(
    llm_backend="gemini-1.5-pro",
    domains=["trip_planning", "calendar_scheduling"]
)

# Add domain-specific constraint patterns (optional)
orchestrator.load_constraint_patterns("./constraints.yaml")

# Execute planning task
def plan_trip(destination, dates, budget):
    task = {
        "type": "trip_planning",
        "destination": destination,
        "dates": dates,
        "budget": budget
    }
    
    # Run EvoMem orchestration
    result = orchestrator.execute(
        task=task,
        max_iterations=5,
        convergence_threshold=0.9
    )
    
    return {
        "plan": result.solution,
        "constraints_used": result.cmem,
        "refinements": result.qmem
    }

# Example usage
trip = plan_trip("Tokyo", "2026-06-01:2026-06-10", 5000)
```

### Compute Requirements

- **LLM Inference:** Standard multi-turn conversation (3-5 turns typical)
- **Memory:** Minimal (CMem: KB-scale, QMem: KB-scale per query)
- **Latency:** 10-30 seconds per query (3-5 agent rounds)
- **Cost:** Proportional to LLM API pricing × number of agent rounds

## Related Work & Context

### Foundation Work

- **Multi-Agent Frameworks:** JADE, ASTRO, CrewAI
- **Cognitive Psychology Models:** Baddeley's Working Memory, ACT-R framework
- **Planning Systems:** Classical planning (PDDL), hierarchical planning
- **Memory-Augmented Agents:** Memory networks, experience replay

### Related Papers on Multi-Agent Planning

- [Efficient Failure Management for Multi-Agent Systems with Reasoning Trace Representation](https://arxiv.org/abs/2603.21522) (2026)
- [Beyond Individual Intelligence: Surveying Collaboration, Failure Attribution, and Self-Evolution](https://arxiv.org/abs/2605.14892) (2026)
- [Planner Matters! An Efficient and Unbalanced Multi-agent Collaboration Framework for Long-horizon Planning](https://arxiv.org/abs/2605.02168) (2026)

### Future Research Directions

1. **Hybrid Memory Systems:** Combining CMem/QMem with other memory types (episodic, semantic)
2. **Adaptive Constraint Discovery:** Learning new constraint patterns from task failures
3. **Cross-Domain Transfer:** CMem patterns learned in one domain applied to others
4. **Agent Specialization:** Different LLM models for Constraint Extractor vs. Verifier vs. Actor
5. **Continuous Learning:** CMem updates in real-time based on task outcomes
6. **Hierarchical Planning:** Nested EvoMem orchestrators for multi-level planning tasks

---

**Citation:**
```bibtex
@article{evomem2025,
  title={EvoMem: Improving Multi-Agent Planning with Dual-Evolving Memory},
  year={2025},
  note={arXiv:2511.01912}
}
```
