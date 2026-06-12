# A Two-Dimensional Framework for AI Agent Design Patterns: Cognitive Function × Execution Topology

**Authors:** Jia Huang, Joey Tianyi Zhou  
**Affiliation:** Agency for Science, Technology and Research (A*STAR), Centre for Frontier AI Research (CFAR), Singapore  
**ArXiv ID:** 2605.13850  
**Submitted:** March 16, 2026 (v2: May 24, 2026)  
**URL:** https://arxiv.org/abs/2605.13850

## Executive Summary

This paper addresses a critical gap in agent architecture design by proposing a two-dimensional classification framework that unifies how we understand LLM-based agents. Rather than viewing agent systems through a single lens—either focusing on execution topology (data flow) or cognitive function (agent behavior)—the authors demonstrate that understanding both dimensions is essential for designing robust, resilient agent systems for software development and complex reasoning tasks. This framework directly impacts how development teams architect multi-agent systems and select appropriate topologies for specific problem domains.

## Problem Statement

Existing frameworks for LLM-based agent architectures suffer from incomplete descriptions:

1. **Industry guides** (Anthropic, Google, LangChain) focus exclusively on execution topology—how data flows through the system, communication patterns, and structural organization
2. **Cognitive science surveys** focus on cognitive function—what agents do (perception, memory, reasoning, action, reflection, collaboration, governance)
3. **The architectural ambiguity problem:** The same Orchestrator-Workers topology can implement fundamentally different patterns:
   - **Plan-and-Execute:** Single planner makes decisions for all workers (different failure modes than hierarchical delegation)
   - **Hierarchical Delegation:** Manager agents dynamically assign tasks to subordinate agents
   - **Adversarial Verification:** Separate agents compete to verify or challenge outputs
   
   These three patterns share identical structural topology but have dramatically different failure modes, resilience properties, and design trade-offs.

This misalignment between topology and function creates implementation challenges for software development teams building autonomous systems—they cannot determine which topology suits their problem domain without understanding the cognitive functions it enables or constrains.

## Core Concepts & Theory

### Two-Dimensional Classification Framework

The paper proposes a comprehensive two-dimensional space for classifying agent architectures:

#### Dimension 1: Cognitive Function (7 Categories)

The cognitive function axis describes *what the agent does* at each step:

```
Cognitive Functions in Agent Systems
─────────────────────────────────────────────

1. PERCEPTION
   └─ Sensing and interpreting information from the environment
      (user input, API responses, file contents, execution output)
   
2. MEMORY
   └─ Storing, retrieving, and updating contextual information
      (short-term working memory, long-term knowledge bases, 
       conversation history, execution traces)
   
3. REASONING
   └─ Decision-making and planning logic
      (Chain-of-Thought, Tree-of-Thought, forward/backward chaining,
       constraint satisfaction, multi-step planning)
   
4. ACTION
   └─ Executing decisions through external systems
      (tool calls, code execution, API invocations, environment manipulation)
   
5. REFLECTION
   └─ Self-evaluation and learning from outcomes
      (error analysis, trajectory replay, self-correction,
       performance metrics, quality checks)
   
6. COLLABORATION
   └─ Coordinating with other agents
      (information sharing, consensus mechanisms, negotiation,
       message passing, role-based division of labor)
   
7. GOVERNANCE
   └─ System-level policies and constraints
      (access control, budget limits, safety constraints,
       monitoring, compliance enforcement)
```

#### Dimension 2: Execution Topology (6 Archetypes)

The execution topology axis describes *how data and control flows* through the system:

```
Agent System Topologies
──────────────────────────────────────────

1. CHAIN
   Agent₁ → Agent₂ → Agent₃ → Output
   
   Characteristics:
   - Linear sequential processing
   - Output of one agent feeds into next
   - Simple to understand and debug
   - Limited parallelism
   - Example: RAG pipeline (retrieval → reasoning → generation)

2. ROUTE (Conditional Branching)
   
            ┌─ Agent₁ ┐
   Input ─→ Router ┤─ Agent₂ ├─→ Output
            └─ Agent₃ ┘
   
   Characteristics:
   - Routing logic determines which agent(s) process input
   - Conditional execution based on input type or state
   - Example: Intent-based routing in task-specific agents

3. PARALLEL
   
            ┌─ Agent₁ ─┐
   Input ─→ ┼─ Agent₂ ├─→ Aggregator → Output
            └─ Agent₃ ─┘
   
   Characteristics:
   - Multiple agents process simultaneously
   - Results aggregated/merged
   - Exploits diversity of agents
   - Example: Consensus-based verification

4. ORCHESTRATE (Orchestrator-Workers)
   
        ┌─────────────────────┐
        │    ORCHESTRATOR     │ (Central coordinator)
        └────────┬────────────┘
          ┌──────┼──────┐
          │      │      │
        Agent₁ Agent₂ Agent₃ (Workers)
   
   Characteristics:
   - Central orchestrator directs task flow
   - Assigns work to specialized agents
   - Monitors and coordinates execution
   - Example: Project manager assigning coding tasks

5. LOOP (Iterative Refinement)
   
        ┌───────────────────┐
        │  Initial Agent    │
        └────────┬──────────┘
                 │
                 ↓
        ┌─────────────────────┐
        │  Refining Agent     │ ←── Feedback Loop
        └────────┬──────────────┘
                 │
         ┌──────────────┐
         │ (Converged?) │
         └──┬──────────┘
            Yes → Output
            No → Loop back
   
   Characteristics:
   - Iterative improvement through feedback
   - Self-correction and refinement
   - Termination criteria required
   - Example: Code generation with debugging loop

6. HIERARCHY (Multi-Level)
   
        ┌──────────────┐
        │   Top-Level  │ (Strategy)
        └────┬─────────┘
             │
        ┌────┴────┐
        │          │
      ┌─┴──┐   ┌──┴─┐
      │Mid │   │Mid │ (Tactics)
      └─┬──┘   └──┬─┘
        │         │
      ┌─┴──┐   ┌──┴─┐
      │Op1 │   │Op2 │ (Operations)
      └────┘   └────┘
   
   Characteristics:
   - Multiple levels of abstraction
   - Delegation cascades down
   - Information aggregates up
   - Example: Multi-level software team structure
```

### Design Pattern Matrix: Cognitive Function × Execution Topology

The same topology can implement different cognitive patterns with different outcomes:

```
CASE STUDY: Orchestrator-Workers Topology Implementation Variants

┌─────────────────────────────────────────────────────────────────┐
│                   ORCHESTRATOR-WORKERS TOPOLOGY                 │
│                      (Identical Structure)                       │
└─────────────────────────────────────────────────────────────────┘

VARIANT 1: PLAN-AND-EXECUTE
─────────────────────────────────────────────────────────────────
REASONING (Orchestrator)
  └─ Creates complete plan for all tasks upfront
COLLABORATION (Workers)
  └─ Execute assigned tasks without feedback to planner
FAILURE MODES
  └─ Plan becomes invalid if environment changes
  └─ Workers cannot adapt to new constraints
  └─ No feedback loop for plan refinement

VARIANT 2: HIERARCHICAL DELEGATION
─────────────────────────────────────────────────────────────────
REASONING (Orchestrator)
  └─ Creates plan incrementally based on worker progress
REFLECTION (Orchestrator)
  └─ Monitors worker execution and adjusts assignments
COLLABORATION (Orchestrator ↔ Workers)
  └─ Bidirectional communication about task status
FAILURE MODES
  └─ Communication overhead with many workers
  └─ Bottleneck at orchestrator (must process all updates)
  └─ Single point of failure if orchestrator crashes

VARIANT 3: ADVERSARIAL VERIFICATION
─────────────────────────────────────────────────────────────────
REASONING (Executor Worker)
  └─ Generates solution/code/plan
REFLECTION (Verifier Worker)
  └─ Challenges solution, identifies flaws
COLLABORATION (Orchestrator mediation)
  └─ Orchestrator adjudicates disputes between agents
GOVERNANCE
  └─ Access control: Verifier cannot modify executor's output
FAILURE MODES
  └─ Verification deadlocks if agents disagree
  └─ Expensive (both agents process same problem)
  └─ Requires careful arbitration logic
```

### Mapping Software Development Tasks to Patterns

```
Task Domain          Effective Topologies    Key Cognitive Functions
─────────────────────────────────────────────────────────────────────
Code Generation      Chain, Loop             Reasoning → Action → Reflection
                     Orchestrate             
Bug Debugging        Loop, Hierarchy         Perception → Reasoning → 
                                             Reflection → Action
Code Review          Parallel, Hierarchy     Perception → Reasoning →
                                             Collaboration
Refactoring          Orchestrate, Loop       Reasoning → Action →
                                             Reflection
System Design        Hierarchy               Reasoning → Collaboration
Test Generation      Parallel, Orchestrate   Reasoning → Action →
                                             Reflection
Documentation        Chain, Loop             Perception → Reasoning →
                                             Action
```

## Main Ideas & Contributions

### 1. Unified Conceptual Framework

The paper's primary contribution is showing that neither topology nor cognitive function alone suffices—they must be considered together:

- **Topology answers:** "How is the system structured?"
- **Cognitive function answers:** "What capabilities does each component need?"
- **Combined view answers:** "Is this architecture suitable for this problem?"

### 2. Seven Cognitive Functions as Design Vocabulary

By systematizing cognitive functions, the paper enables precise communication about agent capabilities:

- Teams can specify requirements in terms of which cognitive functions are needed
- Architects can map those functions to topologies that support them
- Developers can identify which components need to implement each function

### 3. Design Trade-offs and Failure Modes

The framework reveals why different teams choose different topologies for superficially similar problems:

| Design Choice | Benefit | Cost |
|---|---|---|
| **Chain topology** | Simple, easy to debug | No parallelism, brittle |
| **Parallel topology** | Fast, robust via diversity | Harder to aggregate results |
| **Orchestrator-Workers** | Clear coordination | Communication overhead, bottleneck |
| **Hierarchy** | Handles complexity via abstraction | More failure points |
| **Loop** | Self-correcting | May not converge, expensive |

### 4. Practical Implications for Software Development

The framework provides actionable guidance:

1. **For bug fixing:** Use Loop topology (iterative debugging) with Reflection cognitive function
2. **For large-scale code generation:** Use Hierarchy topology (strategic planning → tactical execution) with Reasoning, Collaboration, and Reflection
3. **For quality assurance:** Use Parallel topology (multiple reviewers) with Reflection and Governance
4. **For continuous deployment:** Use Orchestrate topology with Governance cognitive function

## Methodology & Implementation

### Paper Methodology

The authors employed a **systematic literature synthesis** approach:

1. **Literature Review:** Analyzed 50+ existing agent frameworks (LangChain, LangGraph, AutoGen, CrewAI, etc.)
2. **Architecture Analysis:** Extracted common topology patterns and cognitive functions from each framework
3. **Pattern Matching:** Identified which cognitive functions each topology naturally supports or constrains
4. **Case Studies:** Mapped real-world agent systems to the framework
5. **Validation:** Verified that the framework adequately captures design distinctions in published systems

### Cognitive Functions Implementation Matrix

For software development tasks specifically:

**Code Generation Task Example:**

```
Cognitive Function     Implementation Strategy      Tools/Frameworks
─────────────────────────────────────────────────────────────────
PERCEPTION           Parse code requirements,      File I/O, Code AST
                     existing codebase

MEMORY               Store: requirements,          Vector DB, LLM context
                     generated code, test results  window, external stores

REASONING            LLM planning: decompose       o1, Claude, GPT-4
                     coding task into subtasks

ACTION               Execute: write code,          Code editor, REPL,
                     run tests                     Test runner

REFLECTION           Compare generated vs          Linter, test harness,
                     expected, identify issues     code review

COLLABORATION        Agents coordinate on          Message passing,
                     code dependencies             Shared memory

GOVERNANCE           Enforce: code style,          Lint rules, access
                     safety constraints            control, cost budgets
```

### Experimental Validation

The paper validates the framework by:

1. **Showing existing frameworks implicitly follow the patterns** (even if authors don't explicitly describe them this way)
2. **Demonstrating that design conflicts arise when cognitive function requirements don't match topology capabilities**
3. **Providing design guidelines** for choosing topology when requirements are specified in terms of cognitive functions

[Exact quantitative results unavailable — see full paper for benchmark evaluations]

## Practical Applications & Use Cases

### 1. Multi-Agent Code Generation Teams

**Problem:** Generate large software systems with multiple agents (architect, coder, tester, reviewer)

**Solution:** Hierarchy topology with Reasoning (architecture), Action (coding), Reflection (testing), Collaboration (team coordination)

```
Strategic Level (Hierarchy)
  ├─ ARCHITECT AGENT
  │  └─ Cognitive: Reasoning, Collaboration
  │     Output: Architecture document, task decomposition
  │
  ├─ DEVELOPER AGENT
  │  └─ Cognitive: Reasoning, Action, Reflection
  │     Output: Code, passing tests
  │
  └─ REVIEWER AGENT
     └─ Cognitive: Perception, Reasoning, Collaboration, Reflection
        Output: Quality assessment, feedback
```

### 2. Iterative Debugging Systems

**Problem:** Fix bugs in large codebases through multiple refinement iterations

**Solution:** Loop topology with Reflection and Reasoning

```
Iteration 1: Perception (read error) → Reasoning (diagnose) → Action (propose fix)
             ↓
Reflection (test fix) → Did it work? → No ↓
             ↓
Iteration 2: Perception (read new error) → ...
             (Repeat until converged)
```

### 3. Distributed Code Review at Scale

**Problem:** Review code with multiple specialized reviewers (security, performance, maintainability)

**Solution:** Parallel topology with independent Reflection agents

```
                    Code to Review
                          ↓
        ┌─────────────────┼─────────────────┐
        ↓                 ↓                 ↓
    Security           Performance      Maintainability
    Reviewer           Reviewer         Reviewer
        ↓                 ↓                 ↓
        └─────────────────┼─────────────────┘
                          ↓
                  Merge & Prioritize Findings
                          ↓
                    Final Review Report
```

### 4. Continuous Software Development

**Problem:** Maintain and evolve codebase over time with autonomous agents

**Solution:** Orchestrate topology (manager agent) + Loop topology (for individual tasks) + Governance

```
Project Manager (Orchestrator)
  ├─ Cognitive: Reasoning (task decomposition), Governance (budget)
  │
  ├─→ Bug Fixer Agent (Loop topology)
  │    └─ Fixes bugs with iterative refinement
  │
  ├─→ Feature Developer Agent (Orchestrate topology)
  │    └─ Manages implementation of feature
  │
  └─→ Tech Debt Agent (Chain topology)
       └─ Refactors code systematically
```

## Insights & Implications

### 1. Design Patterns are Combinations, Not Monoliths

Successful agent systems rarely use a single topology throughout. Instead:
- Use **Chain** for simple linear tasks (RAG)
- Use **Loop** for refinement tasks (iterative generation)
- Use **Parallel** for verification tasks (consensus)
- Use **Orchestrate** for complex coordination (team of agents)

This "mixed-topology" approach is more resilient than single-topology designs.

### 2. Cognitive Functions as Requirements Language

The seven cognitive functions provide a shared vocabulary for:
- **Requirements specification:** "This system needs strong Reflection capability"
- **Architecture evaluation:** "Does this topology provide adequate Reflection?"
- **Risk assessment:** "This topology lacks Governance—what are the risks?"

### 3. Failure Mode Analysis via Design Patterns

Different topologies fail in different ways:

| Topology | Failure Mode | Recovery |
|---|---|---|
| Chain | Early stage error cascades | Add loop for feedback |
| Parallel | Aggregation conflicts | Add hierarchy for arbitration |
| Orchestrator-Workers | Orchestrator bottleneck/crash | Add redundancy or peer-to-peer |
| Hierarchy | Information loss in aggregation | Add reflection at each level |
| Loop | Non-convergence | Add termination criteria |

### 4. Implications for Autonomous Software Development

1. **No one-size-fits-all topology:** Different development tasks need different coordination patterns
2. **Composition is key:** Effective agent systems combine multiple topologies
3. **Cognitive functions matter more than structure:** Two topologies with identical structure may need different cognitive capabilities
4. **Design for observability:** Governance cognitive function becomes critical as systems scale

## Code & Resources

### Official Resources

- **ArXiv Paper:** https://arxiv.org/abs/2605.13850
- **Authors:** Jia Huang, Joey Tianyi Zhou (A*STAR/CFAR)

### Related Frameworks & Tools

These frameworks implicitly follow patterns described in this paper:

1. **LangGraph** (LangChain) — Graph-based topology (Chain, Route, Parallel)
2. **AutoGen** (Microsoft) — Orchestrate topology with Collaboration cognitive function
3. **CrewAI** — Hierarchy topology with role-based agents
4. **Claude Code SDK** — Multi-topology composition for development tasks

### Design Pattern Implementation Tips

```python
# Example: Implementing Orchestrator-Workers topology

class OrchestratorWorkerSystem:
    def __init__(self):
        self.orchestrator = PlanningAgent()  # Reasoning, Collaboration
        self.workers = [
            CodeGenerationAgent(),  # Action, Reflection
            TestingAgent(),          # Reflection, Action
            ReviewAgent()            # Reflection, Collaboration
        ]
        self.memory = SharedMemory()  # Memory cognitive function
    
    async def execute_task(self, requirement):
        # Cognitive function: REASONING (Orchestrator)
        plan = await self.orchestrator.plan(requirement)
        
        # Cognitive function: COLLABORATION (Orchestrator → Workers)
        tasks = self.orchestrator.decompose(plan)
        
        # Cognitive function: ACTION (Workers)
        results = await asyncio.gather(*[
            worker.execute(task) for task, worker in zip(tasks, self.workers)
        ])
        
        # Cognitive function: REFLECTION (Orchestrator)
        feedback = await self.orchestrator.evaluate(results)
        
        # Cognitive function: GOVERNANCE (System)
        if not self.check_constraints(results):
            raise GovernanceException("Safety constraint violated")
        
        return results
```

## Related Work & Context

### Prior Foundational Work

1. **Agentic Design Patterns: A System-Theoretic Framework** (2601.19752)
   - Provides system-theoretic lens on agent design
   - Focuses more on theoretical properties than practical topology classification

2. **Architecting Agentic Communities using Design Patterns** (2601.03624)
   - Emphasizes governance and organizational structures
   - Less focus on cognitive functions

3. **Agent Design Pattern Catalogue** (2405.10467)
   - Catalogs specific design patterns
   - Complements this framework with concrete implementation patterns

### Related Surveys & Papers

- "An Empirical Study of Agent Developer Practices in AI Agent Frameworks" (2512.01939)
- "Making Sense of AI Agents Hype: Adoption, Architectures, and Takeaways from Practitioners" (2604.00189)
- "SoK: Agentic Skills — Beyond Tool Use in LLM Agents" (2602.20867)

### Future Research Directions

1. **Formal verification:** Can we prove properties of cognitive function/topology combinations?
2. **Adaptive topology switching:** Can agents dynamically change topologies based on task characteristics?
3. **Cognitive function composition:** How do we compose functions that aren't naturally compatible?
4. **Multi-agent communication protocols:** What protocols best enable cognitive functions in distributed systems?
5. **Scalability limits:** How do topologies perform with 100+ agents?

### Integration with Existing Agent Systems

The framework is most useful when combined with:
- **Requirement specification languages** that describe needed cognitive functions
- **Architecture evaluation tools** that check topology/function compatibility
- **Monitoring systems** that track cognitive function utilization
- **Failure recovery mechanisms** specific to topology-cognitive function pairs

This framework provides the conceptual foundation for the next generation of agent system design tools and methodologies.
