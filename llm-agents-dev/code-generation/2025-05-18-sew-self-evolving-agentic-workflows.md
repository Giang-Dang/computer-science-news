# SEW: Self-Evolving Agentic Workflows for Automated Code Generation

**ArXiv ID:** 2505.18646  
**Authors:** Siwei Liu, Jinyuan Fang, Han Zhou, Yingxu Wang, Zaiqiao Meng  
**Affiliations:** University of Aberdeen, University of Glasgow, University of Cambridge, MBZUAI  
**Submission Date:** May 2025

## Executive Summary

SEW introduces a paradigm shift in multi-agent code generation: instead of relying on manually crafted workflows and agent prompts, the system automatically evolves both the agentic workflow topology and agent instructions through evolutionary algorithms. This end-to-end self-evolution approach achieves up to 33% improvement over baseline LLMs on code generation benchmarks, demonstrating that agent orchestration patterns can be discovered rather than designed.

The significance lies in addressing a critical bottleneck in agentic systems—the heavy manual engineering required to design task decomposition and agent coordination. SEW shows that machine-driven evolution can discover effective multi-agent architectures, enabling broader deployment of agentic systems across diverse coding problems without domain expertise.

## Problem Statement

Existing multi-agent code generation systems face a fundamental limitation: they rely on hand-crafted agentic workflows with manually designed agent topologies, task decomposition strategies, and agent prompts. This manual engineering burden:

- **Limits Scalability:** Each new problem domain may require re-engineering the workflow architecture
- **Prevents Adaptation:** Fixed workflows cannot adapt dynamically to different types of coding challenges
- **Requires Domain Expertise:** Designing effective multi-agent orchestration demands deep understanding of agent interactions and task dependencies
- **Lacks Generalization:** Optimal workflows for one task type may be suboptimal for others

Prior approaches like PromptBreeder (prompt-only evolution) and ADAS (single-agent adaptation) don't address the core challenge: how to automatically discover effective multi-agent orchestration patterns. The research gap is clear: **can agentic workflows themselves be treated as learnable artifacts that improve through evolution?**

## Core Concepts & Theory

### Multi-Agent Orchestration Architecture

SEW models agentic workflows as directed acyclic graphs (DAGs) where:
- **Nodes** represent task decompositions or agent roles
- **Edges** represent dependencies and task flows
- **Agent Prompts** define the instructions and capabilities assigned to each node

```
┌─────────────────────────────────────────────┐
│   Initial Workflow (Hand-crafted)           │
├─────────────────────────────────────────────┤
│                                             │
│  ┌──────────┐     ┌──────────┐            │
│  │  Analyze │────▶│  Design  │            │
│  │  Problem │     │  Solution│            │
│  └──────────┘     └──────────┘            │
│       │                │                   │
│       └────┬───────────┘                   │
│            │                               │
│       ┌────▼──────────┐                   │
│       │ Implement &   │                   │
│       │ Test Code     │                   │
│       └───────────────┘                   │
│                                             │
└─────────────────────────────────────────────┘
                    ↓
    ┌──────────────────────────────┐
    │  Evolutionary Optimization    │
    │  - Topology mutations         │
    │  - Prompt enhancement         │
    │  - Agent role redefinition    │
    └──────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│   Evolved Workflow (Auto-discovered)        │
│   ├─ Optimized task decomposition           │
│   ├─ Emergent agent specialization          │
│   └─ Enhanced coordination patterns         │
└─────────────────────────────────────────────┘
```

### Workflow Representation Schemes

SEW evaluates multiple encoding formats to represent workflows, each with tradeoffs:

| Representation | Format | Generation Success | Ease of Mutation |
|---|---|---|---|
| **BPMN** | XML-based Process Notation | Moderate | Low (rigid schema) |
| **Python Code** | Python function calls & control flow | Lower | Moderate (syntax constraints) |
| **YAML** | Structured config format | Good | Moderate |
| **Pseudo-code** | Natural but structured | High | Low (ambiguity) |
| **CoRE (Hybrid)** | Composed symbolic + natural language | **Highest** | **Highest** |

The **CoRE (Composed Reasoning Encoding)** format emerges as optimal because it:
- Encodes workflow structure symbolically (prevents invalid mutations)
- Includes natural language task descriptions (enables flexible evolution)
- Balances LLM generative capability with structural validity

### Dual-Evolution Framework

SEW employs two interdependent evolutionary loops:

**Loop 1: Workflow Topology Evolution**
- Mutate task decomposition structure
- Add/remove/reorder agent stages
- Modify data flow between components
- Evaluate on intermediate code generation tasks

**Loop 2: Prompt Enhancement**
- Refine agent instructions within fixed topology
- Apply genetic operators: crossover, mutation
- Iterative prompt improvement via fitness feedback

### Genetic Operators & Heuristics

**Workflow Mutations:**
- **Decomposition:** Split single agent into specialized agents
- **Merging:** Combine closely-related task steps
- **Reordering:** Change execution sequence if dependencies allow
- **Refinement:** Adjust granularity of task breakdown

**Prompt Mutations:**
- **Instruction Replacement:** Substitute ineffective guidance
- **Example Addition:** Insert helpful code examples
- **Constraint Addition:** Emphasize correctness requirements
- **Style Adjustment:** Tailor output format expectations

**Heuristic Operators:**
- Guided mutation based on error patterns from execution
- Fitness-proportionate selection of high-performing variants
- Elitism: preserve best workflows across generations

## Main Ideas & Contributions

### 1. **Automated Workflow Synthesis**
Rather than manually designing how tasks decompose and agents coordinate, SEW generates candidate workflows automatically. The key insight: **workflow design is a learnable optimization problem**, not requiring human expertise.

### 2. **Task Decomposition Discovery**
The system discovers emergent task decomposition strategies. For example:
- Complex problems might automatically decompose into: Analysis → Design → Implementation → Testing → Refinement
- Simpler problems might optimize to: Understanding → Coding → Verification
- Domain-specific patterns emerge without explicit encoding

### 3. **Emergent Agent Specialization**
Multi-agent roles emerge from the evolutionary process:
- Agents naturally specialize in different aspects of coding (e.g., planning vs. implementation)
- Role boundaries optimize for the specific problem domain
- Agent interactions (dependencies) reflect discovered optimal task flow

### 4. **Representation-Agnostic Evolution**
By supporting multiple workflow encodings (especially CoRE), SEW demonstrates that **workflow evolution is more important than representation specifics**. The system can adapt its encoding to the problem characteristics.

### 5. **Fitness-Driven Optimization**
Success metric: code generation pass@k rates on benchmark tasks. This grounds evolution in real software engineering outcomes rather than abstract metrics.

## Methodology & Implementation

### Experimental Setup

**Benchmarks Evaluated:**

1. **LiveCodeBench** (Primary evaluation)
   - 110 problems with gradual difficulty increase
   - Execution-based evaluation with ground-truth test cases
   - Simulates real coding interview progression

2. **MBPP and HumanEval**
   - Standard program synthesis benchmarks
   - Validate generalization across datasets

**Models Tested:**
- GPT-4o mini (cost-efficient)
- Gemini 1.5-pro-002 (high capability)

### Evolution Process

**Phase 1: Initial Population Generation**
- Generate 5-10 candidate workflows using prompt engineering
- Seed population with diverse task decomposition strategies

**Phase 2: Iterative Evolution**
- **Per Generation:** 
  - Evaluate all candidates on sample problems
  - Compute fitness scores (pass@1 rate)
  - Select top 30% for breeding
  - Apply genetic operators to create next generation
  - Keep elite solutions

- **Generations:** Run 10-20 generations depending on convergence

**Phase 3: Prompt Enhancement**
- Fine-tune agent instructions for best-performing topology
- Apply prompt-level mutations
- Re-evaluate on full benchmark

### Results & Performance Metrics

**Quantitative Results on LiveCodeBench:**

| Model | CoT (Baseline) | PromptBreeder | ADAS | **SEW** | Improvement |
|---|---|---|---|---|---|
| **GPT-4o mini** | 40.1% | 45.9% | 42.5% | **50.9%** | +27% vs CoT, +11% vs ADAS |
| **Gemini 1.5-pro-002** | 39.8% | 44.8% | 43.3% | **47.8%** | +20% vs CoT, +10% vs ADAS |

**Pass Rate Metrics:**
- **pass@1:** Primary metric (first generation solution passes all tests)
- **pass@5:** Top-5 attempts
- **pass@10:** Top-10 attempts

Results show consistent improvements across all metrics, with most gains in pass@1 (single-shot generation).

**Qualitative Insights:**

[Exact figures unavailable — see full paper for detailed breakdown per difficulty tier and problem category]

The evolved workflows demonstrate:
- Better task ordering for complex multi-step problems
- Specialized agent roles for planning, implementation, verification
- Adaptive granularity: fine-grained decomposition for hard problems, coarse-grained for easy ones

### Evolved Agent Topologies (Examples)

**Example 1: Recursive Refinement Topology**
```
┌─────────────────┐
│  Understand     │
│  Specification  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Generate Code  │◄──────┐
│  (Iterate v1)   │       │
└────────┬────────┘       │
         │                │
         ▼                │
┌─────────────────┐       │
│  Test & Debug   │       │
│  (Find Issues)  │       │
└────────┬────────┘       │
         │                │
    Has Bugs? ────── YES ──┘
         │
        NO
         ▼
┌─────────────────┐
│  Final Output   │
└─────────────────┘
```
Evolved for: Problems requiring iterative refinement and debugging

**Example 2: Parallel Verification Topology**
```
        ┌─────────────────┐
        │  Analyze Spec   │
        └────────┬────────┘
                 │
         ┌───────┴────────┐
         │                │
         ▼                ▼
    ┌─────────┐      ┌──────────┐
    │Generate │      │Generate  │
    │Solution1│      │Solution2 │
    └────┬────┘      └────┬─────┘
         │                │
         └────────┬───────┘
                  ▼
         ┌──────────────────┐
         │Compare & Merge   │
         │Best Features     │
         └────────┬─────────┘
                  ▼
         ┌──────────────────┐
         │Unified Test      │
         │Final Solution    │
         └──────────────────┘
```
Evolved for: Problems benefiting from diverse solution exploration

## Practical Applications & Use Cases

### 1. **Code Interview & LeetCode-Style Problems**
LiveCodeBench simulates progressive difficulty interview questions. SEW's evolved workflows adapt:
- Easy (arithmetic operations): Direct implementation workflow
- Medium (data structures): Analysis → Design → Implement → Test
- Hard (algorithms/optimization): Exploratory → Multiple approaches → Verification

### 2. **Domain-Specific Code Generation**
While tested on general programming, SEW's approach applies to:
- **Hardware Description (Verilog/VHDL):** Specialized simulation-aware workflows
- **Database Queries:** Schema analysis → Query planning → Testing workflows
- **Machine Learning Code:** Data preprocessing → Model architecture → Training loops

### 3. **Production Code Generation Systems**
Organizations using LLMs for code could:
- **Evolve task-specific workflows** for their codebase characteristics
- **Reduce manual prompt engineering** through automatic optimization
- **Adapt workflows** as problem distributions change

### 4. **Continuous Workflow Improvement**
In production systems: use live feedback (whether generated code passed tests) to continuously evolve workflows.

## Insights & Implications

### 1. **Workflow Design is Learnable**
The core contribution: task orchestration patterns previously requiring human expertise can be automatically discovered. This democratizes multi-agent system design.

### 2. **Evolution Finds Counter-Intuitive Patterns**
Evolved workflows sometimes use task orderings or role specializations humans wouldn't naturally design, suggesting evolution finds non-obvious optimizations in the agent coordination space.

### 3. **Representation Matters, But Less Than Topology**
While CoRE representation shows highest success, the key variable is topology quality—the representation mainly needs to support efficient evolution.

### 4. **Generalization Challenges**
[Exact cross-benchmark generalization figures unavailable — see paper] The system shows good performance within LiveCodeBench; cross-benchmark generalization (LiveCodeBench-trained → MBPP) may require transfer learning techniques.

### 5. **Scalability to Larger Multi-Agent Systems**
Current system demonstrates effectiveness with 3-5 agent stages. Scaling to 10+ specialized agents introduces:
- Larger search space for topology evolution
- Increased computational cost of fitness evaluation
- Need for hierarchical evolution strategies

### 6. **Open Research Directions**
- **Meta-evolution:** Can workflows themselves learn to evolve better?
- **Human-AI hybrid design:** Bootstrapping evolution with human workflow hints
- **Online adaptation:** Real-time workflow adjustment based on test outcomes
- **Interpretability:** Making evolved orchestration patterns understandable to practitioners

## Code & Resources

**Official Repository:** [To be confirmed — check authors' GitHub profiles]
- Siwei Liu: github.com/[username]
- Related work typically published through institutional repositories

**Dependencies:**
- LLM API access (OpenAI, Google, or compatible)
- Python 3.9+
- Evolutionary algorithm library (e.g., DEAP)
- Code execution environment for fitness evaluation

**Computing Requirements:**
- For LiveCodeBench: ~50-100 GPU hours (depending on number of generations and model)
- Per-generation cost: 110 benchmark problems × multiple candidates × multiple runs

**Quick Integration Guide:**
1. Define your task domain and success metrics
2. Initialize 5-10 seed workflows for your problem type
3. Run evolutionary loop with your LLM backend
4. Monitor fitness trajectory for convergence
5. Deploy highest-fitness workflow to production

## Related Work & Context

### Prior Work in Multi-Agent Code Generation
- **PromptBreeder** (2023): Agent-level prompt optimization, single-agent focus
- **ADAS** (2024): Adaptive decomposition, but fixed orchestration structure
- **AutoGPT / BabyAGI** (2023): Flexible agent loops, but hand-designed orchestration

### Foundational References
- **Program Synthesis:** Neyman et al. (2023) on neural program synthesis efficiency
- **Evolutionary Optimization:** NSGA-II, genetic algorithms for constraint-satisfaction problems
- **Prompt Engineering:** Reynolds & McDonell (2021) on prompt design paradigms

### Connection to This Repository's Themes

SEW directly addresses two key research areas:
1. **Agent Orchestration:** Demonstrates automated orchestration topology generation
2. **Skill Frameworks:** Evolving agent roles as specialized skills rather than hand-crafted tools

### Future Extensions

**Immediate Next Steps:**
- Extend to multi-language code generation (Python, Java, Go)
- Apply to specialized domains (regex, SQL generation)
- Benchmark against human-designed orchestration patterns

**Longer-Term Vision:**
- Self-evolving agent communities that adapt workflows in real-time
- Integration with code quality metrics (complexity, performance) beyond correctness
- Hierarchical evolution for large-scale multi-agent systems

## Summary

SEW represents a paradigm shift in agentic systems: from manual orchestration design to machine-discovered workflows. By treating task decomposition and agent coordination as evolutionary optimization problems, the system achieves state-of-the-art code generation results while eliminating the manual engineering bottleneck. This work has profound implications for scaling autonomous agents to complex real-world software engineering tasks.
