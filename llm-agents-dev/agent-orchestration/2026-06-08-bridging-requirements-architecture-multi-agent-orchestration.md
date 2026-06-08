# Bridging Requirements and Architecture: Multi-Agent Orchestration with External Knowledge and Hierarchical Memory

**Paper:** [Bridging Requirements and Architecture: Multi-Agent Orchestration with External Knowledge and Hierarchical Memory](https://arxiv.org/abs/2606.01385)  
**Authors:** Ruiyin Li, Yiran Zhang, Xiyu Zhou, Yangxiao Cai, Peng Liang, Weisong Sun, Jifeng Xuan, Zhi Jin, Yang Liu  
**Affiliation:** Peking University, Huawei Cloud, Nanjing University  
**ArXiv ID:** 2606.01385  
**Submission Date:** June 8, 2026  
**Venue:** Software Architecture & Design Track

## Executive Summary

This paper introduces **MAAD (Multi-Agent Architecture Design)**, a knowledge-driven, four-agent orchestration framework that transforms requirements engineering into collaborative architecture design. By integrating **hierarchical memory mechanisms (working, episodic, semantic)** with RAG-enhanced knowledge infusion and **evaluation-driven feedback loops**, MAAD enables autonomous generation of production-ready architecture documentation from natural language requirements. The framework demonstrates a novel multi-agent topology where specialized agents (Analyst, Modeler, Designer, Evaluator) collaborate through hierarchical memory and external knowledge sources, advancing the state of automated software architecture design.

## Problem Statement

Software architecture design is a critical bottleneck in modern software engineering:

1. **Semantic Gap Problem:** Converting informal requirements into formal architecture specifications requires deep domain knowledge and architectural expertise
2. **Manual Effort Burden:** Architecture documentation is time-consuming to produce, often incomplete, and difficult to maintain as systems evolve
3. **Coordination Challenges:** Complex architectural design involves multiple stakeholder perspectives (requirements analysts, solution architects, domain experts, quality assurance)
4. **Knowledge Loss:** Architectural rationale and design decisions are often not systematically captured
5. **Verification Gap:** Generated architectures often lack rigorous quality assessment, risking downstream implementation issues

**Existing limitations:**
- Single-agent LLM approaches generate superficial or incomplete architectures
- No systematic mechanism to incorporate architectural standards and best practices
- Lack of iterative refinement and validation during design process
- No structured capture of architectural trade-offs and decisions

## Core Concepts & Theory

### 1. **The MAAD Framework Architecture**

MAAD orchestrates four role-specialized agents working sequentially with feedback loops:

```
Requirements (Natural Language)
          ↓
┌─────────────────────────────────────────┐
│  ANALYST AGENT                          │
│  ├─ Parse requirements                  │
│  ├─ Extract functional requirements     │
│  ├─ Identify non-functional constraints │
│  └─ Detect architectural concerns       │
└─────────────────────────────────────────┘
          ↓ (Requirement Specifications)
┌─────────────────────────────────────────┐
│  MODELER AGENT                          │
│  ├─ Construct 4+1 view models           │
│  │  ├─ Logical View (components)        │
│  │  ├─ Physical View (deployment)       │
│  │  ├─ Process View (runtime behavior)  │
│  │  ├─ Development View (structure)     │
│  │  └─ Use Case View (scenarios)        │
│  └─ Ensure consistency across views     │
└─────────────────────────────────────────┘
          ↓ (Architectural Models)
┌─────────────────────────────────────────┐
│  DESIGNER AGENT                         │
│  ├─ Synthesize architecture decisions   │
│  ├─ Generate architecture documentation │
│  ├─ Create component specifications     │
│  ├─ Define interfaces & protocols       │
│  └─ Document design rationale           │
└─────────────────────────────────────────┘
          ↓ (Architecture Documentation)
┌─────────────────────────────────────────┐
│  EVALUATOR AGENT                        │
│  ├─ Check against requirements          │
│  ├─ Verify architectural standards      │
│  ├─ Assess quality attributes           │
│  ├─ Identify design violations          │
│  └─ Provide improvement recommendations │
└─────────────────────────────────────────┘
          ↓ (Evaluation Report)
    [Feedback Loop to Refinement]
```

### 2. **Hierarchical Memory Architecture**

MAAD implements a three-layer memory system for knowledge management:

#### Layer 1: **Working Memory (Task-Specific)**
- Stores current agent state and intermediate outputs
- Maintains task-specific context (requirements, partial designs)
- Enables real-time decision-making within current task
- Lifespan: Single design task
- Example: "Current component design includes API gateway for rate limiting"

#### Layer 2: **Episodic Memory (Task History)**
- Records completed design tasks and their outcomes
- Captures design decisions and rationale
- Enables learning from past design experiences
- Supports cross-task pattern recognition
- Lifespan: Session/project
- Example: "In Project-X, microservice pattern reduced latency by 40% for similar requirements"

#### Layer 3: **Semantic Memory (Domain Knowledge)**
- Encodes architectural patterns, standards, and best practices
- Stores domain-specific knowledge and constraints
- Integrates external knowledge sources via RAG
- Provides authoritative architectural guidance
- Lifespan: Long-term, continuously updated
- Example: "Cloud-native applications should use 12-factor methodology; containerization recommended for polyglot environments"

#### Memory Integration via RAG

```
Query: "Design architecture for IoT sensor network"
         ↓
[Semantic Retrieval Engine]
         ↓
Retrieve relevant:
├─ Architectural patterns (Event-driven, Message queue)
├─ Design standards (IoT framework standards)
├─ Security guidelines (IoT security best practices)
└─ Quality attribute patterns (Scalability, Latency)
         ↓
[Augment Agent Context]
         ↓
Agent generates informed architecture with:
├─ Industry best practices
├─ Proven patterns for similar domains
├─ Compliance requirements
└─ Quality attribute trade-offs
```

### 3. **Knowledge Infusion Strategy**

MAAD uses RAG to integrate architectural standards and patterns:

- **Architectural Standards Base:** IEEE 1471, C4 model, microservices patterns
- **Domain-Specific Patterns:** Cloud patterns (Netflix, AWS), IoT patterns, mobile patterns
- **Security & Compliance:** OWASP, industry regulations, data protection standards
- **Quality Attribute Patterns:** Scalability, fault-tolerance, latency optimization

**Infusion mechanism:**
1. Agent formulates query based on current task context
2. Retrieve relevant knowledge from semantic memory
3. Rank retrieved knowledge by relevance and authority
4. Inject top-K items into agent prompt/context
5. Agent generates architecture informed by authoritative sources

### 4. **4+1 View Model**

The framework structures architecture design using Kruchten's 4+1 view model:

| View | Purpose | Agent Responsibility |
|------|---------|----------------------|
| **Logical View** | Component structure & relationships | Modeler identifies key components, abstractions |
| **Physical View** | Deployment topology, hardware layout | Designer maps components to nodes/regions |
| **Process View** | Dynamic behavior, concurrency, communication | Modeler specifies interactions, protocols |
| **Development View** | Code organization, build/packaging | Designer defines structure for developers |
| **Use Case View** | Functional scope & user scenarios | Analyst maps requirements to scenarios |

### 5. **Agent Specialization & Coordination**

Each agent has distinct responsibilities and specialized prompts:

```
┌──────────────────────────────────────────────────────────┐
│ ANALYST AGENT (Requirement Specialist)                   │
│ ├─ Expertise: Requirements extraction, domain analysis   │
│ ├─ Input: Natural language requirements document         │
│ ├─ Output: Structured requirement specification          │
│ ├─ Memory: Episodic (past requirement patterns)          │
│ └─ Knowledge: Standards for requirement specifications   │
├──────────────────────────────────────────────────────────┤
│ MODELER AGENT (Architecture Specialist)                  │
│ ├─ Expertise: Modeling techniques, pattern design        │
│ ├─ Input: Requirement specifications                     │
│ ├─ Output: 4+1 view models (diagrams, descriptions)      │
│ ├─ Memory: Episodic (architectural patterns)             │
│ └─ Knowledge: Architectural patterns, modeling standards  │
├──────────────────────────────────────────────────────────┤
│ DESIGNER AGENT (Documentation Specialist)                │
│ ├─ Expertise: Architecture documentation, design rationale│
│ ├─ Input: Architectural models                           │
│ ├─ Output: Complete architecture documentation           │
│ ├─ Memory: Episodic (design decisions made)              │
│ └─ Knowledge: Documentation standards, design practices  │
├──────────────────────────────────────────────────────────┤
│ EVALUATOR AGENT (Quality Assurance Specialist)           │
│ ├─ Expertise: Quality assessment, standards verification │
│ ├─ Input: Architecture documentation                     │
│ ├─ Output: Evaluation report with recommendations        │
│ ├─ Memory: Episodic (past evaluation patterns)           │
│ └─ Knowledge: Quality standards, architectural guidelines│
└──────────────────────────────────────────────────────────┘
```

### 6. **Evaluation-Driven Refinement Loop**

Rather than one-shot generation, MAAD implements iterative refinement:

```
Iteration 1:
├─ Generate initial architecture
├─ Run evaluation
├─ Identify quality gaps
└─ → Refinement needed

Iteration N:
├─ Generate refined architecture
├─ Assess against previous version
├─ Check requirement coverage
└─ → Acceptable? → Done / → Refine again

Evaluation Criteria:
├─ Requirement coverage (all requirements addressed?)
├─ Quality attributes (scalability, security, performance)
├─ Architectural coherence (consistent patterns?)
├─ Standards compliance (follows best practices?)
└─ Design clarity (understandable documentation?)
```

## Main Ideas & Contributions

### 1. **Knowledge-Driven Multi-Agent Orchestration for Architecture Design**

**Key Innovation:** Rather than treating architecture design as a black-box generation task, MAAD:
- Decomposes design into specialized sub-tasks (analysis, modeling, design, evaluation)
- Assigns agents to roles matching their specialization
- Uses structured communication through hierarchical memory
- Integrates external knowledge through RAG at each stage

**Benefit:** Agents can leverage domain knowledge and best practices, producing architectures grounded in industry standards rather than hallucinated patterns.

### 2. **Hierarchical Memory for Cross-Task Knowledge Reuse**

**Key Innovation:** Three-layer memory system enables:
- **Working memory:** Real-time task context without interference from past tasks
- **Episodic memory:** Learning from design patterns across projects
- **Semantic memory:** Authoritative knowledge integration via RAG

**Benefit:** Agents don't restart from scratch on each design task; they accumulate experience while maintaining clean separation of concerns.

### 3. **Evaluation at Every Stage, Not Just End**

**Key Innovation:** Rather than evaluating final output, MAAD embeds evaluation throughout:
- Analyst outputs validated for completeness
- Modeler outputs checked for coherence
- Designer outputs assessed for standards compliance
- Final design iteratively refined based on evaluation

**Benefit:** Early error detection enables correction at the stage where they originate, reducing rework.

### 4. **4+1 View Model Ensures Comprehensive Architecture**

**Key Innovation:** Structuring design using the 4+1 view model ensures all architectural perspectives are covered:
- Logical view (components)
- Physical view (deployment)
- Process view (runtime)
- Development view (code organization)
- Use cases (functional scope)

**Benefit:** Reduces gaps where certain perspectives are overlooked; ensures completeness.

### 5. **RAG-Enhanced Knowledge Integration**

**Key Innovation:** Semantic memory uses RAG to inject relevant architectural knowledge:
- Retrieves patterns matching current task domain
- Provides architectural standards and best practices
- Grounds generation in authoritative sources

**Benefit:** Generated architectures are informed by industry best practices, not just LLM training data.

## Methodology & Implementation

### 1. **System Architecture**

```
┌─────────────────────────────────────────────────────────┐
│ User Input (Natural Language Requirements)              │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│ MAAD Orchestrator                                       │
│  ├─ Agent Coordinator (sequential task assignment)     │
│  ├─ Memory Manager (L1, L2, L3 management)            │
│  ├─ RAG Engine (knowledge retrieval & infusion)        │
│  └─ Feedback Controller (evaluation & refinement)      │
└────────────────────┬────────────────────────────────────┘
                     ↓
        ┌────────────┴────────────┐
        ↓                         ↓
   [Agents] ←────────────→ [Memories]
        ↓                         ↑
┌──────────────────────┐     ┌──────────────────┐
│ Claude 3.5 Sonnet    │     │ Working Memory   │
│ (LLM Backbone)       │     │ Episodic Memory  │
└──────────────────────┘     │ Semantic Memory  │
                             └──────────────────┘
                                     ↑
                             ┌───────────────────┐
                             │ RAG Engine        │
                             │ Knowledge Base    │
                             └───────────────────┘
                                     ↑
        ┌────────────────────────────┼─────────────────┐
        │                            │                 │
   [Architectural    [Architectural  [Security &  [Quality Attr
    Patterns DB]     Standards DB]   Compliance]   Patterns]
```

### 2. **Evaluation Benchmarks & Datasets**

**Datasets used:**
- **Architecture Design Corpus:** 200+ real-world software architecture documents
- **Requirements Collections:** Various industry domains (fintech, healthcare, IoT, enterprise)
- **Architectural Standards:** IEEE 1471, C4 model definitions, domain-specific patterns

**Evaluation metrics:**
- **Requirement Coverage:** % of requirements addressed in final architecture
- **View Completeness:** Presence of all 4+1 views with sufficient detail
- **Pattern Usage:** % of recommended patterns correctly applied
- **Standards Compliance:** Adherence to architectural guidelines and best practices
- **Documentation Quality:** Clarity, completeness, and usefulness for implementation teams

### 3. **Experimental Setup**

**Test scenarios:**
1. **Simple Web Application:** Standard CRUD app (5-7 requirements)
2. **Microservices Platform:** Cloud-native system (15-20 requirements)
3. **IoT System:** Distributed sensor network (12-18 requirements)
4. **Enterprise System:** Legacy modernization (20-30 requirements)
5. **Real-world Requirements:** Actual customer specifications

### 4. **Results & Key Findings**

#### Finding 1: Multi-Agent Orchestration Improves Completeness

**Single-Agent Baseline (Claude 3.5 direct prompt):**
- 4+1 Views completeness: 65% (often 2-3 views missing)
- Requirement coverage: 72%
- Evaluation score: 6.8/10

**MAAD (4-agent orchestration):**
- 4+1 Views completeness: 94% (all views present with detail)
- Requirement coverage: 91%
- Evaluation score: 8.9/10

**Finding:** Specialized agents with role clarity produce more complete architectures than monolithic generation.

#### Finding 2: Knowledge Integration Reduces Hallucination

**Without RAG-enhanced semantic memory:**
- Incorrect patterns applied: 23%
- Non-standard design choices: 31%
- Compliance violations: 15%

**With RAG-enhanced semantic memory:**
- Incorrect patterns applied: 4%
- Non-standard design choices: 8%
- Compliance violations: 2%

**Finding:** Grounding agents in authoritative knowledge sources significantly reduces design mistakes.

#### Finding 3: Iterative Evaluation Improves Quality

**Single-pass design (no evaluation):**
- Requirement misalignment: 18%
- Architectural inconsistencies: 22%
- Quality attribute gaps: 25%

**With 1 evaluation-refinement cycle:**
- Requirement misalignment: 8%
- Architectural inconsistencies: 9%
- Quality attribute gaps: 11%

**With 2+ evaluation-refinement cycles:**
- Requirement misalignment: 3%
- Architectural inconsistencies: 4%
- Quality attribute gaps: 5%

**Finding:** Early evaluation and iterative refinement significantly improve final architecture quality.

#### Finding 4: Memory Hierarchy Enables Cross-Project Learning

**Without episodic/semantic memory (stateless agents):**
- Design time for project N: ~T minutes
- Quality degradation per project: 5-8%

**With episodic memory (task history):**
- Design time for project N: ~0.8T minutes (20% improvement)
- Quality stable across projects

**With episodic + semantic memory (full hierarchy):**
- Design time for project N: ~0.6T minutes (40% improvement)
- Quality improvement as agents accumulate experience

**Finding:** Hierarchical memory enables agents to learn and improve across multiple design tasks.

#### Finding 5: Agent Specialization Matters

Performance comparison:
- Generic single-agent LLM: 6.8/10 quality score
- Generic multi-agent (same prompts): 7.2/10
- Specialized multi-agent (role-specific prompts): 8.9/10

**Finding:** Role specialization and expert-crafted prompts are essential for agent effectiveness.

## Practical Applications & Use Cases

### 1. **Software Architecture Design Automation**

**Direct application:** MAAD can automate initial architecture design from requirements:

```
Input: "Build scalable e-commerce platform for 10M users with
        real-time inventory sync, payment processing, and mobile apps"

Output:
├─ Requirement Analysis (50 structured requirements)
├─ 4+1 Architecture Models
│  ├─ Logical: API Gateway → Microservices (inventory, order, payment)
│  ├─ Physical: Multi-region deployment, CDN, databases
│  ├─ Process: Async event flows, caching layers
│  ├─ Development: Repo structure, API contracts
│  └─ Use Cases: User purchase, admin dashboard, mobile app
├─ Design Decisions (30+ documented choices with rationale)
├─ Implementation Guidelines (deployment, scaling, security)
└─ Quality Assessment (99% uptime target achievable, 2s latency optimal)
```

### 2. **Legacy System Modernization**

**Application:** MAAD guides architecture refactoring:

```
Input: "Modernize 20-year-old monolithic banking system
        to microservices while maintaining HIPAA compliance
        and reducing operational costs by 30%"

MAAD Output:
├─ Migration phases (3-phase approach)
├─ New microservice boundaries (20 services identified)
├─ Data consistency strategy (event sourcing for transactions)
├─ Security architecture (API gateway, service mesh, encryption)
├─ Cost optimization plan (serverless for variable-load services)
└─ Implementation roadmap (8-12 month timeline)
```

### 3. **Architecture Review & Validation**

**Application:** Evaluate existing architectures:

```
Input: "Review existing architecture against updated requirements"

MAAD Output:
├─ Gap analysis (which requirements not well-addressed)
├─ Quality assessment (scalability, security, maintainability scores)
├─ Pattern violations identified (improper use of patterns)
├─ Recommendations for improvement (15-20 specific suggestions)
└─ Risk assessment (technical debt, scalability bottlenecks)
```

### 4. **Cross-Domain Architecture Knowledge Transfer**

**Application:** Learn from one domain, apply to similar domains:

```
Financial System Architecture → Healthcare System Architecture

Episodic Memory:
"In fintech, event-driven architecture reduced coupling between
 payment processing and account management, enabling independent
 scaling and testing. Consider similar for EHR data flow."

→ Applied to healthcare: Event-driven for lab results, insurance
  processing, and medication records
```

### 5. **Real-Time Architecture Guidance for Teams**

**Integration in development workflow:**

1. Development team writes requirements
2. MAAD generates initial architecture
3. Team reviews and provides feedback
4. MAAD refines architecture based on feedback
5. Iterative process until team accepts design

**Timeline:** Full architecture design in hours rather than weeks.

### 6. **Standards Compliance Automation**

**Application:** Ensure architectures meet standards:

```
Regulatory Requirements:
├─ HIPAA (healthcare data protection)
├─ GDPR (data privacy)
├─ SOC 2 Type II (security controls)
└─ Industry-specific standards

MAAD enforces compliance by:
├─ Retrieving relevant standards during design
├─ Checking generated architecture against standards
├─ Recommending compliance patterns
└─ Documenting compliance measures
```

## Insights & Implications

### Key Insights

1. **Architecture design requires specialized expertise:** Decomposing design into specialist roles (analyst, modeler, designer, evaluator) outperforms generic monolithic generation.

2. **Knowledge integration is critical:** Grounding agents in authoritative sources (standards, patterns, best practices) reduces hallucination and improves quality significantly.

3. **Hierarchical memory enables learning:** Three-layer memory (working, episodic, semantic) allows agents to accumulate experience while maintaining task isolation.

4. **Iterative evaluation improves outcomes:** Embedding evaluation at each stage enables early error detection and iterative refinement, improving final quality.

5. **Role-specific prompting matters:** Generic multi-agent frameworks with identical prompts underperform; specialized role-aware prompts drive significant quality improvements.

### Implications for Multi-Agent Development

1. **Role Specialization Pattern:** Multi-agent systems should assign clear, specialized roles rather than treating agents as interchangeable.

2. **Memory Hierarchy Design:** Implementing working/episodic/semantic memory separation improves both performance and knowledge reuse.

3. **Knowledge Integration:** RAG-enhanced semantic memory is essential for grounding agentic behavior in authoritative sources.

4. **Iterative Refinement:** Evaluation should be continuous, not post-hoc; early error detection enables efficient correction.

5. **Feedback Loops:** Agent orchestration should include feedback mechanisms between sequential agents.

### Limitations & Challenges

1. **Knowledge Base Maintenance:** Semantic memory (architectural standards, patterns) requires ongoing curation and updates.

2. **Scalability:** Current approach sequential; parallel agent execution could improve speed but complicates coordination.

3. **Conflict Resolution:** When agents disagree (e.g., Analyst vs. Modeler interpretation), current framework lacks sophisticated conflict resolution.

4. **Domain Coverage:** Knowledge base is most effective for well-documented domains (cloud, microservices); less mature domains lack knowledge resources.

5. **Human Oversight:** Complex architectural decisions still benefit from human expert review; full automation may miss nuanced trade-offs.

## Code & Resources

### Paper & Artifacts

- **ArXiv Paper:** [Bridging Requirements and Architecture: Multi-Agent Orchestration with External Knowledge and Hierarchical Memory](https://arxiv.org/abs/2606.01385)
- **Full PDF:** [PDF Link](https://arxiv.org/pdf/2606.01385)
- **Supplementary Materials:** Architecture templates, evaluation rubrics, knowledge base samples

### Implementation Frameworks

**Agent Frameworks (potential implementations):**
- [AutoGen](https://github.com/microsoft/autogen) - Multi-agent conversation framework with role support
- [LangGraph](https://github.com/langchain-ai/langgraph) - Stateful orchestration with feedback loops
- [CrewAI](https://github.com/joaomdmoura/crewai) - Role-based agent orchestration

**RAG Libraries:**
- [LangChain RAG](https://python.langchain.com/docs/modules/data_connection/) - Knowledge retrieval integration
- [LlamaIndex](https://www.llamaindex.ai/) - Data indexing for LLM applications
- [Semantic Kernel](https://github.com/microsoft/semantic-kernel) - Plugin-based knowledge integration

### Knowledge Bases & Standards

- [IEEE 1471 Standard](https://standards.ieee.org/ieee/1471/6195/) - Architecture description standard
- [C4 Model](https://c4model.com/) - Software architecture visualization
- [AWS Architecture Patterns](https://aws.amazon.com/architecture/patterns/) - Cloud architecture examples
- [Microservices Patterns](https://microservices.io/) - Distributed system patterns
- [12-Factor App Methodology](https://12factor.net/) - Cloud-native application principles

### Sample Integration

```python
from crewai import Agent, Task, Crew
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# Define specialist agents
analyst = Agent(
    role="Requirements Analyst",
    goal="Extract and structure software requirements",
    expertise=["requirements engineering", "domain analysis"]
)

modeler = Agent(
    role="Architecture Modeler",
    goal="Create 4+1 architecture models",
    expertise=["software architecture", "UML modeling"]
)

# Implement hierarchical memory
class HierarchicalMemory:
    def __init__(self):
        self.working = {}
        self.episodic = []
        self.semantic = FAISS.from_documents(
            load_architectural_knowledge(),
            OpenAIEmbeddings()
        )

# Orchestrate with evaluation loop
tasks = [
    Task(agent=analyst, description="Analyze requirements"),
    Task(agent=modeler, description="Model architecture"),
    Task(agent=designer, description="Design architecture"),
    Task(agent=evaluator, description="Evaluate design")
]

crew = Crew(agents=[analyst, modeler, designer, evaluator], tasks=tasks)
```

## Related Work & Context

### Foundational Architecture Design Research

- **[Domain-Driven Design](https://www.domaindriven.org/)** (Evans) - Foundational concepts for architecture design
- **[Software Architecture in Practice](https://www.informit.com/books/software-architecture-practice)** (Bass et al.) - Comprehensive architecture principles
- **[4+1 View Model](https://en.wikipedia.org/wiki/4%2B1_architectural_view_model)** (Kruchten, 1995) - Architectural viewpoint framework

### Recent Multi-Agent Architecture Work

- **[MACOG: Multi-Agent Code Orchestrated Generation Infrastructure](https://arxiv.org/abs/2410.04835)** - Multi-agent code generation
- **[AgentForge: Execution-Grounded Multi-Agent LLM Framework](https://arxiv.org/abs/2604.13120)** - Execution-driven agent orchestration
- **[Self-Organizing Multi-Agent Systems for Continuous Software Development](https://arxiv.org/abs/2603.25928)** - Dynamic multi-agent coordination

### Knowledge Integration & RAG

- **[Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)** - Foundational RAG concepts
- **[How Well Do Agentic Skills Work in the Wild](https://arxiv.org/abs/2604.04323)** - Knowledge and skill integration for agents
- **[Externalization in LLM Agents: A Unified Review](https://arxiv.org/abs/2604.08224)** - Memory and knowledge management

### Specialized Agent Topologies

- **[Agent Skills for Large Language Models](https://arxiv.org/abs/2602.12430)** - Skill-based agent design
- **[AutoSkill: Experience-Driven Lifelong Learning via Skill Self-Evolution](https://arxiv.org/abs/2603.01145)** - Skill learning and adaptation
- **[Trace2Skill: Distill Trajectory-Local Lessons into Transferable Agent Skills](https://arxiv.org/abs/2603.25158)** - Extracting skills from trajectories

### Future Research Directions

1. **Conflict Resolution:** How to resolve disagreements between specialist agents?
2. **Parallel Orchestration:** Can agents work in parallel with asynchronous coordination?
3. **Human-AI Collaboration:** Integrating human expert feedback into iterative refinement
4. **Domain Transfer:** Applying architectures learned in one domain to novel domains
5. **Real-Time Refinement:** Updating architecture based on implementation feedback

---

**Citation:**

```bibtex
@article{li2026bridging,
  title={Bridging Requirements and Architecture: Multi-Agent Orchestration with External Knowledge and Hierarchical Memory},
  author={Li, Ruiyin and Zhang, Yiran and Zhou, Xiyu and Cai, Yangxiao and Liang, Peng and Sun, Weisong and Xuan, Jifeng and Jin, Zhi and Liu, Yang},
  journal={arXiv preprint arXiv:2606.01385},
  year={2026}
}
```
