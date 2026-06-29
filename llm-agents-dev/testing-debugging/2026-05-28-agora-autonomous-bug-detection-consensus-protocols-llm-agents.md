# Agora: Toward Autonomous Bug Detection in Production-Level Consensus Protocols with LLM Agents

**ArXiv ID:** 2605.29910  
**Submitted:** May 28, 2026  
**Authors:** Xiang Liu, Sa Song, Zhaowei Zhang, Huiying Lan, Jason Zeng, Ming Wu, Michael Heinrich, Yong Sun, Ceyao Zhang  
**Domain:** Artificial Intelligence (cs.AI), Software Engineering  
**Code:** [GitHub - lebronlambert/Agora](https://github.com/lebronlambert/Agora)

## Abstract

Agora is the first domain-aware multi-agent framework that combines LLM capabilities with hypothesis-driven testing for autonomous bug detection in production-level consensus protocols. While LLMs show promise in general code analysis, they struggle with deep protocol-level logic bugs involving complex state-dependent behaviors across multiple execution stages. 

Agora integrates **domain knowledge of distributed consensus** with **multi-agent reasoning** to systematically explore protocol state spaces, synthesize attack scenarios using domain-specific constraints, and validate findings through iterative refinement. The system enables reasoning about global protocol invariants beyond single-function code analysis—a critical capability for detecting subtle bugs that violate safety properties in consensus algorithms.

## Problem Addressed

### The Challenge
Consensus protocols form the backbone of blockchain systems and distributed applications. Implementation bugs in these protocols can cause:
- Data corruption and loss
- Financial losses in blockchain systems
- System crashes and unavailability
- Security vulnerabilities and exploitation windows

### Why Current Approaches Fall Short

1. **Manual Testing:** Exponential state space makes comprehensive manual testing infeasible
2. **Traditional Fuzzing:** Generic fuzzing approaches miss protocol-level logic bugs
3. **Naive LLM Analysis:** LLMs applied directly to protocol code fail to detect:
   - Multi-stage execution bugs requiring global state tracking
   - Subtle invariant violations across distributed actors
   - Complex race conditions and timing issues
   - Safety property violations under edge cases

### Key Insight
Protocol-level logic bugs require understanding **global protocol invariants**—properties that must hold across all execution traces—rather than just analyzing individual functions or modules.

## Core Methodology

### Framework Architecture

Agora employs a **three-agent orchestration** following the hypothesis-driven testing (HDT) paradigm:

#### 1. **Orchestrator Agent**
- **Role:** Coordinates the overall testing campaign
- **Responsibilities:**
  - Maintains test strategy and exploration plan
  - Manages the testing loop and iteration
  - Aggregates results from other agents
  - Prioritizes unexplored state space regions
  - Determines when to terminate testing

- **Reasoning Level:** System-level strategy and workflow

#### 2. **Strategy Agent**
- **Role:** Domain expert in consensus protocols
- **Responsibilities:**
  - Analyzes protocol specifications and code
  - Identifies critical invariants and safety properties
  - Generates domain-specific testing hypotheses
  - Suggests relevant attack scenarios and edge cases
  - Constrains the search space using domain knowledge

- **Key Insight:** Encodes knowledge about what bugs are *possible* in consensus protocols based on distributed systems theory

#### 3. **TestGen Agent**
- **Role:** Test case and attack scenario generator
- **Responsibilities:**
  - Synthesizes concrete test cases and attack scenarios
  - Uses domain-specific constraints from Strategy Agent
  - Generates adversarial network conditions
  - Creates unusual node failure patterns
  - Produces inputs designed to violate identified hypotheses

- **Output:** Executable test cases targeting specific vulnerabilities

### Hypothesis-Driven Testing Loop

```
1. Strategy Agent proposes hypothesis about potential bug
   (e.g., "Leader election can hang under message loss")

2. TestGen Agent synthesizes attack scenario
   (e.g., "Flood network, drop critical messages")

3. Execute test on protocol implementation
   (e.g., Run Raft/HotStuff/EPaxos with simulated conditions)

4. Orchestrator collects results
   - Did the hypothesis manifest as a bug?
   - Did we find a new invariant violation?
   
5. If bug found: Validate and document
   
6. If no bug: Refine hypothesis and continue

Repeat until convergence or state space exhausted
```

### Domain-Specific Constraints

Unlike generic testing, Agora incorporates domain knowledge:

- **Protocol-Specific Invariants:**
  - Consensus safety: Only one value can be committed per slot
  - Liveness: System progresses despite failures
  - Linearizability and ordering properties

- **Distributed System Constraints:**
  - Message delivery guarantees (ordering, duplication)
  - Failure models (crash, Byzantine)
  - Network partitions and delays

- **Implementation Considerations:**
  - State machine semantics
  - Timeout configurations
  - Message buffering and ordering

## Experimental Evaluation

### Evaluation Scope

**Consensus Protocols Tested:**
- Raft (leader-based, crash-tolerant)
- EPaxos (leaderless, crash-tolerant)
- HotStuff (leader-based, Byzantine-tolerant)
- BullShark (leaderless, Byzantine-tolerant)

These represent the major families of modern consensus protocols used in production.

### LLM Models Evaluated

Systematic evaluation across **four state-of-the-art LLMs:**
- GPT-4 series
- Claude series
- Other frontier models

This ensures results generalize across different LLM architectures and capabilities.

### Key Experimental Results

#### Bug Detection Performance

**Critical Finding: Discovery of 15 previously unknown protocol-level logic bugs**

**Bug Breakdown by Type:**

1. **Leader Election Failures** (multiple bugs)
   - Deadlock conditions under specific message sequences
   - Infinite loops in leader rotation
   - Election timeout synchronization issues

2. **Safety Violations** (multiple bugs)
   - Scenarios where two different values could be committed for same slot
   - Invariant violations in commit point determination
   - Ordering property violations

3. **Liveness Failures** (multiple bugs)
   - Scenarios where system stops making progress
   - Permanent message delivery issues
   - Coordination failures in multi-step protocols

4. **Byzantine Resilience Issues** (applicable bugs)
   - Improper validation of Byzantine messages
   - Insufficient quorum checks
   - Vulnerability to particular Byzantine patterns

#### Baseline Comparison

**Agora vs. Existing LLM-Based Approaches:**
- Existing LLM agents: **0 protocol-level logic bugs detected**
- Agora: **15 protocol-level logic bugs detected**

This represents a **qualitative breakthrough** in what LLM-based approaches can detect.

#### Low False Positive Rate
- Discovered bugs are **valid and reproducible**
- Require careful case analysis to fix
- Not trivial issues that existing testing would catch

### Analysis of Discovered Bugs

**Characterization:**

1. **Complexity:** Most bugs require 5+ steps to manifest
   - Multiple message exchanges
   - Specific ordering or timing conditions
   - Often involve corner cases in protocol logic

2. **Impact:** Critical bugs with high severity
   - Violate core safety properties
   - Affect protocol correctness
   - Could cause system failures in production

3. **Hardness:** Difficult for human or automated reviewers
   - Not found by existing testing approaches
   - Require understanding of global protocol invariants
   - Involve subtle state-dependent conditions

## Technical Contributions

### 1. **Domain Integration Framework**
Demonstrates how to systematically integrate domain knowledge into LLM-based testing:
- Encode invariants and constraints
- Structure agent roles around domain expertise
- Guide generation toward protocol-relevant scenarios

### 2. **Multi-Agent Bug Detection Architecture**
Shows how to decompose complex testing into complementary agent roles:
- High-level strategy (Strategy Agent)
- Scenario synthesis (TestGen Agent)
- Orchestration and learning (Orchestrator Agent)

### 3. **Hypothesis-Driven LLM Testing**
Adapts classic hypothesis-driven testing to LLM agents, enabling:
- Systematic exploration of state space
- Refinement based on observed outcomes
- Domain-constrained generation

### 4. **Empirical Validation at Scale**
Proves the approach on four different consensus protocols and four LLM models simultaneously.

## Relevance to Software Development Automation

Agora's contributions extend beyond consensus protocols to broader software development:

### 1. **Complex System Testing**
- Demonstrates how agents can test systems with large state spaces
- Applicable to distributed services, databases, microservices
- Shows how domain knowledge constrains search effectively

### 2. **Invariant Specification and Verification**
- Framework for encoding system invariants
- Agent-based exploration to find invariant violations
- Generalizes to any system with specifiable properties

### 3. **Scenario Synthesis**
- Agents can generate complex, multi-step test scenarios
- More sophisticated than random inputs
- Can target specific bugs based on hypothesis

### 4. **Autonomous Testing Agents**
- Shows feasibility of LLM-based autonomous test generation
- Architecture is generalizable to other domains
- Combines domain expertise with LLM reasoning

### 5. **Safety-Critical System Development**
- For systems requiring high reliability (finance, security, infrastructure)
- Demonstrates how to detect subtle bugs before production
- Combines formal reasoning with LLM flexibility

## Agent Coordination Patterns

Key coordination patterns used in Agora:

1. **Sequential Refinement:** Each agent builds on previous agent's output
   - Strategy Agent → TestGen Agent → Execution → Results → Orchestrator

2. **Feedback Loops:** Results inform hypothesis refinement
   - Failed tests generate new hypotheses
   - Successful exploits guide future testing

3. **Specialization:** Each agent has clear domain role
   - Separation of concerns enables expertise focus
   - Reduces hallucination through structured roles

4. **Collective Knowledge:** Agents combine:
   - Domain expertise (Protocol knowledge)
   - Generation capability (Test synthesis)
   - Reasoning ability (Hypothesis formation)

## Limitations and Future Work

### Current Limitations
1. **Protocol-Specific Tuning:** Strategy Agent requires protocol knowledge injection
2. **State Space Coverage:** Exponential growth limits exhaustive exploration
3. **Implementation Coverage:** Tested on specific protocol implementations
4. **Generalization:** Approach most effective for well-specified protocols

### Future Directions
1. **Meta-Strategy Learning:** Agents learning what strategies work for different protocol families
2. **Formal Verification Integration:** Combining with theorem provers for harder properties
3. **Broader System Testing:** Applying to other complex distributed systems
4. **Continuous Monitoring:** Runtime monitoring of deployed protocols for emergent bugs

## Code and Resources

- **Full implementation available:** [GitHub - lebronlambert/Agora](https://github.com/lebronlambert/Agora)
- **Test harnesses for four consensus protocols**
- **Protocol implementations and specifications**
- **Evaluation scripts and result analysis tools**
- **Reproducible benchmark setup**

## Related Work

**Testing and Verification:**
- Fuzzing and symbolic execution for protocol testing
- Formal verification of distributed systems
- Property-based testing

**LLM-Based Testing:**
- LLM agents for code analysis
- LLM-based vulnerability detection
- Automated test generation

**Consensus Protocols:**
- Raft, Paxos, HotStuff, and Byzantine consensus literature
- Formal protocol verification
- Protocol implementation bugs in practice

**Multi-Agent Systems:**
- Agent orchestration and coordination
- LLM-based multi-agent collaboration
- Role-based agent design

## Publications and Links

- **ArXiv:** [2605.29910 - Agora: Toward Autonomous Bug Detection in Production-Level Consensus Protocols with LLM Agents](https://arxiv.org/abs/2605.29910)
- **HTML Version:** [Full paper on ArXiv](https://arxiv.org/html/2605.29910v1)
- **Code Repository:** [lebronlambert/Agora on GitHub](https://github.com/lebronlambert/Agora)

## Conclusion

Agora represents a significant advance in applying LLM agents to the challenging problem of autonomous bug detection in complex protocols. By combining domain-specific knowledge with multi-agent orchestration and hypothesis-driven testing, it achieves the first meaningful detection of protocol-level logic bugs in consensus implementations.

The 15 previously unknown bugs discovered across four major consensus protocols demonstrate that this approach can find subtle, critical bugs that existing testing tools and human reviewers miss. The architecture is generalizable beyond consensus protocols to any complex system with specifiable invariants and constraints.

For teams building autonomous software development systems, Agora provides both a template for coordinating specialized agents and evidence that LLM-based autonomous testing can handle complex, real-world systems with proper domain integration.
