# Externalization in LLM Agents: A Unified Review of Memory, Skills, Protocols and Harness Engineering

**ArXiv ID:** 2604.08224  
**Authors:** Chenyu Zhou, Huacan Chai, Wenteng Chen, Zihan Guo, and 19 co-authors (22 total)  
**Affiliations:** Shanghai Jiao Tong University, Sun Yat-Sen University, Shanghai Innovation Institute, Carnegie Mellon University, OPPO  
**Publication Venue:** Comprehensive Review  
**Submission Date:** April 2026  
**Length:** 54 pages (comprehensive systematic review)

## Executive Summary

This comprehensive review reframes how we understand LLM agents: modern agentic systems are built not primarily by modifying model weights, but by systematically **externalizing cognitive capabilities into runtime infrastructure**. The paper identifies and analyzes four forms of externalization—memory, skills, protocols, and harness engineering—that collectively transform black-box LLMs into reliable, governable agents.

The significance lies in demonstrating that **agent infrastructure is not auxiliary but foundational**. By shifting burden from latent parameters to explicit, persistent, inspectable artifacts, externalization enables scaling, interpretability, debuggability, and fine-grained control. This framework directly supports development of skill-based agent architectures and multi-agent orchestration systems discussed throughout this repository.

## Problem Statement

Existing frameworks for understanding LLM agents focus on:
- Model size and capability scaling (Chinchilla, scaling laws)
- Prompt engineering and instruction tuning
- Fine-tuning and RLHF optimization

Yet these approaches leave a crucial gap: **How do practitioners actually build reliable, production-grade agents?**

The answer: rarely through model weights alone. Instead, real systems externalizes capabilities into:
1. **Memory systems** that augment context
2. **Skills/tools** that extend capability beyond language
3. **Interaction protocols** that enable reliable communication
4. **Harness engineering** that coordinates everything

**Research Gap:** Existing literature lacks unified framework explaining *why* this externalization pattern is fundamental to agent engineering, or *how* different externalization approaches compare and integrate.

The review answers: through systematic analysis of thousands of agent systems, what principles guide externalization design?

## Core Concepts & Theory

### Central Thesis: Externalization as Agent Infrastructure

**Premise:** LLMs alone are insufficient for reliable agentic behavior. Modern agents work by transforming:

```
┌─────────────────────────────────────────────────────────────┐
│         Traditional LLM Approach                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  All capability must reside in model weights                │
│                                                              │
│  ┌──────────────────────────────────────────┐               │
│  │ LLM (Fixed weights)                      │               │
│  │ ├─ Knowledge                             │               │
│  │ ├─ Reasoning                             │               │
│  │ ├─ Planning                              │               │
│  │ ├─ Task execution                        │               │
│  │ ├─ Memory management                     │               │
│  │ ├─ Tool use                              │               │
│  │ └─ Output formatting                     │               │
│  └──────────────────────────────────────────┘               │
│             ↓                                                │
│        Output (text only)                                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘

         Traditional burden: All on model weights
         Problem: Limited capacity, black box, inflexible
```

```
┌─────────────────────────────────────────────────────────────┐
│    Modern Externalized Agent Approach                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Capabilities distributed across infrastructure              │
│                                                              │
│  ┌──────────────────┐  ┌─────────────────┐                 │
│  │ LLM (Focused)    │  │ Memory Systems  │                 │
│  │ ├─ Reasoning ✓   │  │ ├─ Working     │                 │
│  │ ├─ Planning ✓    │  │ ├─ Episodic    │                 │
│  │ ├─ Reflection ✓  │  │ ├─ Semantic    │                 │
│  │ └─ Orchestration │  │ └─ Personalized│                 │
│  └────────┬─────────┘  └────────┬────────┘                 │
│           │                     │                           │
│  ┌────────┴─────────────────────┴────────┐                 │
│  │                                       │                 │
│  ▼                                       ▼                 │
│  ┌──────────────────┐  ┌─────────────────┐                │
│  │ Skills/Tools     │  │ Protocols       │                │
│  │ ├─ Computation   │  │ ├─ Agent-Agent  │                │
│  │ ├─ Integration   │  │ ├─ Agent-Tool   │                │
│  │ ├─ Interaction   │  │ ├─ Agent-User   │                │
│  │ └─ Verification  │  │ └─ Structured   │                │
│  └────────┬─────────┘  └────────┬────────┘                │
│           │                     │                          │
│  ┌────────┴─────────────────────┴────────┐                │
│  │                                       │                 │
│  ▼                                       ▼                 │
│  ┌──────────────────────────────────────┐                 │
│  │ Harness Engineering (Orchestration)  │                 │
│  │ ├─ Constraint enforcement            │                 │
│  │ ├─ Observability & monitoring        │                 │
│  │ ├─ Feedback loops                    │                 │
│  │ ├─ Control points                    │                 │
│  │ └─ Coordination logic                │                 │
│  └──────────────────────────────────────┘                 │
│                                                             │
│         ↓ Coordinated Execution                            │
│                                                             │
│   Structured, governable, reliable agent behavior          │
│                                                             │
└─────────────────────────────────────────────────────────────┘

   Modern burden: Distributed across layers
   Benefit: Scalable, interpretable, governable, debuggable
```

**Key Insight:** The shift from internal (model) to external (infrastructure) capability transfer moves from *implicit knowledge in weights* to *explicit, inspectable procedures*. This is fundamental to production agentic systems.

### Four Forms of Externalization

#### 1. **Memory Externalization: State Across Time**

Addresses: LLMs have no persistent state; context window is finite and expensive

**Four Memory Hierarchies:**

**a) Working Context (Immediate State)**
- **Purpose:** Live state of current task execution
- **Contents:** 
  - Open files, variable bindings
  - Current goals and subgoals
  - Partial plans and intermediate results
  - Hypotheses under exploration
  - Execution checkpoints
- **Mechanism:** Passed in context window to each LLM call
- **Example:** Code editor state, search results cache

**b) Episodic Memory (Historical Trajectories)**
- **Purpose:** Records of prior task attempts to guide future decisions
- **Contents:**
  - Decision points and alternatives taken
  - Tool calls and their outcomes
  - Failures and recovery strategies
  - Reflections on what worked/didn't
  - Entire execution traces
- **Mechanism:** Stored in vector database, retrieval augmented generation (RAG)
- **Example:** "Previous attempt to solve similar problem X used approach Y; it failed because Z"

**c) Semantic Memory (Abstracted Knowledge)**
- **Purpose:** Generalized patterns applicable across tasks
- **Contents:**
  - Domain expertise (best practices, patterns)
  - Tool capabilities and when to use them
  - Common mistakes and mitigations
  - Performance profiles of algorithms
- **Mechanism:** Embeddings, knowledge graphs, skill libraries
- **Example:** "For sorted array problems, binary search is optimal"

**d) Personalized Memory (User/Environment Adaptation)**
- **Purpose:** Cross-session adaptation
- **Contents:**
  - User preferences, interaction history
  - Environmental context and constraints
  - Long-term goals and objectives
  - Learned user response patterns
- **Mechanism:** Long-term storage with periodic summarization
- **Example:** "This user prefers conservative solutions; explain reasoning thoroughly"

**Memory Architecture Paradigms:**

| Paradigm | Structure | Tradeoff |
|----------|-----------|----------|
| **Monolithic Context** | All state in current prompt | Simple but limited by context window |
| **Context + Retrieval** | Live context + retrieved episodic/semantic | Good balance; requires retrieval tuning |
| **Hierarchical Memory** | Layered storage: working → episodic → semantic | Scalable; coordination complexity |
| **Adaptive Memory** | Dynamically adjust what's stored/retrieved based on task | Optimal but requires learned policies |

#### 2. **Skills Externalization: Procedural Expertise**

Addresses: LLMs have broad knowledge but lack specialized execution capability

**Definition:** Skills are **persistent, composable, reusable procedural knowledge** that agents invoke rather than generate from scratch.

**Skill Examples:**
- **Computation Skills:** Matrix inversion, statistical analysis, sorting
- **Integration Skills:** API calls, database queries, library invocations
- **Reasoning Skills:** Program synthesis, formal verification, theorem proving
- **Interaction Skills:** Parsing user input, formatting output, error recovery

**Skill Design Dimensions:**

| Dimension | Considerations |
|-----------|---|
| **Composability** | Can skills be chained? Do inputs/outputs match? |
| **Interpretability** | Can operators understand why skill was selected? |
| **Debuggability** | Can we instrument and trace skill execution? |
| **Reliability** | Does skill handle errors gracefully? |
| **Cost** | What is execution cost (latency, compute, API calls)? |

**Skill Architecture Patterns:**

```
┌────────────────────────────────────────┐
│     Skill Library Architecture         │
├────────────────────────────────────────┤
│                                        │
│  ┌──────────────────────────────────┐ │
│  │   Skill Registry                 │ │
│  │   ├─ Skill name & description    │ │
│  │   ├─ Input/output schema         │ │
│  │   ├─ Expected error modes        │ │
│  │   ├─ Cost profile                │ │
│  │   └─ When to use heuristics      │ │
│  └──────────────────────────────────┘ │
│                                        │
│  ┌──────────────────────────────────┐ │
│  │   Skill Selector                 │ │
│  │   (LLM or learned policy)         │ │
│  │                                  │ │
│  │   Input: Current goal            │ │
│  │   Output: Selected skill + params│ │
│  └──────────────────────────────────┘ │
│                                        │
│  ┌──────────────────────────────────┐ │
│  │   Skill Executor                 │ │
│  │   ├─ Invoke skill                │ │
│  │   ├─ Monitor execution           │ │
│  │   ├─ Capture output              │ │
│  │   └─ Handle errors               │ │
│  └──────────────────────────────────┘ │
│                                        │
└────────────────────────────────────────┘
```

#### 3. **Protocols Externalization: Interaction Structure**

Addresses: Agent-to-agent and agent-to-tool communication can be ad-hoc and error-prone

**Definition:** Protocols are **machine-readable contracts** specifying how agents interact with each other and external systems.

**Protocol Types:**

**a) Agent-to-Agent Protocols:**
- **Sequential Messaging:** Strict message order and format
- **Request-Reply:** Caller waits for response
- **Publish-Subscribe:** Broadcast to multiple agents
- **Hierarchical:** Manager-subordinate relationships
- **Peer-to-Peer:** Decentralized coordination

**b) Agent-to-Tool Protocols:**
- **Function Calling:** Standardized tool invocation (OpenAI format)
- **REST APIs:** HTTP-based tool interfaces
- **Command-Line:** Shell command execution
- **RPC:** Remote procedure calls with serialization

**c) Agent-to-User Protocols:**
- **Natural Language:** Conversational interaction
- **Structured Forms:** Filling predefined input fields
- **System Prompts:** Rules and constraints for interaction

**Protocol Benefits:**
- **Interoperability:** Different agent types can coordinate
- **Debuggability:** Clear message format aids troubleshooting
- **Reliability:** Eliminates ambiguity in communication
- **Auditability:** Complete interaction logs for compliance
- **Composability:** Skills can be chained reliably

**Protocol Design Example (Code Generation Workflow):**
```
Agent: Planner
├─ Input: User requirement (string)
├─ Output: Task decomposition (structured JSON)
│  └─ { "tasks": [{"id": 1, "action": "..."}, ...]}
│
Agent: Implementer
├─ Input: Task decomposition (same format)
├─ Output: Code + execution plan
│
Agent: Verifier
├─ Input: Code + test specifications
├─ Output: Pass/fail verdict + coverage report
```

Without protocols, agents produce incompatible formats; with protocols, composition is guaranteed.

#### 4. **Harness Engineering: Unification Layer**

Addresses: Coordinating memory, skills, and protocols requires reliable runtime infrastructure

**Definition:** Harness engineering is the **engineering discipline of designing runtime systems** that make externalized components work reliably together.

**Harness Components:**

**a) Constraint Enforcement:**
- Prevent invalid state transitions
- Enforce resource limits (tokens, latency, cost)
- Guarantee properties (safety, fairness, correctness)
- Example: "Don't spend >$100 on API calls; fall back to cheaper model"

**b) Observability:**
- Logging all agent decisions and state
- Tracing execution flows
- Monitoring performance metrics
- Alerting on anomalies
- Example: "Log every skill invocation with input, output, latency, cost"

**c) Feedback Loops:**
- Learning from execution outcomes
- Updating agent parameters (prompts, heuristics)
- Reinforcement signals for policy learning
- Error-driven improvement
- Example: "If skill X fails on task type Y, reduce its priority"

**d) Control Points:**
- Human-in-the-loop intervention
- Approval workflows for high-consequence decisions
- Interactive debugging
- Policy override capabilities
- Example: "Require human approval before making external API calls"

**e) Coordination Logic:**
- Sequencing skills in workflows
- Load balancing across agents
- Failover and recovery
- Resource allocation
- Example: "If agent A is overloaded, route to agent B"

**Harness Architecture:**
```
┌─────────────────────────────────────────────────┐
│         Harness Engineering Layer               │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │ Constraint Enforcement Engine            │  │
│  │ - Rate limiting                          │  │
│  │ - Resource quotas                        │  │
│  │ - Safety policies                        │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │ Observability & Monitoring               │  │
│  │ - Event logging                          │  │
│  │ - Metrics collection                     │  │
│  │ - Distributed tracing                    │  │
│  │ - Alerting                               │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │ Feedback & Learning Loop                 │  │
│  │ - Performance analysis                   │  │
│  │ - Failure attribution                    │  │
│  │ - Policy updates                         │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │ Control & Governance                     │  │
│  │ - Manual intervention points             │  │
│  │ - Approval workflows                     │  │
│  │ - Audit logs                             │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │ Orchestration Engine                     │  │
│  │ - Workflow scheduling                    │  │
│  │ - Agent coordination                     │  │
│  │ - Failover & recovery                    │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
│           ↕ (Controls & Observes)              │
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │ Agent Runtime                            │  │
│  │ (LLMs, Skills, Protocols, Memory)        │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
└─────────────────────────────────────────────────┘
```

## Main Ideas & Contributions

### 1. **Unified Framework for Agent Infrastructure**

The paper's central contribution is organizing the fragmented landscape of agent engineering into a coherent taxonomy. Rather than treating memory, skills, protocols, and harness as separate concerns, the review shows they work synergistically to externalize cognitive burden from the model.

### 2. **Empirical Analysis: Infrastructure Impact**

The review provides evidence that externalization decisions have measurable consequences:

- **Memory Architecture Impact:** Monolithic context vs. retrieval-augmented shows trade-offs in accuracy vs. latency
- **Skill Library Design:** Skill granularity affects task success rates (finer-grained skills are more reliable but slower to select)
- **Protocol Standardization:** Standardized protocols reduce agent coordination failures
- **Harness Governance:** Constraint enforcement reduces catastrophic failures

[Exact empirical figures unavailable — see full paper for quantitative comparisons]

### 2. **Infrastructure-Centric Agent Development**

Traditional view: improve agent by improving model (larger, more parameters, better fine-tuning)

**Review's perspective:** Modern agents improve through infrastructure optimization:
- Better memory retrieval strategies
- More reusable, composable skills
- Clearer interaction protocols
- Stronger governance and observability

**Practical implication:** Organizations without access to cutting-edge models can build highly capable agents through infrastructure investment.

### 4. **Auditability & Interpretability Through Externalization**

Key insight: externalized components are **inspectable and modifiable**, unlike latent weights.

- **Memory auditing:** See exactly what facts the agent knows and when
- **Skill tracing:** Follow which skills were invoked and why
- **Protocol recording:** Complete message history for debugging
- **Harness visibility:** All decisions subject to monitoring and intervention

This enables building trustworthy agents—not black boxes, but systems with transparent reasoning.

### 5. **Scalability Patterns**

The review identifies how each form of externalization enables scaling:

- **Memory scaling:** Hierarchical memory allows retaining unlimited historical context
- **Skill scaling:** Skill libraries grow without impacting model weights
- **Protocol scaling:** Standardized protocols enable coordinating hundreds of agents
- **Harness scaling:** Distributed coordination engines handle large agent ecosystems

## Methodology & Structure

### Review Methodology

The paper is a **systematic literature review and synthesis**, not empirical research. Methodology:

1. **Scope Definition:** Identify papers on LLM agents, multi-agent systems, and agent frameworks (2020-2026)
2. **Paper Collection:** Systematic search across ArXiv, conference proceedings, and industry systems
3. **Classification:** Categorize papers by which form(s) of externalization they address
4. **Analysis:** Extract patterns, design choices, and trade-offs
5. **Synthesis:** Identify common principles and emergent patterns

### Coverage Areas

The review analyzes and synthesizes from hundreds of papers across:

- **Memory Systems:** RAG, vector databases, episodic memory in agents
- **Skills & Tools:** Function calling, tool use, skill libraries in frameworks
- **Protocols:** Multi-agent communication, coordination patterns
- **Harness Engineering:** LLM framework design (LangChain, AutoGPT, Claude's SDK, etc.)

### Key Frameworks Analyzed

[Specific framework details from review unavailable — but likely includes:]
- LangChain: Skills as tools, memory as abstractions
- Claude SDK: Agentic harness design
- AutoGPT: Autonomous agent orchestration
- Chorus: Structured agent coordination
- Reflection frameworks: Episodic memory + learning

## Results: Taxonomy & Insights

### Externalization Taxonomy

The review produces a **comprehensive taxonomy** organizing how real-world agent systems externalize capabilities:

**Memory Decisions:**
- Monolithic (single prompt) vs. Retrieval-augmented (RAG)
- What to store (decisions, outcomes, reflections, code)
- Retrieval strategy (similarity search, temporal, contextual)
- Update frequency (continuous vs. periodic summarization)

**Skills Decisions:**
- Built-in tools vs. discoverable skills vs. learned skills
- Skill granularity (atomic vs. composed)
- Selection mechanism (keyword matching vs. semantic search vs. LLM ranking)
- Error handling (graceful fallback vs. escalation)

**Protocol Decisions:**
- Structured output (JSON, XML) vs. natural language
- Message format (request-reply vs. streaming vs. event-driven)
- Versioning & compatibility (backwards compatibility requirements)
- Error signaling (exceptions vs. return codes vs. explicit error messages)

**Harness Decisions:**
- Constraint scope (cost, latency, safety)
- Observability depth (sampling vs. full logging)
- Control granularity (per-call approvals vs. batch policies)
- Orchestration model (centralized vs. distributed)

### Comparative Analysis

| Dimension | Monolithic Agents | Externalized Agents |
|-----------|---|---|
| **Interpretability** | Low (black box) | High (explicit procedures) |
| **Scalability** | Limited (fixed model) | Unlimited (infrastructure scaling) |
| **Reliability** | Unpredictable | Deterministic (with harness) |
| **Debuggability** | Difficult | Traceable (complete logs) |
| **Customization** | Requires fine-tuning | Prompt + infrastructure tuning |
| **Cost** | High (large models) | Can be lower (infrastructure tradeoffs) |

### Empirical Evidence

The review synthesizes evidence that externalization works:

- **Accuracy:** Studies show RAG-enhanced agents outperform monolithic LLMs for fact-heavy tasks
- **Reliability:** Multi-agent systems with protocols have lower failure rates
- **Cost:** Infrastructure investment can reduce reliance on largest/most expensive models
- **Auditability:** Externalized systems pass more compliance and safety audits

[Specific metrics unavailable — see full paper for quantitative backing]

## Practical Applications & Use Cases

### 1. **Enterprise Software Engineering**
Building reliable coding agents requires:
- **Skills:** Linting, testing, compilation tools
- **Memory:** Codebase understanding, prior refactoring attempts
- **Protocols:** Structured code review workflows
- **Harness:** Cost control (don't call expensive APIs unnecessarily), approval gates

### 2. **Healthcare & Finance**
High-stakes domains where auditing is critical:
- **Transparency requirement:** Must show why agent made decision
- **Compliance:** Decisions subject to regulatory review
- **Solution:** Externalize reasoning into protocols and logs

### 3. **Autonomous Research**
Multi-agent systems for discovering and validating scientific claims:
- **Specialization:** Different agents for literature search, hypothesis testing, analysis
- **Coordination:** Protocols ensure agents understand each other's outputs
- **Iteration:** Memory captures failed hypotheses to avoid repetition

### 4. **Multi-Agent Collaboration**
Teams of agents working on complex problems:
- **Protocols:** Enable different teams' agents to interoperate
- **Skills:** Shared libraries reduce duplication
- **Memory:** Shared knowledge base across agent teams
- **Harness:** Prevents interference, enforces team-level policies

## Insights & Implications

### 1. **The Shift Is Irreversible**
Modern agent development has fundamentally shifted from **model-centric** (improve weights) to **infrastructure-centric** (improve runtime systems). This is unlikely to reverse—even future models will benefit from sophisticated externalization.

### 2. **Specialization Through Skills**
Instead of training monolithic models with all capabilities, the future involves:
- Core reasoning models (not task-specific)
- Specialized skill libraries
- Composition of skills to solve problems

This mirrors how human expert teams work—generalists + specialists.

### 3. **Infrastructure as Competitive Advantage**
In an era where model capabilities converge (all using same frontier models), competitive advantage comes from:
- Better memory retrieval strategies
- More robust skill libraries
- Cleaner protocols
- Smarter harness engineering

Small organizations can compete with large ones through infrastructure design.

### 4. **Governance & Safety Through Externalization**
Paradoxically, making agents more powerful requires making them more constrained:
- Externalized constraints are enforceable
- Transparent reasoning enables oversight
- Protocols prevent unintended behavior
- Harness engineering provides safety guarantees

This is how autonomous systems can be trusted in high-stakes domains.

### 5. **The Rise of Agent Infrastructure**
New specializations emerging:
- **Agent architects:** Design orchestration patterns
- **Skill engineers:** Build libraries and ensure reliability
- **Protocol designers:** Standardize multi-agent communication
- **Harness engineers:** Build runtime systems

Software engineering is evolving to require new expertise domains.

## Code & Resources

### Reference Implementations

**Chorus Project** (Agent infrastructure framework)
- GitHub: [Chorus-AIDLC/Chorus](https://github.com/Chorus-AIDLC/Chorus)
- Documentation: Notes on externalization principles for agent design
- Provides templates for skills, memory, protocols, harness

### Academic Tools & Frameworks

**Memory Systems:**
- LangChain's memory abstractions (context managers, vector stores)
- Mem0 (persistent memory for LLMs)
- ChromaDB (vector database for episodic memory)

**Skills & Tools:**
- OpenAI's function calling API
- Tool-use benchmarks (ToolBench, API-Bank)
- Skill libraries in AutoGPT, ReAct

**Protocols:**
- OpenAI function calling specification
- Tool use JSON schema standards
- Agent communication frameworks (research repos)

**Harness Engineering:**
- LangChain framework (tool orchestration, monitoring hooks)
- LLM framework SDKs (Claude SDK, Anthropic SDK)
- Open-source agent harnesses (OpenInterpreter, OpenHands)

### Implementation Guide

**Step 1: Externalize Memory**
```
Start with: prompt context directly containing all facts
Evolve to: vector database + retrieval for episodic memory
Add: Summarization for long-term semantic memory
```

**Step 2: Build Skill Library**
```
Inventory existing capabilities (APIs, tools, computations)
Standardize interfaces (input schema, output schema, error modes)
Implement skill selector (semantic search + LLM ranking)
```

**Step 3: Define Protocols**
```
Document agent-to-agent message format (JSON schema)
Define request/response lifecycle
Specify error handling and retry logic
Version and maintain backward compatibility
```

**Step 4: Engineer Harness**
```
Implement logging at all control points
Add constraint enforcement (cost, latency limits)
Build observability dashboards
Create intervention/approval workflows
```

## Related Work & Context

### Foundational Papers on Agent Infrastructure
- **Agent frameworks:** AutoGPT, ReAct, LangChain (systems papers)
- **Tool use:** Retrieving supporting facts, answering open-domain questions (early work)
- **Multi-agent systems:** Communication patterns, coordination
- **LLM reasoning:** Chain-of-thought, tool-integrated reasoning

### Connection to Repository Themes

This review is directly relevant to multiple repository sections:

1. **Agent Orchestration:** How externalized components coordinate
2. **Multi-Agent Topologies:** Protocols enable different topologies
3. **Tool Use & Skills:** Skill framework design patterns
4. **Program Synthesis & Testing:** How agents with externalized skills solve coding tasks
5. **Software Development:** Infrastructure for building reliable coding agents

### Vision: Future Agentic Systems

The review points toward a future where:

1. **Modularity:** Agents composed from interchangeable components (skills, memory stores, protocols)
2. **Interoperability:** Any agent can coordinate with any other (protocol standardization)
3. **Transparency:** All reasoning is explicit and auditable
4. **Reliability:** Harness engineering provides safety guarantees
5. **Efficiency:** Infrastructure investment reduces dependence on model scale

This aligns perfectly with the **skill-based agent architecture** and **multi-agent orchestration** themes central to this repository.

### Open Research Questions

1. **Optimal skill granularity:** What size/complexity of skills maximizes agent performance?
2. **Memory query strategies:** How to retrieve most relevant memories efficiently?
3. **Protocol evolution:** How protocols should change as agent capabilities grow?
4. **Harness automation:** Can harness engineering itself be automated?
5. **Cross-domain transfer:** Do externalized components transfer across domains?

## Summary

This comprehensive review establishes that modern LLM agents are built not through model engineering but through **infrastructure engineering**. By systematically externalizing cognitive capabilities into memory systems, skill libraries, interaction protocols, and harness engineering, practitioners create reliable, scalable, auditable agents. The framework unifies disparate agent-building practices into a coherent design discipline, providing guidance for building both single-agent and multi-agent systems. For researchers and practitioners developing agentic software engineering systems, this review provides both the conceptual foundations and practical design patterns essential for production-grade agent development.
