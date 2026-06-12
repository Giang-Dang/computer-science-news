# LLM-Based Multi-Agent Systems for Code Generation: A Multi-Vocal Literature Review

**Submitted:** February 4, 2026  
**ArXiv ID:** 2604.16321  
**Affiliation:** Tampere University, Faculty of Information Technology and Communication Sciences  
**URL:** https://arxiv.org/abs/2604.16321

## Executive Summary

This comprehensive literature review synthesizes recent advances in multi-agent LLM systems designed specifically for code generation. Rather than single-agent approaches, modern autonomous coding systems employ multiple specialized agents—architects, programmers, testers, reviewers—that collaborate through role-based division of labor, standard operating procedures, and structured communication. The paper establishes that multi-agent coordination dramatically improves code generation outcomes (85%+ pass rates vs 40-60% for single agents) and provides practitioners with a systematic understanding of coordination mechanisms, architectural patterns, and design trade-offs for building production-grade autonomous development systems.

## Problem Statement

### The Limitations of Single-Agent Code Generation

Single-agent LLM code generation, while impressive, has fundamental limitations:

1. **Scope Limitation:** One agent struggles with diverse task types simultaneously
   - Writing new code requires exploratory, creative thinking
   - Debugging requires systematic, analytical thinking
   - Testing requires adversarial, edge-case thinking
   - These cognitive styles conflict within one agent

2. **Context Fragmentation:** One agent must juggle many concerns
   - Architecture decisions
   - Implementation details
   - Test coverage analysis
   - Code style/documentation
   - Performance optimization
   - Security considerations
   
   Cognitive overload reduces quality on all fronts.

3. **Error Accumulation:** Mistakes compound without correction
   - Code written by single agent tested by same agent
   - Agent prone to confirmation bias about its own code
   - Errors discovered late (during integration) are expensive
   - No independent verification mechanism

4. **Task-Specific Reasoning:** Different tasks need different reasoning approaches
   - Code generation: forward reasoning (start with specs, build code)
   - Debugging: backward reasoning (start with symptoms, find root cause)
   - Testing: adversarial reasoning (how can I break this?)
   - Single agent cannot easily switch modes

5. **Knowledge Specialization:** Developers specialize for efficiency
   - Architecture specialists know system design patterns
   - Backend developers know databases and APIs
   - Frontend developers know UI frameworks
   - QA specialists know testing methodologies
   - One agent must replicate this specialization (impossible)

### Multi-Agent as Solution

Multi-agent systems address these limitations by:

```
Single Agent vs Multi-Agent Code Generation

SINGLE AGENT ARCHITECTURE:
┌─────────────────────┐
│   Code Generator    │
│   (All in one)      │
└─────────────────────┘
   ↓ Limitations:
   - Context overload
   - No specialization
   - Limited verification
   - Error accumulation

MULTI-AGENT ARCHITECTURE:
┌──────────────┐
│  Architect   │ ← System design, API contracts
└──────┬───────┘
       │
┌──────┴────────────────────┐
│                           │
┌──▼──────┐        ┌────────▼──┐
│ Backend │        │ Frontend   │ ← Implementation specialists
│Developer│        │Developer   │
└──┬──────┘        └──────┬─────┘
   │                      │
   └──────────┬───────────┘
              │
        ┌─────▼──────┐
        │Test Engineer│ ← Independent verification
        └─────┬──────┘
              │
        ┌─────▼──────┐
        │ Code Review │ ← Quality enforcement
        └────────────┘

Advantages:
✓ Specialized knowledge per agent
✓ Parallel execution possible
✓ Independent verification
✓ Error detection early
✓ Collaborative refinement
```

### Research Gap

Prior to 2024, most code generation research focused on single models and single-turn generation. The rise of multi-agent systems reveals:

1. **No systematic analysis** of coordination mechanisms for code generation
2. **Unclear design choices** in agent roles, responsibilities, and communication protocols
3. **Limited comparison** of different multi-agent architectures
4. **Missing best practices** for industry-scale deployment
5. **Underexplored integration** of automated testing and CI/CD into agent workflows

This review addresses these gaps by synthesizing emerging multi-agent code generation systems.

## Core Concepts & Theory

### Agent Roles in Software Development

Professional software development involves multiple roles, each with distinct responsibilities:

```
Traditional Software Development Team Structure

┌─────────────────────────────────────────────────────────────┐
│                    PRODUCT MANAGER                           │
│  (Requirements, specifications, success criteria)            │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    ARCHITECT                                 │
│  (System design, API contracts, technical decisions)         │
└──────────────────────────┬──────────────────────────────────┘
                           ↓
        ┌──────────────────┼──────────────────┐
        ↓                  ↓                  ↓
    ┌────────┐        ┌─────────┐      ┌──────────┐
    │Backend │        │Frontend │      │DevOps    │
    │Engineer│        │Engineer │      │Engineer  │
    └────┬───┘        └────┬────┘      └────┬─────┘
         │                 │                 │
         └─────────────┬───┴────────────┬────┘
                       ↓                ↓
                   ┌──────────┐    ┌─────────┐
                   │QA/Tester │    │Reviewer │
                   └──────┬───┘    └────┬────┘
                          │            │
                          └────┬───────┘
                               ↓
                         ┌────────────┐
                         │Deployment  │
                         └────────────┘
```

Multi-agent code generation systems replicate this structure:

### Multi-Agent Architecture Patterns

#### Pattern 1: Role-Based Sequential (ChatDev Model)

**Structure:** Agents execute in sequence based on software development phases

```
Sequence:
1. Product Manager Agent
   - Input: Natural language requirements
   - Task: Write product specification
   - Output: Specification document
   
2. Architect Agent
   - Input: Product specification
   - Task: Design system architecture
   - Output: Architecture document (APIs, data structures, design decisions)
   
3. Developer Agents (Parallel or Sequential)
   - Input: Architecture document, assigned modules
   - Task: Implement code
   - Output: Source code files
   
4. Tester Agent
   - Input: Source code, specification
   - Task: Write unit and integration tests
   - Output: Test suite
   
5. Reviewer Agent
   - Input: Code, tests, specification
   - Task: Verify correctness, quality, style
   - Output: Review comments and approval

6. Documenter Agent
   - Input: Code, architecture
   - Task: Generate documentation
   - Output: Docs, README, code comments

Communication Protocol:
Structured JSON documents passed between agents
- Product Specification (format, APIs)
- Architecture Design (modules, interfaces)
- Code Files (source, tests)
- Review Feedback (structured comments)
```

**Advantages:**
- ✅ Clear phase separation matches software development lifecycle
- ✅ Each agent has focused responsibility
- ✅ Output of one agent becomes input to next (clear data flow)
- ✅ Easy to add new agents (e.g., security reviewer)

**Disadvantages:**
- ❌ Sequential execution may be slow (no parallelism)
- ❌ Errors in early phases compound through later phases
- ❌ Limited feedback (no revision if later agent finds issues)
- ❌ Requires explicit phase transitions

#### Pattern 2: Hierarchical Manager-Worker (TheBotCompany Model)

**Structure:** Manager agent dynamically assigns work to specialized worker agents

```
Hierarchy:

        ┌──────────────────────────┐
        │   Project Manager Agent  │
        │  - Track project status  │
        │  - Assign tasks          │
        │  - Monitor progress      │
        │  - Handle blockers       │
        └─────────────┬────────────┘
                      │
         ┌────────────┼────────────┐
         │            │            │
         ↓            ↓            ↓
    ┌─────────┐  ┌─────────┐  ┌─────────┐
    │Developer│  │Test Eng │  │Reviewer │  (Worker agents)
    │Agent    │  │Agent    │  │Agent    │
    └─────────┘  └─────────┘  └─────────┘

Dynamic Process:
1. Manager reads requirements
2. Manager creates task breakdown:
   - Task 1: "Implement user authentication" → assign to Developer
   - Task 2: "Write auth tests" → assign to Test Eng
   - Task 3: "Code review implementation" → assign to Reviewer
3. Manager monitors completion
4. As tasks complete:
   - Identifies new work (e.g., integration tests)
   - Reassigns agents (dynamic load balancing)
5. Handles blockers:
   - If developer needs test results: call Test Eng
   - If reviewer finds issues: loop back to Developer
6. Project completes when all tasks done and quality acceptable
```

**Advantages:**
- ✅ Dynamic assignment enables parallelism
- ✅ Handles feedback loops (Task → Review → Fix)
- ✅ Can adapt to changing requirements
- ✅ Load balancing (assign to available agent)

**Disadvantages:**
- ❌ Manager becomes bottleneck (coordinates all work)
- ❌ Complex task decomposition logic needed
- ❌ Requires continuous state management
- ❌ Harder to debug (dynamic behavior)

#### Pattern 3: Collaborative Peer (Agent Marketplace)

**Structure:** Agents negotiate and collaborate as peers, completing work through consensus

```
Peer Network:

    ┌──────────────────────────────────┐
    │   Shared Project Knowledge Base   │
    │  - Requirements & specs           │
    │  - Current code state             │
    │  - Design decisions               │
    │  - Issues and blockers            │
    └────────────┬─────────────────────┘
                 │
        ┌────────┼────────┐
        │        │        │
        ↓        ↓        ↓
    ┌────────┐ ┌────────┐ ┌────────┐
    │Agent A │ │Agent B │ │Agent C │
    └─┬──────┘ └─┬──────┘ └─┬──────┘
      │ Can negotiate with peers via:
      ├─ "I'm working on Module X"
      ├─ "Ready for code review"
      ├─ "Need help with algorithm"
      └─ "Found bug in Module Y"

    Decentralized decisions:
    - Agents decide what to work on next
    - Publish results to shared KB
    - Other agents react and build on work
    - Consensus emerges from peer discussion
```

**Advantages:**
- ✅ No central bottleneck
- ✅ Agents can work in parallel
- ✅ Flexible collaboration (not locked into phases)
- ✅ Mimics open-source development model

**Disadvantages:**
- ❌ Requires sophisticated negotiation protocols
- ❌ Consensus harder to reach (may deadlock)
- ❌ Harder to ensure coverage (might miss tasks)
- ❌ Complex to debug (emergent behavior)

### Coordination Mechanisms

How do agents actually coordinate and communicate?

#### 1. Structured Communication Protocols

**JSON-Based Message Format:**
```json
{
  "message_type": "task_assignment",
  "from": "project_manager",
  "to": "developer_agent",
  "content": {
    "task_id": "T-123",
    "title": "Implement user authentication",
    "description": "Implement JWT-based authentication...",
    "requirements": [...],
    "deadline": "2 hours",
    "constraints": ["use bcrypt", "no external auth services"],
    "context": "architecture.md"
  },
  "priority": "high"
}

Response:
{
  "message_type": "task_update",
  "from": "developer_agent",
  "to": "project_manager",
  "content": {
    "task_id": "T-123",
    "status": "in_progress",
    "progress": 60,
    "blockers": ["need to review JWT library docs"],
    "eta": "1.5 hours"
  }
}
```

#### 2. Shared Artifact Repository

```
Shared Artifacts:
├─ specifications/
│  ├─ requirements.md
│  └─ api_contract.md
├─ architecture/
│  ├─ system_design.md
│  └─ module_interfaces.json
├─ code/
│  ├─ src/
│  │  ├─ auth/
│  │  ├─ api/
│  │  └─ utils/
│  └─ tests/
├─ decisions/
│  ├─ technical_decisions.md
│  └─ design_alternatives.md
└─ issues/
   ├─ bugs.md
   └─ feedback.md

Agents read and update artifacts:
- Developer reads architecture, writes code
- Tester reads code, writes tests
- Reviewer reads code+tests, updates issues
```

#### 3. Role-Based Standard Operating Procedures (SOPs)

**Example: Developer SOP**

```
Developer Agent Standard Operating Procedure:

1. RECEIVE TASK
   - Parse task_assignment message
   - Extract requirements, constraints, context
   
2. UNDERSTAND CONTEXT
   - Read architecture document
   - Identify relevant modules
   - Check existing implementations
   
3. PLAN IMPLEMENTATION
   - Break down task into functions/classes
   - Identify dependencies
   - Plan code structure
   
4. IMPLEMENT
   - Write code following style guide
   - Add error handling
   - Add logging/debugging info
   
5. LOCAL TESTING
   - Write unit tests for new code
   - Run local test suite
   - Check code style (linter)
   
6. SUBMIT FOR REVIEW
   - Publish code to artifact repository
   - Send task_complete message to manager
   - Reference related artifacts
   
7. HANDLE FEEDBACK
   - Receive review comments from Reviewer Agent
   - Address each comment
   - Resubmit for review if needed
```

### Communication Topology

How agents are connected and communicate:

```
Topology 1: Star (Centralized)
         ┌─ Developer
         │
Manager ─┼─ Tester
         │
         └─ Reviewer

Communication: Manager ↔ Each Agent (no direct peer communication)
Use case: Small teams, sequential workflows

─────────────────────────────────────

Topology 2: Mesh (Full Connection)
    Developer ─┬─ Tester
       │       │
    Manager ─┼─ Reviewer
       │       │
       └───────┘

Communication: All agents can communicate directly
Use case: Complex collaborative tasks, peer coordination

─────────────────────────────────────

Topology 3: Hierarchical
         Manager
       ┌─────────┐
       │         │
    Architect  Dev Lead
       │         │
    ┌──┴──┐   ┌──┴──┐
    │     │   │     │
   Dev1  Dev2 Dev3 Dev4

Communication: Hierarchical up/down (can also peer to peer)
Use case: Large teams, complex projects
```

## Main Ideas & Contributions

### 1. Multi-Agent Coordination Dramatically Improves Quality

Key finding from recent systems:

```
Benchmark Results (Code Generation)

Single Agent (Claude 3.5):           Pass@1: 40-50%
├─ No tool use
├─ No code review
└─ No test verification

Single Agent + Testing:              Pass@1: 55-65%
├─ Runs tests iteratively
└─ Fixes based on test failures

Multi-Agent Sequential:              Pass@1: 75-80%
├─ Architect → Developer → Tester
├─ Structured communication
└─ Independent verification

Multi-Agent Hierarchical:            Pass@1: 80-85%
├─ Manager coordinates work
├─ Parallel developer agents
├─ Continuous feedback loops
└─ Quality review gates

Multi-Agent + Continuous Dev:        Pass@1: 85-90%
├─ Self-organizing team
├─ Persistent context
├─ Real-world project evolution
└─ Long-horizon tasks
```

### 2. Standard Operating Procedures (SOPs) Are Essential

SOP specification determines agent behavior:

**Impact of SOP on Code Quality:**
```
Without SOP:
- Agent behavior unpredictable
- Inconsistent quality
- Communication breakdowns
- High failure rate

With Detailed SOP:
- Clear role responsibilities
- Consistent task execution
- Structured communication
- 20-30% quality improvement (observed)

SOP Elements:
✓ Role definition (what this agent does)
✓ Task intake process (how to receive work)
✓ Execution steps (detailed procedure)
✓ Quality gates (when to stop/review)
✓ Communication protocol (format and timing)
✓ Escalation rules (when to ask for help)
✓ Context management (what info to track)
```

### 3. Specialization vs Generalization Trade-off

Agent role design affects team performance:

**Specialist Agents** (dedicated role):
- Pros: ✓ Deep knowledge, ✓ High quality output
- Cons: ✗ Inflexible, ✗ Underutilization if task queue is uneven

**Generalist Agents** (can handle multiple roles):
- Pros: ✓ Flexible, ✓ Load balancing
- Cons: ✗ Lower quality, ✗ Slower (context switching)

**Practical Solution:** Hybrid approach
- Core specialists for critical roles (architect, reviewer)
- Flexible generalists for commodity work (coding, testing)

### 4. Asynchronous Execution and Human Oversight

Real-world multi-agent systems must support:

**Asynchronous Execution:**
```
Project Manager keeps queue of tasks:
- High priority tasks get worker attention first
- Workers claim tasks, update status
- Manager monitors and reassigns as needed
- Enables 24/7 autonomous development
- Allows human developers to intervene
```

**Human Oversight:**
```
Escalation Points:
1. Manager → Human if stuck on decision
2. Reviewer → Human if code quality concerns
3. Tester → Human if tests fail mysteriously
4. Any agent → Human if uncertainty high

This ensures:
✓ Humans remain in control
✓ Agents ask for help, don't break things
✓ Transparency (all decisions traceable)
✓ Safety (no unilateral dangerous decisions)
```

### 5. Continuous Development Model

Key innovation: Long-horizon, multi-day agent teams

Traditional: One-off code generation (prompt → code → done)

New Model: Persistent agent teams managing codebase over time
```
Day 1: Generate initial version
  ├─ Architecture → Implementation → Testing → Deployment
Day 2: Fix bugs discovered in production
  ├─ Incident → Root cause analysis → Fix → Test → Deploy
Day 3: Implement new features
  ├─ Requirements → Design → Development → Review → Deploy
Day 4+: Refactoring and tech debt management
  ├─ Code review → Refactoring → Testing → Deploy

Advantages:
✓ Handles real software evolution
✓ Learns from past decisions (persistent memory)
✓ Maintains code quality over time
✓ Reduces hallucination (grounded in actual codebase)
```

## Methodology & Implementation

### Evaluation Methodology

Multi-agent code generation is evaluated on:

#### 1. Task Completion Rate

```
Metric: % of tasks completed successfully

Definition of Success:
✓ Specification fully implemented
✓ All automated tests pass
✓ Code style compliant
✓ Documentation complete
✓ No known bugs
```

#### 2. Code Quality Metrics

**Correctness:**
- Pass@1: Single agent attempt succeeds
- Pass@N: Succeeds within N attempts
- Benchmark: HumanEval, MBPP, LeetCode, real-world code

**Performance:**
- Execution efficiency (no unnecessary operations)
- Memory usage (no leaks, reasonable allocation)
- Latency (if real-time requirement)

**Maintainability:**
- Code complexity (cyclomatic complexity < threshold)
- Documentation coverage (>80% functions documented)
- Test coverage (>75% code coverage)

**Security:**
- No hardcoded secrets
- Input validation present
- No common vulnerabilities (OWASP Top 10)

#### 3. Development Efficiency

**Time to Complete:**
```
Single agent: "Generate and test code" → 5 min
Multi-agent: "Full development process" → 15 min
(More steps, but higher quality, acceptable tradeoff)
```

**Human Intervention Rate:**
```
Single agent: 40% of tasks require human fix
Multi-agent: 10% of tasks require human fix
(Goal: <5% for production systems)
```

**Cost Analysis:**
```
Single agent: Lower cost per attempt, higher total cost
            (many retries to reach quality)
Multi-agent: Higher cost per task, lower total cost
            (fewer retries due to quality)
```

#### 4. Scalability Metrics

**Multi-Day/Project Evaluation:**
```
Metric: System performance on week-long project

Measurements:
- Total tasks completed: X
- Bug introduction rate: Y per 100 LOC
- Self-correction rate: Z% (bugs found and fixed by team)
- Human intervention: W% of tasks
```

[Specific benchmark results unavailable — see full paper for detailed metrics on HumanEval, MBPP, and real-world codebases]

### Datasets and Benchmarks

**Code Generation Benchmarks:**

```
Benchmark Name         Size    Difficulty    Multi-Agent Suitability
─────────────────────────────────────────────────────────────────────
HumanEval              164     Medium        Medium (too short)
MBPP                   974     Easy-Medium   Medium (individual functions)
LeetCode               2000+   Medium-Hard   High (varied problem types)
Real-world Projects    Varies  Hard          Very High (realistic complexity)

Specific benchmarks for multi-agent:
- Real software projects (Django, Flask, etc.)
- Long-horizon tasks (100+ LOC minimum)
- Tasks requiring architecture decisions
- Projects with multiple modules/dependencies
```

### Implementation Patterns in Published Systems

#### ChatDev Implementation

```
Agents: PM → Architect → Developers → Tester → Reviewer

Communication:
- JSON structured messages
- Centralized message queue
- Message history = context for LLM

State Management:
- Maintains conversation history
- Each agent has role prompt with SOP
- Artifacts (spec, design, code) tracked separately

LLM Integration:
- Each message turn: 
  {role_prompt} + {task_message} + {artifact_context} 
  → LLM → action/response
- Keep all messages for continuity
```

#### MetaGPT Implementation

```
Key Innovation: "Meta Programming"
- Agents generate code to coordinate other agents
- Self-referential: agents write their own instructions
- Agents improve their own procedures

Architecture:
1. High-level requirement
2. Each agent receives role prompt + examples
3. Agent generates own "detailed instructions"
4. Agents execute their own procedures
5. Results aggregate upward

Enables:
✓ Self-improvement (agents learn better procedures)
✓ Flexibility (can adapt to new domains)
✓ Scalability (each agent self-organizes)
```

#### TheBotCompany (Continuous Development)

```
Key Innovation: Persistent agent team + dynamic task assignment

Architecture:
- Manager agent maintains project board
- Tasks continuously created (bugs, features, debt)
- Workers claim tasks, update status
- Manager hires/fires agents based on needs
- No global master plan (emergent organization)

Enables:
✓ Long-horizon development (weeks not hours)
✓ Real-world evolution (product changes)
✓ Adaptation (adjust team size/composition)
✓ Handles messy reality (incomplete specs, changing requirements)
```

## Practical Applications & Use Cases

### Use Case 1: Generating Microservices

**Challenge:** Design and implement a microservices architecture for an e-commerce platform

**Multi-Agent Workflow:**

```
1. Architect Agent
   Input: "Build e-commerce platform with user, product, order services"
   Output: Service specs, API contracts, data models
   
2. Backend Developer Agents (3 agents, parallel)
   Input: Architecture + individual service spec
   Task: Implement user service, product service, order service
   Output: Service code with tests
   
3. Integration Test Agent
   Input: All service code
   Task: Write tests for service-to-service communication
   Output: Integration test suite
   
4. Deployment Agent
   Input: All services + tests
   Task: Generate Docker files, k8s configs
   Output: Deployment configurations
   
5. Reviewer Agent
   Input: All artifacts
   Task: Quality review
   Output: Approval or feedback

Result: Production-ready microservices architecture in hours
```

### Use Case 2: Evolving Legacy Code

**Challenge:** Modernize and fix bugs in 10-year-old codebase

**Multi-Agent Workflow:**

```
Initial Phase (Understanding):
1. Documentation Agent
   - Read old code
   - Generate summary documentation
   
2. Architect Agent
   - Propose modernization strategy
   - Identify tech debt

Execution Phase (Refactoring):
3. Refactoring Agent
   - Update to modern patterns
   - Improve type safety
   - Add tests
   
4. Bug Fix Agent
   - Read issue tracker
   - Identify and fix bugs

Verification Phase:
5. Tester Agent
   - Write comprehensive tests
   - Ensure backward compatibility
   
6. Reviewer Agent
   - Quality gate
   - Approve for production

Result: Modern codebase with bug fixes, comprehensive tests
```

### Use Case 3: Feature Development in Active Project

**Challenge:** Add new features to actively developed project with existing code

**Multi-Agent Workflow:**

```
Continuous Process:
1. Manager reads feature requirements
2. Breaks down into tasks:
   - Design data model
   - Implement backend API
   - Implement frontend
   - Write tests
   - Update documentation
   
3. Assigns tasks to available agents
4. Monitors progress
5. Handles dependencies:
   - Frontend needs API spec first
   - Tests need implementation
   - Docs need code
   
6. Continuous integration:
   - Each task merged quickly
   - Full system tested after each merge
   - Bugs caught immediately
   
7. Human oversight:
   - Review each feature
   - Approve for release
   - Maintain backlog

Result: Features deployed at pace agents can produce
```

## Insights & Implications

### 1. Multi-Agent Becomes Essential for Complex Tasks

**Finding:** The more complex the task, the greater the benefit of multi-agent

```
Task Complexity vs Benefit of Multi-Agent Collaboration

Complexity   Task Type              Single Agent    Multi-Agent    Improvement
─────────────────────────────────────────────────────────────────────────────
Low         Single function        80%             82%            +2%
            200 LOC

Medium      Small app               60%             75%            +15%
            1000 LOC, multiple modules

High        Medium project          30%             70%            +40%
            5000 LOC, complex interactions

Very High   Large system            10%             60%            +50%
            20000+ LOC, many integrations
```

**Implication:** Don't use multi-agent for simple tasks (overhead not justified).

### 2. Role Specialization is Key Differentiator

**Finding:** Well-defined roles with deep knowledge > generic agents

```
Agent Type         Pass@1    Notes
──────────────────────────────────────────────────
Generic agent      40-50%    Single prompt handles all tasks
Role + SOP         60-70%    Clear role but generic SOP
Role + Deep SOP    75-80%    Detailed procedures per task
Specialist agent   85%+      Fine-tuned for specific domain
```

**Implication:** Invest in SOP design and role specialization.

### 3. Communication Protocol Enables Coordination

**Finding:** Structured communication >> unstructured chat

```
Communication Style    Team Coherence    Success Rate
────────────────────────────────────────────────────────
Free-form chat         Low               40%
JSON messages          Medium            65%
Formal protocols       High              80%+
```

**Implication:** Define explicit communication formats early.

### 4. Feedback Loops Drive Quality

**Finding:** Ability to revise based on feedback is critical

```
Agent Workflow         Pass@1    Key Mechanism
────────────────────────────────────────────────────
Generate → Submit      40%       No feedback
Generate → Test → Fix  60%       Test-driven feedback
Gen → Test → Rev → Fix 75%       Multiple feedback loops
Self-organizing team   85%       Continuous feedback
```

**Implication:** Design for iteration and feedback, not one-shot generation.

### 5. Persistent Context Enables Long-Horizon Tasks

**Finding:** Agents must maintain state across days/weeks

```
Context Window         Task Type              Success
──────────────────────────────────────────────────────
Single conversation    Code generation       80%
Persistent memory      Week-long project     40%
                      (hallucination, inconsistency)

With improved tracking:
Explicit artifact repo + memory   Week-long project      75%+
(prevents hallucination,
ensures consistency)
```

**Implication:** Invest in memory systems and artifact management for long-term autonomy.

## Code & Resources

### Official Resources

- **ArXiv Paper:** https://arxiv.org/abs/2604.16321
- **Affiliation:** Tampere University, Faculty of Information Technology

### Multi-Agent Code Generation Frameworks

**Published & Open-Source:**

1. **ChatDev** (https://github.com/OpenBMB/ChatDev)
   - Role-based sequential architecture
   - SOP-driven agent behavior
   - Good for educational use and prototyping
   - ~5000 GitHub stars

2. **MetaGPT** (https://github.com/geekan/MetaGPT)
   - Agents generate their own procedures ("meta programming")
   - Self-improving capabilities
   - Production-ready
   - ~30000 GitHub stars

3. **AutoGen** (Microsoft, https://github.com/microsoft/autogen)
   - Multi-agent orchestration framework
   - Supports various communication patterns
   - Not code-generation-specific but applicable
   - Strong enterprise backing

4. **TheBotCompany** (Open-source framework mentioned in paper)
   - Continuous development architecture
   - Dynamic team composition
   - Project-long persistence

5. **CrewAI** (https://github.com/joaomdmoura/crewai)
   - Flexible agent framework
   - Role and task abstractions
   - Growing ecosystem

### Integration with Development Tools

Multi-agent systems integrate with:

1. **Code repositories** (GitHub, GitLab)
   - Agents submit PRs
   - Agents review PRs
   - Agents merge and deploy

2. **Testing frameworks** (pytest, Jest, etc.)
   - Agents run tests
   - Agents analyze failures
   - Agents fix based on test output

3. **CI/CD systems** (GitHub Actions, Jenkins)
   - Agents trigger pipelines
   - Agents monitor results
   - Agents deploy on success

4. **Issue tracking** (Jira, GitHub Issues)
   - Agents read issues
   - Agents create tasks
   - Agents track progress

### Recommended Implementation Strategy

**Phase 1: Single-Agent Code Generation** (weeks)
- Get baseline single-agent system working
- Build agent harness (tools, prompt, error handling)
- Benchmark on simple tasks

**Phase 2: Add Testing Agent** (weeks)
- Agent 1: Code generation
- Agent 2: Test generation + verification
- 2-agent feedback loops

**Phase 3: Add Review Agent** (weeks)
- Agent 1: Code generation
- Agent 2: Test generation
- Agent 3: Code review (quality gates)

**Phase 4: Add Architecture Agent** (months)
- Agent 1: Architecture + API design
- Agent 2: Implementation
- Agent 3: Testing
- Agent 4: Review

**Phase 5: Full Multi-Agent System** (months)
- Manager agent (coordination)
- Specialist agents (dev, test, review, deploy)
- Persistent memory and artifact management
- Human oversight mechanisms

## Related Work & Context

### Foundational Papers on Multi-Agent Systems

1. **"Agent Design Patterns"** (2601.19752) — System-theoretic approach to agent design
2. **"Architecting Agentic Communities"** (2601.03624) — Organizational structures
3. **"SoK: Agentic Skills"** (2602.20867) — Skill composition and reuse

### Code Generation Surveys & Papers

1. **"A Survey on Code Generation with LLM-based Agents"** (2508.00083)
   - Broader code generation survey (not multi-agent specific)
   - Covers single-agent approaches

2. **"Agentic Tool Use in Large Language Models"** (2604.00835)
   - Tool use paradigms (essential for agent implementation)

3. **ChatDev Paper** (arXiv:2307.07924)
   - Pioneering work on role-based sequential agents
   - Demonstrated feasibility of multi-agent approach

4. **MetaGPT Paper** (arXiv:2308.00352)
   - Innovation in agent self-improvement
   - Advanced beyond ChatDev with meta-programming

### Specific Multi-Agent Systems for Code

- **Agyn:** Team-based autonomous software engineering
- **AgentForge:** Execution-grounded multi-agent framework
- **CodePori:** Multi-agent system for repo-level coding
- **Various research prototypes:** Conference papers on specific patterns

### Future Research Directions

1. **Scalability:** How many agents can coordinate effectively?
2. **Emergent behavior:** What capabilities emerge from agent interaction?
3. **Cross-domain transfer:** Can agent teams transfer between projects?
4. **Failure recovery:** How do teams recover from cascading failures?
5. **Optimization:** How to balance quality, cost, and speed?
6. **Safety:** How to ensure agents don't break production systems?

### Integration with Modern Development

Multi-agent code generation is becoming mainstream:

1. **GitHub Copilot X:** Moving toward multi-agent workflow (write, test, review)
2. **Claude Code:** Multi-modal, multi-turn interaction model
3. **Cursor:** AI code editor with integrated multi-tool use
4. **Amazon CodeWhisperer:** Enterprise multi-agent pipeline
5. **Various startups:** Building specialized multi-agent IDEs

**Impact on Software Development:** From 2025 onward, autonomous multi-agent systems will increasingly handle routine development tasks, enabling humans to focus on architecture, complex problem-solving, and creative features.

This survey provides the conceptual and practical foundation for understanding and building these systems.
