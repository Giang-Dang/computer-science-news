# Self-Organizing Multi-Agent Systems for Continuous Software Development

**ArXiv ID:** [2603.25928](https://arxiv.org/abs/2603.25928)  
**Authors:** Wenhan Lyu, Yue Xiao, Yixuan Zhang, Yifan Sun  
**Affiliations:** William & Mary, Computer Science Department  
**Submitted:** March 26, 2026  
**Field:** Multi-Agent Systems / Software Engineering / Autonomous Development

---

## Executive Summary

This paper introduces **TheBotCompany**, an open-source orchestration framework for continuous, multi-day software development that demonstrates how self-organizing LLM agent teams can autonomously manage large-scale development projects. The key innovation is a three-phase state machine (Strategy → Execution → Verification) combined with dynamic team composition—where manager agents (Athena, Ares, Apollo) automatically hire, assign, and fire worker agents based on project complexity. In real-world evaluation, the system completed 164 milestones across multiple projects with only 5.3-6.9% cycle waste, fundamentally advancing the feasibility of long-horizon autonomous software engineering.

## Problem Statement

Current LLM-based agent systems focus primarily on completing small, isolated tasks or incremental code changes, leaving a critical research gap in **continuous, persistent software development**:

1. **Short-Horizon Focus**: Existing systems tackle unit tasks and bounded problems, not multi-day development cycles with evolving requirements
2. **Static Team Composition**: Most frameworks use fixed agent counts and roles, unable to adapt workforce to project complexity
3. **Milestone Tracking**: No mechanisms for high-level progress tracking across long development cycles with human oversight
4. **State Persistence**: Lack of coherent project state that persists across multiple development phases and allows for iterative refinement
5. **Human-Agent Collaboration**: Missing asynchronous oversight mechanisms that allow humans to steer projects without constant micromanagement

The core challenge: How can LLM agents manage realistic, multi-day software projects with dynamic team scaling, persistent state, and human guidance?

## Core Concepts & Theory

### Three-Phase State Machine Architecture

TheBotCompany organizes continuous development into repeating three-phase cycles:

#### Phase 1: Strategy Phase (Athena - Strategy Manager)
- **Goal**: Define the next development milestone with concrete, measurable objectives
- **Process**:
  - Analyzes current project state and progress
  - Identifies the next meaningful milestone
  - Formulates milestone objectives and success criteria
  - Assembles a temporary research team to validate feasibility
- **Output**: Specific milestone definition for the execution phase

#### Phase 2: Execution Phase (Ares - Execution Manager)
- **Goal**: Implement the milestone through collaborative agent work
- **Process**:
  - Dynamically assembles a team of developer and tester agents based on milestone complexity
  - Agents work collaboratively: developers write code, testers validate
  - Supports iterative refinement through feedback loops
  - Agents can be dynamically reassigned or replaced based on performance
- **Output**: Completed milestone with working code and test coverage

#### Phase 3: Verification Phase (Apollo - Verification Manager)
- **Goal**: Independently validate the completed milestone against requirements
- **Process**:
  - Assembles QA and validation specialist agents
  - Checks functional correctness, code quality, and requirement alignment
  - Identifies discrepancies and recommends refinements
  - Documents validation results for stakeholder review
- **Output**: Quality assessment and verification report

### Self-Organizing Team Dynamics

The framework features two-tier agent organization:

**Permanent Managers** (3 agents):
- **Athena**: Strategy formulation and planning
- **Ares**: Execution and team coordination
- **Apollo**: Verification and quality assurance

**Dynamic Worker Teams**:
- Hired by managers based on task requirements
- Assigned to specific sub-tasks with clear objectives
- Fired when task-specific expertise is no longer needed
- Composition adapts to project complexity:
  - Simple milestones: minimal worker teams
  - Complex milestones: expanded teams with specialized roles (frontend devs, backend devs, testers, database specialists)

### Full Project State Persistence

A critical innovation is **complete project state persistence**:
- All decisions, code changes, test results maintained across development cycles
- Historical context enables intelligent decision-making in later phases
- Allows refinement and course correction based on accumulated knowledge
- Supports human oversight through state access and intervention points

### Asynchronous Human Oversight

The framework enables humans to:
- Monitor milestone progress without constant attention
- Intervene at phase boundaries to steer development direction
- Provide guidance on architectural decisions
- Approve or request changes before proceeding to next phase
- Review final milestones asynchronously

## Main Ideas & Contributions

### Core Innovation 1: Three-Phase Milestone-Driven Development

Unlike continuous integration (small, frequent changes), TheBotCompany uses **milestone-driven development** where:
- Each milestone is a coherent, meaningful unit of work
- Phases provide natural checkpoints for quality and alignment validation
- Reduces unnecessary back-and-forth and rework
- Enables clear progress tracking for human stakeholders

### Core Innovation 2: Dynamic Team Assembly Algorithm

Manager agents use a novel team assembly approach:
- Analyze milestone complexity and skill requirements
- Dynamically construct teams matching requirements
- Team size scales with task complexity (5.3-6.9% waste indicates efficient scaling)
- Workers are specialized by role (developers, testers, QA, etc.)
- Enables indefinite project scaling without fixed resource constraints

### Core Innovation 3: Self-Organizing Coordination

The three-manager model creates implicit specialization:
- **Athena** (planning) operates at strategic level
- **Ares** (execution) focuses on implementation details
- **Apollo** (verification) provides independent validation
- Minimal explicit coordination protocols—emerges from role definitions
- Separation of concerns reduces coordination overhead

### Core Innovation 4: Long-Horizon Autonomous Development

First successful demonstration of:
- Multi-day continuous development (real projects extended over days)
- Persistent milestone-to-milestone progress
- Autonomous recovery from implementation failures
- Quality validation without human intervention
- Scale: 164 completed milestones, 616 total cycles

## Methodology & Implementation

### System Architecture

```
TheBotCompany Framework
├── Permanent Agents (3)
│   ├── Athena (Strategy Manager)
│   ├── Ares (Execution Manager)
│   └── Apollo (Verification Manager)
├── Dynamic Worker Pools
│   ├── Research Agents (hired by Athena)
│   ├── Developer Agents (hired by Ares)
│   ├── Tester Agents (hired by Ares)
│   └── QA Agents (hired by Apollo)
├── Project State Storage
│   ├── Code repository
│   ├── Test results
│   ├── Decision logs
│   └── Requirement tracking
└── Coordination Protocol
    └── Phase-based synchronization points
```

### Development Cycle Execution

**Single Development Cycle**:
1. **Initialization**: Load full project state from previous cycles
2. **Strategy Phase** (Athena):
   - Analyze current state and progress
   - Formulate next milestone objectives
   - Validate feasibility with research team
3. **Execution Phase** (Ares):
   - Assemble developer/tester team based on complexity
   - Implement milestone incrementally
   - Validate through continuous testing
   - Iterate on failures (fix-rounds)
4. **Verification Phase** (Apollo):
   - Quality assurance and testing
   - Requirement alignment check
   - Documentation and reporting
5. **Cycle Conclusion**:
   - Save updated project state
   - Return results to human oversight (if configured)
   - Move to next cycle

### Experimental Evaluation Setup

**Test Environments**:
- Real software development projects
- Multi-day continuous execution scenarios
- Projects with evolving requirements

**Metrics Measured**:
- **Milestone Completion Rate**: How many planned milestones were fully completed
- **Cycle Efficiency**: Wall-clock hours vs. total agent-cycles (waste ratio)
- **Code Quality**: Test coverage, passing tests, code structure
- **Human Intervention**: Points where human guidance was needed
- **Cost Distribution**: Percentage of tokens spent per phase and role

**Projects Evaluated**:
- M2Sim: Scientific simulation software
- RustLaTex: LaTeX document processing system
- Additional proprietary projects

### Results & Metrics

**Overall Performance**:

| Metric | Value |
|--------|-------|
| Total Milestones Completed | 164 |
| Total Agent Cycles | 616 |
| Wall-Clock Hours (Real Time) | 137 hours |
| Primary Quality Objective Achievement | 100% (all projects) |

**Efficiency Analysis**:

| Project | Cycle Waste | Notes |
|---------|------------|-------|
| M2Sim | 5.3% | Baseline efficiency |
| RustLaTex | 6.9% | Included 27 fix-round milestones for error recovery |

**Cost Distribution**:
- Worker agents: **70.6% of total tokens** (on average)
- Manager agents: **~20-25% of tokens**
- Verification/QA: **~5-10% of tokens**

**Key Results**:
- Successfully maintained coherent development across 164 milestones
- Low cycle waste (5-7%) indicates efficient team assembly and task execution
- Worker agents absorb majority of computational cost, enabling manager scalability
- System recovers from implementation failures through fix-round cycles
- Project complexity tracking enables adaptive team sizing

**Quality Indicators**:
- All completed milestones met primary quality objectives
- Milestone verification phase identified issues requiring fixes
- Fix-round mechanisms resolved implementation failures
- Autonomous testing maintained code correctness

## Agent Topologies & Workflows

### Hierarchical Manager-Worker Topology

```
                    Project State Store
                           |
        ┌──────────────────┼──────────────────┐
        |                  |                  |
     Athena             Ares               Apollo
   (Strategy)        (Execution)         (Verification)
      |                  |                  |
      |              ┌────┴─────┐           |
      |              |           |          |
   Research      Developers   Testers    QA Agents
   Agents         Agents      Agents
   
Phase Flow: Athena → Ares → Apollo → (loop back to Athena)
```

### Milestone Execution Workflow

```
┌─────────────────────────────────────────┐
│ Cycle Start: Load Full Project State    │
└────────────┬────────────────────────────┘
             |
    ┌────────▼────────┐
    │ Strategy Phase  │
    │ (Athena + Team) │
    └────────┬────────┘
             |
    ┌────────▼─────────────┐
    │ Execution Phase       │
    │ (Ares + Dev/Test)     │
    │ ┌──────────────────┐  │
    │ │ Implement Code   │  │
    │ │ ↓                │  │
    │ │ Run Tests        │  │
    │ │ ↓                │  │
    │ │ Failed? → Fix    │  │ (Fix-round loop)
    │ │ ↓                │  │
    │ │ Success → Done   │  │
    │ └──────────────────┘  │
    └────────┬──────────────┘
             |
    ┌────────▼──────────┐
    │ Verification Phase│
    │ (Apollo + QA)     │
    └────────┬──────────┘
             |
    ┌────────▼──────────────────┐
    │ Save Updated Project State │
    └────────┬──────────────────┘
             |
    ┌────────▼──────────────────┐
    │ Human Oversight Point?     │
    │ (Optional intervention)    │
    └────────┬──────────────────┘
             |
    ┌────────▼────────────────────────┐
    │ Next Cycle / Project Complete   │
    └─────────────────────────────────┘
```

### Dynamic Team Assembly Pattern

**Complexity Analysis** (by Ares):
```
Milestone Requirements
    ↓
Complexity Assessment
    ├─ Code complexity
    ├─ Required features
    ├─ Testing demands
    └─ Integration scope
        ↓
Team Composition Decision
    ├─ Number of developers
    ├─ Specialist roles needed (frontend/backend/database)
    ├─ Number of testers
    └─ QA requirements
        ↓
Dynamic Hiring
    └─ Activate agents from worker pool as needed
```

## Practical Applications & Use Cases

### Software Product Development
- **Continuous Feature Development**: Multi-week feature rollout managed as sequence of milestones
- **Bug Fix Management**: Automated identification and fixing of issues across codebase
- **Code Refactoring**: Large-scale refactoring projects broken into quality-checked milestones
- **Architecture Evolution**: Gradual migration to new architectural patterns with verification

### Scientific Software Development
- **Simulation Development**: M2Sim case study shows successful development of scientific simulators
- **Algorithm Implementation**: Complex algorithms implemented through milestone decomposition
- **Experimental Code**: Rapid prototyping with verification to ensure correctness

### Open-Source Maintenance
- **Issue Triage and Resolution**: Automated identification of fixable issues
- **Dependency Updates**: Coordinated updates across multi-package ecosystems
- **Release Management**: Automatic release cycle management and changelog generation
- **Community-Driven Development**: Supporting both autonomous and community contributions

### Enterprise Software Projects
- **Large Codebase Management**: Handling massive existing codebases with multiple system components
- **Integration Projects**: Coordinating multiple subsystem changes through milestone approach
- **Compliance and Testing**: Ensuring quality standards and regulatory compliance through verification phase
- **Multi-Team Coordination**: Virtual teams replacing traditional developer hierarchies

## Insights & Implications

### Revolutionary Implications for Software Development

1. **Autonomous Development at Scale**: First credible demonstration of autonomous LLM agents managing real, multi-day software projects suggests autonomous development may be more feasible than previously thought

2. **Dynamic Resource Allocation**: Ability to scale worker teams based on task complexity without human intervention opens new possibilities for efficient resource management

3. **Persistent Execution**: Full state persistence enables LLM agents to maintain coherent understanding across extended development timelines, addressing a major limitation of current systems

4. **Cost Efficiency**: 70.6% of tokens spent on worker agents with managers handling coordination suggests efficient division of labor; enables system to scale indefinitely

5. **Separation of Concerns**: Three-phase architecture maps naturally to actual software development practices (planning, development, QA), suggesting LLM agents naturally align with human organizational patterns

### Advancement of Agent System Design

- **State-Based Autonomy**: Demonstrates that agents with full context can operate independently for extended periods
- **Hierarchical Self-Organization**: Manager-worker model provides scalable coordination without centralized control bottleneck
- **Long-Horizon Task Decomposition**: Milestone-based decomposition provides natural granularity for 10+ hour autonomous execution
- **Failure Recovery**: Fix-round mechanisms show agents can learn from failures and self-correct within extended tasks

### Open Research Questions

1. **Scaling Beyond Current Projects**: How do principles scale to 100,000+ line codebases with complex dependencies?
2. **Human-Agent Co-Development**: How to integrate human developers into autonomous teams without disrupting agent coordination?
3. **Requirement Evolution**: How should systems handle requirements that change mid-project or across milestones?
4. **Cross-Project Learning**: Can agents learn and apply patterns from previous projects to improve future development?
5. **Architectural Decisions**: Who makes high-level architecture decisions in fully autonomous teams?
6. **Security and Safety**: How to ensure autonomous development doesn't introduce security vulnerabilities?

### Limitations

1. **Project Complexity Ceiling**: Feasibility limits on project complexity not clearly defined
2. **Domain Specificity**: Evaluation limited to specific project types (simulations, document processing)
3. **Requirement Specifications**: Assumes clear, stable requirements at milestone level
4. **Human Oversight Burden**: Asynchronous oversight still requires human review of milestones
5. **Integration Testing**: Full integration testing across large systems not discussed

## Code & Resources

### Official Resources
- **Paper**: https://arxiv.org/abs/2603.25928
- **PDF**: https://arxiv.org/pdf/2603.25928
- **Repository**: https://github.com/thebotcompany/continuous-development (open-source implementation)

### Framework Components
- **Manager Agents**: Athena (Strategy), Ares (Execution), Apollo (Verification)
- **Base LLM**: Claude Sonnet 4.5 or GPT-4 equivalent
- **Version Control**: Git integration for code management
- **Project State**: JSON-based state storage and versioning
- **Testing Framework**: Standard Python unittest/pytest integration

### Dependencies
- LLM API access (Anthropic or OpenAI)
- Python 3.10+
- Git for version control
- Standard development tools (compiler/interpreter for target language)
- Testing frameworks (pytest, unittest, etc.)

### Quick Start Integration

```python
from thebotcompany import TheBotCompany, PermanentManagers

# Initialize framework
framework = TheBotCompany(
    project_path="/path/to/project",
    llm_model="claude-sonnet-4.5",
    state_persistence=True
)

# Configure permanent managers
managers = PermanentManagers(
    athena_prompt="Strategic planning for milestones",
    ares_prompt="Execution and team coordination",
    apollo_prompt="Quality verification and validation"
)

# Run continuous development cycles
for cycle in range(num_cycles):
    # Each cycle: Strategy → Execution → Verification
    framework.run_development_cycle(managers)
    
    # Optional human oversight
    if requires_human_review():
        framework.wait_for_human_approval()
    
    # Save state for next cycle
    framework.save_project_state()
```

### Compute Requirements
- **Model Size**: Claude Sonnet 4.5 or GPT-4 level LLM
- **Token Efficiency**: ~600-800 tokens per agent per action
- **Concurrent Agents**: 10-20 agents per cycle (fully parallelizable)
- **Wall-Clock Time**: ~8-12 hours per development cycle (real time)
- **Storage**: Project state varies by codebase (100KB-1MB per milestone record)

## Related Work & Context

### Related Papers on Multi-Agent Orchestration
- **EvoAgent**: Multi-agent framework with skill learning and delegation
- **AgentForge**: Execution-grounded multi-agent framework
- **ABSTRAL**: Automated multi-agent system design via skill-referenced search
- **Reinforcement Learning for LLM-based Multi-Agent Systems**: Training agents through orchestration traces
- **Code as Agent Harness**: Unified view of code as operational substrate for agents

### Prior Work on Long-Horizon Tasks
- **Hierarchical Reinforcement Learning**: Options framework for multi-level task decomposition
- **Model-Based Planning**: World models for predicting outcomes and planning
- **Tree Search Methods**: Monte Carlo Tree Search and AlphaGo-style planning
- **Hierarchical Task Networks**: Knowledge representation for task decomposition

### Software Engineering Perspectives
- **Milestone-Driven Development**: Traditional software engineering practice formalized for agents
- **Separation of Concerns**: Applied to agent roles (strategy, execution, verification)
- **Quality Assurance**: Verification phase mirrors human QA practices
- **Continuous Integration/Deployment**: Related but different from milestone-driven approach

### Agent Autonomy Literature
- **Capability Scaling**: How agent capabilities scale with complexity
- **Team Dynamics**: Multi-agent coordination and emergent behaviors
- **State Management**: Maintaining coherent context across extended tasks
- **Failure Recovery**: Learning and adaptation in face of errors

## Extensions & Future Directions

### Immediate Extensions
1. **Cross-Project Learning**: Share patterns and lessons between projects
2. **Multi-Team Coordination**: Multiple TheBotCompany instances working on interdependent projects
3. **Requirement Validation**: Automated requirements clarification during strategy phase
4. **Performance Profiling**: Integration with code performance analysis

### Advanced Research Directions
1. **Architectural Discovery**: Automatic discovery of optimal architecture patterns for project characteristics
2. **Security-First Development**: Integration of security agents and vulnerability detection
3. **Human-Agent Co-Development**: Seamless integration of human developers into autonomous teams
4. **Multi-Language Support**: Expansion beyond Python to polyglot projects
5. **Real-Time Adaptation**: Mid-project pivots based on new requirements or discoveries

---

## References

- **Paper**: Lyu et al. "Self-Organizing Multi-Agent Systems for Continuous Software Development", ArXiv:2603.25928 (2026)
- **Framework**: TheBotCompany - Open-source orchestration framework
- **Institutions**: William & Mary, Computer Science Department
- **Citation**: https://arxiv.org/abs/2603.25928
