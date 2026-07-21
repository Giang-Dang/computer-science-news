# SEARL: Joint Optimization of Policy and Tool Graph Memory for Self-Evolving Agents

**ArXiv ID:** 2604.07791  
**Authors:** Xinshun Feng, Xinhao Song, Lijun Li, Gongshen Liu, Jing Shao  
**Venue:** ACL 2026 (Accepted)  
**Submission Date:** April 9, 2026 (Latest: April 20, 2026)  
**Field:** LLM Agents & Development / Tool Use

## Executive Summary

This paper introduces SEARL, a framework for training self-evolving agents that simultaneously optimize both their reasoning policy and a structured external memory of reusable tools. The core insight is that agents benefit from explicitly creating, refining, and reusing abstract tools for subtasks rather than monolithic solvers. SEARL extends reinforcement learning with a Tool-Memory-Aware training algorithm that provides fine-grained credit assignment for both tool creation and execution, enabling agents to accumulate and leverage problem-solving capabilities over time.

## Problem Statement

**Limitations of Monolithic Policy Learning:**
- Single policy must solve all aspects of a problem
- Cannot reuse solutions to recurring subproblems
- Knowledge dissipates when policies are updated
- Difficult to generalize across related tasks

**The Tool Synthesis Paradigm:**
Recent work recognizes that agents can improve by synthesizing new tools—specialized solutions to frequently encountered subproblems. However, existing approaches lack:
- Structured representation of tool knowledge and dependencies
- Principled credit assignment for tool creation vs. tool usage
- Integration with policy optimization for end-to-end learning

**Research Gap:**
While experience accumulation and memory systems are discussed separately, their joint optimization for tool learning and policy improvement remains underexplored.

## Core Concepts & Theory

### Tool Graph Memory Framework

**Definition:** A structured, persistent representation of tool knowledge that captures:
- Individual tool specifications (inputs, outputs, implementation)
- Tool composition relationships (which tools call which)
- Tool dependency graph (prerequisites and side-effects)
- Usage statistics and success rates

**Key Innovation:** Unlike flat tool lists or linear tool sequences, the Tool Graph Memory maintains causal relationships between tools, enabling:
- Principled credit assignment through the graph structure
- Identification of bottleneck tools that limit performance
- Targeted improvement of high-impact tools

### Tool Creation and Refinement

**Tool Synthesis:**
When agents encounter similar subproblems repeatedly, they create specialized tools rather than solving them monolithically. This involves:
- Pattern recognition: Identifying recurring subproblem structure
- Abstraction: Generalizing specific solutions
- Implementation: Creating executable tool code

**Tool Reuse:**
Agents leverage existing tools to solve new problems, with refinement through:
- Contextual adaptation: Modifying tool parameters for new contexts
- Composition: Combining multiple tools for complex tasks
- Fine-tuning: Improving tool implementations based on usage feedback

### Credit Assignment with Tool Memory

**Challenge:** How to attribute credit for success when many tools are involved?

**Solution - Memory-Anchored Clustering:**
1. Segment trajectories based on tool usage boundaries
2. Cluster segments by underlying tool usage patterns
3. Provide step-level advantages anchored to specific tool operations
4. Propagate credit through tool dependency graph

**Mathematical Framework:**
- Trajectory advantage functions extended from single-policy RL
- Tool-specific advantage functions measuring tool quality
- Composition advantages for tool combinations

## Main Ideas & Contributions

### 1. Structured Tool Graph Memory

**Representation:**
```
Tool Graph = {
  tools: [tool_1, tool_2, ..., tool_n],
  dependencies: [(tool_i → tool_j), ...],
  usage_history: {tool_id → [success_rate, avg_cost, ...]},
  composition_patterns: [frequent_combinations]
}
```

**Properties:**
- Persistent across episodes (long-term memory)
- Evolving structure as new tools are added
- Queryable for tool discovery and planning
- Human-readable documentation of learned solutions

### 2. Tool-Memory-Aware Training Algorithm

**Phase 1: Trajectory Collection**
- Agent executes policy while building/using tools
- Record tool calls, arguments, results, and outcomes
- Identify new patterns requiring new tools

**Phase 2: Segmentation and Clustering**
- Segment trajectories at tool boundaries
- Group similar segments (same or related tools)
- Extract subproblem patterns

**Phase 3: Credit Assignment**
- Compute step-level advantages relative to tool usage
- Assign tool creation credit (bootstrapping from scratch)
- Assign tool execution credit (using existing tools)
- Propagate credit through tool dependency graph

**Phase 4: Policy Update**
- Standard policy gradient (PPO, GRPO) with tool-aware advantages
- Auxiliary loss for tool improvement objectives
- Update both LLM policy and tool implementations

### 3. End-to-End Learning Framework

**Unified Objective:**
```
L = L_policy + λ_tool * L_tool + λ_discovery * L_discovery

where:
- L_policy: Standard RL objective for agent actions
- L_tool: Tool quality improvement (tool success rate)
- L_discovery: Tool discovery incentive (encourage new tools when beneficial)
```

**Key Innovation:** Policy learning and tool learning are not decoupled but jointly optimized, creating positive feedback:
- Better tools enable more effective policies
- More effective policies generate better training signal for tools
- Emerging tools enable new problem-solving strategies

## Methodology & Implementation

### System Architecture

**Agent Components:**

1. **Language Model Policy**: LLM-based reasoning over observations and available tools
2. **Tool Discovery Module**: Detects when new tools are needed
3. **Tool Generator**: Creates executable code for new tools
4. **Tool Executor**: Calls tools and captures results
5. **Memory Manager**: Maintains Tool Graph Memory

**Tool Representation:**
- Tool specification: Natural language description
- Function signature: Input/output types
- Implementation: Python/pseudocode
- Metadata: Creation date, usage statistics, dependencies

### Training Algorithm

**Offline Training:**
- Dataset: Task trajectories with tool interactions
- Batch size: Episodes organized by tool usage patterns
- Iterations: Multiple epochs with different trajectory groupings

**Online Learning:**
- Agent explores environment while building tool repertoire
- Periodic training on recent trajectories
- Tool library grows throughout training

### Datasets and Experimental Setup

**Benchmark Tasks:**

1. **Knowledge Reasoning (KBQA):**
   - Knowledge base question-answering
   - Tools: Database queries, reasoning steps, fact verification
   - Difficulty: Multi-hop reasoning requiring tool composition

2. **Mathematical Problem Solving:**
   - Complex arithmetic and symbolic math
   - Tools: Arithmetic operations, equation solvers, proof verification
   - Difficulty: Multi-step derivations requiring tool sequences

3. **General Task Environments:**
   - TextWorld-Cooking: Recipe-based reasoning
   - Countdown: Word and number puzzles
   - MindBrowser: General web navigation

### Evaluation Metrics

**Task-Level Metrics:**
- Success rate (goal achieved)
- Steps to completion
- Efficiency (steps/solution complexity)

**Tool-Level Metrics:**
- Number of tools learned
- Tool reuse frequency
- Tool generalization (usage across different tasks)
- Tool dependency chain length

**Learning Efficiency:**
- Sample complexity (trajectories needed for convergence)
- Convergence speed (wall-clock time)
- Scalability with problem complexity

### Experimental Results

[Exact figures unavailable — see full paper]

Key findings demonstrated:
- Significant improvements over monolithic policy learning
- Tool reuse reduces sample complexity
- Tool Graph Memory structure improves generalization
- Credit assignment through tool dependencies yields better policies
- Hybrid approaches combining tool learning and policy gradient outperform alternatives

## Practical Applications & Use Cases

### Current Applications

**Knowledge-Intensive Tasks:**
- Question answering systems with multi-step reasoning
- Information retrieval and knowledge synthesis
- Fact-checking and verification systems

**Problem Solving:**
- Mathematical theorem proving
- Coding assistance with function libraries
- Strategic planning in complex domains

**Multi-Domain Automation:**
- Customer support combining different task types
- Scientific research assistance
- Data analysis workflows

### Emerging Applications

**Continual Learning Systems:** Agents that accumulate tools over months of deployment

**Cross-Domain Transfer:** Tools learned in one domain transferred to related domains

**Collaborative Agents:** Multiple agents sharing and improving tool libraries

### Feasibility and Implementation Challenges

**Challenge 1: Tool Generalization**
- Problem: Tools learned for specific contexts may not transfer
- Solution: Abstract tool specifications, meta-learning for tool adaptation
- Trade-off: Generality vs. specialization

**Challenge 2: Memory Management**
- Problem: Tool libraries grow unbounded, slowing lookup and execution
- Solution: Tool clustering, periodic pruning, hierarchical organization
- Trade-off: Memory size vs. completeness

**Challenge 3: Tool Verification**
- Problem: Automatically generated tools may contain bugs or logical errors
- Solution: Verification testing, type checking, formal methods
- Trade-off: Correctness guarantees vs. generation speed

## Insights & Implications

### Broader Field Impact

1. **Modularity in Agent Learning:** Demonstrates that explicit modularity (tools) plus implicit learning (policy) is more effective than end-to-end approaches

2. **Structured Experience Accumulation:** Shows how to build persistent, reusable knowledge structures from RL trajectories

3. **Credit Assignment Innovation:** Extends credit assignment techniques to handle complex hierarchical decision structures

### State-of-the-Art Advancement

- First integrated framework for joint policy and tool optimization
- Novel credit assignment mechanism for structured tool graphs
- Empirical validation on multiple task domains
- Path toward more capable and efficient self-evolving agents

### Limitations and Open Questions

1. **Tool Abstraction Levels:** How to determine appropriate tool abstraction granularity?

2. **Scalability:** How do methods scale to thousands of tools or very deep dependency graphs?

3. **Knowledge Transfer:** How to transfer tool libraries across significantly different domains?

4. **Tool Composition:** How to handle complex tool compositions beyond simple chains?

5. **Human Interpretability:** How to make learned tools interpretable to human operators?

## Code & Resources

**Official Resources:**
- Code for SEARL framework implementation
- Tool Graph Memory data structures and operations
- Training algorithms and RL optimization components
- Evaluation scripts and benchmark environments

**Key Libraries:**
- PyTorch for neural network policy
- Ray RLlib for distributed RL training
- OpenAI Gym environments for benchmarks
- Custom graph libraries for Tool Graph operations

**Compute Requirements:**
- GPU: Single to multi-GPU setups (8 GPUs for large-scale experiments)
- Memory: 16-32 GB for storing large tool libraries
- Storage: 10-100 GB for trajectory logs and trained models

**Quick Start:**
```
1. Define tool specification language
2. Initialize empty Tool Graph Memory
3. Train agent on benchmark with DQN/PPO + tool discovery
4. Monitor tool growth and reuse patterns
5. Evaluate on test tasks
```

## Related Work & Context

### Related Recent Papers

- **Next-Generation Agentic Reinforcement Learning Systems** (2607.01120)
  Addresses production infrastructure for self-evolving agents with tools

- **GUI Agents with Reinforcement Learning: Toward Digital Inhabitants** (2604.27955)
  Broad survey of RL for GUI agents including tool use patterns

- **Beyond Trajectory-Level Attribution: Graph-Based Credit Assignment** (2605.26684)
  Extends credit assignment to graph structures (complementary to SEARL)

- **Memory Beyond Recall: Dual-Process Cognitive Memory** (2606.09483)
  Explores cognitive-inspired memory systems for agent learning

### Prior Work Foundations

- **Hierarchical Reinforcement Learning:** Learning at multiple abstraction levels
- **Option Frameworks:** Temporal abstraction through reusable behaviors
- **Modular Networks:** Neural architectures with modular components
- **Skill Learning:** Extracting and reusing skills from trajectories
- **Graph Neural Networks:** Learning representations over structured data

### Future Research Directions

1. **Hierarchical Tool Structures:** Multi-level abstraction hierarchies for tools

2. **Tool Composition Learning:** Discovering effective tool sequences automatically

3. **Cross-Agent Tool Sharing:** Multiple agents collaboratively building shared tool libraries

4. **Formal Tool Verification:** Guaranteeing correctness of learned tools

5. **Tool Interpretability:** Making learned tools human-interpretable and debuggable

6. **Meta-Learning over Tools:** Learning which tools to learn given a new task
