# EEVEE: Towards Test-time Prompt Learning in the Real World for Self-Improving Agents

**arXiv ID:** 2606.11182  
**Submitted:** June 9, 2026  
**Authors:** Weixian Xu, Shilong Liu, Mengdi Wang

## Executive Summary

EEVEE is the first multi-dataset test-time prompt learning framework that enables LLM agents to continuously adapt prompts to new, unseen task streams. Unlike previous methods designed for static, single-dataset scenarios, EEVEE enables self-improving agents to handle heterogeneous data distributions and task variations in real-world deployments. Through a router-prompt co-evolution strategy that clusters inputs and optimizes prompt assignments, EEVEE improves robustness across multiple datasets while maintaining computational efficiency, addressing a critical gap between research benchmarks and production deployment requirements.

## Problem Statement

Current LLM agent deployment faces a fundamental mismatch:

1. **Research-to-Production Gap**: Existing test-time prompt learning methods assume single-dataset, stationary distributions. Real-world applications encounter heterogeneous task streams from multiple domains with different distributions.
2. **Static Prompt Limitations**: Fixed prompts designed for one dataset often underperform on others, but retraining for each dataset is computationally expensive.
3. **Scalability Challenge**: As agents face more diverse tasks, prompt engineering becomes a bottleneck requiring manual intervention for each new domain.

The core research question: How can agents continuously learn and adapt their prompts to handle diverse task distributions without retraining entire models?

## Core Concepts & Theory

### Multi-Task Prompt Learning Problem

Unlike single-task prompt optimization, multi-dataset learning requires:

- **Task Cluster Recognition**: Identifying which inputs belong to which task distribution
- **Prompt-Task Alignment**: Ensuring each prompt is optimized for its corresponding task cluster
- **Inter-Prompt Consistency**: Maintaining coherent prompt evolution across clusters

### Router Architecture

EEVEE's router component:

- **Input Clustering**: Partitions incoming inputs into clusters representing different task distributions
- **Soft Assignment**: Uses probabilistic assignments allowing inputs at cluster boundaries to use multiple prompts
- **Dynamic Routing**: Adjusts cluster assignments as new data arrives

### Router-Prompt Co-Evolution

The key algorithmic innovation addresses the mutual dependency problem:

1. **Phase 1 - Router Learning**: With fixed prompts, learn which inputs belong to which clusters
2. **Phase 2 - Prompt Learning**: With fixed clusters, optimize prompts for each cluster
3. **Iteration**: Repeat phases to handle mutual dependencies

This alternating optimization solves the chicken-and-egg problem where good prompts require good clustering and vice versa.

### Gradient-Based Prompt Optimization

For each cluster:
- Prompts are treated as learnable parameters (or discrete selections from a candidate pool)
- Loss function measures task accuracy on the cluster's inputs
- Optimization can be done via gradient descent (continuous prompts) or reinforcement learning (discrete prompt selection)

## Main Ideas & Contributions

### 1. First Multi-Dataset Test-Time Prompt Learning

Key innovation: Extends test-time learning from single-dataset to multi-dataset scenarios:
- Previous methods: "Given data from Task A, learn the best prompt for Task A"
- EEVEE: "Given streaming data from Tasks A, B, C, ..., learn to route each input and optimize prompts for each"

### 2. Router-Prompt Co-Evolution Algorithm

Rather than treating routing and prompt learning sequentially:
- Designs interleaved learning phases that optimize both simultaneously
- Proven to converge to better local optima than sequential approaches
- Computationally efficient relative to joint optimization

### 3. Online Learning Capability

EEVEE handles continuously arriving data:
- **Incremental Cluster Update**: New inputs can trigger cluster boundary adjustments
- **Prompt Refinement**: Accumulated data within clusters improves prompt quality
- **Cold-Start**: Handles initial arrivals when cluster statistics are uncertain

## Methodology & Implementation

### Experimental Setup

**Datasets**: Evaluated on heterogeneous task streams:
- Multiple NLP datasets with different characteristics (question answering, classification, generation)
- Vision-language datasets with domain shifts
- Mixed task types: classification, generation, reasoning

**Baseline Comparisons**:
1. Single fixed prompt across all tasks
2. Single adaptive prompt (learns one prompt for all data)
3. Oracle multi-prompt (assumes known cluster assignments)
4. Sequential learning (learn clusters first, then prompts)
5. Joint optimization (simultaneous router-prompt learning without co-evolution)

### Evaluation Metrics

1. **Accuracy/Performance**: Task-specific metrics (F1, BLEU, ROUGE, etc.)
2. **Robustness**: Consistency across tasks with different characteristics
3. **Efficiency**: Computational cost of router and prompt learning
4. **Generalization**: How well learned prompts transfer to held-out task variations
5. **Convergence Speed**: How quickly the router-prompt system adapts to new data

### Key Results

- **Accuracy Improvement**: [Exact figures unavailable — see full paper for task-specific metrics]
- **Robustness Gains**: Maintains single-benchmark performance while improving multi-dataset robustness
- **Efficiency**: Router-prompt co-evolution reduces iterations needed for convergence vs. naive alternating optimization
- **Real-World Feasibility**: Computational cost compatible with deployment on resource-constrained devices

## Practical Applications & Use Cases

### 1. Multi-Domain LLM Agents
- Customer service agents handling tickets from multiple departments
- Autonomous systems managing diverse task categories
- Agents adapting to new domains without retraining

### 2. Cross-Lingual Services
- Single model serving users in multiple languages
- Router identifies language/cultural context
- Prompts optimized for cultural specificity and linguistic variation

### 3. Adaptive Question-Answering Systems
- Question types: factual QA, reasoning, open-ended discussion
- Router classifies question type
- Each type uses task-specific prompt
- System improves as more questions arrive

### 4. Medical AI Systems
- Single model serves multiple hospital departments
- Router identifies department and patient population
- Prompts calibrated for department-specific terminology and protocols
- Continuous improvement as more cases accumulate

### 5. Autonomous Vehicles
- Router identifies scenario type (highway, urban, adverse weather)
- Prompts optimized for decision-making in each scenario
- System adapts as new edge cases encountered

## Insights & Implications

### Broader Field Impact

This work demonstrates:

- **Stateful Agents**: Agents that maintain and refine internal models (prompts, routing policies) over time are more practical
- **Continuous Learning**: Production systems need online adaptation beyond static pre-training
- **Specialization Through Routing**: Generic models can achieve specialized performance through learned routing and prompt selection

### State-of-the-Art Advancement

- Bridges gap between research (controlled settings) and production (diverse distributions)
- Extends test-time training to realistic multi-task scenarios
- Shows that prompt learning is viable for deployment despite previous scalability concerns

### Limitations & Open Questions

1. **Cluster Interpretability**: Are learned clusters semantically meaningful or statistical artifacts?
2. **Scaling Cluster Numbers**: How does performance degrade as number of task types increases?
3. **Prompt Transferability**: Can prompts learned on one population transfer to related tasks?
4. **Theoretical Guarantees**: What convergence properties does router-prompt co-evolution have?
5. **Prompt Interpretability**: How to understand what different prompts are learning?

## Code & Resources

### Implementation Details
- **Base Model**: Compatible with various LLM architectures (GPT-3, Claude, open-source models)
- **Router**: Learnable routing network (neural network or attention-based)
- **Prompt Learning**: Gradient-based optimization or discrete selection via RL
- **Infrastructure**: Supports streaming data processing and online updates

### Compute Requirements
- Training: Moderate GPU requirements (varies by model size and dataset scale)
- Inference: Minimal overhead beyond base model inference
- Scaling: Routable to distributed inference systems

### Quick-Start Scenario

```
1. Initialize base LLM with generic prompt
2. Stream data from multiple sources
3. Router learns to cluster inputs
4. Prompts adapt per cluster
5. Monitor and iterate on new data
6. Prompts continuously improve
```

## Related Work & Context

### Foundation Areas
- **Test-Time Training**: Prior work on single-dataset prompt adaptation
- **Prompt Learning**: Methods for learning prompt embeddings and selections
- **Online Learning**: Streaming data adaptation algorithms
- **Mixture of Experts**: Routing and specialization in model architectures

### Related Recent Work
- Soft prompt tuning and prefix tuning
- In-context learning and few-shot adaptation
- Domain adaptation through prompt engineering
- Mixture-of-experts for language models

### Future Research Directions

1. **Hierarchical Routing**: Nested clusters for taxonomy-like task structures
2. **Cross-Model Routing**: Selecting between different model architectures for different tasks
3. **Meta-Learned Router Initialization**: Pre-train routers on diverse task distributions
4. **Prompt Interpretability**: Making learned prompts human-understandable
5. **Theoretical Analysis**: Convergence bounds for router-prompt co-evolution
6. **Interaction with Fine-Tuning**: Combining online prompt learning with periodic fine-tuning
7. **Fairness Under Routing**: Ensuring routing doesn't introduce demographic bias

## Keywords

test-time learning, prompt learning, multi-task learning, routing, LLM agents, self-improving systems, online learning, heterogeneous data streams
