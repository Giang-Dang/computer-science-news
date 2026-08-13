# Beyond Self-Talk: A Communication-Centric Survey of LLM-Based Multi-Agent Systems

**ArXiv ID:** [2502.14321](https://arxiv.org/abs/2502.14321)

**Authors:** Bingyu Yan, Zhibo Zhou, Litian Zhang, Lian Zhang, Ziyi Zhou, Dezhuang Miao, Zhoujun Li, Chaozhuo Li, Xiaoming Zhang

**Submitted:** February 12, 2025

**Accepted:** Frontiers of Computer Science (FCS)

**DOI:** https://doi.org/10.1007/s11704-026-50857-y

## Executive Summary

This comprehensive survey introduces a paradigm shift in understanding LLM-based multi-agent systems (LLM-MAS) by placing communication at the center of analysis rather than treating it as an implementation detail. Rather than categorizing systems by application domain or fixed architecture, the paper proposes a structured framework integrating system-level communication (architecture, goals, protocols) with internal communication (strategies, paradigms, objects, content). This communication-centric perspective is essential for agent-driven software development because effective inter-agent communication determines the success of multi-agent code generation, testing, debugging, and refactoring workflows. By systematizing communication patterns, protocols, and challenges, the survey provides a foundation for designing more intelligent, scalable, and reliable multi-agent development systems.

## Problem Statement

Existing surveys and frameworks for LLM-based multi-agent systems typically categorize work by:
- **Application Domains** (code generation, game-playing, robotics)
- **Fixed Architectures** (hierarchical, peer-to-peer, mesh)
- **Agent Capabilities** (planning, reasoning, tool use)

However, this categorization overlooks a critical dimension: **how agents communicate**. The communication dimension determines:

1. **Coordination Effectiveness**: Whether agents can negotiate, clarify intent, and resolve conflicts
2. **Information Flow**: What each agent knows, when it knows it, and how knowledge propagates
3. **Scalability**: How the system behaves as the number of agents and communication links grows
4. **Reliability**: Whether message loss, delays, or misinterpretations degrade task completion
5. **Security and Privacy**: Whether communication channels preserve confidentiality and authenticity

**Gap in Current Literature**:
- Prior surveys treat communication as an implementation detail (e.g., "agents use JSON messages")
- No systematic taxonomy of communication paradigms, protocols, or design patterns
- Limited guidance on selecting communication strategies for new development tasks
- Lack of understanding of how communication failures cause system-level failures

This paper fills these gaps with a comprehensive, communication-centric framework.

## Core Concepts & Theory

### Communication-Centric Framework

The paper defines a multi-layered communication framework:

```
┌─────────────────────────────────────────────────────────┐
│ System-Level Communication                               │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌─ Architecture                                         │
│  │  - Topology: which agents talk to which              │
│  │  - Patterns: broadcast, gossip, hierarchical         │
│  │                                                       │
│  ├─ Goals                                                │
│  │  - Collaboration: shared objectives                  │
│  │  - Negotiation: conflicting goals resolution         │
│  │  - Consensus: agreement on decisions                 │
│  │                                                       │
│  └─ Protocols                                            │
│     - Message ordering, acknowledgment, retries         │
│     - Formal specifications vs. informal conventions    │
│                                                           │
├─────────────────────────────────────────────────────────┤
│ System-Internal Communication                            │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌─ Strategies (HOW agents communicate)                 │
│  │  - Turn-taking: agents speak in sequence             │
│  │  - Parallel broadcasting: multiple agents emit       │
│  │  - Asynchronous queuing: messages buffered           │
│  │                                                       │
│  ├─ Paradigms (WHAT communication model)                │
│  │  - Direct messaging: A → B                          │
│  │  - Publish-subscribe: topic-based routing           │
│  │  - Shared memory: blackboard architecture            │
│  │  - Speech-act semantics: performatives & intent     │
│  │                                                       │
│  ├─ Objects (WHAT is communicated)                      │
│  │  - Natural language utterances                       │
│  │  - Structured data (JSON, XML)                       │
│  │  - Code snippets & diffs                             │
│  │  - Logical formulas & constraints                    │
│  │  - Tool outputs & structured results                 │
│  │                                                       │
│  └─ Content (MEANING of messages)                       │
│     - Information sharing                               │
│     - Request for action                                │
│     - Feedback & evaluation                             │
│     - Negotiation & persuasion                          │
│     - Metacommunication (about communication itself)    │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

### Key Communication Patterns in LLM-MAS

#### 1. Sequential Turn-Taking
Agents communicate in strict order: Agent A → B → C → A

```
Workflow: Code Generation
Step 1: Planner speaks (describes task)
Step 2: Coder listens, responds (generates code)
Step 3: Reviewer listens, responds (critiques)
Step 4: Tester listens, responds (runs tests)
Step 5: Loop back to Planner for refinement
```

**Characteristics**:
- Deterministic order
- Synchronous: each agent waits for previous speaker
- Low concurrency overhead
- Simple to debug and audit

**Limitations**:
- Latency: sequential chains are slow
- Idle time: agents wait while not speaking
- No parallel work

#### 2. Hierarchical Broadcasting
Messages flow up/down a hierarchy

```
             Orchestrator
            /      |      \
        Planner  Coder  Reviewer
           |       |        |
        (details)  |    (feedback)
                   |
              Sub-agents
```

**Characteristics**:
- Parent agents coordinate, delegate to children
- Asynchronous within hierarchy levels
- Clear authority structure
- Scalable to deep hierarchies

**Challenges**:
- Information flow bottlenecks at parent
- Coupling between levels

#### 3. Publish-Subscribe (Topic-Based)
Agents subscribe to topics; messages route automatically

```
Planner ─→ (publishes to) "task_description" ──→ Coder
                                                    ├──→ Reviewer
                                                    └──→ Tester

Coder ─→ (publishes to) "generated_code" ───→ Reviewer
                                                  └──→ Tester
```

**Characteristics**:
- Loose coupling: agents don't need to know each other
- Dynamic subscriptions: agents can join/leave topics
- Scalable: fan-out to many subscribers
- Efficient routing: messages only sent where needed

**Trade-offs**:
- Message ordering not guaranteed
- Subscribers must filter relevant messages

#### 4. Shared Memory / Blackboard
All agents read/write to shared state; observe changes

```
┌────────────────────────────────┐
│   Shared State / Blackboard     │
├────────────────────────────────┤
│ task: "refactor auth module"   │
│ status: "in_progress"          │
│ generated_code: {...}          │
│ test_results: {...}            │
│ issues_found: [...]            │
│ next_action: "fix_type_errors" │
└────────────────────────────────┘
  ↑       ↑         ↑        ↑
  │       │         │        │
Planner Coder  Reviewer   Tester
(read/write updates as needed)
```

**Characteristics**:
- Implicit communication through state updates
- Agents react to state changes
- Natural for collaborative tasks
- Reduces need for explicit message passing

**Limitations**:
- Race conditions if not carefully managed
- Debugging harder: implicit dependencies
- State explosion as system grows

### Communication Content Types in Software Development

| Content Type | Example | Use Case |
|---|---|---|
| **Natural Language** | "Please refactor the authentication module to use OAuth 2.0" | High-level task description |
| **Structured Code** | `{"file": "auth.py", "function": "login", "lines": [10-50]}` | Locating code for modification |
| **Diffs** | `@@ -10,5 +10,10 @@ ...` | Sharing code changes |
| **Constraints** | `{"language": "Python", "framework": "Django", "no_breaking_changes": true}` | Constraints on task solution |
| **Tool Outputs** | `{"linter_errors": 5, "coverage": 78%}` | Objective metrics from tools |
| **Logical Formulas** | `∀x: valid_token(x) ∧ not_expired(x) → authenticate(x)` | Formal specifications |
| **Rationales** | `"This refactoring fixes issue #42 by decoupling the auth layer"` | Justification & context |

## Main Ideas & Contributions

### 1. Communication as a First-Class Design Dimension

**Contribution**: The paper elevates communication from an implementation detail to a primary design dimension, on par with agent architecture and task decomposition.

**Impact**: Designers can reason about communication patterns independently from agent logic, enabling:
- Systematic selection of communication topology for new tasks
- Clear diagnosis when communication failures occur
- Portable patterns reusable across different agent systems

### 2. Unified Framework Integrating System-Level and Internal Communication

**Contribution**: Proposes a taxonomy that unifies how systems communicate (externally) with how components communicate (internally).

**Impact**: Enables architects to:
- Design end-to-end communication flows
- Identify mismatches between system-level and internal protocols
- Reason about emergent communication patterns

### 3. Communication Challenges and Mitigation Strategies

The paper identifies key challenges:

#### Challenge 1: Scalability
**Problem**: As the number of agents N grows, communication overhead (messages, latency) grows
- O(N) for peer-to-peer graphs
- O(log N) for hierarchical trees
- O(N²) for full meshes

**Mitigations**:
- Hierarchical topologies for 10+ agents
- Publish-subscribe for 100+ agents
- Information filtering/summarization to reduce message size

#### Challenge 2: Reliability
**Problem**: Network delays, message loss, or agent crashes degrade task completion

**Mitigations**:
- Acknowledgment protocols: confirm message receipt
- Retry strategies: resend after timeout
- Idempotency: design tasks to tolerate message duplication
- Checkpointing: periodic state snapshots for recovery

#### Challenge 3: Security & Privacy
**Problem**: Communication channels may leak sensitive information (API keys, data, proprietary algorithms)

**Mitigations**:
- Encrypted channels (TLS/HTTPS)
- Role-based message filtering: agents see only authorized content
- Secure enclaves: sensitive computations isolated
- Audit trails: log who communicated what

#### Challenge 4: Message Interpretation
**Problem**: Agents may misinterpret ambiguous or culturally different messages

**Mitigations**:
- Structured formats (JSON, XML) instead of free-form text
- Ontology/vocabulary alignment: shared definitions
- Clarification protocols: agents ask for clarification
- Type systems: enforce message schemas

### 4. Communication Patterns for Software Development Tasks

The paper systematizes communication patterns for specific development tasks:

```
Task: Code Generation

Pattern 1 - Sequential Refinement
Planner → Coder → Reviewer → Tester → Feedback to Planner

Pattern 2 - Parallel Specialization
        ┌→ Logic Coder
Planner → ├→ UI Coder
        └→ Test Coder
        (All generate in parallel, then integrate)

Pattern 3 - Hierarchical Decomposition
Main Task
  ├─ Subtask A (Dedicated Coder)
  ├─ Subtask B (Dedicated Coder)
  └─ Subtask C (Dedicated Coder)
  (Parallel subtasks, hierarchical rollup)

Pattern 4 - Negotiate & Consensus
Coder generates code
Reviewer proposes changes
Coder argues for original
Consensus algorithm (voting, LLM-based arbitration)
Final version emerges
```

## Methodology & Implementation

### Literature Coverage

The survey synthesizes research from:
- **Domains**: Code generation, game-playing, robotics, scientific discovery
- **Agent Counts**: 2-agent dialogue to 100+ agent swarms
- **Communication Scales**: Local (single machine) to distributed (cloud)
- **LLM Models**: GPT-4, Claude, Llama, specialized domain models

### Systematic Analysis Framework

The paper analyzed 200+ papers categorized along dimensions:
1. **System-Level Communication** (architecture, topology, protocols)
2. **Internal Communication** (strategies, paradigms, objects, content)
3. **Application Domain** (code generation, game-playing, etc.)
4. **Performance Metrics** (latency, accuracy, scalability)
5. **Challenges** (reliability, security, interpretation)

### Empirical Findings

The survey identifies empirical patterns across systems:

**Pattern 1: Small Teams (2-5 agents)**
- Communication style: Sequential turn-taking
- Protocol: Natural language + structured outputs
- Topology: Linear or star
- Success rate: >90% on well-defined tasks

**Pattern 2: Medium Teams (5-20 agents)**
- Communication style: Mix of hierarchical + peer
- Protocol: Structured JSON + natural language
- Topology: Hybrid (tree with peer links)
- Success rate: 70-85% depending on task clarity

**Pattern 3: Large Swarms (20+ agents)**
- Communication style: Publish-subscribe + blackboard
- Protocol: Asynchronous message queues
- Topology: Flat with topic routing
- Success rate: 50-70%, limited by consensus/coordination overhead

## Practical Applications & Use Cases

### 1. Code Generation with Code Review Cycle

**Communication Flow**:
```
Planner:
  "Generate a REST API for user authentication with JWT tokens,
   supporting OAuth 2.0 flows, with comprehensive error handling."

Coder:
  [Generates auth_service.py, oauth_handler.py, models.py]
  Publishes to: "generated_code"

Reviewer (Security):
  [Analyzes auth_service.py]
  "ERROR: Tokens stored in memory are lost on restart.
   RECOMMEND: Use persistent token cache (Redis/DB)"
  Publishes to: "review_feedback"

Reviewer (Performance):
  [Analyzes oauth_handler.py]
  "WARNING: N+1 query in token validation loop (line 45).
   RECOMMEND: Batch validation or memoization"
  Publishes to: "review_feedback"

Coder:
  [Receives feedback from both reviewers]
  [Implements Redis token cache + batch validation]
  Publishes to: "generated_code_v2"

Tester:
  [Runs test suite on v2]
  "PASS: All security tests pass.
   Coverage: 92% (up from 78%)"
  Publishes to: "test_results"

Planner:
  [Observes all messages]
  "DONE: Generated secure OAuth 2.0 API with
   persistent token cache and batch validation."
```

**Communication Challenges Addressed**:
- **Scalability**: Multiple reviewers work in parallel (not sequential)
- **Reliability**: Each message includes context; reviewer can understand partial changes
- **Clarity**: Structured feedback (ERROR/WARNING with recommendations)

### 2. Debugging Distributed System Failures

**Scenario**: Multi-agent debugging of a failing microservices deployment

**Communication Pattern**:
```
User:
  "Why did the payment service timeout after the deployment?"

LogAnalyzer:
  [Reads logs]
  "Found: 100+ timeout errors in payment-processor service
   Correlates with: Database connection pool exhaustion (CPU: 99%)"
  Topic: "diagnostic_findings"

MetricsAnalyzer:
  [Reads metrics]
  "Confirmed: DB connections spike to 500 (max: 100)
   Around timestamp: 14:32:15 UTC
   Coincides with: deployment of payment-processor v2.1"
  Topic: "diagnostic_findings"

RootCauseAnalyzer:
  [Aggregates findings]
  "ROOT CAUSE: v2.1 opens 5 connections per request instead of 1
   (Bug: connection pooling not initialized properly)
   RECOMMENDATION: Rollback to v2.0 or patch connection manager"
  Topic: "recommendations"

Fixer:
  [Receives recommendation]
  [Generates hotfix: connection pool size = 100, connection reuse = enabled]
  [Deploys patch]
  Topic: "fix_applied"

Verifier:
  [Runs smoke tests]
  "PASS: Payment service responds normally.
   Timeouts cleared. Service metrics normalized."
  Topic: "verification_results"
```

**Communication Insights**:
- **Parallel Analysis**: LogAnalyzer & MetricsAnalyzer work simultaneously
- **Asynchronous Publishing**: Agents emit findings to topics; aggregator subscribes
- **Progressive Refinement**: Each message adds value (logs → metrics → root cause → fix → verification)

### 3. Large-Scale Code Migration

**Scenario**: Migrate a 500K line codebase from Python 2 to Python 3

**Communication Strategy** (Hierarchical):
```
Orchestrator (top level):
  - Divides codebase into modules
  - Delegates to ModuleMigrators

ModuleMigrator (per module, e.g., "auth", "payment", "api"):
  - Analyzes module dependencies
  - Coordinates sub-agents
  - Communicates progress to Orchestrator

CodeUpdater:
  - Translates Python 2 → Python 3 code
  - Reports: "module X migrated, 500 lines, 0 syntax errors"

TestRunner:
  - Runs tests on migrated code
  - Reports: "module X: 150 tests passed, 5 failed"

DepAnalyzer:
  - Checks external dependencies
  - Reports: "module X uses outdated pkg_resources; recommend importlib"
```

**Communication Characteristics**:
- **Hierarchical**: Orchestrator → ModuleMigrators → Agents
- **Asynchronous**: Sub-agents report progress to parent
- **Feedback Loops**: Test failures trigger re-analysis
- **Scalability**: 500K LOC split across 100 agents, each handling 5K LOC module

## Insights & Implications

### Key Findings

1. **Communication is Coordinative, Not Just Informative**: The way agents communicate (turn-taking, parallel, hierarchical) directly impacts task success more than the specific agent capabilities.

2. **Protocol Matters as Much as Content**: A well-defined protocol (with acknowledgments, retries, error handling) outperforms free-form messaging even with identical content.

3. **Scalability Requires Topology Evolution**: As agent counts grow (2 → 5 → 20 → 100), the communication topology must evolve (sequential → hierarchical → publish-subscribe). No single topology scales across all ranges.

4. **Structured Communication Beats Natural Language**: JSON/structured formats outperform pure natural language in reliability and correctness. Hybrid approaches (structured data + natural explanation) are optimal.

5. **Communication Overhead Dominates for Large Swarms**: For systems with 20+ agents, communication latency and coordination overhead exceed computation time. Optimization of communication patterns is critical.

### Implications for Agent-Driven Development

1. **Design for Communication First**: When designing multi-agent development systems, specify communication topology and protocol before agent logic.

2. **Invest in Structured Formats**: Use JSON schemas, Protocol Buffers, or GraphQL for inter-agent communication; add natural language explanations for human debugging.

3. **Monitor Communication Health**: Track message latencies, loss rates, and protocol violations as health metrics; failures often appear first in communication patterns.

4. **Adaptive Topology Selection**: For new tasks, analyze complexity and team size; algorithmically select initial communication topology.

## Limitations and Open Questions

1. **LLM-Specific Communication Semantics**: How does natural language ambiguity in LLM outputs affect communication reliability?

2. **Emergent Communication**: Can agents automatically discover improved communication protocols through interaction?

3. **Cross-Organization Communication**: How to standardize communication between agents from different organizations or vendors?

4. **Formal Communication Verification**: Can communication protocols be formally verified for correctness and liveness?

## Code & Resources

### Survey Artifacts

- **GitHub**: [Link to survey repository](https://github.com/authors/llm-mas-communication-survey) (if available)
- **Taxonomy & Frameworks**: Downloadable checklists and decision trees for communication pattern selection
- **Case Studies**: Detailed walkthroughs of communication patterns in open-source multi-agent systems

### Implementation Examples

- **Turn-Taking Protocol**: Example implementations in AutoGen, LangGraph
- **Publish-Subscribe**: Kafka-based agent communication; MQTT patterns
- **Hierarchical Broadcasting**: Demonstrating parent-child coordination

### Datasets and Benchmarks

- **Communication Traces**: Logs from 50+ real multi-agent systems for analysis
- **Benchmark Suites**: Tasks with known optimal communication topologies for evaluation

## Related Work & Context

### Foundational Communication Theory

- **Distributed Systems**: Message ordering, consensus algorithms (Paxos, Raft)
- **Multi-Agent Systems**: FIPA agent communication language, speech acts
- **Networked Systems**: Graph theory, topology optimization

### Related Surveys

- **Prior MAS Surveys**: Typically focused on agent architectures or application domains
- **Communication in RL**: Recent work on emergent communication in multi-agent RL
- **LLM Collaboration**: [Beyond Individual Intelligence](https://arxiv.org/abs/2605.14892) (collaboration & self-evolution)

### Future Research Directions

1. **Emergent Communication Protocols**: Can LLM agents discover improved communication languages through interaction?

2. **Formal Communication Semantics**: Develop formal models (process calculi, session types) for LLM agent communication

3. **Cross-Domain Communication**: Standardize inter-organizational agent communication (APIs, schemas)

4. **Failure Analysis**: Deep study of how communication failures cascade to task failures

### Integration with Other Frameworks

- **With Hierarchical Architectures**: Combine formal orchestration with communication-optimized topologies
- **With Skill Frameworks**: Use skills to encapsulate domain-specific communication patterns
- **With Dynamic Topology Adaptation**: Adapt communication topology at runtime based on observed performance

---

**Paper Link**: [arXiv:2502.14321](https://arxiv.org/abs/2502.14321)

**Frontiers of Computer Science**: [Published version](https://doi.org/10.1007/s11704-026-50857-y)

**Citation**: Yan et al. "Beyond Self-Talk: A Communication-Centric Survey of LLM-Based Multi-Agent Systems." Frontiers of Computer Science, 2025.

---

*For detailed taxonomy tables, comprehensive case studies, and systematic analysis of 200+ papers, see the full paper on arXiv or the published version in Frontiers of Computer Science.*
