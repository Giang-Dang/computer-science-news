# Agentic AI Frameworks: Architectures, Protocols, and Design Challenges

**Paper:** Derouiche, H., Brahmi, Z., & Mazeni, H. (2025). Agentic AI Frameworks: Architectures, Protocols, and Design Challenges. arXiv:2508.10146

**ArXiv ID:** 2508.10146 | **Submitted:** August 13, 2025

---

## Executive Summary

This comprehensive systematic review analyzes leading Agentic AI frameworks—CrewAI, LangGraph, AutoGen, Semantic Kernel, Agno, Google ADK, and MetaGPT—to establish foundational architectures and design patterns for multi-agent LLM systems. The paper provides a comparative evaluation of how these frameworks handle agent coordination, tool integration, memory management, and safety guardrails, directly addressing the critical challenge of building scalable, interoperable agent systems for autonomous software development tasks.

---

## Problem Statement

### Development Automation Challenge

As Large Language Models become increasingly capable, the paradigm of single-model prompting is insufficient for complex development tasks. Organizations need frameworks that enable multiple specialized LLM agents to work collaboratively on:
- Code generation and refinement
- Testing and quality assurance
- Debugging and analysis
- Architecture design and planning

### Prior Agent System Limitations

Early agent frameworks lacked:
- Standardized communication protocols for agent-to-agent interaction
- Consistent memory and state management patterns
- Unified approaches to tool integration and orchestration
- Clear guidelines for safety, alignment, and guardrails
- Interoperability between different frameworks and tools

### Research Gap

No comprehensive comparative analysis existed that systematically evaluated how leading frameworks address these challenges, making it difficult for practitioners to select and deploy appropriate solutions. This paper fills that gap by providing a taxonomy of frameworks and protocols.

---

## Core Concepts & Theory

### Agentic AI Fundamentals

**Definition:** Agentic AI systems are autonomous architectures where Large Language Models (LLMs) exhibit:
- **Goal-directed autonomy:** Agents independently plan and execute multi-step tasks
- **Contextual reasoning:** Agents interpret requirements and adapt to environment feedback
- **Dynamic coordination:** Multiple agents communicate and collaborate on shared objectives

### Agent Orchestration Patterns

The paper identifies three primary orchestration approaches:

1. **Hierarchical Coordination**
   - Central orchestrator manages task decomposition and agent assignment
   - Example: MetaGPT's project manager role delegates tasks to specialized agents
   - Strengths: Clear control flow, deterministic execution
   - Weaknesses: Bottleneck at orchestrator level

2. **Collaborative Coordination**
   - Peer agents communicate directly with shared memory
   - Example: CrewAI's role-based collaboration pattern
   - Strengths: Distributed problem-solving, natural task delegation
   - Weaknesses: Complex communication graphs, potential deadlocks

3. **Graph-Based Orchestration**
   - Stateful, composable task flows with branching and retry logic
   - Example: LangGraph's node-and-edge model for sequencing
   - Strengths: Flexible, traceable, composable
   - Weaknesses: Requires explicit flow definition

### Agent Communication Protocols

The paper analyzes four main communication protocols:

#### 1. Contract Net Protocol (CNP)
- **Mechanism:** Agents advertise tasks, other agents bid, task manager selects winner
- **Use case:** Dynamic task allocation in multi-agent systems
- **Agent roles:** Task manager, bidder agents
- **Message flow:**
  ```
  Task Manager --[Task Announcement]--> All Agents
  All Agents --[Bids]--> Task Manager
  Task Manager --[Task Award]--> Selected Agent
  Selected Agent --[Result]--> Task Manager
  ```

#### 2. Agent-to-Agent (A2A) Protocol
- **Mechanism:** Direct peer-to-peer agent communication
- **Use case:** Information sharing, collaborative problem-solving
- **Agent roles:** Peer agents with symmetric communication rights
- **Example:** CrewAI agents exchanging intermediate results

#### 3. Agent Network Protocol (ANP)
- **Mechanism:** Agents operate on a network with defined message-passing topology
- **Use case:** Distributed reasoning, large-scale coordination
- **Agent roles:** Network nodes with defined connection patterns

#### 4. Agora Protocol
- **Mechanism:** Shared memory-based communication (blackboard architecture)
- **Use case:** Decentralized coordination where agents read/write to shared state
- **Agent roles:** Independent agents accessing centralized knowledge base
- **Message flow:**
  ```
  Agent 1 --[Write State]--> Shared Memory/Blackboard
  Agent 2 --[Read State]--> Shared Memory/Blackboard
  Agent 2 --[Update State]--> Shared Memory/Blackboard
  Agent 3 --[Read Updated State]--> Shared Memory/Blackboard
  ```

### Framework Architecture Comparison

| Component | CrewAI | LangGraph | AutoGen | MetaGPT | Semantic Kernel |
|-----------|--------|-----------|---------|---------|-----------------|
| **Orchestration Model** | Role-based collaboration | Graph-based flows | Actor-based (v0.4) | Hierarchical (PM-driven) | Plugin-based |
| **Agent Communication** | Direct peer collaboration | Node state transitions | Message passing | Hierarchical delegation | Service composition |
| **Memory Management** | Task history, shared context | Stateful checkpoints | Persistent storage | Memory hierarchy | Session state |
| **Tool Integration** | Tool registry per agent | Tool nodes in graph | Native tool registry | Tool definitions | Plugin system |
| **Safety Guardrails** | Role-based constraints | Validation nodes | Validators + retry logic | Constraints in roles | Policy enforcement |
| **Learning Curve** | Moderate | Steeper (graph design) | Shallow | Moderate | Steep (SDK concepts) |
| **Scalability** | Suitable for small teams | Suitable for complex flows | Actor model scales well | Hierarchical bottleneck | Limited guidance |

---

## Main Ideas & Contributions

### 1. Foundational Taxonomy for Agentic AI Systems

The paper establishes a structured taxonomy organizing frameworks by:
- **Architectural paradigm:** hierarchical, collaborative, graph-based, network-based
- **Orchestration mechanism:** centralized, distributed, hybrid
- **Communication protocol:** direct, protocol-based, shared-memory
- **Memory strategy:** flat history, hierarchical, episodic, persistent

### 2. Protocol-Driven Design Guidance

By analyzing communication protocols (CNP, A2A, ANP, Agora), the paper provides:
- **Decision framework** for choosing protocols based on use case
- **Scalability implications** of each protocol
- **Failure modes** and recovery mechanisms
- **Interoperability patterns** for multi-framework systems

### 3. Comparative Framework Evaluation

The systematic comparison reveals:
- **AutoGen's strengths:** Native guardrails, flexible actor model, mature tooling
- **LangGraph's strengths:** Composability, traceability, complex workflow support
- **CrewAI's strengths:** Ease of use, role-based intuition, delegation patterns
- **MetaGPT's strengths:** Software engineering domain specialization, role simulation
- **Tradeoffs:** No single framework excels in all dimensions

### 4. Service-Oriented Computing Alignment

The paper connects agentic frameworks to classical SOC principles:
- **Services as agents:** Each agent encapsulates a capability
- **Orchestration languages:** Similar to BPEL (Business Process Execution Language)
- **Interoperability standards:** Pathways to vendor-neutral frameworks
- **Enterprise deployment:** Lessons from SOC architecture patterns

---

## Methodology & Implementation

### Systematic Review Approach

1. **Framework Selection:** Seven leading frameworks selected based on GitHub stars, adoption, documentation maturity
2. **Evaluation Criteria:** 15+ dimensions including architecture, communication, memory, safety, scalability
3. **Protocol Analysis:** Deep dive into CNP, A2A, ANP, Agora implementations across frameworks
4. **Literature Synthesis:** Cross-referencing academic literature on multi-agent systems

### Frameworks Analyzed

| Framework | Release | Maturity | Primary Use Case |
|-----------|---------|----------|------------------|
| **CrewAI** | 2023 | Production-ready | Multi-agent team simulation |
| **LangGraph** | 2024 | Growing | Complex stateful workflows |
| **AutoGen** | 2023 | Mature | Research & prototyping |
| **MetaGPT** | 2023 | Stable | Software engineering automation |
| **Semantic Kernel** | 2023 | Maturing | Enterprise integration |
| **Agno** | 2024 | Early | Trust-layer focus |
| **Google ADK** | 2024 | Emerging | Google Workspace integration |

### Safety & Guardrails Evaluation

The paper grades frameworks on guardrail capabilities:

- **AutoGen:** ⭐⭐⭐⭐⭐ Native validators, retry mechanisms, input validation
- **LangGraph:** ⭐⭐⭐⭐ Node-level validation, flow-level checks
- **Agno:** ⭐⭐⭐⭐ Trust layer, early-stage safety focus
- **OpenAI SDK:** ⭐⭐⭐⭐ Schema validation, developer-defined safeguards
- **CrewAI:** ⭐⭐⭐ Role-based constraints, limited validation
- **MetaGPT:** ⭐⭐⭐ Role constraints, limited guardrails
- **Semantic Kernel:** ⭐⭐⭐ Policy enforcement, plugin safety

### Results and Findings

**Key Findings:**

1. **Communication Protocol Adoption:**
   - Contract Net Protocol widely used for task allocation
   - Shared-memory (Agora-style) approaches gaining adoption for state management
   - Pure hierarchical approaches limiting scalability
   - Hybrid protocols emerging in production systems

2. **Tool Integration Patterns:**
   - Tool registries increasingly standardized
   - OpenAPI specifications enabling framework interoperability
   - MCP (Model Context Protocol) emerging as standard for tool definition

3. **Memory Management Trade-offs:**
   - Flat history insufficient for long tasks (>50 steps)
   - Hierarchical memory (short-term context + long-term summaries) optimal
   - Token budget constraints require aggressive summarization

4. **Scalability Bottlenecks:**
   - Hierarchical systems bottleneck at coordinator level
   - Graph-based systems scale better but require careful DAG design
   - Actor-based systems (AutoGen v0.4) provide distributed scaling
   - Message passing latency becomes critical >10 agents

5. **Developer Experience:**
   - CrewAI has lowest learning curve (intuitive role metaphor)
   - LangGraph steeper but more powerful for complex flows
   - AutoGen requires understanding of message passing patterns
   - MetaGPT benefits domain specialists (software engineers)

---

## Practical Applications & Use Cases

### 1. Software Development Automation

**Multi-Agent Development Team:**
```
Requirement Analyst Agent --> Architect Agent --> Developer Agent --> Tester Agent
    |                            |                    |                 |
    +------ Orchestrator (MetaGPT Style) <----------+
                                                      |
                                              Shared Memory: Task Queue, Code Repository
```

- **Agent roles:** Analyst, architect, developer, tester, reviewer
- **Coordination:** Hierarchical via project manager, shared code repository
- **Tool integration:** IDE APIs, version control, test runners, linters
- **Result:** End-to-end code generation with quality checks

### 2. Content Generation & Analysis Pipeline

**Multi-Source News Analysis (CrewAI pattern):**
```
Research Agent <--> Analyst Agent <--> Writer Agent <--> Editor Agent
         |              |                  |                 |
         +------ Shared Memory (Article Draft, Facts) ------+
                        |
                   Task Coordinator
```

- **Agent roles:** Research, analysis, writing, editing, publication
- **Coordination:** Peer-to-peer with shared memory
- **Tool integration:** Web search, fact-checking APIs, publishing platforms
- **Result:** Verified, multi-perspective content

### 3. System Architecture & Design Review

**Hierarchical Design Review (MetaGPT approach):**
```
Chief Architect (Coordinator)
    |
    +-- Design Agent (architecture patterns, scalability)
    |
    +-- Security Agent (threat modeling, compliance)
    |
    +-- Performance Agent (bottleneck identification)
    |
    +-- Cost Agent (infrastructure optimization)
```

### Integration Challenges & Solutions

| Challenge | CrewAI Solution | LangGraph Solution | AutoGen Solution |
|-----------|-----------------|-------------------|------------------|
| **Agent divergence** | Role constraints | Validation nodes | Retry logic |
| **Context explosion** | Task history pruning | Checkpoint management | Memory management |
| **Tool failures** | Fallback agents | Error branches | Retry with backoff |
| **Cost control** | Model switching | Token budgeting | Usage tracking |
| **Debugging** | Agent introspection | Graph visualization | Message logging |

### Scalability Considerations

- **Small teams (2-3 agents):** All frameworks sufficient
- **Medium teams (4-10 agents):** CrewAI or LangGraph recommended
- **Large systems (10+ agents):** AutoGen (actor model) or custom hybrid
- **Cost implications:** Each agent call incurs API costs (~$0.001-$0.01 per call)
- **Latency:** Sequential agent calls add 1-2 seconds per step; parallel execution critical

---

## Insights & Implications

### Impact on Agent-Driven Development Systems

1. **Standardization Opportunity:** No de facto standard exists; frameworks could converge on common protocols (emerging: OpenAI Function Calling, MCP)
2. **Enterprise Adoption Barrier:** Organizations need clear framework selection criteria; this paper provides that guidance
3. **Interoperability Gap:** Multi-framework systems require custom adapters; standard protocol bridges needed

### Advancement in Autonomous Coding

- **Reproducibility:** LangGraph's stateful approach enables deterministic, auditable workflows
- **Fault tolerance:** AutoGen's actor model naturally supports partial failures and recovery
- **Human-in-the-loop:** All frameworks support human approval gates; MetaGPT provides structured integration points

### Limitations and Open Research Questions

1. **Protocol Standardization:** Which communication protocol will dominate for production systems?
2. **Scalability Beyond 20 Agents:** How do frameworks handle truly large multi-agent teams?
3. **Cost Optimization:** How to intelligently distribute work across model tiers (GPT-4 vs. GPT-4o mini)?
4. **Fairness & Bias:** How do frameworks surface and mitigate agent disagreement or biased reasoning?
5. **Real-time Streaming:** Limited support for streaming agent outputs; token streaming in multi-agent contexts undefined

### Relevance to Skill Frameworks & Agent Topologies

- **Skill-based agents:** Frameworks show path toward decomposing tasks into reusable skills
- **Topology implications:** Different frameworks suit different topologies:
  - **Hub-and-spoke:** MetaGPT (hierarchical)
  - **Peer network:** CrewAI (collaborative)
  - **Directed acyclic graph (DAG):** LangGraph (graph-based)
  - **Actor grid:** AutoGen v0.4 (distributed)

---

## Code & Resources

### Official Repositories

- **CrewAI:** https://github.com/joaomdmoura/crewAI
- **LangGraph:** https://github.com/langchain-ai/langgraph
- **AutoGen:** https://github.com/microsoft/autogen
- **MetaGPT:** https://github.com/geekan/MetaGPT
- **Semantic Kernel:** https://github.com/microsoft/semantic-kernel
- **Agno:** https://github.com/agno-oss/agno
- **Google ADK:** https://github.com/google-cloud-samples/agent-builder-samples

### Dependencies & Requirements

| Framework | Language | Min Python | LLM APIs | Key Dependencies |
|-----------|----------|-----------|----------|------------------|
| **CrewAI** | Python | 3.10+ | OpenAI, Anthropic, local | pydantic, requests |
| **LangGraph** | Python | 3.9+ | Any LangChain-supported | langchain, jsonschema |
| **AutoGen** | Python | 3.8+ | OpenAI, Azure, local | openai, tiktoken |
| **MetaGPT** | Python | 3.9+ | OpenAI, local | pydantic, aiohttp |

### Quick-Start Integration Guide

**Example: CrewAI Multi-Agent System**

```python
from crewai import Agent, Task, Crew

# Define specialized agents
code_agent = Agent(
    role='Python Developer',
    goal='Write clean, tested code',
    backstory='Expert in design patterns and best practices'
)

test_agent = Agent(
    role='QA Engineer',
    goal='Ensure code quality',
    backstory='Meticulous tester focusing on edge cases'
)

# Create tasks
code_task = Task(
    description='Implement user authentication module',
    agent=code_agent
)

test_task = Task(
    description='Write comprehensive tests',
    agent=test_agent
)

# Orchestrate
team = Crew(
    agents=[code_agent, test_agent],
    tasks=[code_task, test_task]
)

result = team.kickoff()
```

**Example: LangGraph Complex Workflow**

```python
from langgraph.graph import StateGraph

# Define workflow nodes
def code_generation_node(state):
    return {'code': generate_code(state['requirements'])}

def code_review_node(state):
    return {'review': review_code(state['code']), 'approved': False}

def revision_node(state):
    if state['approved']:
        return {'code': state['code']}
    else:
        return code_generation_node({'requirements': state['review']})

# Build graph
workflow = StateGraph(dict)
workflow.add_node('generate', code_generation_node)
workflow.add_node('review', code_review_node)
workflow.add_node('revise', revision_node)

workflow.add_edge('generate', 'review')
workflow.add_conditional_edges('review', 
    lambda state: 'generate' if not state['approved'] else 'end'
)
```

---

## Related Work & Context

### Foundational Papers on Multi-Agent Systems

- **Shoham & Tennenholtz (1992):** "On the Synthesis of Useful Agents" — foundational work on agent design
- **Wooldridge & Jennings (1995):** "Intelligent Agents: Theory and Practice" — classical agent theory
- **Lesser (1999):** Distributed AI systems and coordination mechanisms

### Recent Surveys on LLM-Based Agents

- **2404.04834:** "LLM-Based Multi-Agent Systems for Software Engineering: Literature Review, Vision and the Road Ahead" — comprehensive survey on agent applications in SE
- **2508.11126:** "AI Agentic Programming: A Survey of Techniques, Challenges, and Opportunities" — focuses on agentic programming techniques
- **2601.12560:** "Agentic Artificial Intelligence: Architectures, Taxonomies, and Evaluation" — broader survey on agent architectures

### Emerging Standards

- **OpenAI Function Calling:** De facto standard for tool invocation in agents
- **Model Context Protocol (MCP):** Emerging standard for defining agent tools and capabilities
- **LLM Evaluation:** HumanEval, SWE-bench, CodeQL benchmarks for measuring agent code quality

### Possible Extensions & Future Research

1. **Federated Frameworks:** Multi-framework orchestration enabling best-of-breed tool use
2. **Self-Adaptive Protocols:** Agents dynamically selecting communication protocols based on task characteristics
3. **Cost-Aware Routing:** Intelligent model selection for cost optimization across agent teams
4. **Formal Verification:** Proofs of correctness for agent-generated code
5. **Emergent Behaviors:** Understanding unexpected agent behaviors in long-running systems

### Connection to This Paper's Research

This paper provides the architectural foundation upon which:
- **Skill-based agent frameworks** (like those in EvoAgent, ABSTRAL) can be built
- **Topology-specific optimizations** can be developed (e.g., hierarchical vs. peer orchestration)
- **Protocol-agnostic tools** can be designed to work across frameworks
- **Safety and governance** frameworks can be standardized

---

## Summary

"Agentic AI Frameworks: Architectures, Protocols, and Design Challenges" is essential reading for anyone building production multi-agent systems. By providing a systematic taxonomy of frameworks, communication protocols, and design patterns, it enables practitioners to make informed choices about agent architecture. The key insight is that different development tasks (team simulation vs. complex workflows vs. researcher prototyping) map naturally to different frameworks, and understanding these mappings is critical for successful agent-driven development automation.

The paper's analysis of communication protocols—particularly the Contract Net Protocol for dynamic task allocation and shared-memory architectures for state management—provides concrete guidance for designing scalable, fault-tolerant multi-agent systems. As the field converges on standards (MCP, OpenAI Function Calling), this foundational taxonomy will become increasingly important for framework interoperability and multi-tool orchestration in large-scale development automation pipelines.
