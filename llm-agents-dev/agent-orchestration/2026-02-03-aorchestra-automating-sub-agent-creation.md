# AOrchestra: Automating Sub-Agent Creation for Agentic Orchestration

**ArXiv ID:** 2602.03786  
**Authors:** Jianhao Ruan, Zhihao Xu, Yiran Peng, Fashen Ren, Zhaoyang Yu, Xinbing Liang, Jinyu Xiang, Yongru Chen, Bang Liu, Chenglin Wu, Yuyu Luo, Jiayi Zhang  
**Submission Date:** February 3, 2026  
**Venue:** ArXiv  

---

## Executive Summary

AOrchestra introduces a unified framework for dynamic multi-agent orchestration that automatically creates specialized sub-agents on demand for complex, long-horizon tasks. By modeling agents as composable 4-tuples (Instruction, Context, Tools, Model), the system achieves 22.13% average improvement over baseline approaches on competitive code generation and task automation benchmarks. This work addresses a critical bottleneck in agentic systems: the need for adaptive agent creation and coordination without manual redesign for each task.

---

## Problem Statement

Existing multi-agent LLM systems face fundamental limitations when handling increasingly complex, long-horizon tasks:

1. **Static Agent Design:** Pre-designed agents lack flexibility to adapt their capabilities and specialization for diverse task requirements
2. **Manual Orchestration Burden:** Building effective multi-agent teams requires extensive manual engineering of agent roles, communication patterns, and task decomposition
3. **Capability Mismatch:** A single fixed agent design cannot efficiently handle tasks requiring vastly different tool sets, instruction paradigms, and reasoning approaches
4. **Scalability Issues:** As tasks grow in complexity and diversity, maintaining separate agent implementations becomes costly and error-prone
5. **Framework Fragmentation:** Multi-agent solutions are often tightly coupled to specific frameworks, limiting portability and reusability

Prior work like OpenHands and similar systems rely on static agent architectures that must be manually reconfigured for different task classes, reducing their effectiveness on diverse benchmarks.

---

## Core Concepts & Theory

### Unified Agent Abstraction

At the heart of AOrchestra is a simple yet powerful agent abstraction that models any agent as a 4-tuple:

```
Agent = (Instruction, Context, Tools, Model)
```

Where:
- **Instruction:** Natural language specification of the agent's role, responsibilities, and behavioral constraints
- **Context:** Task-specific state, conversation history, and relevant domain knowledge
- **Tools:** Set of callable operations (APIs, shell commands, code execution) available to the agent
- **Model:** The underlying LLM backbone (e.g., Claude, GPT, Gemini) providing reasoning capabilities

This abstraction serves as a **compositional recipe** for capabilities. Rather than pre-engineering a monolithic multi-agent system, AOrchestra treats agents as interchangeable components that can be instantiated on demand.

### Central Orchestrator Architecture

The system uses a centralized orchestrator that:

```
┌─────────────────────────────────────────────────────┐
│         Central Orchestrator (Planning Layer)       │
│                                                     │
│  - Task analysis and decomposition                  │
│  - Sub-agent requirement specification              │
│  - Context curation and routing                     │
│  - Tool & model selection per task                  │
└────────────────┬────────────────────────────────────┘
                 │
        ┌────────┴────────┬─────────────┬─────────────┐
        │                 │             │             │
    ┌───▼──┐      ┌──────▼──┐  ┌──────▼───┐  ┌──────▼────┐
    │ Sub- │      │  Sub-   │  │   Sub-   │  │  Sub-     │
    │Agent │      │  Agent  │  │   Agent  │  │  Agent    │
    │  A   │      │    B    │  │    C     │  │   D       │
    └──────┘      └─────────┘  └──────────┘  └───────────┘
    (Execute)    (Planning)     (Tools)      (Reasoning)
```

**Key Workflow:**
1. Orchestrator analyzes user task and decomposes into subtasks
2. For each subtask, determines required capabilities
3. Dynamically specifies the (Instruction, Context, Tools, Model) tuple
4. Spawns a specialized executor agent with those exact capabilities
5. Orchestrator curates responses and coordinates multi-turn interaction
6. Adapts agent specifications based on intermediate results

### Framework-Agnostic Design

AOrchestra operates independently of underlying agent implementation frameworks. The 4-tuple abstraction allows:
- Seamless integration with OpenHands, AutoGPT, LangChain, or custom implementations
- Switching between LLM backends without architectural changes
- Reuse of agents across different orchestration systems
- Gradual adoption in existing systems

---

## Main Ideas & Contributions

### 1. Unified Agent Composition Model

The 4-tuple abstraction enables treating agent creation as a **program synthesis task**:
- Orchestrator learns optimal (Instruction, Context, Tools, Model) specifications for different task categories
- Agents become stateless, disposable components that are spawned per subtask
- Composition enables mixing specialized executors for maximum efficiency

### 2. On-Demand Sub-Agent Creation

Rather than maintaining a fixed team of agents:
- **Before:** Static multi-agent team with predefined roles
- **After:** Dynamic creation of exactly-fitted agents for each task requirement

Benefits:
- Reduced computational overhead by creating only needed agents
- Specialized context injection per agent (no irrelevant information pollution)
- Precise tool allocation (each agent gets only necessary tools)
- Optimal model selection per task (lightweight models for simple tasks, reasoning models for complex ones)

### 3. Continuous Context Curation

The orchestrator maintains a **task-relevant context window**:
- Filters conversation history to retain only relevant information
- Removes redundant or outdated context
- Injects domain-specific knowledge on demand
- Prevents context bloat across multi-turn interactions

This is critical for:
- Keeping context windows manageable
- Improving reasoning quality by reducing noise
- Accelerating inference (smaller contexts = faster processing)

### 4. Intelligent Tool & Model Selection

Orchestrator makes principled decisions:

**Tool Selection:**
- Analyze task requirements and dependencies
- Select minimal tool set needed for success
- Avoid over-provisioning tools (reduces cognitive load)
- Enable tool chaining across agent handoffs

**Model Selection:**
- Route lightweight tasks to faster, cheaper models
- Allocate reasoning models to complex subtasks
- Consider latency vs. quality tradeoffs
- Optimize cost across heterogeneous model portfolio

### 5. Sub-Agent-as-Tools Paradigm

Specialized sub-agents become tools for higher-level orchestration:
```
Level 1: Orchestrator invokes Level 2 agents
Level 2: Specialized agents (Code Planner, Executor, Reviewer)
Level 3: Agents invoke primitive tools (shell, file ops, API calls)
```

This hierarchical abstraction enables:
- Recursive task decomposition
- Clear separation of concerns
- Reusable agent implementations
- Adaptive depth (deep hierarchies for complex tasks, shallow for simple)

---

## Methodology & Implementation

### Datasets & Benchmarks Tested

Three challenging benchmarks representing different task categories:

1. **GAIA (General AI Assistant Benchmark)**
   - Complex reasoning across diverse domains
   - Requires tool use, web search, data analysis
   - Representative of real-world assistant tasks

2. **SWE-Bench-Verified (Software Engineering)**
   - Autonomous code modification in real repositories
   - Complex file navigation and code understanding
   - Requires planning, tool use, and execution

3. **Terminal-Bench 2.0 (Terminal Interaction)**
   - Long-horizon terminal task completion
   - File system manipulation, process management
   - Tests harness robustness and safety

### Experimental Setup

**Baseline Comparisons:**
- OpenHands (OpenDev): Flexible multi-agent framework
- Single-agent systems with task-specific prompting
- Fixed multi-agent topologies

**Model Backbones Tested:**
- Gemini-3-Flash (fast, efficient model)
- Claude-4.5-Haiku (efficient reasoning)
- GPT-4-like systems

**Evaluation Metrics:**
- **Pass@1:** Strict success on first attempt
- **Pass@3:** Success within 3 tries (measures robustness)
- Inference cost (tokens consumed)
- Execution time per task

### Results and Statistical Analysis

**Primary Results (with Gemini-3-Flash backbone):**

| Benchmark | AOrchestra | Baseline | Improvement |
|-----------|-----------|----------|-------------|
| GAIA | 80.00 | 66.06 | +13.94 pts |
| SWE-Bench | [accurate figures unavailable] | [baseline] | [Exact figures unavailable — see full paper] |
| Terminal-Bench | [accurate figures unavailable] | [baseline] | [Exact figures unavailable — see full paper] |

**Key Findings:**
- **22.13% average improvement** in pass@1 across all three benchmarks
- **16.28% relative improvement** compared to strongest OpenHands baseline
- GAIA: 80.00 pass@1, 86.06 pass@3 (demonstrates robustness via retries)
- With Claude-4.5-Haiku: 60.61 pass@1 on GAIA (maintains strong performance on smaller model)

**Ablation Study Results:**
[Exact ablation metrics unavailable — see full paper]

The consistent improvements across diverse benchmarks suggest AOrchestra's approach generalizes well, not just excelling at specific task types.

### Agent Topologies and Workflows

**AOrchestra Orchestration Flow:**

```
User Task Input
      │
      ▼
┌──────────────────────────────┐
│  Task Analysis & Decompose   │
│  - Parse requirements        │
│  - Identify subtasks         │
│  - Determine dependencies    │
└──────────┬───────────────────┘
           │
      ┌────┴──────┬──────────┬──────────┐
      │           │          │          │
      ▼           ▼          ▼          ▼
   [Subtask 1] [Subtask 2] [Subtask 3] [Subtask 4]
      │           │          │          │
   Instr,      Instr,     Instr,     Instr,
   Ctx,        Ctx,       Ctx,       Ctx,
   Tools,      Tools,     Tools,     Tools,
   Model A     Model B    Model C    Model B
      │           │          │          │
      ▼           ▼          ▼          ▼
  SubAgent    SubAgent   SubAgent   SubAgent
    Exec        Plan       Review      Code
      │           │          │          │
      └─────────┬─────────┬──────────┬─┘
                │         │          │
                ▼         ▼          ▼
          Response Synthesis & Coordination
                │
                ▼
           Orchestrator Decision
           (Integrate, Route, or Retry)
                │
                ▼
           User Response
```

**Typical Multi-Turn Flow:**
1. **Turn 1 - Planning:** Orchestrator spawns planning agent to decompose task
2. **Turn 2 - Execution:** Spawns execution agents for each identified subtask in parallel
3. **Turn 3 - Review:** Spawns review agents to assess intermediate outputs
4. **Turn 4+:** Adaptive spawning based on results and user feedback

---

## Practical Applications & Use Cases

### 1. Complex Software Engineering Tasks

**Use Case:** Autonomous code modification in unfamiliar codebases
- **Planning Agent:** Analyzes repo structure and requirements
- **Exploration Agent:** Navigates files and understands existing code
- **Implementation Agent:** Writes and tests modifications
- **Review Agent:** Validates against requirements

**Benefit:** Each agent specializes in its subtask; orchestrator adapts based on codebase complexity and change scope.

### 2. Research Automation

**Use Case:** Literature review and synthesis across papers
- **Search Agent:** Finds relevant papers (needs web tools)
- **Reading Agent:** Extracts key findings (needs context windows)
- **Synthesis Agent:** Creates summaries and comparisons (needs reasoning model)
- **Citation Agent:** Formats references (needs formatting tools)

**Benefit:** Task-specific tool and model allocation; lightweight search agent doesn't waste reasoning model capacity.

### 3. Data Analysis Pipelines

**Use Case:** End-to-end data processing and visualization
- **Cleaning Agent:** Data quality checks and transformation
- **Analysis Agent:** Statistical analysis and insights
- **Visualization Agent:** Creates charts and dashboards
- **Reporting Agent:** Generates insights and recommendations

### 4. Customer Support Automation

**Use Case:** Handling diverse support tickets
- **Triage Agent:** Categorizes issues (lightweight model sufficient)
- **Investigation Agent:** Gathers context and error logs
- **Resolution Agent:** Provides solutions or escalates
- **Follow-up Agent:** Tracks resolution quality

### 5. Integration Challenges & Scalability

**Challenge 1: Context Coordination**
- Multiple agents need coherent shared state
- Solution: Orchestrator maintains authoritative task context
- Limitation: Communication overhead for highly parallel agents

**Challenge 2: Error Propagation**
- Failure in one subtask can cascade to dependent subtasks
- Solution: Intermediate validation and retry mechanisms
- Example: If code generation fails, restart with adjusted instructions

**Challenge 3: Cost Management**
- Dynamic agent creation can lead to runaway costs
- Solution: Model routing and token budgets per agent
- Monitor: Cost accounting per agent type and task

**Challenge 4: Latency vs. Parallelism**
- Sequential subtasks add latency; parallel spawning increases contention
- Solution: Intelligent task dependency analysis
- Tradeoff: Accept some latency for reliability on serial-dependent tasks

### Cost and Latency Implications

**Cost Model:**
- Sequential orchestration: Lower concurrency, higher latency, lower peak cost
- Parallel orchestration: Higher concurrency, lower latency, higher total cost
- Hybrid: Mix sequential and parallel based on task dependencies

**Latency Analysis:**
- Dynamic agent creation overhead: ~100-500ms per agent (API call)
- Context injection: Proportional to context size
- Benefit: Smaller contexts = faster inference per agent

**Optimization Strategy:**
- Batch create agents when possible
- Pre-warm common agent types (planning, execution)
- Cache frequently used context templates

---

## Insights & Implications

### 1. Paradigm Shift: From Static to Dynamic Multi-Agent Systems

Traditional approach: Design fixed team of agents, tune communication patterns
AOrchestra approach: Dynamically compose agents based on task structure

**Implication:** Multi-agent systems become more adaptive and less fragile to task distribution shifts.

### 2. Separation of Concerns

Orchestration logic (what subtasks are needed) is decoupled from execution logic (how each agent solves its subtask).

**Benefit:** 
- Easier to improve orchestration without touching agent implementations
- Easier to upgrade individual agent implementations
- Clearer debugging and monitoring

### 3. Scaling to More Complex Tasks

By treating agents as composable components, AOrchestra enables:
- Recursive orchestration (agents that spawn sub-agents)
- Hierarchical task decomposition
- Graceful scaling to very long-horizon tasks

### 4. Model Heterogeneity Becomes a Feature

Rather than forcing all tasks through the same model, AOrchestra can route:
- Simple classification → Haiku/Sonnet
- Complex reasoning → Opus
- Specialized domains → Domain-specific fine-tuned models

This is both cost-efficient and capability-enhancing.

### 5. Advancement in Autonomous Systems

Current state-of-the-art on competitive benchmarks (GAIA, SWE-Bench) shows AOrchestra achieves strong performance through intelligent decomposition and specialization, not just larger models.

### 6. Limitations and Open Questions

**Known Limitations:**
- Orchestration overhead for simple tasks (may not justify sub-agent creation)
- Difficulty in learning optimal agent specifications (currently manual or heuristic)
- Potential for cascading failures if intermediate subtasks fail unexpectedly
- Context explosion in deeply recursive orchestration

**Open Research Questions:**
1. Can we learn optimal agent specifications from task distributions?
2. How to automatically detect and recover from single-agent failures?
3. What is the theoretical limit to hierarchical orchestration depth?
4. How do different orchestration topologies compare across task categories?

### 7. Relevance to Agent Topologies and Skill Frameworks

AOrchestra demonstrates:
- **Topology as Dynamic:** Optimal agent team varies by task; orchestrator learns this
- **Skills as Composable:** Tools and instructions can be mixed and matched
- **Models as Selective:** Not all agents need the same underlying LLM

This opens doors for skill frameworks that adaptively route based on task requirements.

---

## Code & Resources

### Official Implementation

**GitHub Repository:** [Not publicly disclosed in paper]
- Reference implementation mentioned but not released
- Authors: Jianhao Ruan et al.
- Status: Research code (as of submission date)

### Framework Dependencies

The implementation is framework-agnostic, but paper demonstrates compatibility with:

1. **OpenHands/OpenDev**
   - Repository: https://github.com/All-Hands-AI/OpenHands
   - Used as baseline for comparison
   - Provides base agent execution harness

2. **LangChain/LangGraph**
   - Repository: https://github.com/langchain-ai/langgraph
   - Orchestration layer can be implemented using LangGraph's StateGraph
   - Agent abstraction maps cleanly to LangChain's LLMAgent

3. **AutoGen**
   - Repository: https://github.com/microsoft/autogen
   - Demonstrates agent conversation patterns compatible with AOrchestra
   - Tool registry and message passing align with 4-tuple model

### Quick-Start Integration Guide

**Implementing AOrchestra 4-Tuple Model:**

```python
# 1. Define Agent Abstraction
class Agent:
    def __init__(self, instruction, context, tools, model):
        self.instruction = instruction  # Role and behavior spec
        self.context = context           # Task-specific state
        self.tools = tools               # Available callable operations
        self.model = model               # LLM backbone

# 2. Create Central Orchestrator
class Orchestrator:
    def decompose_task(self, user_task):
        """Analyze task and return list of subtasks"""
        # Use LLM to identify (Instruction, Context, Tools, Model) for each
        return subtasks
    
    def spawn_agent(self, instruction, context, tools, model):
        """Create and execute specialized agent"""
        agent = Agent(instruction, context, tools, model)
        return agent.execute()
    
    def orchestrate(self, user_task):
        """Main orchestration loop"""
        subtasks = self.decompose_task(user_task)
        results = []
        for subtask in subtasks:
            result = self.spawn_agent(
                instruction=subtask['instruction'],
                context=subtask['context'],
                tools=subtask['tools'],
                model=subtask['model']
            )
            results.append(result)
        return self.synthesize(results)

# 3. Integrate with Framework
# Can wrap OpenHands Agent, LangChain Agent, or custom implementation
```

### Dependencies and API Requirements

**Recommended Stack:**
- LLM API: Claude API, OpenAI API, or Gemini API (for model backbone)
- Orchestration: LangGraph or custom ReAct loop implementation
- Tools: File system, shell execution, web search APIs
- Monitoring: Token counters, cost trackers, latency profilers

**Compute Requirements:**
- Memory: 8GB+ for context windows + model inference
- Concurrency: Orchestrator can spawn 10-50 agents in parallel
- Latency: ~1-5 seconds per orchestrator cycle (depends on LLM latency)

---

## Related Work & Context

### Foundational Work on Multi-Agent Systems

1. **AutoGen (Microsoft Research)**
   - Two-agent conversational framework with tool use
   - Demonstrated effectiveness on code generation
   - AOrchestra extends with dynamic creation and specialization

2. **MACOG**
   - Multi-Agent Code-Orchestrated Generation
   - Uses code-driven coordination (similar spirit to AOrchestra's abstraction)
   - Earlier work on orchestration patterns

3. **AgentForge**
   - Execution-grounded framework for autonomous software engineering
   - Demonstrated agent effectiveness on SE tasks
   - AOrchestra's orthogonal approach (topology rather than execution harness)

### Related Approaches to Agent Composition

1. **Routing Models (MoE-inspired)**
   - Mixture-of-Experts dynamically select expert models
   - AOrchestra applies similar ideas to agent selection

2. **Hierarchical Agent Systems (prior work)**
   - Manager agents coordinating worker agents
   - AOrchestra differs: no persistent hierarchy, dynamic spawning

3. **Prompt Composition Techniques**
   - Few-shot learning with specialized prompts
   - AOrchestra formalizes this via 4-tuple abstraction

### Possible Extensions and Future Research

1. **Learning Orchestration Policies**
   - Use RL or supervised learning to optimize agent specifications
   - Learn which (Instruction, Context, Tools, Model) combinations work best
   - Adaptation to new task distributions

2. **Recursive Orchestration**
   - Agents that spawn their own sub-agents
   - Hierarchical task decomposition unlimited by manual design
   - Challenges: Termination conditions, deep context propagation

3. **Agent Communication Protocols**
   - Currently: Orchestrator collects responses and coordinates
   - Future: Direct agent-to-agent communication with protocols
   - May reduce latency and improve solution quality

4. **Adversarial Verification**
   - Specialized reviewer agents that challenge proposed solutions
   - Detect and fix errors before user-facing output
   - Combines with DOVA's deliberation-first approach

5. **Federated Orchestration**
   - Multiple orchestrators coordinating across domains
   - Useful for enterprise systems with specialized services
   - Challenge: Distributed state management and consensus

### Comparative Analysis with Existing Frameworks

| Aspect | AOrchestra | OpenHands | AutoGen | MACOG |
|--------|-----------|-----------|---------|-------|
| **Agent Creation** | Dynamic | Static | Static | Static |
| **Tool Selection** | Per-agent | Fixed | Fixed | Fixed |
| **Model Routing** | Per-subtask | Single | Single | Single |
| **Communication** | Centralized | Hierarchical | Conversational | Code-based |
| **Scalability** | Moderate | Good | Good | Good |
| **Ease of Use** | Medium | High | High | Medium |

---

## References

**Citation:**
```bibtex
@article{aorchestra2026,
  title={AOrchestra: Automating Sub-Agent Creation for Agentic Orchestration},
  author={Ruan, Jianhao and Xu, Zhihao and Peng, Yiran and others},
  journal={arXiv preprint arXiv:2602.03786},
  year={2026}
}
```

**Paper Link:** https://arxiv.org/abs/2602.03786
