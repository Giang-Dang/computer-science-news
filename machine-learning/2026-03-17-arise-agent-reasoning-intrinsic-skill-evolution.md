# ARISE: Agent Reasoning with Intrinsic Skill Evolution in Hierarchical Reinforcement Learning

## Executive Summary

ARISE introduces a hierarchical reinforcement learning framework that significantly improves mathematical reasoning in large language models by maintaining a dynamic skill library that evolves during training. Unlike traditional approaches that treat each problem in isolation, ARISE leverages reusable reasoning strategies accumulated through training, achieving consistent improvements across competition mathematics and diverse benchmarks with notable gains on out-of-distribution tasks.

## Problem Statement

Current reinforcement learning approaches for improving LLM reasoning have several limitations:

- **Isolated Problem Solving**: Each problem is treated independently without leveraging patterns and strategies from previous solutions
- **No Strategy Reuse**: Successful reasoning patterns are not captured or reused across problems
- **Limited Skill Accumulation**: Models don't maintain or build upon previously learned reasoning approaches
- **Scalability Issues**: Approaches don't scale efficiently to handle diverse problem types (competition math, olympiad problems, etc.)

Traditional RL methods like GRPO optimize on individual problems but miss opportunities to build cumulative reasoning knowledge. ARISE addresses these limitations through hierarchical skill learning.

## Core Concepts & Theory

### Hierarchical Policy Architecture

ARISE uses a two-level hierarchical policy structure:

1. **Skills Manager (High-Level)**: 
   - Maintains a dynamic library of reusable reasoning skills
   - Decides which skills to apply to current problems
   - Learns skill selection through experience

2. **Worker (Low-Level)**:
   - Generates actual reasoning traces and solutions
   - Operates conditioned on selected skills
   - Can fall back to independent reasoning if needed

### Skill Library Mechanism

The skill library evolves through:
- **Skill Generation**: Summarizes successful solution traces into reusable skill descriptions
- **Skill Storage**: Maintains a growing collection of proven reasoning patterns
- **Skill Selection**: Retrieves relevant skills based on problem context
- **Skill Refinement**: Library quality improves through two-phase training

### Two-Phase Training Pipeline

**Phase I: Warm-up with Standard GRPO**
- Trains without explicit skill management
- Skill library silently populated from successful traces
- Builds foundational reasoning capability
- Switches from policy gradient to full hierarchical training

**Phase II: Hierarchical Joint Training**
- Manager actively selects skills for each problem
- Reward switches from binary to three-level (incorrect/partial/correct)
- Policy optimization and skill evolution proceed jointly
- Library continuously enriched with new effective strategies

### Hierarchical Reward Design

The reward structure in Phase II distinguishes:
1. **Incorrect solutions**: 0 reward
2. **Partial/intermediate progress**: Intermediate reward
3. **Correct solutions**: Full reward

This three-level reward allows fine-grained learning of skill applicability.

## Main Ideas & Contributions

### 1. **Skill Evolution Framework**
- Novel approach to capture and reuse successful reasoning strategies
- Automatic skill summarization from solution traces
- Policy-driven skill selection mechanism
- Tiered skill library with quality metrics

### 2. **Hierarchical Architecture**
- Shared policy for both skill management and response generation
- Clear separation between strategic (manager) and tactical (worker) levels
- Flexible fallback mechanisms for novel problems

### 3. **Comprehensive Experimental Validation**
- Tested on competition mathematics (AMC, AIME)
- Evaluated on diverse problem sets (Omni-MATH with 4,428 Olympiad problems)
- Demonstrated out-of-distribution generalization
- Consistent improvements over GRPO baselines

### 4. **Practical Scalability**
- Works with multiple base models
- Scales across problem domains
- Demonstrates particular strength on unseen problem types

## Methodology & Implementation

### Datasets and Experimental Setup

**Base Models Tested**:
- Two different LLM scales/architectures
- State-of-the-art models fine-tuned for reasoning

**Benchmark Suite**:
1. **In-Distribution Competition Benchmarks**:
   - AMC 2023 (American Mathematics Competition)
   - AIME 2024 (American Invitational Mathematics Examination)
   - AIME 2025
   - Same problem type as training but no temporal overlap

2. **Out-of-Distribution Benchmark (Omni-MATH)**:
   - 4,428 Olympiad-level problems
   - Coverage: Algebra, Number Theory, Combinatorics, Geometry
   - Represents more challenging unseen problem types
   - Tests true generalization capability

### Training Procedure

1. **Data Preparation**: Collect solution traces with correctness labels
2. **Phase I Warm-up**: Train with standard GRPO on base models for N steps
3. **Skill Mining**: Extract and summarize successful solution traces
4. **Phase II Joint Training**: Train with active skill selection and hierarchical rewards
5. **Evaluation**: Test on in-distribution and out-of-distribution benchmarks

### Evaluation Metrics

- **Accuracy**: Percentage of problems solved correctly
- **Skill Library Quality**: Relevance and effectiveness of extracted skills
- **In-Distribution Performance**: Results on problem types seen during training
- **Out-of-Distribution Performance**: Results on unseen problem types (key metric for true advancement)
- **Skill Selection Frequency**: Which skills are most useful

### Results and Comparisons

**Key Findings**:
- ARISE consistently outperforms GRPO-family algorithms
- ARISE outperforms memory-augmented baselines
- **Particularly notable gains on out-of-distribution tasks** (OmniMATH)
- Results hold across both tested base models

**Benchmark Performance**:
[Exact figure numbers unavailable — see full paper for detailed results]
- In-distribution: Improvements on AMC 2023, AIME 2024/2025
- Out-of-distribution: Significant gains on Omni-MATH across all math domains

**Computational Efficiency**:
- Two-phase training shows faster convergence than continuous hierarchical training
- Phase I provides strong initialization for Phase II

## Practical Applications & Use Cases

### Academic and Educational
1. **Mathematical Problem Solving**: Tutoring systems that improve reasoning
2. **Competition Math Training**: Helping students prepare for AMC/AIME
3. **Mathematics Education**: Explaining multiple solution approaches via skill library
4. **Advanced Problem Research**: Supporting mathematicians in novel problem solving

### Professional Applications
1. **Scientific Research**: Assisting with mathematical modeling and calculations
2. **Engineering Design**: Supporting calculations in engineering optimization
3. **Financial Modeling**: Complex quantitative finance problem solving
4. **Theoretical Computer Science**: Algorithm analysis and proof assistance

### Implementation Feasibility
- Requires training on mathematical problem datasets
- Knowledge base building is gradual during training
- Can work with existing LLM architectures with minimal modifications
- Skill library can be domain-specific or general

## Insights & Implications

### Broader Field Impact
- **Skill Reuse is Effective**: Mathematical reasoning benefits significantly from accumulated strategies
- **Hierarchical Learning is Natural**: Two-level hierarchy mirrors human problem-solving (planning then execution)
- **Out-of-Distribution Generalization is Achievable**: Skills learned on one problem type transfer to others
- **RL Benefits from Structured Knowledge**: Explicit skill representation helps RL optimization

### State-of-the-Art Advancement
- Shows practical path to improving mathematical reasoning beyond base model capabilities
- Demonstrates superiority over simpler memory-augmented approaches
- Achieves human-competitive reasoning on olympiad-level problems
- Establishes skill evolution as promising research direction

### Limitations and Open Questions
- Reliance on correctness verification (complete-solution problems vs. partial credit)
- Skill library size and management complexity at scale
- Generalization to domains beyond mathematics
- Transferability of skills across problem domains
- Computational overhead of skill management

## Code & Resources

### Official Repositories
- Code availability: [Exact repository URL unavailable — see arXiv abstract]
- Model checkpoints: Available through institutional repositories or upon request

### Dependencies and Requirements
- Base models: State-of-the-art reasoning-capable LLMs
- Training framework: Standard PyTorch/Transformers
- Math verification: Tool for checking solution correctness (e.g., symbolic math evaluators)
- Compute requirements: [Estimated] 8-80 GPUs for full training pipeline depending on model scale

### Quick-Start Guide
1. Prepare mathematical problem datasets (AMC, AIME, custom)
2. Implement base LLM fine-tuning with GRPO (Phase I)
3. Build skill extraction and summarization module
4. Implement hierarchical manager/worker architecture
5. Train Phase II with joint skill evolution
6. Evaluate on test benchmarks including out-of-distribution sets
7. Analyze skill library composition and selection patterns

## Related Work & Context

### Related Recent Papers
- **GRPO**: Base RL method that ARISE builds upon
- **In-context Learning for Math**: Related approaches to improving mathematical reasoning
- **Hierarchical RL**: Foundational work in multi-level policy learning
- **Skill Learning in RL**: Related approaches to skill discovery and reuse
- **Memory-Augmented Models**: Compared baseline approaches

### Prior Work Foundations
- Reinforcement learning with verifiable rewards
- Chain-of-thought prompting and step-by-step reasoning
- Hierarchical reinforcement learning theory
- Mathematical reasoning benchmarks (MATH, GSM8K)
- Process supervision for reasoning tasks

### Possible Future Research Directions
- Extending to non-mathematical domains (writing, coding, logic puzzles)
- Cross-domain skill transfer (math to physics to engineering)
- Continual learning with skill library evolution
- Multi-agent skill sharing and collaboration
- Skill explanation and interpretability
- Combination with retrieval-augmented approaches
- Scaling to larger problem sets and skill libraries

## Citation & Metadata
- **Title**: ARISE: Agent Reasoning with Intrinsic Skill Evolution in Hierarchical Reinforcement Learning
- **Authors**: Yu Li, Rui Miao, Zhengling Qi, Tian Lan
- **Affiliations**: George Washington University, University of Texas at Dallas
- **arXiv ID**: 2603.16060
- **Submission Date**: March 17, 2026
- **Field**: Reinforcement Learning, Mathematical Reasoning, Hierarchical Learning

---
*Documentation generated for computer-science-news research tracking. For the most current information and implementation details, please refer to the official arXiv paper.*
