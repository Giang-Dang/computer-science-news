# Harness-1: Reinforcement Learning for Search Agents with State-Externalizing Harnesses

## Executive Summary

Harness-1 introduces a novel architecture for training search agents that externalizes state management to the environment rather than forcing the policy to handle both semantic decisions and routine bookkeeping. This 20B parameter model demonstrates that separating state concerns from decision-making significantly improves search agent training efficiency and reliability through reinforcement learning. The key innovation addresses a fundamental inefficiency in how RL agents are typically formulated—reducing wasted cognitive capacity on environment state tracking.

## Problem Statement

Traditional search agent architectures formulate policies over growing transcripts, where the model must simultaneously:
- Make semantic search decisions
- Remember previous observations
- Track evidence relevance and validity
- Monitor constraint satisfaction
- Verify claims against evidence

This conflates two distinct responsibilities: (1) high-level reasoning about what to search for, and (2) low-level state management that could be reliably maintained by the environment. This architecture forces reinforcement learning to optimize both aspects, introducing unnecessary complexity and reducing training efficiency.

The core challenge is that search agents need to maintain extensive working memory—candidate pools, curated evidence sets, evidence links, and verification records—while simultaneously learning when and how to search. Mixing these concerns in the policy makes it harder for the RL algorithm to focus on the core semantic task.

## Core Concepts & Theory

### Traditional Transcript-Based Policy

```
State: [query, search_history, evidence_found, claims_made, ...]
Policy: (state) → Action
Actions: search(query), verify(claim), claim(statement), ...
```

The policy must track everything in the transcript, making decisions based on a growing context that includes both meaningful evidence and administrative details.

### Harness-1 Architecture: State Externalization

The breakthrough approach moves state management to a persistent environment harness:

**Environment-Maintained State:**
- **Candidate Pool**: Maintains potential search targets
- **Importance-Tagged Curated Set**: Tracks high-value evidence with relevance scores
- **Compact Evidence Links**: Stores connections between claims and supporting evidence
- **Verification Records**: Maintains history of what has been checked

**Policy Input:**
The policy operates over a simplified interface that exposes only decision-relevant information, not the full administrative state.

**Key Insight**: By moving routine state management to the harness, the RL algorithm can focus entirely on learning high-quality semantic decisions about when to search, which evidence to prioritize, and how to reason about complex queries.

## Main Ideas & Contributions

### 1. **State-Externalizing Architecture**
The primary contribution is demonstrating that formulating search agents with environment-side working memory significantly improves both training efficiency and generalization. The harness maintains five categories of state that the policy queries but doesn't need to manage.

### 2. **Policy-Harness Interaction Protocol**
The interface between policy and harness is carefully designed:
- Policy observes: decision-relevant facts, current goal, available actions
- Policy decides: next action (search direction, evidence selection, or reasoning step)
- Harness updates: internal state, handles bookkeeping, provides feedback

### 3. **RL Training in Structured Environment**
By constraining the policy's action space and simplifying its input representation, RL can more effectively learn:
- When additional search is valuable vs. when to reason with current evidence
- Which evidence threads to follow
- How to consolidate findings into coherent answers

### 4. **Verification-Ready Design**
The externalized structure makes verification and interpretability easier:
- Exact evidence chains are explicit in the harness state
- Claims can be automatically traced to supporting evidence
- Decision history is cleanly separated from outcome history

## Methodology & Implementation

### Architecture Details

**Model Size**: 20B parameters
**Training Approach**: Reinforcement learning with reward signals from search quality

**Harness Components**:

1. **Candidate Pool Manager**
   - Maintains unexplored search directions
   - Ranks candidates by relevance and uncertainty
   - Feeds to policy for selection decisions

2. **Evidence Curator**
   - Stores found evidence with importance tags
   - Deduplicates across multiple search attempts
   - Exposes high-value evidence to policy

3. **Link Tracker**
   - Maintains evidence-to-claim mappings
   - Tracks evidence necessity and sufficiency
   - Enables transparent claim justification

4. **Verification Engine**
   - Records verification attempts
   - Tracks claim validity
   - Prevents redundant verification

### Training Setup

**Datasets**: Search tasks requiring multi-step reasoning with external verification

**Reward Signal**: 
- Positive reward for finding relevant evidence
- Bonus for efficient search (fewer steps)
- Verification signal for claim correctness
- Penalties for redundant actions

**RL Algorithm**: Policy gradient methods adapted for structured action spaces

### Experimental Results

[Exact figures unavailable — see full paper for comprehensive evaluation metrics]

The paper evaluates Harness-1 on complex search tasks, demonstrating:
- Improved sample efficiency compared to transcript-based baselines
- Better generalization to novel queries
- More interpretable decision-making
- Reduced hallucination in complex reasoning chains

## Practical Applications & Use Cases

### 1. **Question Answering Systems**
Multi-step reasoning over large knowledge bases where agents must decide which information to retrieve and how to verify claims.

### 2. **Information Retrieval**
Search scenarios requiring iterative refinement, where an agent must explore different search directions and consolidate findings.

### 3. **Fact-Checking and Verification**
Agents that need to find supporting evidence for claims and track which facts have been verified, with explicit traceability.

### 4. **Technical Support and Documentation Search**
Finding relevant documentation across multiple sources while maintaining clear evidence trails for recommendations.

### 5. **Research and Literature Review**
Agents performing comprehensive literature searches, tracking which papers have been reviewed and how they relate to research questions.

## Insights & Implications

### Architectural Principles for Agent Design
Harness-1 demonstrates that well-designed agent architectures should separate concerns:
- **Semantic layer** (policy): What decisions to make
- **Administrative layer** (harness): How to track state
- **Verification layer** (verification engine): How to validate claims

This separation enables cleaner RL training and more interpretable agent behavior.

### State-of-the-Art Advancement
The work advances RL for language agents by:
- Showing that policy formulation matters as much as the model size
- Demonstrating that auxiliary structure can improve sample efficiency
- Providing a blueprint for building interpretable, verifiable search agents

### Limitations and Open Questions

1. **Harness Complexity**: Designing the harness for new domains requires domain knowledge
2. **Generalization**: How well does the approach transfer to completely novel task types?
3. **Scalability**: Performance with even larger policy models (50B+) remains unexplored
4. **Competing Objectives**: Balancing efficiency (fewer searches) with thoroughness (complete coverage)

## Code & Resources

**Official Repository**: Available on arXiv paper page (2606.02373)

**Dependencies**:
- Standard RL frameworks (PyTorch, JAX, or similar)
- Search environment simulation
- Reward model training pipeline

**Key Compute Requirements**:
- Training: 8-16 A100/H100 GPUs for extended training runs
- Inference: Single GPU sufficient for policy execution

## Related Work & Context

### Prior Search Agent Work
- Traditional transcript-based RL agents (baseline comparison)
- Monte Carlo Tree Search approaches for complex reasoning
- Tool-using language models (Agent frameworks)

### Relevant Foundation Papers
- Policy gradient methods for discrete action spaces
- Attention mechanisms in transformer models
- Multi-step reasoning in large language models

### Future Research Directions

1. **Adaptive Harness Design**: Learning the harness structure from data
2. **Transfer Learning**: Transferring learned policies across harness designs
3. **Multi-Agent Search**: Multiple agents working with shared harness state
4. **Hierarchical Reasoning**: Nested harnesses for multi-level reasoning tasks

**Potential Extensions**:
- Application to collaborative filtering and recommendation systems
- Integration with retrieval-augmented generation systems
- Combination with other RL approaches (model-based RL, inverse RL)
- Scaling to trillion-parameter models with distributed harnesses

## References

**Paper**: [2606.02373] Harness-1: Reinforcement Learning for Search Agents with State-Externalizing Harnesses

**ArXiv**: https://arxiv.org/abs/2606.02373
