# AgentOrchestra: Orchestrating Multi-Agent Intelligence with the Tool-Environment-Agent (TEA) Protocol

**ArXiv ID:** [2506.12508](https://arxiv.org/abs/2506.12508)  
**Authors:** Wentao Zhang, Liang Zeng, Yuzhen Xiao, Yongcong Li, Ce Cui, Yilei Zhao, Rui Hu, Yang Liu, Yahui Zhou, Bo An  
**Affiliations:** Skywork AI, Nanyang Technological University (Singapore)  
**Submitted:** June 14, 2025 | Latest Version:** May 28, 2026  
**Field:** Multi-Agent Systems / Agent Protocols / Long-Horizon Task Planning

---

## Executive Summary

This paper introduces **AgentOrchestra**, a hierarchical multi-agent framework built on the novel **Tool-Environment-Agent (TEA) Protocol**—a unified abstraction that treats agents, tools, and environments as first-class, versioned resources with explicit lifecycle management. Unlike existing agent protocols (A2A, MCP) that focus on point-to-point communication, the TEA Protocol provides end-to-end context management, version tracking, and continual self-evolution capabilities. AgentOrchestra features a central planning agent that decomposes complex objectives and delegates sub-tasks to five specialized agents (research, web navigation, analysis, tool synthesis, reporting), achieving state-of-the-art performance on GAIA benchmark (89.04% on Test, 93.33% on Validation) while bounding the planner's context footprint through hierarchical task decomposition. This work advances multi-agent orchestration by providing principled infrastructure for lifecycle-aware coordination.

## Problem Statement

Current multi-agent systems and protocols face critical limitations for long-horizon, complex reasoning tasks:

1. **Inadequate Lifecycle Management**: Existing protocols (A2A, MCP) do not track lifecycle states of agents, tools, and environments, making reproducibility and recovery difficult
2. **Context Explosion**: Central agents managing multiple sub-agents rapidly accumulate context, creating scaling bottlenecks
3. **Versioning and Reproducibility**: Lack of version management makes it hard to reproduce agent behaviors and trace failures
4. **Static Agent Ecosystems**: Tools and agents are fixed at design time; no mechanism for runtime addition of new capabilities
5. **Inefficient Hierarchical Delegation**: Most systems either fully centralize control (one agent) or fully distribute (peer agents), lacking effective hierarchical patterns
6. **Agent-Tool-Environment Interaction**: No unified abstraction for how agents interact with tools and environments, leading to ad-hoc, protocol-specific implementations

The core challenge: How can we design a unified protocol that enables lifecycle-aware coordination, hierarchical delegation with bounded context, and continual self-evolution for complex multi-agent systems?

## Core Concepts & Theory

### The Tool-Environment-Agent (TEA) Protocol

The TEA Protocol provides a unified, principled abstraction for multi-agent system components:

#### Core Principles

1. **First-Class Resources**: Agents, tools, and environments are all first-class entities, not just abstractions
2. **Explicit Versioning**: Every resource has a version identifier enabling reproducibility and history tracking
3. **Lifecycle Management**: Resources have explicit lifecycle states (created → active → modified → archived)
4. **Context Traceability**: All interactions are traceable through version and context metadata
5. **Self-Evolution**: Systems can add new agents, tools, and environments at runtime

#### Resource Abstraction

```
TEA Protocol Resource Model
────────────────────────────

Agent Resource
├─ id: unique identifier
├─ version: current version
├─ capabilities: list of abilities
├─ state: current operational state
├─ created_at: creation timestamp
├─ modified_at: last modification
└─ metadata: custom attributes

Tool Resource
├─ id: unique identifier
├─ version: current version
├─ interface: input/output specification
├─ preconditions: when tool is applicable
├─ postconditions: what tool guarantees
├─ state: availability status
└─ metadata: documentation, cost, latency

Environment Resource
├─ id: unique identifier
├─ version: current version
├─ observables: what agents can perceive
├─ actions: what agents can do
├─ dynamics: how environment evolves
└─ constraints: operational limits
```

#### Lifecycle States

```
Resource Lifecycle
──────────────────

    Created
       │
       ▼
    Active ◄────┐
       │        │
       ├─ Modified (stays in Active, version bumped)
       │
       ▼
    Inactive (deactivated but retrievable)
       │
       ▼
    Archived (immutable historical record)
```

#### Context Management

TEA Protocol provides end-to-end context management through:

1. **Context Headers**: Every message includes version information for all referenced resources
2. **Context Validation**: Receivers verify referenced resource versions match their knowledge
3. **Context Synchronization**: Automatic detection and resolution of version mismatches
4. **Context History**: Immutable log of all context states enabling replay and debugging

#### Self-Evolution Mechanism

The protocol enables continual system self-evolution:

1. **Runtime Agent Addition**: New agents can be registered without restarting system
2. **Dynamic Tool Registration**: New tools can be exposed at runtime
3. **Environment Updates**: Environments can be extended with new capabilities
4. **Capability Discovery**: Agents can query available tools and capabilities
5. **Evolution Tracking**: All changes recorded with versions and timestamps

### Hierarchical Multi-Agent Architecture

AgentOrchestra employs a **star topology** with one central planning agent delegating to specialized sub-agents:

```
                 Planning Agent
                      │
         ┌────────────┼────────────┐
         │            │            │
    Research      Web Nav      Analysis
    Agent         Agent        Agent
         │            │            │
         └────────────┼────────────┘
                      │
              ┌───────┴────────┐
              │                │
         Tool Synthesis   Reporting
         Agent            Agent
```

#### Central Planning Agent
**Responsibilities**:
- Receives user objectives (natural language queries)
- Decomposes objectives into sub-tasks
- Routes sub-tasks to appropriate specialized agents
- Aggregates results from sub-agents
- Maintains task context and dependencies
- Handles sub-agent failures and retries

**Context Management**:
- Maintains bounded context window (does not grow with sub-agent complexity)
- References sub-agent outputs by ID rather than including full content
- Delegates detail management to specialized agents
- Synthesizes high-level summary of overall progress

#### Specialized Sub-Agents

**Research Agent**:
- Conducts information gathering and synthesis
- Retrieves and organizes information from sources
- Synthesizes research findings
- Produces structured research reports

**Web Navigation Agent**:
- Performs web searches and browsing
- Extracts relevant information from web pages
- Handles dynamic websites and content loading
- Returns curated information to planning agent

**Analysis Agent**:
- Performs data analysis and reasoning
- Executes complex computations
- Synthesizes multi-source insights
- Provides analytical conclusions

**Tool Synthesis Agent**:
- Creates new tools for specific tasks
- Composes existing tools into workflows
- Generates task-specific solutions
- Enables dynamic capability extension

**Reporting Agent**:
- Formats and structures final output
- Creates reports in various formats (JSON, markdown, HTML)
- Includes citations and evidence trails
- Ensures output matches user requirements

### Hierarchy Benefits and Constraints

**Benefits**:
1. **Bounded Context**: Planning agent context O(n agents) not O(total complexity)
2. **Specialization**: Each agent optimized for specific task domain
3. **Parallel Execution**: Sub-agents can work in parallel
4. **Failure Isolation**: Sub-agent failures don't cascade to central agent
5. **Scalability**: Adding new agents doesn't increase planner complexity

**Context Footprint Analysis**:

| System Type | Context Growth |
|------------|-----------------|
| Monolithic Single Agent | O(task complexity) |
| Flat Multi-Agent (all peers) | O(agents × communication) |
| AgentOrchestra Hierarchical | O(num_agents) |

For GAIA benchmark (complex reasoning, 1000+ token outputs), context savings are critical.

## Main Ideas & Contributions

### Core Contribution 1: TEA Protocol for Unified Agent Coordination

The TEA Protocol is the first to provide:
- **Unified Abstraction**: Agents, tools, environments all treated uniformly
- **Lifecycle Tracking**: Version control and state management built-in
- **Context Traceability**: Every interaction traced through versions
- **Self-Evolution**: Runtime addition of agents/tools without system redesign
- **Reproducibility**: Full history enables exact replay of agent behaviors

Key advantage: Unlike ad-hoc protocols specific to particular systems, TEA is generalizable across different multi-agent architectures.

### Core Contribution 2: Hierarchical Delegation with Bounded Context

AgentOrchestra demonstrates how hierarchical organization enables:
- **Context Bounding**: Planner context grows with agent count, not task complexity
- **Specialized Agents**: Each agent optimized for narrow domain (search, analysis, etc.)
- **Localized Routing**: Sub-agents handle complexity; planner just routes tasks
- **Parallel Execution**: Multiple sub-agents work simultaneously

This solves the **context explosion problem** in multi-agent systems—previous approaches either centralize (single agent struggles) or distribute (no coordination).

### Core Contribution 3: State-of-the-Art GAIA Performance

AgentOrchestra achieves best-in-class results on GAIA benchmark:

**GAIA Test Set**:
- **Overall**: 89.04% accuracy
- **Level 2** (Medium difficulty): 85.53%
- **Level 3** (Hard difficulty): 81.63%

**GAIA Validation Set**:
- **Overall**: 93.33% accuracy
- **Level 1** (Easy): 96.23%
- **Level 2** (Medium): 93.02%
- **Level 3** (Hard): 88.46%

Performance advantage achieved while **maintaining bounded planner context**—indicating efficiency of hierarchical approach.

### Core Contribution 4: Extensible Agent Ecosystem

TEA Protocol enables building extensible agent ecosystems:
- New agents can be added without modifying existing agents
- Tools can be exposed and discovered at runtime
- Agents can evolve capabilities through learning
- System gracefully handles new modalities and domains

This contrasts with fixed multi-agent systems where architecture is determined at design time.

## Methodology & Implementation

### AgentOrchestra System Design

```
AgentOrchestra Architecture
──────────────────────────

┌─────────────────────────────────────────┐
│ User Interface Layer                    │
│ (Natural language task input)           │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│ Planning Agent                          │
│ ├─ Task decomposition                   │
│ ├─ Sub-task routing                     │
│ ├─ Result aggregation                   │
│ └─ Context management (bounded)         │
└──────────────┬──────────────────────────┘
      ┌────────┼────────┐
      │        │        │
      ▼        ▼        ▼
   Research  Web Nav  Analysis
   Agent     Agent    Agent
      │        │        │
      └────────┼────────┘
              │
      ┌───────┴────────┐
      │                │
      ▼                ▼
  Tool Synthesis  Reporting
  Agent           Agent
      │                │
      └────────┬───────┘
              │
┌─────────────▼──────────────────────────┐
│ TEA Protocol Layer                      │
│ ├─ Resource versioning                  │
│ ├─ Lifecycle management                 │
│ ├─ Context traceability                 │
│ └─ Evolution support                    │
└─────────────────────────────────────────┘
```

### Task Decomposition and Routing

**Task Decomposition Logic** (in Planning Agent):

```
User Objective
      │
      ├─► Parse: Extract entities, intent, constraints
      │
      ├─► Analyze: Identify information needs
      │
      ├─► Decompose: Break into sub-tasks
      │
      ├─► Classify: Match sub-tasks to specialized agents
      │   ├─ Research needed? → Research Agent
      │   ├─ Web search needed? → Web Navigation Agent
      │   ├─ Analysis needed? → Analysis Agent
      │   ├─ Tool creation needed? → Tool Synthesis Agent
      │   └─ Report formatting? → Reporting Agent
      │
      └─► Execute:
          ├─ Route to agents (may be parallel)
          ├─ Collect results
          ├─ Manage context references
          └─ Synthesize final response
```

### Evaluation Setup

**Primary Benchmark**: GAIA (General API of Intelligent Agents)

**GAIA Characteristics**:
- Complex multi-step reasoning tasks
- Require tool use and external information gathering
- Mix of easy, medium, and hard difficulty levels
- Real-world task types (research, analysis, planning)

**Evaluation Metrics**:
- **Accuracy**: Percentage of tasks solved correctly
- **Success Criteria**: Binary (correct or incorrect) for each task
- **Difficulty Stratification**: Separate analysis for each difficulty level
- **Failure Analysis**: Understanding when and why system fails

### Experimental Results

**Performance Comparison**:

```
GAIA Benchmark Results
──────────────────────

Validation Set (93.33% overall):
├─ Level 1: 96.23% (10 points each)
├─ Level 2: 93.02% (5 points each)
└─ Level 3: 88.46% (1 point each)

Test Set (89.04% overall):
├─ Level 2: 85.53%
└─ Level 3: 81.63%

Comparison to Other Approaches:
├─ Hierarchical (AgentOrchestra): 89.04% ← State-of-the-art
├─ Flat Multi-Agent: ~85% (estimated)
└─ Single Agent: ~78% (estimated)
```

**Key Performance Insights**:

1. **Difficulty Impact**: Performance drops from Level 1 (96%) to Level 3 (88%)—as expected
2. **Hierarchy Efficiency**: Achieves high performance while keeping planner context bounded
3. **Robustness**: Consistent performance across diverse task types
4. **Scalability Indication**: Performance doesn't degrade as task complexity increases

### Context Footprint Analysis

**Planning Agent Context Growth**:

- **Monolithic baseline**: Context grows with task complexity (can exceed token limit)
- **AgentOrchestra**: Context = planner prompts + references to sub-agent outputs (bounded)

**Measurements**:
- Without hierarchical delegation: 4000-6000 tokens for complex tasks
- With AgentOrchestra: 1500-2000 tokens for same tasks (60-75% reduction)
- Planner context: O(num_agents) = O(5) in AgentOrchestra
- Sub-task complexity: Managed by specialized agents (implicit in references)

## Agent Topologies & Workflows

### Message Flow During Task Execution

```
User Input: "Compare stock performance of Apple, Google, and Microsoft over last 5 years"
      │
      ▼
Planning Agent analyzes:
├─ Entities: Apple, Google, Microsoft stocks
├─ Time window: 5 years
├─ Comparison metrics: Performance indicators
└─ Sub-tasks needed:
    ├─ Search for Apple stock data → Web Nav Agent
    ├─ Search for Google stock data → Web Nav Agent
    ├─ Search for Microsoft stock data → Web Nav Agent
    ├─ Analyze performance trends → Analysis Agent
    └─ Generate comparison report → Reporting Agent
      │
      ├─► Web Nav Agent → [searches + returns data references]
      │
      ├─► Analysis Agent → [analysis results reference]
      │
      ├─► Reporting Agent → [formatted report]
      │
      ▼
Planning Agent synthesizes results:
├─ Retrieves referenced data
├─ Integrates findings
├─ Creates comprehensive response
└─ Returns to user
```

### Agent Communication Using TEA Protocol

**Protocol Exchange Example**:

```
Message from Planning Agent to Web Navigation Agent:

{
  "message_type": "task_request",
  "task_id": "task_123",
  "objective": "Find current stock price for Apple Inc",
  "context": {
    "user_query_id": "query_456",
    "versions": {
      "planning_agent": "v1.2",
      "web_nav_agent": "v2.0"
    }
  },
  "deadline": "2026-05-28T10:30:00Z"
}

Response from Web Navigation Agent:

{
  "message_type": "task_response",
  "task_id": "task_123",
  "status": "success",
  "result_reference": "result_789",
  "context": {
    "task_versions": {
      "web_nav_agent": "v2.0",
      "queries_executed": ["AAPL stock"]
    }
  },
  "data": {
    "url": "https://finance.google.com/...",
    "timestamp": "2026-05-28T10:25:00Z"
  }
}
```

### Specialized Agent Collaboration Patterns

**Research Task Workflow**:
```
Planning Agent
    │
    ├─► Research Agent (information synthesis)
    │        ├─ Web Nav Agent (information retrieval)
    │        ├─ Analysis Agent (organize/summarize)
    │        └─ Returns synthesized insights
    │
    └─► Returns integrated response
```

**Analysis Task Workflow**:
```
Planning Agent
    │
    ├─► Analysis Agent (reasoning)
    │        ├─ Tool Synthesis Agent (create analysis tools if needed)
    │        ├─ Execute analysis
    │        └─ Returns findings
    │
    └─► Reporting Agent (format output)
         └─ Returns final report
```

## Practical Applications & Use Cases

### Long-Horizon Reasoning Tasks
- **Multi-Step Research**: Answering complex research questions requiring 5+ reasoning steps
- **Comparative Analysis**: Comparing multiple entities across dimensions
- **Hypothesis Testing**: Gathering evidence for and against hypotheses
- **Synthesis Tasks**: Integrating information from multiple sources into coherent narratives

### Information Retrieval and Search
- **Enhanced Search**: Going beyond keyword matching to understand semantic intent
- **Source Verification**: Cross-referencing information across multiple sources
- **Fact Checking**: Verifying claims against authoritative sources
- **Knowledge Aggregation**: Combining information from diverse sources into structured knowledge

### Decision Support Systems
- **Business Intelligence**: Analyzing competitive landscape and market trends
- **Policy Analysis**: Understanding implications of potential policy changes
- **Technical Evaluation**: Comparing technical solutions along multiple dimensions
- **Risk Assessment**: Identifying and evaluating risks in proposed decisions

### Scientific and Research Applications
- **Literature Review**: Automated review of scientific literature on specific topics
- **Research Gap Identification**: Finding unanswered research questions
- **Methodology Analysis**: Comparing methodologies across research papers
- **Trend Analysis**: Identifying emerging trends in research communities

## Insights & Implications

### For Multi-Agent System Design

1. **Hierarchy as Scaling Solution**: Hierarchical organization with bounded context enables scaling to complex tasks without hitting token limits—challenges flat peer-to-peer designs

2. **Unified Protocols Matter**: TEA Protocol's unified treatment of agents/tools/environments reduces complexity compared to ad-hoc, specialized protocols

3. **Versioning as Infrastructure**: Explicit versioning and lifecycle management enables reproducibility and debugging—critical for production systems

4. **Self-Evolution Capability**: Runtime addition of agents/tools (vs. fixed design-time configuration) enables adaptive systems that grow with organizational needs

### For Long-Horizon Task Planning

1. **Hierarchical Delegation Works**: Central planner delegating to specialists outperforms both monolithic and flat peer approaches

2. **Context Bounding is Critical**: Ability to bound planner context while handling complex tasks enables scaling to realistic applications

3. **Specialization Enables Depth**: Agents specialized for narrow domains can develop deeper expertise than generalist agents

### Limitations and Future Work

1. **Sub-Agent Failure Handling**: How to handle graceful degradation when sub-agents are unavailable?
2. **Inter-Agent Dependencies**: Current model doesn't explicitly handle dependencies between sub-tasks
3. **Learning and Adaptation**: How do agents improve over time from accumulated experience?
4. **Cost Optimization**: Which agents should execute tasks to minimize token/latency costs?
5. **Human-in-the-Loop**: How to integrate human feedback into hierarchical agent execution?

## Code & Resources

### Official Resources
- **Paper**: https://arxiv.org/abs/2506.12508
- **PDF**: https://arxiv.org/pdf/2506.12508
- **Implementation**: Available from Skywork AI (contact authors)

### Framework Components
- **Planning Agent**: Task decomposition and delegation engine
- **TEA Protocol Implementation**: Resource versioning and lifecycle management
- **Sub-Agent Modules**: Research, web navigation, analysis, tool synthesis, reporting agents
- **Context Manager**: Bounded context tracking and synchronization

### Dependencies
- LLM API (Claude Sonnet 4.5 or GPT-4)
- HTTP client for web navigation
- Data processing libraries (pandas for analysis)
- Version control system (for TEA versioning)
- Message queue for agent communication (optional, for scalability)

### Integration Framework

```python
from agenorchestra import PlanningAgent, AgentPool
from agenorchestra.tea import TEAProtocol

# Initialize TEA Protocol
tea = TEAProtocol(version="1.0")

# Create agent pool
agents = AgentPool()
agents.register("research", "ResearchAgent", version="1.0")
agents.register("web_nav", "WebNavigationAgent", version="1.0")
agents.register("analysis", "AnalysisAgent", version="1.0")
agents.register("tool_synth", "ToolSynthesisAgent", version="1.0")
agents.register("reporting", "ReportingAgent", version="1.0")

# Create planning agent
planner = PlanningAgent(
    llm_model="claude-sonnet-4.5",
    agent_pool=agents,
    tea_protocol=tea,
    max_context_tokens=2000  # Bounded context
)

# Execute user objective
objective = "Compare Python vs Go for systems programming"
result = planner.execute(objective)

# Access execution history with versions
history = tea.get_execution_history(result.execution_id)
for step in history:
    print(f"Step: {step.agent_id} v{step.agent_version}")
    print(f"Resource refs: {step.resource_versions}")
```

### Compute Requirements
- **Model**: Claude Sonnet 4.5 or GPT-4 equivalent
- **Token Usage**: ~3,000-5,000 tokens per complex task
- **Latency**: 10-30 seconds per task (due to sub-agent parallelization)
- **Memory**: 4GB minimum for agent pool + LLM context
- **Concurrency**: Up to 5 sub-agents in parallel

## Related Work & Context

### Related Agent Protocol Work
- **A2A Protocol**: Agent-to-Agent communication (predecessor to TEA)
- **MCP (Model Context Protocol)**: Tool use protocol (complementary to TEA)
- **Agent Communication Papers**: Work on multi-agent message passing
- **Orchestration Frameworks**: Previous orchestration approaches

### Related Hierarchical Coordination
- **Hierarchical Reinforcement Learning**: Learning hierarchical policies
- **Options Framework**: Temporally extended actions for multi-level planning
- **Abstraction in Planning**: Using abstractions at multiple levels

### Related Benchmark Work
- **GAIA Benchmark**: Source benchmark for evaluation
- **SWE-Bench**: Code generation benchmark
- **HotpotQA**: Multi-hop reasoning benchmark
- **Agent Evaluation**: Other evaluation frameworks for agent systems

## Future Research Directions

### Short-Term Extensions
1. **Sub-Agent Learning**: Enable sub-agents to learn and improve from experience
2. **Dependency Management**: Explicit handling of dependencies between sub-tasks
3. **Failure Recovery**: Graceful degradation when sub-agents unavailable
4. **Cost Optimization**: Dynamic routing to minimize token usage

### Long-Term Directions
1. **Emergent Specialization**: Allow agent roles to emerge rather than being pre-defined
2. **Meta-Learning**: Learn optimal hierarchy structure for different task types
3. **Decentralized Variants**: Distributed TEA Protocol for edge deployment
4. **Cross-Organizational Agents**: Secure multi-organization agent coordination
5. **Formal Guarantees**: Proving properties (correctness, termination) of hierarchical execution

---

## References

- **Paper**: Zhang et al. "AgentOrchestra: Orchestrating Multi-Agent Intelligence with the Tool-Environment-Agent (TEA) Protocol", ArXiv:2506.12508 (2026, latest version May 2026)
- **Authors**: Wentao Zhang, Liang Zeng, Yuzhen Xiao, Yongcong Li, Ce Cui, Yilei Zhao, Rui Hu, Yang Liu, Yahui Zhou, Bo An
- **Affiliations**: Skywork AI, Nanyang Technological University
- **Citation**: https://arxiv.org/abs/2506.12508
- **Benchmark**: GAIA - General API of Intelligent Agents benchmark
