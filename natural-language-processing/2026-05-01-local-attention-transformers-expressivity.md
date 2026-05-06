# Characterizing the Expressivity of Local Attention in Transformers

**ArXiv ID:** [2605.00768](https://arxiv.org/abs/2605.00768)  
**Authors:** Jiaoda Li, Ryan Cotterell  
**Date:** May 1, 2026  
**Field:** Natural Language Processing / Machine Learning

---

## Executive Summary

This paper provides the first formal characterization of why local attention in transformers improves model quality despite reducing expressivity. Using formal language theory, the authors prove that global and local attention mechanisms are expressively complementary, and combining them yields richer computational expressivity than either alone.

## Problem Statement

Transformers rely on a global attention mechanism that allows each token to aggregate information from all preceding tokens. A common variant is **local attention**, which restricts each token to aggregating information from a bounded window of predecessors, reducing computational complexity from O(n²) to O(n).

Although local attention is typically justified for efficiency reasons, empirical evidence consistently shows that it also **improves model quality**—a phenomenon that has lacked a satisfactory theoretical explanation. This paper addresses this puzzle through the lens of formal language theory.

## Core Concepts & Theory

### Formal Language Recognition Framework

The authors analyze transformer expressivity through their ability to recognize formal languages, which serves as a standard lens in the formal study of neural models.

**Key Theoretical Results:**

1. **Global Attention Expressivity:** Fixed-precision transformers with global attention correspond to a fragment of **Linear Temporal Logic (LTL)** containing a single past operator (◇ₚ), which allows looking back into unbounded history.

2. **Local Attention Expressivity:** Adding local attention introduces a second temporal operator (◆ₚ for bounded past), which is not subsumed by global attention alone.

3. **Complementarity:** Global and local attention are **expressively complementary**:
   - Neither subsumes the other
   - Global attention can recognize languages that require unbounded lookback
   - Local attention can recognize certain sequential patterns more efficiently
   - Combining both yields the richest fragment with maximum computational power

### Mathematical Foundation

The paper formalizes transformers as:
- Token sequences processed left-to-right
- At each position, aggregation is restricted to a window or globally available context
- Fixed-point arithmetic limits expressivity (leading to correspondence with LTL fragments)

The formal analysis demonstrates:
- **Global-only**: Can express unlimited historical context access
- **Local-only**: Naturally expresses windowed contextual reasoning
- **Hybrid (Global + Local)**: Combines both advantages, enabling flexible context aggregation

## Main Ideas & Key Contributions

### Core Innovation

The key insight is that **local and global attention capture different computational patterns**:

1. **Unbounded Context Requirements:** Some linguistic phenomena require access to distant information (global attention excels here)
2. **Window-Based Patterns:** Other phenomena are better captured with bounded, recent context (local attention excels here)
3. **Flexibility:** Hybrid architectures can dynamically use appropriate attention modes

### Technical Contributions

1. **Formal Expressivity Analysis:** First formal characterization connecting attention patterns to recognizable language classes
2. **Empirical Validation:** Experiments confirm theoretical predictions on both synthetic language recognition tasks and natural language modeling
3. **Design Insights:** Provides theoretical justification for architectural choices in modern transformers

## Methodology & Implementation

### Experimental Setup

**Formal Language Tasks:**
- Dyck languages (balanced parentheses)
- Palindromes
- Copy languages
- Other formal language benchmarks

**Natural Language Modeling:**
- Standard language modeling benchmarks
- Evaluation on text prediction accuracy

### Key Results

**Formal Language Recognition:**
- Hybrid global-local transformers outperform global-only variants on tasks requiring both bounded and unbounded context
- Results align with theoretical predictions from LTL analysis

**Natural Language Modeling:**
- Hybrid architectures show consistent improvements over global-only attention
- Improvements are particularly pronounced on tasks requiring both short and long-range dependencies

### Performance Metrics

- Language recognition accuracy on formal language benchmarks
- Perplexity on natural language modeling tasks
- Computational efficiency (wall-clock time, memory usage)

## Practical Applications & Real-World Use Cases

### Language Modeling Applications

1. **Machine Translation:** Many translation phenomena benefit from local context (word order, agreement) combined with global context (discourse coherence)
2. **Code Generation:** Programming languages naturally exhibit both local scope rules and global function/module dependencies
3. **Summarization:** Requires local detail capture plus global narrative understanding

### Model Architecture Design

1. **Efficient Long-Context Models:** Use local attention for efficiency while maintaining expressivity through hybrid designs
2. **Interpretability:** Local attention windows provide interpretable attention patterns, useful for understanding model behavior
3. **Hardware Optimization:** Local attention reduces memory requirements, enabling deployment on resource-constrained devices

### Implementation Considerations

- **Window Size Selection:** Theory suggests window size should be chosen based on linguistic phenomena in the task
- **Computational Efficiency:** Hybrid approach reduces O(n²) global attention to O(n) for local windows while maintaining expressivity
- **Training Stability:** Local attention patterns provide more interpretable gradients and can improve training stability

## Insights & Implications

### Theoretical Advances

1. **Expressivity-Efficiency Tradeoff:** Formalizes the relationship between model capacity and computational resources
2. **Architectural Design Principles:** Provides theoretical justification for design choices in modern NLP systems
3. **Foundation for Future Work:** Opens door to systematic analysis of other architectural variants

### Implications for the Field

1. **Beyond Empirical Rules:** Moves beyond "local attention works because it's efficient" to explain why it works better
2. **Hybrid Design Philosophy:** Advocates for combining different attention mechanisms rather than choosing one
3. **Future Directions:** Suggests other architectural patterns could be analyzed similarly

### Limitations & Open Questions

1. **Hardness Bounds:** Paper characterizes expressivity but doesn't fully address learning efficiency
2. **Practical Window Sizes:** Theory doesn't precisely prescribe optimal window sizes for specific tasks
3. **Extension to Other Architectures:** Analysis focused on transformers; applicability to other architectures unclear

## Code & Resources

- **ArXiv Paper:** [https://arxiv.org/abs/2605.00768](https://arxiv.org/abs/2605.00768)
- **HTML Version:** [https://arxiv.org/html/2605.00768](https://arxiv.org/html/2605.00768)
- **Official Code:** Expected to be released by authors
- **Related Implementations:** [Local Attention PyTorch](https://github.com/lucidrains/local-attention)

### Requirements

- PyTorch or similar deep learning framework
- Formal language test datasets (provided in paper)
- Standard NLP evaluation tools

## Related Work & Context

### Prior Work on Attention Mechanisms

1. **Attention Is All You Need (Vaswani et al., 2017):** Introduced global attention in transformers
2. **Local Attention for Long Sequences:** Prior work used local attention for efficiency without formal analysis
3. **Formal Analysis of Neural Networks:** Previous work on expressivity of RNNs and other architectures

### Connection to Broader Research

1. **Formal Verification of ML:** Part of growing effort to formally verify neural network properties
2. **Interpretability Research:** Connects to work on understanding what neural networks compute
3. **Efficient Transformers:** Contributes to understanding of efficient transformer variants

### Potential Future Directions

1. **Extension to Other Mechanisms:** Analyze expressivity of multi-head attention, cross-attention
2. **Learning Bounds:** Characterize not just expressivity but also learning efficiency
3. **Dynamic Attention:** Study architectures that learn to switch between attention patterns
4. **Application to Other Domains:** Analyze computer vision transformers and other domains

---

## Summary

This paper provides crucial theoretical understanding of why local attention works in practice despite being computationally restricted. By proving that local and global attention are expressively complementary, it justifies hybrid approaches and opens new directions for transformer design. The work bridges the gap between empirical success and theoretical understanding, providing principled guidance for architectural choices in modern NLP systems.
