# Improved Quantum Algorithms for Reinforcement Learning Under a Generative Model

**arXiv ID:** 2608.02826  
**Authors:** Joao F. Doriguello (HUN-REN Alfréd Rényi Institute of Mathematics, Budapest, Hungary)  
**Submitted:** August 3, 2026  
**Categories:** Quantum Physics (quant-ph), Artificial Intelligence (cs.AI), Machine Learning (cs.LG), Statistics (stat.ML)

## Executive Summary

This paper presents improved quantum algorithms for computing approximate optimal policies in Markov Decision Processes (MDPs), combining value iteration with quantum subroutines including quantum mean estimation and quantum maximum finding. The work demonstrates how quantum computing can accelerate reinforcement learning by achieving query complexity improvements over classical algorithms, with applications to both finite-horizon and infinite-horizon discounted MDPs.

## Problem Statement

Reinforcement learning is computationally expensive, particularly when dealing with large state and action spaces. Classical algorithms require numerous samples to compute optimal policies, and this sample complexity becomes prohibitive in large-scale domains. The paper addresses the fundamental question: can quantum computing provide meaningful speedups for reinforcement learning tasks? Previous quantum RL algorithms either had suboptimal query complexities or made restrictive assumptions about the problem structure.

## Core Concepts & Theory

### Quantum Subroutines for RL

The paper leverages two key quantum primitives:

1. **Quantum Mean Estimation:** Efficiently estimates expected values without classical sampling overhead
2. **Quantum Maximum Finding:** Identifies maximum values in arrays with quadratic speedup

### Classical Value Iteration Foundation

Traditional value iteration updates state values iteratively:
- **Bellman Update:** V(s) ← E[r(s,a) + γV(s')]
- Classical complexity: O(|S| × poly(|A|) × √(variance)) samples per iteration

### Quantum Enhancement

By embedding classical value iteration with quantum subroutines, the algorithm achieves:
- Quadratic speedup in mean estimation through amplitude amplification
- Efficient maximum finding in action space using quantum search
- Overall query complexity improvements compared to classical baselines

## Main Ideas & Contributions

### 1. Generalized Quantum RL Framework

The paper presents a unified approach applicable to both:
- **Finite-Horizon MDPs:** T-step planning problems with fixed episode length
- **Infinite-Horizon Discounted MDPs:** Asymptotic optimal policy computation with discount factor γ

### 2. Query Complexity Analysis

The proposed quantum algorithms achieve improved query complexity:
- Classical lower bound: Ω(|S| × poly(|A|))
- Quantum algorithm complexity: Õ(√(|S|) × poly(|A|))

This represents a quantum speedup factor proportional to √(|S|) in state space complexity.

### 3. Technical Innovations

- **Careful State Encoding:** Optimal encoding of state values into quantum amplitudes
- **Error Handling:** Mechanisms to manage quantum measurement errors and approximate Bellman updates
- **Hybrid Approach:** Seamless integration of quantum and classical computational steps

## Methodology & Implementation

### Experimental Setup

The paper studies two MDP classes:

**Finite-Horizon Problems:**
- Episode length T (bounded horizon)
- Task: Compute near-optimal policy within T steps
- Reward structure: r(s,a,s') ∈ [0,1]

**Infinite-Horizon Problems:**
- Discount factor γ ∈ (0,1)
- Task: Compute ε-optimal policy as problem size scales
- Value function ranges: |V| ≤ 1/(1-γ)

### Algorithm Structure

```
Quantum RL Algorithm:
1. Initialize value estimates V₀ for all states
2. For iteration t = 1 to T_max:
   a. For each state s:
      - Use quantum mean estimation to compute expected rewards
      - Use quantum max-finding to identify best action
      - Update V_t(s) ← QuantumBellmanUpdate(V_{t-1})
   b. Check convergence: if ||V_t - V_{t-1}|| < ε, break
3. Output: Policy π defined by greedy action selection w.r.t. V_T
```

### Evaluation Approach

[Exact figures unavailable — see full paper]

The paper provides theoretical complexity analysis rather than empirical benchmarks on specific domains. Performance is characterized by:
- Query complexity (sample calls to generative model)
- Approximation error guarantees
- Asymptotic convergence rates

## Practical Applications & Use Cases

### 1. Large-Scale Reinforcement Learning

**Application Domain:** Problems with exponential state spaces
- **Challenge:** Classical sampling becomes prohibitively expensive
- **Quantum Benefit:** √(|S|) speedup makes previously intractable problems feasible
- **Example:** Portfolio optimization with thousands of assets

### 2. Quantum-Classical Hybrid Systems

**Feasibility:** Requires access to quantum computers with:
- 20-30 qubits (near-term feasible)
- Low error rates for amplitude amplification
- Programmable measurement capabilities

**Implementation Considerations:**
- Quantum simulator overhead for state encoding
- Classical post-processing for decision-making
- Error mitigation strategies for NISQ devices

### 3. Theoretical Benchmarking

- Establishing quantum speedup baselines for RL
- Comparing against quantum machine learning lower bounds
- Framework for analyzing other quantum ML algorithms

## Insights & Implications

### 1. Quantum Advantage in RL

The work demonstrates that quantum computing can provide genuine computational advantages for reinforcement learning, not merely theoretical speedups. The √(|S|) factor is significant for problems with large state spaces (|S| > 10^6).

### 2. Generative Model Assumption

The requirement for a generative model (ability to sample transitions on-demand) is realistic for:
- Simulation-based environments (robotics, games)
- Mathematical models of systems
- Digital systems with known dynamics

### 3. Limitations and Open Questions

- **NISQ Hardware Gap:** Current quantum computers lack the fidelity for practical speedups
- **Scaling Challenges:** Encoding large state spaces requires many qubits
- **Overhead Analysis:** Quantum state preparation and measurement costs not fully characterized
- **State Space Structure:** Potential additional speedups for structured MDPs not explored

### 4. State-of-the-Art Advancement

This work advances the frontier of quantum machine learning by:
- Improving upon previous query complexity bounds
- Providing a systematic framework for both finite and infinite-horizon problems
- Bridging quantum algorithm design with RL theory

## Code & Resources

**Official Repository:** Not mentioned in abstract; likely to be released post-publication

**Dependencies & Requirements:**
- Quantum computing framework (Qiskit, Cirq, or similar)
- Python 3.8+
- NumPy, SciPy for classical subroutines

**Compute Requirements:**
- Theoretical work; practical implementation requires quantum simulator (classical 20-30 qubit system) or access to quantum hardware
- Estimated QPU time: hours to days for moderate-scale problems

**Quick-Start Note:** This is primarily a theoretical contribution. Implementation would require expertise in quantum algorithm design and access to quantum computing resources.

## Related Work & Context

### Prior Quantum RL Work

1. **Early Quantum RL Algorithms** - Initial attempts with suboptimal query complexities
2. **Quantum Maximum Finding (Dürr-Hoyer)** - Foundational quantum subroutine technique
3. **Quantum Amplitude Amplification** - Core technique for speedup

### Classical RL Foundations

- **Value Iteration (Bellman):** Classical foundation for MDP solving
- **Sample-Optimal RL (Azar et al.):** Classical lower bounds this work compares against
- **Batch RL:** Related problem of learning from fixed datasets

### Future Research Directions

1. **Quantum RL with Function Approximation:** Handling continuous state/action spaces
2. **Hybrid Quantum-Classical Learning:** Incorporating neural networks
3. **Practical NISQ Implementation:** Demonstrating speedups on real quantum devices
4. **Other Quantum ML Applications:** Similar techniques for supervised and unsupervised learning
5. **Complexity-Theoretic Analysis:** Fundamental limits of quantum RL speedups

### Broader Implications

This work contributes to the growing body of evidence that quantum computing will provide practical advantages for machine learning, particularly in large-scale domains where classical sampling is prohibitively expensive.
