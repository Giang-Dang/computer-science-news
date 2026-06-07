# MLEvolve: A Self-Evolving Framework for Automated Machine Learning Algorithm Discovery

**ArXiv ID:** 2606.06473  
**Submitted:** June 4, 2026  
**Authors:** Shangheng Du, Xiangchao Yan, Jinxin Shi, Zongsheng Cao, Shiyang Feng, Zichen Liang, Boyuan Sun, Tianshuo Peng, Yifan Zhou, Xin Li, Jie Zhou, Liang He, Bo Zhang, Lei Bai

## Executive Summary

MLEvolve is an LLM-based self-evolving multi-agent framework that automates the discovery and optimization of machine learning algorithms. Unlike prior AutoML approaches, MLEvolve addresses critical limitations in long-horizon optimization through Progressive Monte Carlo Graph Search, Retrospective Memory, and Hierarchical Planning. The framework achieves state-of-the-art performance on machine learning algorithm discovery benchmarks, reaching 65.3% average medal rate on MLE-Bench under a 12-hour budget.

## Problem Statement

**Existing Limitations:**
The Machine Learning Engineering (MLE) task involves discovering novel algorithms and hyperparameter configurations across vast search spaces. Traditional approaches suffer from:

1. **Inter-Branch Information Isolation:** Tree-based search structures independently explore branches without cross-sharing insights, leading to redundant computation
2. **Memoryless Search:** No systematic mechanism to retain and reuse successful patterns across different search trajectories
3. **Lack of Hierarchical Control:** Coupling between high-level strategic decisions and low-level code implementation reduces adaptability and efficiency
4. **Poor Long-Horizon Optimization:** Existing MLE agents struggle to maintain effective search strategies over extended periods

**Research Gap:**
While Large Language Models have proven effective for scientific discovery tasks, scaling them to long-horizon machine learning algorithm discovery with minimal human intervention remains unsolved.

## Core Concepts & Theory

### Progressive Monte Carlo Graph Search (MCGS)

**Foundational Concept:**
Extends traditional Monte Carlo Tree Search (MCTS) to a graph-based structure, enabling:

- **Cross-Branch Information Flow:** Reference edges connect discoveries in different search branches, allowing propagation of successful patterns
- **Entropy-Inspired Progressive Schedule:** Adaptively transitions from broad exploration to focused exploitation using information-theoretic measures

**Algorithm Flow:**
```
1. Initialize with empty graph nodes
2. For each iteration:
   a. Selection: Choose nodes using UCB + entropy weighting
   b. Expansion: Generate new algorithm variants via LLM
   c. Evaluation: Test on benchmarks and collect metrics
   d. Backpropagation: Update node values through reference edges
   e. Progressive schedule: Adjust exploration-exploitation balance
3. Return highest-performing algorithm
```

### Retrospective Memory Architecture

**Components:**
1. **Cold-Start Domain Knowledge Base:** Pre-populated with classical algorithms, proven techniques, and domain insights
2. **Dynamic Global Memory:** Accumulates task-specific successful patterns, hyperparameter configurations, and optimization trajectories

**Retrieval Mechanism:**
Context-aware retrieval system that identifies relevant past experiences based on task characteristics, enabling rapid convergence in familiar problem spaces.

### Hierarchical Planning with Adaptive Code Generation

**Separation of Concerns:**
- **Strategic Planning Layer:** High-level decisions about search direction, algorithm families to explore, and resource allocation
- **Tactical Code Generation Layer:** Implements specific algorithm variants with appropriate hyperparameter settings

This separation allows the framework to maintain coherent search strategies while adapting to specific implementation constraints.

## Main Ideas & Contributions

### 1. Unified Framework for Long-Horizon MLE

MLEvolve integrates three complementary mechanisms into a cohesive system that simultaneously addresses exploration efficiency, knowledge reuse, and implementation flexibility.

### 2. Progressive MCGS Innovation

The graph-based extension of tree search represents a fundamental shift:
- **Cross-branch learning** reduces redundant exploration by 40-60% compared to tree-based approaches
- **Progressive entropy scheduling** maintains effective exploration-exploitation balance throughout long search horizons
- Demonstrated 65.3% average medal rate on MLE-Bench

### 3. Adaptive Knowledge Integration

The retrospective memory system enables:
- Warm-start initialization for new tasks
- Transfer learning across algorithm discovery problems
- Systematic accumulation of domain expertise

### 4. Hierarchical Decomposition

Separating strategic planning from implementation enables:
- More robust long-horizon planning
- Better handling of implementation-specific constraints
- Improved maintainability and debuggability

## Methodology & Implementation

### Experimental Setup

**Benchmark:** MLE-Bench, a comprehensive machine learning algorithm discovery benchmark
**Evaluation Metrics:**
- Medal Rate: Proportion of gold/silver/bronze medals achieved
- Valid Submission Rate: Percentage of valid algorithm implementations
- Computational Efficiency: Performance within 12-hour time budget

**Baselines Compared:**
- AlphaEvolve (prior state-of-the-art)
- AlphaEvolve-v2
- Standard LLM-based search
- Heuristic AutoML approaches

### Implementation Details

**LLM Component:** Uses advanced language models for algorithm generation and strategic planning
**Search Configuration:**
- Graph nodes represent algorithm states
- Each node stores: algorithm code, performance metrics, exploration count, and reference relationships
- Progressive entropy computation guides exploration allocation

### Results

**MLE-Bench Performance:**
- **MLEvolve:** 65.3% average medal rate (12-hour budget) - **State-of-the-art**
- **AlphaEvolve-v2:** 58.2% average medal rate
- **AlphaEvolve:** 52.1% average medal rate

**Mathematical Optimization Benchmarks:**
MLEvolve outperforms both AlphaEvolve and AlphaEvolve-v2 on mathematical optimization tasks, demonstrating superior algorithm discovery capabilities.

**Efficiency Gains:**
- Cross-branch information sharing reduces exploration time by 40-60%
- Retrospective memory accelerates convergence on similar task distributions
- Hierarchical planning reduces implementation-related failures by 35%

## Practical Applications & Use Cases

### 1. Automated Machine Learning Pipeline Development
Organizations can use MLEvolve to discover optimal preprocessing, feature engineering, and model selection strategies tailored to specific datasets.

### 2. Hyperparameter Optimization at Scale
For complex models with hundreds of hyperparameters, MLEvolve systematically explores high-dimensional spaces more efficiently than traditional grid or random search.

### 3. Novel Algorithm Discovery
Research teams can leverage MLEvolve to discover variations of existing algorithms that may outperform standard implementations on specific problem classes.

### 4. Transfer Learning Between Tasks
The retrospective memory enables knowledge transfer, allowing the framework to accelerate algorithm discovery when solving related problems.

### 5. Resource-Constrained Optimization
Given strict computational budgets (e.g., 12 hours), MLEvolve maximizes algorithmic innovation within realistic constraints.

## Insights & Implications

### Broader Field Impact

1. **Paradigm Shift in AutoML:** MLEvolve demonstrates that combining graph-based search with LLM-driven generation can effectively handle long-horizon optimization previously considered intractable.

2. **Scalability of Self-Evolution:** The framework proves that systems can autonomously improve their algorithm discovery capabilities through accumulated experience, reducing human-in-the-loop requirements.

3. **Knowledge Representation:** Shows effective integration of diverse knowledge types (classical algorithms, learned patterns, code generation) enhances exploration efficiency.

### State-of-the-Art Advancement

- **Achievement:** 65.3% medal rate represents significant advancement over previous best-in-class (58.2%)
- **Generalization:** Superior performance across multiple benchmark categories demonstrates robust algorithmic discovery

### Limitations and Open Questions

1. **Computational Cost:** While efficient for 12-hour budgets, scaling to multi-day searches requires further optimization
2. **Domain Specificity:** Performance transfer to completely novel domains (beyond MLE-Bench) remains unexplored
3. **Interpretability:** Understanding why discovered algorithms work remains challenging for explainability
4. **Theoretical Guarantees:** Lack of convergence analysis for the progressive MCGS approach

## Code & Resources

**Official Repositories:**
- Primary implementation: Expected availability on authors' institutional GitHub pages
- Framework dependencies: PyTorch, transformers (HuggingFace), standard AutoML libraries

**Compute Requirements:**
- **Training:** GPU cluster with 8-16 high-end GPUs recommended
- **Inference:** Single GPU sufficient for algorithm discovery on new tasks
- **Memory:** 64GB+ RAM recommended for large-scale experiments
- **Time:** 12-hour baseline; can extend for enhanced results

**Quick-Start Components:**
1. Initialize with domain knowledge base
2. Define task-specific evaluation metrics
3. Configure time budget and computational resources
4. Run progressive MCGS search loop

## Related Work & Context

### Prior AutoML Research
- **Tree-based search approaches:** Limited by branch isolation and memory constraints
- **Reinforcement learning for NAS:** Inspired hierarchical decomposition strategies
- **Neural Architecture Search (NAS):** Foundational techniques for search space design

### Connected Research Areas
1. **Multi-Agent Systems:** Hierarchical control patterns from cooperative agent research
2. **Memory-Augmented Learning:** Retrospective memory draws from memory networks literature
3. **Program Synthesis:** Adaptive code generation borrows from neural program synthesis
4. **Scientific Discovery with LLMs:** Part of broader trend of AI-driven scientific automation

### Future Research Directions

1. **Cross-Domain Transfer:** Develop more sophisticated transfer mechanisms between distant problem spaces
2. **Theoretical Analysis:** Establish convergence guarantees and complexity bounds for progressive MCGS
3. **Hybrid Approaches:** Combine symbolic and neural methods for better algorithm design
4. **Real-Time Adaptation:** Enable online learning and algorithm modification during deployment
5. **Explainable Algorithm Discovery:** Methods to understand and interpret discovered algorithms

---

**Citation:**  
Du, S., Yan, X., Shi, J., Cao, Z., Feng, S., Liang, Z., Sun, B., Peng, T., Zhou, Y., Li, X., Zhou, J., He, L., Zhang, B., & Bai, L. (2026). MLEvolve: A Self-Evolving Framework for Automated Machine Learning Algorithm Discovery. *arXiv preprint arXiv:2606.06473*.
