# Agentic Software Engineering: Foundational Pillars and Paradigm Shift

**Paper:** [Agentic Software Engineering: Foundational Pillars and Paradigm Shift to SE 3.0](https://arxiv.org/abs/2509.06216)  
**ArXiv ID:** 2509.06216  
**Submission Date:** September 7, 2025 (Revised: June 24, 2026)  
**Authors:** Ahmed E. Hassan, Hao Li, Dayi Lin, Bram Adams, Tse-Hsun Chen, Yutaro Kashiwa, Dong Qiu  
**Affiliations:** Queen's University, Huawei Canada Research Centre, University of New South Wales

## Executive Summary

Agentic Software Engineering represents a fundamental paradigm shift from SE 2.0 (AI-augmented development) to SE 3.0 (autonomous agent-driven development). This foundational vision paper reimagines the four classical SE pillars—Actors, Processes, Tools, and Artifacts—in the context of autonomous LLM agents. Rather than agents simply augmenting human developers, SE 3.0 positions autonomous agents as first-class participants in software development, requiring new architectural patterns (Agent Command Environment and Agent Execution Environment), new process models, and new tool/artifact abstractions. This paper establishes the conceptual framework, research roadmap, and critical open questions for this transition.

## Problem Statement

**The SE 2.0 Limitation:**
Current AI-augmented development (SE 2.0) treats LLMs as tools that humans orchestrate:
- Humans remain the primary decision-makers and control flow orchestrators
- Agents assist with specific subtasks (code completion, bug fixing, testing)
- Integration is shallow: agents don't participate in architectural decisions or long-term planning
- Scalability is limited to human capacity for oversight and coordination

**Transitioning to SE 3.0:**
Autonomous agents capable of end-to-end software engineering create a new reality:
- Agents can make decisions, decompose problems, execute plans independently
- Agents can coordinate with other agents without human mediation
- Traditional roles (architect, developer, tester, reviewer) blur when agents perform all simultaneously
- The software development process fundamentally changes

**Research Gaps:**
1. **Architectural paradigms**: No established patterns for agent-human collaboration at scale
2. **Process models**: Classical SE processes (waterfall, agile, DevOps) assume human workflow
3. **Tool abstractions**: IDEs, version control, CI/CD designed for human use; ill-suited for agent teams
4. **Organizational structures**: How do teams of humans + agents collaborate?
5. **Trustworthiness**: How do we ensure autonomous agent decisions are safe and verifiable?

## Core Concepts & Theory

### SE 3.0 Architecture: Dual Modality

**Classical SE (SE 1.0 & 2.0):**
```
Human Developer
    ↓
    Uses: IDE, VCS, Build tools, Debuggers
    ↓
Produces: Code, Commits, Tests, Docs
```

**SE 3.0: Dual Modality (Human-Agent Collaboration):**
```
┌─────────────────────────────────────────────────┐
│  Agent Command Environment (ACE)                │
│  - Human orchestration center                   │
│  - Strategic direction setting                  │
│  - High-level goals and constraints             │
│  - Oversight and approval gates                 │
└──────────────┬──────────────────────────────────┘
               │
               ↓
┌─────────────────────────────────────────────────┐
│  Agent Execution Environment (AEE)              │
│  - Autonomous agent workspace                   │
│  - Multi-agent coordination                     │
│  - Tool execution and orchestration             │
│  - Decision-making and planning                 │
└─────────────────────────────────────────────────┘
               ↓
    Produces: Code, Plans, Tests, Reviews, Docs
```

**Key Principle**: Clear separation of human oversight (ACE) from autonomous execution (AEE), enabling both human control and agent autonomy.

### Reimagined SE Pillars for SE 3.0

#### 1. **Actors**

**SE 1.0/2.0 View**: Humans (developers, architects, testers, reviewers)

**SE 3.0 View**: Humans + Autonomous Agents as first-class participants

| Dimension | SE 2.0 | SE 3.0 |
|-----------|--------|--------|
| **Developer** | Human writes code | Agents generate code; humans review |
| **Architect** | Human designs systems | Agents propose architectures; humans decide |
| **Tester** | Human tests code | Agents test; humans validate test strategies |
| **Reviewer** | Human reviews code | Agents review; humans make final decisions |
| **DevOps** | Human manages deployment | Agents manage; humans oversee |

**Agent Specialization**:
- **Planning Agents**: Decompose requirements, propose architectures
- **Coding Agents**: Generate implementations, refactor, optimize
- **Testing Agents**: Design tests, identify edge cases, generate test data
- **Review Agents**: Code analysis, style checking, security auditing
- **Coordination Agents**: Orchestrate multi-agent workflows, resolve conflicts

#### 2. **Processes**

**SE 1.0/2.0**: Linear or iterative (waterfall, agile, DevOps)

**SE 3.0**: Iterative agent-driven with human checkpoints

**Modified Agile Process for SE 3.0**:
```
1. Human sets high-level sprint goal (ACE)
2. Planning agents break into tasks (AEE)
3. Agents self-organize and execute (AEE)
4. Testing agents validate (AEE)
5. Code review agents audit (AEE)
6. Humans review agent work (ACE)
7. Humans approve or redirect (ACE)
8. Agents integrate and deploy (AEE)
9. Humans monitor production (ACE)
```

**Key Difference**: Feedback loops are tighter; agent-to-agent communication replaces many human handoffs.

#### 3. **Tools**

**SE 1.0/2.0 Tools**: IDE, Git, Jira, Jenkins, VS Code, IntelliJ

**SE 3.0 Tool Evolution**:
- **IDE → Agentic Development Environment (ADE)**: Agents query codebase semantically, not just text search
- **Git → Semantic VCS**: Tracks not just diffs but conceptual changes and architectural decisions
- **Jira → Agent-Accessible Task Protocol**: Machine-readable task descriptions with formal preconditions/postconditions
- **Jenkins → Agent-Native CI/CD**: Agents understand build failures semantically, propose fixes

**New SE 3.0 Tools**:
- **Agent Communication Middleware**: Publish-subscribe for agent coordination
- **Knowledge Graphs**: Repository-wide semantic understanding (codebase structure, dependencies, business logic)
- **Formal Verification Systems**: Prove agent-generated code correctness
- **Agent Capability Registries**: Discover which agent can solve which problem

#### 4. **Artifacts**

**SE 1.0/2.0 Artifacts**: Source code, documentation, build artifacts, test cases

**SE 3.0 Artifacts** (expanded):
- **Executable Code**: As before, but also generated by agents
- **Agent Logs & Decisions**: Full audit trail of how agents decided to implement features
- **Architectural Models**: Machine-readable architecture specifications agents can reason over
- **Skill Libraries**: Reusable agent capabilities packaged as composable modules
- **Verification Certificates**: Formal proofs that code satisfies specifications
- **Agent Instructions**: Explicit prompts and configurations that drove code generation

## Main Ideas & Contributions

### 1. **Dual-Modality Architecture**

First systematic treatment of human-agent collaboration as architectural concern:
- **Agent Command Environment (ACE)**: Humans provide strategic direction, review decisions, set constraints
- **Agent Execution Environment (AEE)**: Agents operate autonomously, coordinate with peers, execute plans
- Clear information flow and decision boundaries

**Why This Matters**:
- Humans remain in control (approval gates, veto power)
- Agents gain autonomy (no per-decision human approval)
- Scales to large teams (N agents, M humans with asymmetric communication)

### 2. **Reimagined SE Pillars Framework**

Classical SE foundations (actors, processes, tools, artifacts) need reconceptualization for agent participation:
- **New actor model**: Agents as professionals (not just assistants)
- **New processes**: Agent-to-agent handoffs, asynchronous coordination
- **New tools**: Semantic understanding, formal verification, agent-native interfaces
- **New artifacts**: Decision logs, architectural models, verification certificates

**Why This Matters**:
- Provides vocabulary for SE 3.0 research
- Identifies gaps in current infrastructure (tools, processes, organizational structures)
- Guides future tool development

### 3. **Research Roadmap for SE 3.0**

Identifies critical open questions across five dimensions:

**Technical Dimension**:
1. How do agents understand large codebases semantically?
2. How do agents coordinate to avoid conflicts?
3. How do we verify agent-generated code is correct?
4. How do agents handle ambiguous requirements?

**Process Dimension**:
5. What process models suit human-agent teams?
6. How do we set appropriate oversight checkpoints?
7. How do agents report decisions to humans?
8. What metrics measure agent productivity?

**Organizational Dimension**:
9. How do organizations restructure for autonomous agents?
10. What new roles emerge (Agent Manager, Agent Coach)?
11. How do humans retain meaningful work?
12. How do we transition from SE 2.0 to SE 3.0?

**Trustworthiness Dimension**:
13. How do we ensure agent decisions are safe?
14. How do we audit agent behavior?
15. How do we hold agents accountable?
16. What regulations apply to autonomous coding?

**Economics Dimension**:
17. What are cost/benefit tradeoffs of agent teams?
18. How do agent capabilities affect labor economics?
19. How do we price agent services?
20. What business models emerge?

## Methodology & Implementation

### Architectural Patterns

**Agent Command Environment (ACE) - Human-Centric**:
```python
# Pseudocode for ACE
human_goal = "Implement payment processing module with PCI compliance"

# ACE components
acl_manager = ACLManager()  # Access control
goal_translator = GoalTranslator()  # Convert to agent-solvable tasks
oversight_engine = OversightEngine()  # Approval gates
audit_log = AuditLog()  # Decision tracking

# Human sets constraints
acl_manager.set_policy(code_review_required=True, security_audit=True)
constraints = {"max_cost": "$100", "timeline": "3 days", "languages": ["Python", "Kotlin"]}

# Translate to agent tasks
agent_tasks = goal_translator.decompose(human_goal, constraints)
# [Task: "Analyze PCI compliance requirements", Task: "Design schema", ...]
```

**Agent Execution Environment (AEE) - Agent-Centric**:
```python
# Pseudocode for AEE
class DevelopmentTeam:
    def __init__(self):
        self.architect = ArchitecturalAgent()
        self.coder = CodingAgent()
        self.tester = TestingAgent()
        self.reviewer = ReviewAgent()
        
    async def execute_task(self, task):
        # Agent self-coordination
        architecture = await self.architect.propose(task)
        code = await self.coder.generate(architecture)
        tests = await self.tester.design(code)
        review = await self.reviewer.audit(code)
        
        # Conflict resolution (agent-to-agent)
        if review.concerns:
            code = await self.coder.refine(code, review.concerns)
        
        return code, review, tests
```

### Dual-Environment Communication

```
ACE (Human Layer)                    AEE (Agent Layer)
┌──────────────────┐                ┌─────────────────┐
│ Human Developer  │                │ Planning Agent  │
│   - Sets goal    │────────────────→│   - Decomposes  │
│   - Reviews plan │←────────────────│   - Proposes    │
└──────────────────┘                └─────────────────┘
        ↓                                    ↓
┌──────────────────┐                ┌─────────────────┐
│ Approval Gate    │                │ Coding Agent    │
│  - Constraints   │────────────────→│   - Generates   │
│  - Veto power    │←────────────────│   - Implements  │
└──────────────────┘                └─────────────────┘
        ↓                                    ↓
┌──────────────────┐                ┌─────────────────┐
│ Oversight Engine │                │ Testing Agent   │
│  - Checkpoints   │────────────────→│   - Validates   │
│  - Audit trail   │←────────────────│   - Certifies   │
└──────────────────┘                └─────────────────┘
```

## Results and Metrics

This is a **vision/framework paper**, not an empirical study. However, it establishes evaluation criteria for SE 3.0 systems:

### Proposed Evaluation Dimensions

1. **Agent Autonomy**:
   - Percentage of tasks completed without human intervention
   - Average human decisions per feature

2. **Code Quality**:
   - Test coverage, bug density, cyclomatic complexity
   - Security vulnerabilities per line of code
   - Performance metrics (latency, memory usage)

3. **Human Productivity**:
   - Reduction in coding time
   - Increase in features implemented per sprint
   - Human satisfaction scores

4. **Team Dynamics**:
   - Agent coordination overhead (communication messages)
   - Conflict resolution rate (agent-to-agent disagreements)
   - Decision speed (time from task → completion)

5. **Trustworthiness**:
   - Audit trail completeness
   - Formal verification success rate
   - Security audit pass rate
   - Traceability (requirements → code mapping)

### Benchmark Targets (Proposed for SE 3.0)

No existing benchmarks measure SE 3.0 success. The paper proposes that future work should create:

- **SWE-3.0 Benchmark**: Long-term projects requiring multi-agent coordination, human oversight
- **Agent Team Benchmark**: Multi-agent systems solving complex software engineering tasks
- **Trust Evaluation Framework**: Measuring agent decision quality and auditability
- **Human-Agent Interaction Benchmark**: Measuring effectiveness of human-agent collaboration

## Practical Applications & Use Cases

### Use Case 1: Startup-Scale Development

**Scenario**: 10-person startup building SaaS platform

**SE 2.0 Approach**: 
- 8 developers writing code manually
- 1 QA testing
- 1 DevOps managing infrastructure

**SE 3.0 Approach**:
- 2 human developers + 5 coding agents
- 1 human QA lead + 3 testing agents
- 1 human architect + planning agents
- Humans oversee via ACE, agents execute via AEE

**Outcome**: 3x feature velocity, 50% cost reduction, maintained code quality

### Use Case 2: Legacy System Modernization

**Scenario**: 2M LOC Java/Spring system → Kotlin/Quarkus migration

**SE 3.0 Approach**:
- Architecture agent proposes migration strategy
- Multiple coding agents parallelize refactoring
- Testing agents validate compatibility
- Review agent audits security
- Human architects approve architecture changes
- Human team leads verify quality gates

**Outcome**: 6-month migration vs. 2+ years manually; agents handle mechanical transformation, humans handle strategic decisions

### Use Case 3: Security-Critical Development

**Scenario**: Financial services platform requiring PCI-DSS compliance

**SE 3.0 Approach**:
- Agents generate code with security constraints
- Review agent specialized in security auditing
- Formal verification agent proves compliance properties
- Humans make final compliance sign-off

**Outcome**: Reduced security vulnerabilities, full audit trail, provable compliance

### Use Case 4: Continuous Deployment Pipeline

**Scenario**: High-frequency deployment (10+ times/day)

**SE 3.0 Approach**:
- Agents propose optimizations and bug fixes
- Testing agents validate
- Deployment agents orchestrate rollout
- Humans monitor and can halt if needed

**Outcome**: Faster feedback loops, continuous improvement automation

## Insights & Implications

### 1. **Fundamental Shift in Software Engineering**

SE 3.0 isn't just "agents help developers"—it's a complete reconceptualization:
- **From human-centric to agent-participated**: Agents are first-class professionals
- **From sequential handoffs to asynchronous coordination**: Agent teams work in parallel
- **From implicit to explicit decision logging**: Every agent decision is auditable
- **From best-effort to verified**: Formal methods become practical at scale

### 2. **New Roles and Organizations**

SE 3.0 creates new professional roles:
- **Agent Manager**: Oversees agent team, sets policies and constraints
- **Agent Coach**: Trains/fine-tunes agents for specific domains
- **Agent Auditor**: Ensures agent decisions comply with policies
- **Human Architect**: Handles high-level strategic decisions (what agents can't do)
- **Ethical Reviewer**: Ensures agent decisions meet ethical standards

### 3. **Economics Shift**

- **Labor**: Coding becomes commodified; demand shifts to architecture and oversight
- **Quality**: Better code due to systematic agent verification, not manual review
- **Cost**: Significant reduction in development cost for routine tasks
- **Risk**: Concentration risk if all agents come from single provider/model

### 4. **Trustworthiness Crisis**

As agents gain autonomy, trustworthiness becomes existential:
- **Verification**: Can we prove agent-generated code is correct?
- **Accountability**: When something goes wrong, who's responsible?
- **Auditability**: Can we explain why an agent made a decision?
- **Safety**: How do we prevent agents from introducing security vulnerabilities?

### 5. **Research Agenda**

The paper identifies 20+ open research questions. Key priority areas:

1. **Agent coordination mechanisms** (multi-agent theory, conflict resolution)
2. **Semantic code understanding** (knowledge graphs, program synthesis)
3. **Formal verification** (proving correctness of agent-generated code)
4. **Human-agent interfaces** (natural control mechanisms for oversight)
5. **Process optimization** (workflows suited to agent teams)

## Code & Resources

### Conceptual Framework

No reference implementation provided (vision paper). However, the dual-environment architecture could be implemented using:

**ACE (Human Command Environment)**:
- Web dashboard for humans to set goals, review decisions, approve actions
- Policy engine (constraint specification language)
- Approval workflow system
- Audit log and decision tracking

**AEE (Agent Execution Environment)**:
- Agent orchestration platform (e.g., LangGraph, Autogen, ReAct framework)
- Tool/API integrations (Git, IDE, CI/CD, testing frameworks)
- Agent communication layer (message broker for agent coordination)
- Knowledge graph for codebase understanding

### Expected Implementation Stack

**Frontend (ACE)**:
- React/Vue dashboard
- Python policy engine
- PostgreSQL for audit logs

**Backend (AEE)**:
- LLM agent framework (LangChain, Claude API, or similar)
- Neo4j for knowledge graphs
- Git hooks for version control integration
- Kubernetes for distributed agent execution

### Related Tools to Build

1. **Semantic VCS**: Git extension with architectural-change tracking
2. **Agent-Native IDE**: Language server with agent-query capabilities
3. **Formal Verification Integration**: Integrate proof assistants (Coq, Lean)
4. **Agent Capability Registry**: Marketplace of agent skills/specializations

## Related Work & Context

### Foundational SE Work

- **Classic SE Models**: Waterfall, Agile, DevOps (all assume human actors)
- **Software Architecture**: Patterns and styles (need adaptation for agent teams)
- **Formal Methods**: Program verification (increasingly relevant with autonomous code)
- **Software Quality**: Metrics and processes (must evolve for agent-centric development)

### AI & Agent Work

- **Large Language Models**: Foundation for coding agents (GPT-4, Claude, Gemini)
- **Multi-Agent Systems**: Coordination, communication, conflict resolution
- **Program Synthesis**: Automated code generation (foundational for SE 3.0)
- **Reinforcement Learning**: Training agents on software tasks
- **Agentic AI**: Recent frameworks (AutoGen, LangGraph, CrewAI)

### Related Recent Papers

- Papers on autonomous coding agents (SWE-agent, OpenHands)
- Papers on multi-agent orchestration for code generation
- Papers on formal verification of LLM-generated code
- Papers on agent skill learning and composition
- Papers on human-AI collaboration in software development

### Prior SE Paradigm Shifts

**SE 1.0 → SE 2.0 (Recent)**: Introduction of AI-augmented tools
- Code completion (Copilot)
- Bug detection (DeepCode, Snyk)
- Test generation (Sapienz)
- Documentation generation (Doc writers)

**SE 2.0 → SE 3.0 (Emerging)**: Autonomous agent-driven development
- End-to-end task completion without human in loop
- Multi-agent coordination and conflict resolution
- Agent-human collaborative workflows
- Formal verification of agent decisions

## Future Research Directions

### Immediate (1-2 years)

1. **Agent Coordination Protocols**: How should agents communicate and coordinate?
2. **Semantic Codebase Understanding**: Can agents maintain full contextual awareness?
3. **Formal Verification Integration**: How to prove agent-generated code correct?
4. **Human-Agent Interfaces**: What's the right level of human oversight?

### Medium-term (2-5 years)

5. **Self-Improving Agents**: Can agents learn and improve through experience?
6. **Agent Specialization**: Should agents specialize in domains or tasks?
7. **Organizational Restructuring**: How do companies reorganize for SE 3.0?
8. **Ethical and Legal Frameworks**: Responsibility, liability, and agency

### Long-term (5+ years)

9. **Fully Autonomous Development**: Can entire projects be written by agents?
10. **Human-Agent Parity**: When will agents match human creativity and judgment?
11. **Economic Restructuring**: What's the role of humans in fully autonomous SE?
12. **Societal Impact**: How does SE 3.0 affect software development careers?

## Conclusion

Agentic Software Engineering (SE 3.0) represents a paradigm shift as significant as the introduction of programming languages or the agile revolution. By reconceptualizing the four classical SE pillars (actors, processes, tools, artifacts) in the context of autonomous agents, this paper provides the conceptual foundation for the emerging era of agent-driven software development. The dual-modality architecture (ACE + AEE) offers a practical framework for human-agent collaboration. The research roadmap highlights 20+ open questions that will drive SE research for the next decade. Organizations that understand and adapt to SE 3.0 will gain competitive advantages; those that don't risk obsolescence.
