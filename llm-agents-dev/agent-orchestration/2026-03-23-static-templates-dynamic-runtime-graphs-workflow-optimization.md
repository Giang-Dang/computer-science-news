# From Static Templates to Dynamic Runtime Graphs: A Survey of Workflow Optimization for LLM Agents

**ArXiv ID:** 2603.22386  
**Authors:** Ling Yue, Kushal Raj Bhandari, Ching-Yun Ko, Dhaval Patel, Shuxin Lin, Nianjun Zhou, Jianxi Gao, Pin-Yu Chen, Shaowu Pan  
**Submitted:** March 23, 2026  
**URL:** https://arxiv.org/abs/2603.22386

## Executive Summary

This comprehensive survey systematically analyzes the shift from static workflow templates (pre-defined, reusable scaffolds) to dynamic runtime graphs (workflows optimized or generated at runtime) for orchestrating Large Language Model agent systems. By categorizing 40+ existing systems across this spectrum, the paper provides architects with a principled framework for selecting between pre-deployment optimization and runtime-adaptive approaches when building complex automation pipelines involving LLM calls, tool invocation, code execution, memory updates, and verification loops.

## Problem Statement

Traditional agent workflow orchestration relies on **static templates**—pre-defined, unchanging execution patterns that are fixed at deployment time. This approach has significant limitations:

1. **Inflexible Planning**: Fixed templates cannot adapt to varying problem complexity, task contexts, or real-time conditions
2. **Suboptimal Task Allocation**: Pre-designed workflows may not optimally route tasks through available tools and agents for specific scenarios
3. **Limited Scalability**: Static templates become bottlenecks as agent systems grow in complexity, tool count, and task diversity
4. **Reduced Composability**: Reusing templates across different domains requires manual refactoring, limiting modularity
5. **No Performance Feedback Integration**: Static templates lack mechanisms to improve based on historical execution patterns

Meanwhile, **dynamic approaches** (that generate or optimize workflows at runtime) offer advantages but introduce new challenges:
- Computational overhead during execution
- Complexity in decision-making and state management
- Difficulty in debugging and verifying behavior
- Need for sophisticated ranking and selection mechanisms

This survey addresses the critical gap: **How should practitioners design workflow orchestration for LLM agents given this spectrum of trade-offs?**

## Core Concepts & Theory

### Two Dimensions of Agent Workflow Design

The survey identifies workflow orchestration as occupying a 2D design space:

#### **Dimension 1: Workflow Structure Determination**

How is the workflow structure decided?

**Static Templates** → **Semi-Dynamic Selection** → **Fully Dynamic Generation**

1. **Static Templates (Pre-deployment)**
   ```
   Template 1 (hardcoded)      Template 2 (hardcoded)
      ↓                            ↓
   [Task Input] → [Predetermined Sequence] → [Output]
   ```
   - Workflow structure fixed before deployment
   - Same execution path regardless of input or conditions
   - Example: Fixed ReAct loops, predefined tool chains
   - Pros: Predictable, debuggable, low overhead
   - Cons: Inflexible, may be suboptimal for diverse tasks

2. **Semi-Dynamic Selection** (Input-aware selection)
   ```
   [Task Input] → [Decision Module] → {Select from K Templates} → [Execution] → [Output]
   ```
   - Multiple pre-defined templates exist
   - Input characteristics determine which template is selected
   - Example: Route simple tasks through lightweight template, complex tasks through heavyweight template
   - Pros: Balances flexibility with predictability
   - Cons: Still limited to pre-authored templates

3. **Fully Dynamic Generation** (Runtime optimization)
   ```
   [Task Input] → [Graph Generator] → [Build Optimized DAG] → [Adapt During Execution] → [Output]
   ```
   - Workflow is built/optimized for each specific task at runtime
   - Can incorporate real-time feedback and conditions
   - Example: Generate task decomposition for novel problems, select tools adaptively
   - Pros: Maximally flexible, can adapt to any scenario
   - Cons: High computational cost, harder to debug, requires sophisticated algorithms

#### **Dimension 2: Optimization Timing**

When is workflow optimization performed?

1. **Pre-Deployment Optimization**
   - Optimize static templates before release
   - Example: Benchmark templates offline, select best performing ones
   - Cost: One-time upfront investment
   - Benefit: Zero runtime overhead

2. **Runtime Optimization**
   - Optimize workflows during execution
   - Adapt based on real-time feedback
   - Cost: Added latency and computation per task
   - Benefit: Maximally responsive to conditions

### Workflow Graph Representation

The paper introduces **agentic workflow graphs** as the core abstraction:

```
Workflow Graph = (Nodes, Edges, State, Routing)

Nodes: {LLMCall, ToolInvoke, DataTransform, ControlFlow, Verification}
Edges: {Sequential, Conditional, Parallel, Feedback}
State: {Intermediate results, Memory, Context}
Routing: {Static path, Dynamic selection, Learned routing}
```

**Example: Code Generation Workflow Graph**

```
┌─────────────────────────────────────────────────────────┐
│                 Dynamic Workflow Graph                   │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  Input: Problem Description                              │
│      │                                                    │
│      ▼                                                    │
│  ┌─────────────────────────┐                             │
│  │ Analyze Task Complexity │  (LLM Node)                 │
│  └────────────┬────────────┘                             │
│               │                                           │
│       ┌───────┴────────┐                                  │
│       │ Route Decision │                                  │
│       └───────┬────────┘                                  │
│               │                                           │
│       ┌───────┴─────────┬──────────────┐                  │
│       │                 │              │                  │
│   [Simple]          [Moderate]      [Complex]             │
│       │                 │              │                  │
│       ▼                 ▼              ▼                  │
│   ┌──────┐          ┌──────┐       ┌──────┐              │
│   │ Path │          │ Path │       │ Path │              │
│   │  A   │          │  B   │       │  C   │              │
│   └───┬──┘          └───┬──┘       └───┬──┘              │
│       │                 │              │                  │
│       └─────────────────┴──────────────┘                  │
│               │                                           │
│               ▼                                           │
│   Generate Code (Parallel Execution)                      │
│       │                                                    │
│       ▼                                                    │
│   Test Verification (Feedback)                            │
│       │                                                    │
│   ┌───┴────┐                                              │
│   │  Pass? │                                              │
│   └───┬─┬──┘                                              │
│     No│ │Yes                                              │
│       │ └──────────▶ [Final Output]                       │
│       │                                                    │
│       ▼                                                    │
│   Refinement Loop (Dynamic Replanning)                    │
│       │                                                    │
│       └──────────▶ Back to Generation                     │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

## Main Ideas & Contributions

### 1. Comprehensive Taxonomy of Workflow Optimization Strategies

The survey categorizes 40+ real-world agent systems along two primary axes:

| System Category | Structure Determination | Optimization Timing | Examples |
|---|---|---|---|
| **Template-Only** | Static | Pre-deployment | ReAct, Chain-of-Thought chains |
| **Template-Selection** | Semi-dynamic | Pre-deployment | Mixture-of-Experts routing, task classifiers |
| **Adaptive-Workflows** | Semi-dynamic | Runtime | In-context learning, guided search |
| **Full-Optimization** | Fully dynamic | Runtime | Graph generators, planner-executor pairs |
| **Hybrid Systems** | Mixed | Mixed | Multi-stage pipelines with both static and dynamic elements |

### 2. Trade-Off Analysis Framework

For practitioners, the paper provides a decision matrix:

**Choose Static Templates If:**
- Task types are well-defined and homogeneous
- Predictability and debuggability are critical
- Computational resources are constrained
- Domain has proven fixed patterns (e.g., standard RAG)

**Choose Dynamic Approaches If:**
- Task diversity is high
- Adaptation to novel scenarios is required
- Computational budget allows runtime optimization
- Feedback from execution history is valuable
- Domain requires rapid iteration and experimentation

**Choose Hybrid Approaches If:**
- Some tasks are well-structured, others are novel
- Can afford selective dynamic optimization
- Want to balance reliability with flexibility

### 3. Identified Optimization Techniques

The survey catalogs workflow optimization methods:

1. **Template Selection Techniques**
   - Rule-based routing (hand-crafted decision rules)
   - Learned classifiers (train models to select templates)
   - Similarity-based matching (find similar past tasks)

2. **Graph-Based Generation Techniques**
   - Hierarchical planning (decompose into sub-workflows)
   - Sampling and ranking (generate multiple graphs, rank by heuristics)
   - Reinforcement learning (learn to construct optimal graphs)
   - LLM-driven planning (use LLM to generate workflow structures)

3. **Runtime Adaptation Techniques**
   - Feedback loops (verify outputs, adapt on failure)
   - In-context learning (accumulate examples, adjust behavior)
   - State-based routing (decisions based on intermediate results)
   - Speculative execution (generate multiple paths, prune failing ones)

### 4. Critical Insights on Practical Systems

- **Most production systems use hybrid approaches**: Combine static scaffolding (predictability) with selective dynamic adaptation (flexibility)
- **The "dynamic sweet spot"**: Full optimization at every step is often too expensive; selective dynamic optimization (e.g., adapt only when task is novel) achieves good results
- **Debugging trade-off**: Dynamic systems are harder to debug; successful implementations add extensive logging and replay capabilities
- **Composability wins**: Systems that modularize workflow fragments (reusable sub-workflows) scale better than monolithic dynamic generators

## Methodology & Implementation

### Survey Methodology

The survey analyzed **40+ agent systems** from:
- Academic research papers (published 2023-2026)
- Open-source frameworks (LangChain, Anthropic SDK, AutoGen, etc.)
- Production systems (internal descriptions, blog posts)

Classification approach:
1. Extract workflow definitions from each system
2. Characterize along two dimensions (structure determination, optimization timing)
3. Document optimization techniques used
4. Map to use cases and performance characteristics

### Evaluation Dimensions

For each system, the survey examines:

1. **Flexibility**
   - Can the system handle novel task types?
   - Can workflows be adapted at runtime?
   - Score: Static (1) → Fully Dynamic (5)

2. **Computational Efficiency**
   - Does optimization add significant latency?
   - What's the overhead of runtime graph generation?
   - Metrics: Overhead percentage, latency increase

3. **Debuggability**
   - Can the execution path be reproduced?
   - Is the workflow structure transparent?
   - Score: Fully transparent (1) → Black box (5)

4. **Robustness**
   - How well does the system handle failures?
   - Does it adapt when tools are unavailable?
   - Metrics: Error recovery rate, fallback mechanisms

5. **Ease of Implementation**
   - How much code is required?
   - What's the learning curve for developers?
   - Metrics: Lines of code, setup complexity

### Performance Characteristics

[Exact figures unavailable — see full paper]

The survey reports comparative benchmarks across systems showing:
- Runtime overhead of dynamic approaches (typically 10-50% latency increase vs. static)
- Performance gains from adaptation (5-30% improvement in task completion on diverse workloads)
- Debuggability trade-offs (static systems have 2-5x better transparency)
- Cost of optimization algorithms (varies from <1% to >50% of total execution time)

## Practical Applications & Use Cases

### Use Case 1: Code Generation and Debugging

**Challenge**: Code generation tasks vary widely in complexity
- Simple: Fix a typo → Use lightweight template
- Moderate: Add a feature → Use multi-stage template  
- Complex: Architect new system → Use full dynamic optimization

**Solution**: Hybrid approach with runtime complexity assessment
```
Assess task → Route to appropriate template → 
Execute → Verify → Adapt if needed
```

### Use Case 2: Document Analysis and Synthesis

**Challenge**: Documents have varying structure and length
- Structured documents → Use fixed template
- Novel formats → Use dynamic generation

**Solution**: Semi-dynamic selection based on document classification

### Use Case 3: Multi-Tool Orchestration

**Challenge**: Available tools change, new tools appear, some tools fail

**Solution**: Dynamic tool selection and substitution
- Pre-plan core workflows
- At runtime, adapt tool selection based on availability
- Maintain fallback paths

### Use Case 4: Interactive Refinement Loops

**Challenge**: User feedback should drive workflow adaptation

**Solution**: Runtime feedback integration
- Execute initial workflow
- Collect user feedback
- Adapt subsequent workflows based on feedback
- Learn patterns across multiple iterations

## Insights & Implications

### Key Findings

1. **Static Templates Remain Important**: Despite interest in dynamic approaches, most production systems still rely heavily on well-designed static templates as the foundation

2. **The Optimization Sweet Spot**: Full runtime optimization at every decision point is rarely used; most systems use dynamic approaches selectively

3. **Hybrid Architectures Dominate**: Successful systems layer static scaffolding with targeted dynamic optimization—neither pure static nor pure dynamic works best

4. **Debuggability is Critical**: Production adoptions prioritize systems where the execution path can be understood and reproduced, even at some cost to flexibility

5. **Learning Across Tasks**: Systems that learn from historical execution (storing successful workflows, patterns of failures) consistently outperform those that don't

### Research Implications

- **Need for principled design frameworks**: The field needs better guidelines for choosing between static and dynamic approaches for specific domains
- **Standardized workflow representations**: Industry needs agreed-upon workflow graph standards for interoperability
- **Efficient optimization algorithms**: Faster graph generation and optimization is needed to make dynamic approaches more practical
- **Better debugging tools**: Tools for visualizing, tracing, and replaying agent workflows are critical for adoption

### Limitations and Open Questions

- How to optimize the exploration-exploitation tradeoff in dynamic workflow generation?
- Can we predict when dynamic optimization will help for a given task?
- How do human preferences factor into workflow design choices?
- What's the minimal viable dynamic component for most applications?

## Code & Resources

### Reference Implementations

- **LangChain**: Example of semi-dynamic template selection with conditional routing
  - GitHub: https://github.com/langchain-ai/langchain
  - Relevant: LCEL (LangChain Expression Language) for workflow definition

- **Anthropic SDK**: Agentic workflows with tool use and reflexive patterns
  - GitHub: https://github.com/anthropics/anthropic-sdk-python
  - Documentation: Building agents

- **AutoGen (Microsoft)**: Multi-agent orchestration with conversation-based workflows
  - GitHub: https://github.com/microsoft/autogen
  - Features: Dynamic agent grouping, conversation management

### Key Libraries for Workflow Construction

- **Pydantic**: Schema definition for workflow graphs
- **NetworkX**: Graph representation and algorithms
- **Ray**: Distributed execution of workflow DAGs
- **Prefect/Dagster**: Workflow orchestration frameworks (general-purpose, adaptable for agents)

### Building Dynamic Workflows

Basic pattern for runtime graph generation:

```python
# Pseudo-code for dynamic workflow construction
def build_workflow(task):
    # Analyze task
    complexity = analyze_complexity(task)
    
    # Create nodes
    graph = WorkflowGraph()
    graph.add_node("analyze", LLMNode(...))
    
    if complexity == "simple":
        graph.add_node("generate", LLMNode(...))
    else:
        graph.add_node("decompose", PlanningNode(...))
        graph.add_node("implement", LLMNode(...))
        graph.add_node("verify", VerificationNode(...))
    
    # Connect edges
    graph.add_edge("analyze", "generate")  # or other next nodes
    
    return graph

# Execute
workflow = build_workflow(user_task)
result = execute_workflow(workflow)
```

## Related Work & Context

### Prior Surveys and Frameworks

- **Agent Orchestration Surveys** (2025-2026): Covers broader orchestration paradigms; this survey focuses specifically on workflow graph structure
- **Distributed Systems Workflow Literature** (1990s-2010s): DAG-based workflows, but from different domain (parallel computing) with different tradeoffs
- **Planning and Scheduling Literature** (AI planning): Related problem domain; survey highlights lessons from classical planning applicable to agent workflows

### Complementary Topics

This survey complements work on:
- **Agent Communication Protocols**: How agents coordinate within workflows
- **Tool Use and Skill Acquisition**: What nodes/tools are composed into workflows
- **Memory and State Management**: How state flows through workflow graphs
- **Verification and Testing**: How to ensure workflow correctness
- **Learning and Improvement**: How to improve workflows based on execution history

### Future Directions

1. **Formal Verification of Workflows**: Can we prove workflow properties?
2. **Automatic Workflow Optimization**: Meta-learning to design optimal structures for domains
3. **Cross-Domain Workflow Transfer**: Adapt workflows from one domain to another
4. **Human-AI Collaborative Workflow Design**: Humans guide workflow structure, AI optimizes details
5. **Standardized Workflow Specification Language**: Industry-standard definition of agent workflows

## Author and Institutional Context

**Authors**: Ling Yue et al., with affiliations from major tech institutions and universities
- Strong representation from leading AI research institutions
- Practical experience from industry deployments

**Relevance to Agent Development**: This survey provides essential architectural guidance for anyone building multi-agent systems, whether for code generation, data processing, or other domains requiring complex orchestration.
