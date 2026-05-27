# Self-Organizing Multi-Agent Systems for Continuous Software Development

**ArXiv ID:** [2603.25928](https://arxiv.org/abs/2603.25928)  
**Authors:** Wenhan Lyu, Yue Xiao, Yixuan Zhang, Yifan Sun  
**Institution:** William & Mary  
**Submitted:** March 26, 2026  
**Subcategory:** `multi-agent-topologies`

---

## Executive Summary

This paper introduces TheBotCompany, an open-source orchestration framework for continuous multi-agent software development that implements self-organizing agent teams capable of autonomously managing multi-day development projects. The framework's central innovation is a three-phase state machine (Strategy → Execution → Verification) where manager agents dynamically hire, assign, and fire worker agents based on evolving project needs — enabling long-horizon autonomous development that adapts to changing requirements and discovered complexity. This work is pivotal for agent-driven development because it demonstrates that LLM-based systems can operate as genuine software development teams over extended timeframes, not just as single-shot code generators.

---

## Problem Statement

### Development Automation Challenge

Existing LLM-based code generation systems are fundamentally episodic: they handle discrete, bounded tasks (write a function, fix a bug, implement a feature) within a single session. Real software development, however, is a continuous process spanning days, weeks, or months — involving long-horizon planning, iterative refinement, team coordination, and adaptive resource allocation as project complexity is progressively revealed.

### Prior Agent System Limitations

Previous multi-agent systems suffer from several critical gaps when applied to real-world, continuous software development:

- **Fixed team topologies**: Agent teams are pre-configured at initialization; they cannot adapt as task complexity changes
- **Single-session scope**: Systems lack mechanisms for persisting progress, resuming work, and building on prior accomplishments
- **No quality enforcement**: Without an independent verification layer, defects compound silently
- **Synchronous coordination only**: Agents block waiting for each other, preventing asynchronous human oversight or intervention
- **Milestone blindness**: Systems have no notion of incremental progress; they target entire deliverables at once

### Research Gap

No prior framework treated multi-agent software development as a **continuous organizational process** with adaptive team composition, milestone-driven progress tracking, and independent quality verification — the core elements that make human software teams effective over extended timeframes.

---

## Core Concepts & Theory

### Organizational Metaphor: The Digital Software Company

TheBotCompany's architecture is explicitly modeled on how human software companies organize:

| Human Organization | TheBotCompany |
|-------------------|---------------|
| CTO / Project Manager | Orchestrator (JavaScript-based) |
| Team Lead (Strategy) | Strategy Manager Agent |
| Engineering Manager | Execution Manager Agent |
| QA Lead | Verification Manager Agent |
| Software Engineers | Worker Agents (dynamically hired) |
| Sprint Planning | Milestone Definition |
| Code Review / QA | Verification Phase |
| Project Board | State Machine |

### The Three-Phase Milestone State Machine

Development is organized around **milestones** — discrete, verifiable units of work. Each milestone progresses through a repeating three-phase lifecycle:

```
                    ┌──────────────────────────────────┐
                    │         MILESTONE CYCLE           │
                    │                                   │
                    │   ┌─────────────────────────┐    │
                    │   │    STRATEGY PHASE        │    │
                    │   │                          │    │
                    │   │  Strategy Manager:        │    │
                    │   │  - Analyzes project state │    │
                    │   │  - Defines next milestone │    │
                    │   │  - Sets concrete objectives│   │
                    │   │  - Outputs: Milestone Spec│    │
                    │   └────────────┬────────────┘    │
                    │                │                  │
                    │                ▼                  │
                    │   ┌─────────────────────────┐    │
                    │   │   EXECUTION PHASE        │    │
                    │   │                          │    │
                    │   │  Execution Manager:       │    │
                    │   │  - Assembles worker team  │    │
                    │   │  - Assigns tasks          │    │
                    │   │  - Monitors progress      │    │
                    │   │  - Hires/fires workers    │    │
                    │   │  - Handles failures       │    │
                    │   └────────────┬────────────┘    │
                    │                │                  │
                    │                ▼                  │
                    │   ┌─────────────────────────┐    │
                    │   │  VERIFICATION PHASE      │    │
                    │   │                          │    │
                    │   │  Verification Manager:    │    │
                    │   │  - Independently reviews  │    │
                    │   │  - Runs test suites       │    │
                    │   │  - Evaluates completeness │    │
                    │   │    PASS → Next Milestone  │    │
                    │   │    FAIL → Back to Strategy│    │
                    │   └────────────┬────────────┘    │
                    │                │                  │
                    │                ▼                  │
                    │       [Next Milestone]             │
                    └──────────────────────────────────┘
```

### Self-Organization: Dynamic Team Composition

The defining feature is that worker agent teams are **not fixed** — they emerge from the needs of each milestone:

```
Pseudocode: Dynamic Team Assembly

class ExecutionManager:
    def assemble_team(self, milestone_spec):
        required_skills = self.analyze_skills_needed(milestone_spec)
        # Hire specialist agents
        for skill in required_skills:
            worker = WorkerAgent(specialization=skill)
            self.team.hire(worker)
        
    def monitor_progress(self):
        for worker in self.team:
            if worker.is_blocked() or worker.is_underperforming():
                self.team.fire(worker)
                replacement = WorkerAgent(
                    specialization=worker.specialization,
                    context=worker.current_task
                )
                self.team.hire(replacement)
    
    def complete_milestone(self):
        self.team.disband()  # Release all workers after milestone
```

Worker agent types that may be instantiated include:
- **Implementation Workers**: Write code for assigned modules
- **Test Workers**: Generate and run test cases
- **Documentation Workers**: Update docs and comments
- **Integration Workers**: Handle cross-module connections
- **Debugging Workers**: Diagnose and fix specific failures

### Asynchronous Human Oversight

Unlike systems requiring synchronous human approval at each step, TheBotCompany implements **asynchronous oversight**:

- The orchestrator exposes a checkpoint interface where humans can observe state and inject feedback
- Humans can approve/reject milestone transitions without blocking execution
- The framework queues human feedback and incorporates it in the next Strategy phase
- Time limits on phases prevent indefinite blocking when human oversight is unavailable

### Mathematical Model

Let `M = {m₁, m₂, ..., mₙ}` be the set of milestones for a project `P`. For each milestone `mᵢ`:

```
State(mᵢ) ∈ {PENDING, STRATEGY, EXECUTION, VERIFICATION, COMPLETE, FAILED}

Transition Function:
  PENDING     → STRATEGY     (always)
  STRATEGY    → EXECUTION    (milestone_spec ≠ ∅)
  EXECUTION   → VERIFICATION (team.all_tasks_complete() ∨ time_limit_exceeded())
  VERIFICATION → COMPLETE    (quality_score ≥ threshold ∧ human_approved())
  VERIFICATION → STRATEGY    (quality_score < threshold)  [corrective cycle]
  EXECUTION   → STRATEGY     (critical_failure_detected())

Team composition at milestone mᵢ:
  Team(mᵢ) = ExecutionManager.assemble(Spec(mᵢ))
  |Team(mᵢ)| is dynamic; not predetermined
```

---

## Main Ideas & Contributions

### Novel Contributions

1. **Self-organizing team topology**: First framework where agent team composition emerges dynamically from milestone requirements rather than being pre-configured
2. **Milestone-driven state machine**: Formal three-phase lifecycle that gives continuous development a structured, verifiable progression
3. **Independent verification layer**: Separation of construction (Execution) from evaluation (Verification) mirrors the human engineering practice of independent QA
4. **Asynchronous human oversight**: Humans participate as stakeholders, not controllers — able to guide without blocking autonomous progress
5. **Long-horizon evaluation**: Empirical evaluation over multiple days of continuous development on real-world projects

### Agent Topology: Hierarchical with Dynamic Leaves

The overall topology is **hierarchical** at the management level but **elastic at the worker level**:

```
┌─────────────────────────────────────────────────────┐
│                   ORCHESTRATOR                       │
│              (JavaScript, Central Hub)               │
│   - Drives milestone lifecycle                       │
│   - Invokes manager agents per phase                 │
│   - Enforces time limits                             │
│   - Detects failures                                 │
└──────────────┬──────────────┬───────────────────────┘
               │              │              │
        ┌──────┴───┐   ┌──────┴───┐   ┌─────┴────────┐
        │ Strategy │   │Execution │   │Verification  │
        │ Manager  │   │ Manager  │   │  Manager     │
        └──────────┘   └─────┬────┘   └──────────────┘
                             │
               ┌─────────────┼─────────────┐
               │             │             │
        ┌──────┴──┐   ┌──────┴──┐   ┌─────┴────┐
        │Worker 1 │   │Worker 2 │   │Worker N  │
        │(Coder)  │   │(Tester) │   │(Doc)     │
        └─────────┘   └─────────┘   └──────────┘
          ↑ Dynamically hired and fired per milestone
```

### Technical Innovations

- **Phase-gated context sharing**: Each phase receives only the context relevant to its function, preventing information overload
- **Structured milestone specs**: Machine-parseable milestone definitions that workers can decompose into individual tasks
- **Failure taxonomy**: Classification of execution failures (blocked, underperforming, conflict) to guide targeted interventions

---

## Methodology & Implementation

### Experimental Setup

The evaluation uses real-world software projects (not synthetic benchmarks) with continuous development runs spanning multiple days. This is a key methodological departure from existing work, which typically uses single-session benchmarks.

**Projects evaluated include:**
- Web applications (backend APIs, frontend components)
- Command-line tools
- Library implementations
- Projects with evolving requirements introduced mid-development

**Evaluation dimensions:**
- **Milestone completion rate**: Fraction of milestones reaching COMPLETE state
- **Team adaptation patterns**: How often workers are hired/fired, and for what reasons
- **Cost efficiency**: LLM API cost per milestone, per working line of code
- **Code quality**: Static analysis scores, test coverage, maintainability metrics
- **Verification effectiveness**: Rate at which Verification catches defects before milestone acceptance

### Agent Communication Flow

```
MESSAGE PASSING SEQUENCE: Single Milestone

Orchestrator → Strategy Manager:
  {project_state, completed_milestones, remaining_requirements}

Strategy Manager → Orchestrator:
  {milestone_spec: {objectives, acceptance_criteria, skills_needed}}

Orchestrator → Execution Manager:
  {milestone_spec}

Execution Manager → Worker Agents (parallel):
  {task_assignments[]}

Worker Agents → Execution Manager (async):
  {task_completion_reports[]}

Execution Manager → Orchestrator:
  {milestone_implementation, blockers_encountered}

Orchestrator → Verification Manager:
  {implementation, milestone_spec, acceptance_criteria}

Verification Manager → Orchestrator:
  {verdict: PASS|FAIL, feedback: [], quality_score: float}

[If FAIL]:
Orchestrator → Strategy Manager:
  {project_state, failed_milestone, verification_feedback}
  → New milestone cycle with corrective objectives
```

### Results Summary

| Metric | Finding |
|--------|---------|
| Milestone Completion | Self-organizing teams complete significantly more milestones than fixed-topology baselines |
| Team Adaptation | Workers hired/fired an average of 1.3x per milestone; peaks at complex integration tasks |
| Defect Detection | Verification phase catches 60–75% of defects before milestone acceptance |
| Cost Efficiency | ~$2–8 per milestone depending on complexity and team size |
| Long-horizon Progress | Projects show consistent forward progress across 3+ day development runs |

### Statistical Analysis

Multi-day evaluation reveals that self-organization provides compounding benefits: teams that adapt early to project complexity patterns become more efficient in later milestones, demonstrating learning at the system level even without explicit memory mechanisms in individual agents.

---

## Practical Applications & Use Cases

### Direct Software Development Applications

1. **Autonomous feature development**: Given a product roadmap, the system autonomously implements features milestone by milestone with human checkpoints at transitions
2. **Legacy system modernization**: Long-running projects to migrate, refactor, or update codebases over weeks
3. **Rapid prototyping**: Spinning up fully functional prototypes from specifications without developer involvement in routine implementation tasks
4. **Continuous delivery automation**: Integration with CI/CD pipelines to automatically implement, test, and prepare code changes

### Concrete Multi-Agent Workflow: Building a REST API

```
Day 1, Milestone 1: Database Schema
  Strategy: "Define user and product schemas with PostgreSQL"
  Team: [Schema Worker, Migration Worker]
  Verify: Schema files present, migrations runnable
  Result: PASS

Day 1, Milestone 2: Core CRUD Endpoints  
  Strategy: "Implement GET/POST/PUT/DELETE for users"
  Team: [API Worker, Test Worker, Auth Worker]
  Verify: All endpoints return correct status codes, tests pass
  Result: FAIL (auth integration broken)
  → Strategy: "Fix auth middleware integration"
  Team: [Auth Worker (replacement)]
  Verify: Auth tests pass
  Result: PASS

Day 2, Milestone 3: Business Logic
  Strategy: "Implement product inventory management"
  Team: [Logic Worker, DB Worker, Test Worker, Integration Worker]
  ...
```

### Integration Challenges

- **Context window management**: Long-running projects accumulate large amounts of state that must be summarized for each phase
- **Tool access**: Workers need environment access (terminals, file systems, databases) that requires careful sandboxing
- **Human oversight latency**: Asynchronous oversight works well when humans respond within hours; longer delays may cause phase stalls

### Scalability Considerations

- Team size scales with milestone complexity — simple milestones use 2–3 workers, complex integration milestones may use 6–8
- The orchestrator becomes a bottleneck at very large team sizes; future work suggests hierarchical orchestrators
- LLM API costs scale linearly with team size × milestone complexity; cost budgeting is essential

---

## Insights & Implications

### Impact on Agent-Driven Development

TheBotCompany establishes the **organizational paradigm** for long-horizon agent development: discrete milestones, phase-gated quality checks, and dynamic team composition are more robust than fixed pipelines or single-session generation. This mirrors how effective human engineering teams operate.

### Advancement in Autonomous Coding

The critical advancement is demonstrating **temporal continuity** — the ability to maintain coherent development direction across multiple days while adapting team structure to discovered complexity. Prior systems were stateless across sessions; this framework maintains project memory through structured state representation.

### Limitations

- Evaluation is on relatively small-scale projects; applicability to enterprise-scale codebases (millions of LOC) remains unproven
- The framework does not yet handle multi-repository development or microservices architectures
- Worker agent specialization is coarse-grained; fine-grained skill specialization (e.g., "database indexing expert") is future work
- Asynchronous human oversight can introduce inconsistencies if feedback arrives mid-phase

### Open Research Questions

- Can the state machine learn optimal milestone granularity from project complexity signals?
- How does self-organization scale to 20+ worker agents per milestone?
- What are the failure modes when verification agents themselves have systematic biases?
- Can the framework integrate with existing IDE tooling (LSP, debuggers) for richer worker capabilities?

### Relevance to Skill Frameworks

The self-organizing topology directly maps to **dynamic skill dispatching**: rather than pre-configuring which skills are available, the Execution Manager could be reimplemented as a skill broker that identifies and instantiates skills on-demand based on task requirements, with the Verification Manager using skill-based evaluation tools.

---

## Code & Resources

- **ArXiv Paper:** https://arxiv.org/abs/2603.25928
- **Implementation Note:** TheBotCompany is described as open-source; the orchestrator is implemented in JavaScript
- **Institution:** William & Mary (Computer Science Department)

### Dependencies and Compute Requirements

- JavaScript/Node.js runtime for the orchestrator layer
- LLM API access (any capable instruction-following model)
- Sandboxed execution environment for worker agents (Docker recommended)
- Persistent storage for project state and milestone history
- Optional: human oversight interface (web dashboard or CLI)

### Conceptual Integration Guide

```javascript
// TheBotCompany conceptual API
const TheBotCompany = require('thebotcompany');

const company = new TheBotCompany({
  llm: { provider: 'anthropic', model: 'claude-sonnet-4-6' },
  executionEnvironment: { type: 'docker', image: 'dev-sandbox:latest' },
  humanOversight: { mode: 'async', checkpointAt: 'milestone_transitions' }
});

const project = company.createProject({
  requirements: `
    Build a REST API for a task management application with:
    - User authentication (JWT)
    - Task CRUD operations
    - PostgreSQL backend
    - OpenAPI documentation
  `,
  successCriteria: 'All endpoints functional with >80% test coverage'
});

// Runs continuously until project completion or human intervention
await project.run({
  maxMilestones: 10,
  costBudget: 50.00,   // USD
  timeBudget: 72 * 60  // minutes
});
```

---

## Related Work & Context

### Related Papers

- **Self-Organized Agents (SoA)** ([arXiv:2404.02183](https://arxiv.org/abs/2404.02183)): Earlier framework for large-scale code generation via self-organization; TheBotCompany extends this to continuous development
- **ChatDev** ([arXiv:2307.07924](https://arxiv.org/abs/2307.07924)): Multi-agent system modeled on software company roles (CEO, CTO, Developer, Tester); fixed topology rather than dynamic
- **MetaGPT** ([arXiv:2308.00352](https://arxiv.org/abs/2308.00352)): Assigns human software roles to agents; single-session focus
- **AgentMesh** ([arXiv:2507.19902](https://arxiv.org/abs/2507.19902)): Cooperative multi-agent framework (Planner, Coder, Debugger, Reviewer) without self-organization
- **SOEN-101** ([arXiv:2403.15852](https://arxiv.org/abs/2403.15852)): Emulates software process models with LLM agents; complementary process focus

### Prior Foundational Work

- **Organizational Theory (Conway's Law)**: The insight that system architecture mirrors team communication structure; TheBotCompany inverts this — team structure adapts to system architecture
- **Agile/Scrum methodology**: Sprint-based milestone thinking is the human practice this framework operationalizes
- **AutoGPT / BabyAGI**: Early autonomous agent systems that demonstrated long-horizon task decomposition but lacked multi-agent team coordination

### Future Research Directions

- **Hierarchical orchestration**: Multiple orchestrators managing sub-teams for larger projects
- **Cross-project learning**: Milestones and team compositions from past projects informing future ones
- **Hybrid human-agent teams**: Seamlessly mixing human developers with agent workers within the same milestone
- **Formal verification integration**: Using formal methods tools as the Verification Manager for safety-critical systems
- **Cost-performance optimization**: Automatic model selection per worker role based on task complexity and cost constraints
