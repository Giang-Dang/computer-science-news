# The Periodic Table of LLM Reasoning: A Structured Survey of Reasoning Paradigms, Methods, and Failure Modes

**ArXiv ID:** 2606.11470  
**Submission Date:** June 9, 2026  
**Authors:** Avinash Anand, Mahisha Ramesh, Avni Mittal, Ashutosh Kumar, Erik Cambria, Zhengkui Wang, Timothy Liu, Aik Beng Ng, Simon See, Rajiv Ratn Shah

## Executive Summary

This comprehensive meta-survey organizes over 300 recent papers on LLM reasoning research into a unified taxonomy, identifying nine distinct reasoning paradigms and their characteristic failure modes. By synthesizing reasoning capabilities across diverse domains—from mathematical logic to visual understanding—the paper reveals recurring patterns in how reasoning emerges in language models and where systematic failures occur. This work provides researchers and practitioners with a structured map of the reasoning landscape, essential for advancing reliable AI systems.

## Problem Statement

While Large Language Models have achieved remarkable performance across natural language processing tasks, **reliable reasoning remains an open challenge**. Despite significant progress in structured inference, multi-step problem solving, and contextual understanding, LLM reasoning exhibits critical inconsistencies:

- **Sensitivity to prompting strategies**: Small changes in how questions are framed dramatically affect reasoning performance
- **Task design dependency**: Reasoning quality varies significantly based on task formulation
- **Model scale variability**: Reasoning capabilities don't scale predictably with model size
- **Domain generalization failure**: Patterns that work in one domain often fail in another

**Prior Research Gaps:** Previous work lacked a comprehensive, unified taxonomy for understanding diverse reasoning paradigms and their failure modes across different domains and model scales. This fragmentation made it difficult to identify universal principles of reasoning in LLMs.

## Core Concepts & Theory

The paper introduces a structured taxonomy organizing LLM reasoning research into nine primary paradigms:

### 1. **Chain-of-Thought (CoT) Reasoning**
- Decomposing complex problems into intermediate steps
- Sequential reasoning through explicit thought processes
- Foundation for most modern reasoning approaches

### 2. **Multi-Hop Reasoning**
- Connecting multiple pieces of information across knowledge graphs
- Reasoning through entity and relation chains
- Critical for complex question answering

### 3. **Mathematical Reasoning**
- Symbolic manipulation and calculation
- Logical proof generation
- Formal reasoning about mathematical objects

### 4. **Common Sense Reasoning**
- Background knowledge application
- Implicit understanding of physical/social world
- Reasoning about typical scenarios and exceptions

### 5. **Visual and Temporal Reasoning**
- Spatial understanding and relationships
- Temporal sequences and causality
- Multimodal integration of visual-linguistic information

### 6. **Code and Algorithmic Reasoning**
- Program synthesis and understanding
- Logical algorithm design
- Software engineering task reasoning

### 7. **Retrieval-Augmented Reasoning**
- Information retrieval integration
- Evidence-based reasoning
- Grounding reasoning in external knowledge

### 8. **Tool-Augmented and Agentic Reasoning**
- Interaction with external tools and APIs
- Multi-step planning with agents
- Environment interaction and feedback loops

### 9. **Reinforcement Learning-Based Reasoning**
- Learning from reward signals
- Policy optimization for reasoning tasks
- Integration of RL objectives with language models

## Main Ideas & Contributions

### Novel Taxonomy Framework
The paper's primary contribution is organizing the fragmented landscape of reasoning research into a coherent "Periodic Table" structure—analogous to chemistry's organization of elements by properties. This allows researchers to:
- Identify missing combinations or approaches
- Predict which techniques might transfer between domains
- Recognize patterns in reasoning failure modes

### Comprehensive Failure Mode Analysis
The meta-analysis identifies **five major categories of reasoning failures**:

1. **Reasoning Hallucinations**
   - Generating spurious reasoning traces that don't support conclusions
   - Fabricated intermediate steps
   - False justifications for correct answers

2. **Brittle Multi-Step Inference**
   - Reasoning that fails when chain length increases
   - Cascading errors through reasoning steps
   - Loss of information through reasoning process

3. **Weak Causal Abstraction**
   - Difficulty distinguishing correlation from causation
   - Inability to reason about counterfactuals
   - Weak understanding of causal mechanisms

4. **Poor Cross-Domain Generalization**
   - Reasoning patterns that fail when task domain changes
   - Limited transfer of reasoning capabilities
   - Domain-specific overfitting in reasoning strategies

5. **Sensitivity to Presentation and Prompting**
   - Reasoning quality dependent on task formulation
   - Vulnerability to adversarial reformulations
   - Brittle reasoning with respect to input variations

### Methodological Contributions
- **Meta-analytical approach**: Systematic analysis of 300+ papers identifying common patterns
- **Quantitative mapping**: Detailed enumeration of techniques and their success/failure rates
- **Cross-domain analysis**: Identification of universally applicable principles

## Methodology & Implementation

### Research Approach
- **Scope**: 300+ papers from arXiv, Semantic Scholar, Google Scholar, Papers with Code, and ACL Anthology
- **Analysis Period**: Focus on 2024-2026 advances in reasoning research
- **Classification Method**: Systematic taxonomy development based on:
  - Problem domain and task type
  - Technical approach and algorithm
  - Failure mode characterization
  - Evaluation metrics and benchmarks

### Key Dimensions Analyzed
- **Prompting methods and techniques**: In-context learning strategies, few-shot prompting, instruction tuning
- **Model architectures**: Specific architectural innovations for reasoning
- **Training objectives**: Loss functions and training procedures for reasoning
- **Reward modeling**: Design of reward signals for agentic reasoning
- **Evaluation benchmarks**: Comprehensive analysis of reasoning evaluation suites

### Failure Mode Detection
The paper develops systematic approaches to identify and categorize failure modes:
- Error pattern analysis across models and domains
- Sensitivity testing with adversarial inputs
- Cross-domain generalization evaluation
- Scaling behavior analysis

### Datasets and Benchmarks
- Analyzed reasoning evaluation datasets across multiple domains
- Covered benchmarks: GSM8K, MATH, HotpotQA, VQA, CommonsenseQA, and domain-specific suites
- Identified benchmark limitations and annotation quality issues

## Practical Applications & Use Cases

### For Research Teams
- **Navigation and Planning**: Use the taxonomy to identify underexplored reasoning combinations
- **Paper Selection**: Reference taxonomy when choosing related work for new papers
- **Method Evaluation**: Systematic comparison of approaches against taxonomy categories

### For Practitioners Building Reasoning Systems
- **Architecture Selection**: Choose reasoning paradigm(s) appropriate for target domain
- **Failure Prevention**: Anticipate failure modes common in selected reasoning paradigm
- **Hybrid Approaches**: Combine multiple paradigms to overcome individual limitations

### Domain-Specific Applications

**Mathematical Domains**
- Apply mathematical reasoning paradigm + retrieval-augmented techniques
- Implement step-by-step verification of symbolic manipulations
- Address: weak symbolic grounding, brittle multi-step inference

**Knowledge-Heavy Tasks**
- Integrate retrieval-augmented reasoning with tool use
- Combine multi-hop reasoning with external knowledge bases
- Address: poor cross-domain generalization, information gap

**Decision-Making Systems**
- Employ agentic reasoning with RL integration
- Use tool-augmented approaches for environment interaction
- Address: reasoning hallucinations through feedback loops

**Multimodal Understanding**
- Combine visual/temporal reasoning with other paradigms
- Ensure consistent reasoning across modalities
- Address: multimodal hallucinations, temporal reasoning brittleness

## Insights & Implications

### Broader Field Impact

1. **Unified Research Agenda**
   - First comprehensive map of the reasoning landscape
   - Enables systematic research across paradigms
   - Facilitates reproducibility and comparison

2. **Understanding Reasoning Emergence**
   - Reveals that no single paradigm dominates across all domains
   - Shows scaling effects vary dramatically by paradigm
   - Indicates hybrid approaches often superior to single paradigm

3. **Systematic Failure Analysis**
   - Failure modes are often paradigm-specific but sometimes universal
   - Some failures trace to fundamental model limitations (e.g., causal reasoning)
   - Others are engineering problems solvable through better training

4. **Implications for Model Development**
   - No single training objective creates universal reasoning
   - Multi-objective training approaches needed for diverse reasoning
   - Evaluation needs domain-specific and cross-domain metrics

### State-of-the-Art Advances
- Chain-of-thought prompting: Established foundation with known limitations
- Agentic reasoning: Emerging as most general paradigm with highest ceiling
- Retrieval-augmented approaches: Practical solution for knowledge-heavy tasks
- RL-based reasoning: Most robust to distribution shift but requires careful reward design

### Limitations and Open Questions

1. **Fundamental Capability Limits**
   - Uncertainty about whether LLMs can achieve true causal reasoning
   - Questions about limitations of next-token prediction for multi-step reasoning
   - Unclear if emergent reasoning is repeatable or model-specific

2. **Evaluation Challenges**
   - Reasoning evaluation often conflates understanding with success
   - Benchmark saturation in some domains
   - Need for more adversarial and out-of-distribution reasoning tests

3. **Generalization Mysteries**
   - Why some reasoning patterns transfer across domains while others don't
   - How to design reasoning systems with guaranteed generalization
   - Integration of multiple paradigms without negative interference

## Code & Resources

### Primary Source
- **Paper**: https://arxiv.org/abs/2606.11470
- **HTML Version**: https://arxiv.org/html/2606.11470

### Related Implementation Resources
Since this is a survey paper, code availability varies by cited papers. Key resources:

**Chain-of-Thought Implementations**
- Wei et al. CoT prompting: OpenAI API demonstrations and datasets

**Reasoning Benchmarks**
- GSM8K: https://github.com/openai/grade-school-math
- MATH: https://github.com/hendrycks/math
- HotpotQA: https://hotpotqa.github.io

**Agentic Reasoning Frameworks**
- Referenced frameworks: AutoGPT, LangChain, LlamaIndex
- RL implementations: StepPO, ARTIST, ML-Agent

### Quick Start for Practitioners
1. **Identify your reasoning task domain** → Find in the taxonomy
2. **Review paradigm-specific papers** → Cited in corresponding section
3. **Note common failure modes** → Anticipate challenges
4. **Select appropriate techniques** → Hybrid combination recommended
5. **Implement with relevant benchmarks** → Use domain-specific evaluation suite

### Compute Requirements
- Survey paper: No computational requirements for reading/understanding
- Implementing cited approaches: Varies from single GPU to distributed training
- Benchmarking: Recommend GPU access for evaluation and comparison

## Related Work & Context

### Builds On
- Chain-of-Thought prompting (Wei et al., 2022)
- In-context learning foundations (Brown et al., 2020)
- Reasoning evaluation benchmarks (2020-2024)
- Reinforcement learning for language models (2024-2026)

### Related Research Areas
- **Interpretability**: Understanding how reasoning processes work internally (mechanistic interpretability)
- **Robust Reasoning**: Adversarial robustness and out-of-distribution generalization
- **Multimodal Reasoning**: Extending paradigms to vision-language and embodied settings
- **Knowledge Integration**: Combining symbolic knowledge with neural reasoning
- **Agentic Systems**: Tool use and multi-step planning (detailed in separate paradigm)

### Future Research Directions

1. **Paradigm Composition**
   - How to effectively combine multiple reasoning paradigms
   - When to apply each paradigm component
   - Avoiding negative interference between paradigms

2. **Fundamental Limitations**
   - Characterizing what reasoning is fundamentally impossible for LLMs
   - Boundaries of next-token prediction for reasoning
   - Theoretical foundations of reasoning in neural networks

3. **Evaluation Evolution**
   - Better metrics that measure actual reasoning vs. pattern matching
   - Adversarial evaluation of reasoning robustness
   - Human-aligned evaluation of reasoning quality

4. **Scaling and Efficiency**
   - Which paradigms scale effectively to larger models
   - Efficient reasoning with resource-constrained models
   - Training-inference tradeoffs for reasoning

5. **Grounding and Verification**
   - Integration of formal verification with neural reasoning
   - Cross-modal grounding for visual/temporal reasoning
   - Automated verification of reasoning chains

## Citation

```
@article{anand2026periodic,
  title={The Periodic Table of LLM Reasoning: A Structured Survey of Reasoning Paradigms, Methods, and Failure Modes},
  authors={Anand, Avinash and Ramesh, Mahisha and Mittal, Avni and Kumar, Ashutosh and Cambria, Erik and Wang, Zhengkui and Liu, Timothy and Ng, Aik Beng and See, Simon and Shah, Rajiv Ratn},
  journal={arXiv preprint arXiv:2606.11470},
  year={2026}
}
```
