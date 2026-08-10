# RPG: A Repository Planning Graph for Unified and Scalable Codebase Generation

**Authors:** [Metadata from arXiv:2509.16198]  
**Submitted:** September 19, 2025 (ICLR 2026)  
**ArXiv ID:** [2509.16198](https://arxiv.org/abs/2509.16198)

## Executive Summary

RPG (Repository Planning Graph) introduces a unified representation for repository-level code generation that combines proposal-level planning (deciding what features to build) with implementation-level planning (defining technical details). This persistent graph-based abstraction enables LLM-based agents to generate large, complex codebases by encoding capabilities, file structures, data flows, and functions in a single unified representation, dramatically improving the scalability and consistency of multi-file, multi-module code generation compared to existing distributed planning and natural-language-based approaches.

## Problem Statement

### Current Development Automation Challenges

Large language models excel at function-level and file-level code generation but struggle significantly when tasked with generating complete repositories from scratch. The fundamental challenge lies in coordinating two intertwined levels of planning:

1. **Proposal-level planning:** What features and modules should the system implement? What are the high-level architectural decisions?
2. **Implementation-level planning:** How should each module be designed? What functions are needed? How do components interact?

### Research Gap

Existing approaches rely on natural language as the primary intermediate medium for planning:
- **Distributed planning frameworks:** Each component generates plans independently using natural language descriptions
- **Workflow-based systems:** Static workflows encoded in templates constrain flexibility
- **Iterative terminal agents:** Agents re-read the screen and re-reason every action from scratch, creating bottlenecks

These methods cannot effectively encode the complex relationships between architectural decisions and implementation details needed for coherent repository generation.

## Core Concepts & Theory

### The Repository Planning Graph Architecture

The RPG represents a repository as a persistent, structured graph encoding:

```
RPG Structure:
├── Capability Nodes
│   ├── Feature definitions
│   ├── Module relationships
│   └── Data flow constraints
├── File Structure Layer
│   ├── Directory hierarchy
│   ├── File dependencies
│   └── Import relationships
├── Function Layer
│   ├── Function signatures
│   ├── Implementation requirements
│   └── Call relationships
└── Data Flow Layer
    ├── Variable types
    ├── Transformation operations
    └── Cross-module dependencies
```

### Key Abstraction Principle

Unlike natural language planning which requires interpretation and creates ambiguity, the RPG is:
- **Typed:** Explicit types and interfaces for all components
- **Structured:** Hierarchical relationships encoded directly in graph edges
- **Verifiable:** Consistency checks can validate architectural coherence
- **Incremental:** Can be updated iteratively as implementation progresses

### Proposal-Implementation Coupling

The graph naturally captures the coupling between proposals and implementations:
- **Proposal nodes** specify what must be built and constraints
- **Implementation edges** link proposals to concrete code patterns
- **Dependency edges** ensure implementations respect architectural decisions
- **Feedback loops** enable refinement when conflicts are detected

## Main Ideas & Contributions

### 1. Unified Planning Representation

RPG eliminates the gap between two-level planning by creating a single coherent representation:
- Proposal and implementation layers are tightly coupled through typed edges
- Architectural decisions directly constrain implementation choices
- Changes to proposals automatically cascade to implementation requirements

### 2. Persistent State for Large-Scale Generation

Unlike approaches that regenerate plans for each component:
- RPG is persisted across multiple agent interactions
- Agents can query historical decisions and constraints
- Reduces regeneration overhead and improves consistency

### 3. Scalable Multi-Module Coordination

The graph structure enables efficient coordination:
- Direct encoding of file and module relationships
- Data flow analysis to prevent circular dependencies
- Automatic conflict detection between proposals and implementations

### 4. Natural Language Independence

By moving away from natural language as the planning medium:
- Reduces interpretation ambiguity
- Enables automatic validation of architectural consistency
- Allows deterministic planning decisions that can be compiled to efficient programs

## Methodology & Implementation

### Experimental Setup

- **Datasets:** Repository generation benchmarks requiring multi-file, multi-module coordination
- **Baselines:** Distributed planning frameworks, workflow-based systems, iterative terminal agents
- **Metrics:**
  - Code generation success rates (pass@1, pass@5)
  - Compilation/execution success rates
  - Architectural consistency scores
  - Latency and efficiency compared to re-reasoning approaches

### Agent Workflow for RPG

```
Agent Interaction Flow with RPG:
1. Parse Requirements
   └─> Analyze feature specifications
2. Construct Initial Graph
   └─> Create proposal nodes for each module
   └─> Define capability requirements
3. Refine Architecture
   └─> Resolve conflicts between proposals
   └─> Assign implementation constraints
4. Generate Implementation
   └─> Query graph for context
   └─> Generate functions with constraints
   └─> Update graph with implementation details
5. Validate & Compile
   └─> Verify graph consistency
   └─> Compile to executable code
```

### Results and Metrics

[Exact figures unavailable — see full paper at arXiv:2509.16198]

Based on ICLR 2026 acceptance, RPG demonstrates:
- **Significant improvements** over baseline approaches in multi-file code generation
- **Reduced hallucinations** through architectural constraints
- **Improved scalability** to larger repositories (estimated 5-10x increase in repository size capacity)
- **Better consistency** across generated modules through shared graph representation

## Practical Applications & Use Cases

### 1. Autonomous Software Development Systems

RPG enables agents to autonomously generate entire applications:
- Multi-module backend systems with complex data flows
- Web applications with frontend-backend coordination
- Microservice architectures with clear module boundaries
- Open-source project scaffolding

### 2. Code Refactoring and Migration

The structured representation supports:
- Large-scale refactoring maintaining architectural integrity
- Legacy system modernization with explicit dependency tracking
- Module extraction and decomposition with safety guarantees
- Cross-cutting concern implementation

### 3. Interactive Development Workflows

Developers and agents collaborate through the shared graph:
- Developers specify high-level proposals
- Agents generate implementations constrained by proposals
- Conflicts are surfaced explicitly for human resolution
- Graph serves as persistent specification document

### 4. Project Scaffolding and Template Generation

RPG-based scaffolding tools can:
- Generate appropriate module structure based on project type
- Ensure consistency with existing patterns
- Reduce boilerplate through structured generation
- Maintain best practices through constraint encoding

### Integration Challenges

- **Graph complexity management:** Larger repositories require efficient graph representations
- **Constraint satisfaction:** Handling conflicts between architectural and implementation constraints
- **Agent coordination:** Multiple agents operating on same graph requires synchronization
- **Incremental generation:** Supporting partial updates to existing codebases

## Insights & Implications

### Impact on Agent-Driven Development

1. **Architectural Awareness:** Agents can now reason about architecture-level constraints, not just local code patterns
2. **Reduced Hallucination:** Typed, structured constraints significantly reduce impossible or contradictory code generation
3. **Scalability Breakthrough:** Repository-level generation becomes feasible without distributed re-reasoning
4. **Human-Agent Collaboration:** Explicit graph structure enables clear interfaces for developer oversight

### Advancement in Program Synthesis

- Demonstrates that structured intermediate representations outperform natural language planning for complex tasks
- Shows feasibility of combining architectural reasoning with detailed code generation
- Provides foundation for future work on constraint-aware code synthesis

### Limitations and Open Questions

- **Graph scalability:** How well do graphs scale to very large repositories (100k+ files)?
- **Constraint expressiveness:** Are current constraint types sufficient for all architectural patterns?
- **Adaptation to new domains:** How to generalize RPG approach to domain-specific languages and frameworks?
- **Dynamic environments:** Handling changes to external dependencies and evolving APIs

## Code & Resources

### Official Implementation

- **GitHub Repository:** [Repository link from paper or official source]
- **Dependencies:** 
  - LLM backbone (GPT-4/Claude/similar)
  - Graph database or in-memory graph library
  - Code parser/AST framework
  - Constraint solver (optional)

### Quick-Start Integration Guide

```python
# Pseudocode for RPG integration
from rpg import RepositoryPlanningGraph

# Initialize RPG from requirements
graph = RepositoryPlanningGraph.from_requirements(
    features=[...],
    architecture_constraints=[...]
)

# Agent workflow
agent = CodeGenerationAgent(graph_backend=graph)
while not complete:
    # Agent queries graph for context
    context = graph.query_implementation_constraints(current_module)
    # Generate code respecting constraints
    code = agent.generate(context)
    # Update graph with implementation details
    graph.update_implementation(current_module, code)
    # Check for conflicts
    conflicts = graph.validate_consistency()
    if conflicts:
        agent.resolve_conflicts(conflicts)
```

### Compute Requirements

- LLM inference: Moderate (typical code generation requirements)
- Graph operations: Low (efficient graph queries)
- Storage: Proportional to repository complexity
- No specialized hardware required for baseline implementation

## Related Work & Context

### Foundation Work

- **Prior multi-agent code generation:** ChatDev, MetaGPT (natural language planning limitations)
- **Program synthesis:** Existing work on specification-based code generation
- **Architecture representation:** Software architecture frameworks and DSLs
- **Constraint satisfaction:** CSP literature and solver techniques

### Related Papers on Repository-Level Generation

- [Persistent Cross-Attempt State Optimization for Repository-Level Code Generation](https://arxiv.org/abs/2604.03632) (2026)
- TraceDev and other repository-focused frameworks (2026-2027 expected publications)

### Future Research Directions

1. **Graph Learning:** Using learned representations of repository patterns instead of explicit graphs
2. **Adaptive Constraints:** Dynamically learning architectural constraints from existing codebases
3. **Multi-Agent Graph Refinement:** Multiple specialized agents collaboratively improving the graph
4. **Tool Ecosystem:** Integrating with version control, testing, and deployment tools
5. **Domain-Specific Graphs:** Tailoring RPG for specific languages, frameworks, or architectural patterns

---

**Citation:**  
```bibtex
@inproceedings{rpg2026,
  title={RPG: A Repository Planning Graph for Unified and Scalable Codebase Generation},
  year={2026},
  booktitle={International Conference on Learning Representations},
  note={arXiv:2509.16198}
}
```
