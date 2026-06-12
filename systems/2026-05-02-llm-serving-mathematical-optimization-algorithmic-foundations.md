# Position: LLM Serving Needs Mathematical Optimization and Algorithmic Foundations, Not Just Heuristics

**Author:** Zijie Zhou  
**ArXiv ID:** 2605.01280  
**Submitted:** May 2, 2026  
**Category:** Systems / LLM Infrastructure  
**Paper Type:** Position Paper  

## Executive Summary

This position paper argues that large language model (LLM) inference serving has fundamentally outgrown the generic distributed systems heuristics that still dominate serving systems. Despite rapid advances in serving frameworks like vLLM and SGLang, their core algorithms rely on classical approaches (FIFO scheduling, LRU eviction, round-robin routing) that ignore the distinctive characteristics of LLM inference. The author advocates for developing mathematical optimization models and algorithmic foundations that capture LLM-specific properties—dynamically growing KV cache, prefill-decode asymmetry, unknown output lengths—to enable provably optimal solutions across diverse workloads.

## Problem Statement

### Current State of LLM Serving Systems

Modern LLM serving frameworks have made impressive engineering advances:
- Continuous batching for better GPU utilization
- Efficient memory management for KV cache
- Request-level parallelism and pipelining

**Yet their algorithmic cores remain unchanged from classical distributed computing:**
- **Request Routing**: Join-shortest-queue (JSQ) or round-robin approaches
- **Job Scheduling**: FIFO (First-In-First-Out) queue disciplines
- **Memory Eviction**: LRU (Least-Recently-Used) cache replacement

### Why Classical Heuristics Fail for LLMs

These general-purpose policies ignore the distinctive structure of LLM inference:

| System Property | Classical Systems | LLM Inference | Implication |
|-----------------|------------------|---------------|-------------|
| **Memory Growth** | Fixed per task | Grows with output tokens | Eviction decisions require output length prediction |
| **Compute Phases** | Uniform | Asymmetric (prefill vs. decode) | Scheduling must account for phase differences |
| **Output Length** | Known a priori | Unknown until generation | Admission control becomes probabilistic |
| **Batching Constraints** | Independent tasks | Sequence length interdependencies | Traditional bin-packing fails |

### Research Gap

Current heuristics succeed in some scenarios but fail unpredictably in others. For example:
- FIFO scheduling is optimal when all requests have similar characteristics but performs poorly with mixed workloads (short and long contexts)
- LRU eviction works well for uniform access patterns but not for the complex dependencies in LLM KV caches
- Round-robin routing assumes homogeneous servers but doesn't account for heterogeneous GPU capabilities or thermal constraints

**The field lacks mathematical models capturing LLM-specific characteristics, enabling algorithms with provable performance guarantees.**

## Core Concepts & Theory

### LLM Inference Anatomy

To understand the need for better algorithms, we must first characterize LLM inference:

**Phase 1: Prefill**
- Input prompt is processed token-by-token (or in parallel, depending on implementation)
- All KV cache entries are computed once
- Memory bandwidth and compute are both bottlenecks
- Duration: relatively short but compute-intensive

**Phase 2: Decode**
- Model generates output tokens one at a time (autoregressively)
- KV cache is read repeatedly, memory bandwidth-bound
- Duration: long (proportional to output length), but compute-efficient
- Each iteration adds a new token to KV cache

### Key LLM-Specific Characteristics

1. **Dynamic KV Cache Growth**
   - Memory requirement: `M(t) = base_model_size + KV_cache_size(t)`
   - `KV_cache_size(t)` grows dynamically with generated tokens
   - Cannot be predicted accurately without completing generation

2. **Prefill-Decode Asymmetry**
   - Prefill: compute-bound, parallel processing possible
   - Decode: memory-bound, sequential generation
   - Optimal batch composition differs between phases

3. **Unknown Output Lengths**
   - Output length unknown until generation completes (stopping criteria met)
   - Admission control and resource allocation must handle uncertainty
   - Classical worst-case analysis may be overly pessimistic

4. **Continuous Batching Constraints**
   - Requests with different prompt lengths and output lengths share GPU memory
   - Fragmentation: GPU resources sit idle while waiting for requests to complete
   - Pausing and resuming requests adds complexity

### Mathematical Modeling Framework

**Optimization Problem Formulation** (Illustrative):

```
Minimize: E[response_latency]
Subject to:
  - GPU memory constraint: ∑ KV_cache(i,t) ≤ GPU_memory
  - GPU compute constraint: compute_demand(batch_t) ≤ GPU_compute_capacity
  - Fairness constraint: P(latency(i) ≥ threshold) ≤ ε (for all requests i)
  - Batch constraint: batch_size(t) respects sequence length interdependencies
```

**Where:**
- `KV_cache(i,t)` = dynamic cache size for request i at time t
- `compute_demand(batch)` = prefill or decode compute based on batch composition
- `response_latency` = end-to-end latency from admission to completion

This formulation reveals that:
- Classical bin-packing (assuming fixed sizes) is inappropriate
- Probabilistic models of output length are necessary
- Joint optimization of scheduling and batching is required

## Main Ideas & Contributions

### 1. Identification of the Fundamental Gap

**Contribution**: Clearly articulates that despite engineering advances, the algorithmic foundations of LLM serving lag behind the unique computational requirements.

**Impact**: Shifts focus from incremental system improvements to principled algorithmic innovation.

### 2. Characterization of LLM-Specific Structure

**Contribution**: Explicitly enumerates the properties that distinguish LLM inference from classical distributed computing.

**Value**: Provides a checklist for algorithm designers to ensure they're not ignoring critical LLM characteristics.

### 3. Call for Principled Algorithm Design

**Contribution**: Advocates for moving from domain-specific heuristics to algorithms with provable performance guarantees.

**Examples of Principled Approaches**:
- Stochastic scheduling algorithms accounting for output length uncertainty
- Online algorithms for KV cache admission and eviction with competitive analysis
- Approximation algorithms for batch composition with formal approximation ratios

### 4. Emerging Evidence

**Contribution**: Points to recent work showing that algorithmic rigor improves practical performance.

**Key Finding**: Principled methods designed specifically for LLM inference can match or exceed heuristic performance while providing theoretical guarantees—making them strictly better.

## Methodology & Implementation

### Research Agenda

The position paper outlines a research agenda rather than proposing a specific algorithm. However, the recommended approach includes:

### 1. Problem Formulation

- Develop precise mathematical models for each subproblem (scheduling, admission control, batching)
- Use techniques from operations research: linear programming relaxations, Markov decision processes
- Characterize the computational complexity (NP-hardness, approximation schemes)

### 2. Algorithm Design

- For tractable problems: design exact algorithms or approximation schemes
- For intractable problems: design online algorithms with competitive ratios or approximation guarantees
- For dynamic environments: use online learning and regret bounds

### 3. Empirical Validation

- Benchmark against current heuristics using diverse workloads
- Measure: latency, throughput, fairness, memory efficiency
- Evaluate under realistic conditions: request arrival patterns, prompt length distributions, output length distributions

### Proposed Research Directions

#### Direction 1: Probabilistic Scheduling

**Problem**: FIFO scheduling ignores heterogeneous request characteristics.

**Approach**: Use Markov decision process (MDP) formulation with state = (batch_composition, GPU_utilization, queue_state).

**Expected Outcome**: Scheduling policy optimizing latency or throughput under LLM-specific constraints.

#### Direction 2: Online KV Cache Eviction

**Problem**: LRU eviction doesn't account for future reference patterns in KV caches.

**Approach**: Design online algorithms with competitive analysis against optimal offline eviction.

**Competitive Ratio Target**: Minimize gap between online (unknown future) and offline (perfect knowledge) performance.

#### Direction 3: Admission Control under Uncertainty

**Problem**: Determining which requests to accept given uncertain output lengths.

**Approach**: Stochastic optimization under output length distributions.

**Guarantees**: Bounds on SLA violations (requests exceeding latency deadlines).

#### Direction 4: Batch Composition Optimization

**Problem**: Mixed-length batches cause GPU fragmentation.

**Approach**: Joint optimization of batch composition and scheduling to maximize utilization.

**Methods**: Integer linear programming (ILP) for exact solutions on small problems, approximation algorithms for larger instances.

## Practical Applications & Use Cases

### 1. Cloud LLM Serving Platforms

**Current Setup**: vLLM or SGLang on GPUs or TPUs

**Opportunity**: Replace heuristic scheduling with principled algorithms

**Implementation Feasibility**: High—can augment existing systems without major rewrites

**Expected Impact**: 10-30% latency reduction at constant throughput, or 20-50% throughput increase at constant latency targets (estimated based on algorithm design potential)

### 2. Multi-Model Serving

**Challenge**: Sharing GPU/TPU resources across multiple LLMs with different resource profiles

**Algorithmic Approach**: Extended formulations handling multiple models in scheduling and batching

**Feasibility**: Moderate—requires understanding resource sharing and contention patterns

### 3. Inference under SLA Constraints

**Use Case**: Meeting service-level agreements (e.g., 99th percentile latency ≤ 500ms)

**Algorithmic Goal**: Admission control and scheduling policies that provably satisfy SLAs

**Value**: Enables overbooking and better resource utilization

### 4. Cost Optimization in Heterogeneous Clusters

**Setup**: Mix of GPU types (H100, A100, L40S, etc.) with different performance and cost characteristics

**Algorithmic Challenge**: Routing and scheduling decisions accounting for cost per token

**Feasibility**: High—many existing cost optimization techniques apply

### 5. Edge and Mobile Inference

**Context**: Limited and variable compute resources

**Algorithmic Need**: Robust algorithms tolerating high variability in resource availability

**Potential**: Enable efficient LLM serving on edge devices

## Insights & Implications

### Why This Matters Now

1. **Scale**: LLM serving is transitioning from research to production at massive scale
2. **Diversity**: Workloads range from latency-critical (chat) to throughput-optimized (batch processing)
3. **Economics**: Infrastructure costs dominate LLM deployment; algorithmic improvements directly impact profitability
4. **Competition**: Leading serving systems (vLLM, SGLang, TensorRT) compete on performance; principled algorithms could be a differentiator

### Paradigm Shift

**From**: "Better engineering and caching strategies"  
**To**: "Algorithms with formal performance guarantees tailored to LLM inference"

### Broader Implications

- **Operations Research Renaissance**: Classical techniques (linear programming, approximation algorithms) gain new relevance in ML systems
- **Systems × Algorithms**: Highlights the underexplored intersection where domain knowledge (systems) meets algorithmic theory
- **Reproducibility**: Algorithms with proofs are more reproducible and transferable across implementations than engineering heuristics

### Limitations

The position paper itself doesn't propose complete solutions; rather, it frames the problem and advocates for the research community to engage. Actual progress requires:

- Collaboration between systems researchers, algorithms experts, and practitioners
- Benchmarks capturing diverse LLM serving workloads
- Implementation frameworks supporting rapid prototyping of new algorithms

## Code & Resources

### No Official Implementation

As a position paper, this work doesn't include code. However, it highlights opportunities for implementation:

### Tools and Frameworks for Algorithm Development

- **Optimization Libraries**: CPLEX, Gurobi, SCIP (for exact and approximate solutions)
- **Simulation**: OMNeT++, ns-3 (for validating algorithms before deployment)
- **Serving Frameworks**: vLLM, SGLang (as target systems for implementation and benchmarking)
- **Learning Tools**: TensorFlow, PyTorch (for learning-based algorithm development)

### Implementation Strategy

1. **Start with simulation**: Implement algorithms in a discrete-event simulator
2. **Validate mathematically**: Prove approximation ratios or competitive bounds
3. **Benchmark against baselines**: Compare against FIFO, round-robin, LRU
4. **Integrate into serving system**: Port successful algorithms into production framework
5. **A/B test**: Measure real-world impact on latency, throughput, cost

## Related Work & Context

### Foundation: Scheduling Theory

- Classical scheduling algorithms (earliest deadline first, shortest job first)
- Online algorithms and competitive analysis
- Approximation algorithms for bin packing and resource allocation

### Systems Context

- LLM inference optimization (vLLM, SGLang, Ansor)
- GPU memory management and resource allocation
- Cloud resource scheduling and allocation literature

### ML Systems

- Serving systems design (clipper, Ansor, BentoML)
- Batching strategies in deep learning
- Federated inference and edge computing

### Related Position Papers & Vision Work

- Trends in ML systems emphasizing algorithmic rigor
- Systems papers identifying gaps in current practices
- Calls for bridging operations research and ML

## Future Research Directions

### Short-term (1-2 years)

1. **Algorithm Development**: Design and analyze scheduling, eviction, and admission control algorithms
2. **Benchmarking Suite**: Create standard benchmarks for LLM serving workloads
3. **Simulation Validation**: Demonstrate improvements in discrete-event simulators
4. **Feasibility Studies**: Assess computational overhead of candidate algorithms

### Medium-term (2-4 years)

1. **Production Implementation**: Integrate promising algorithms into vLLM, SGLang, or similar systems
2. **Real-world Measurement**: A/B test on production workloads
3. **Theoretical Analysis**: Extend algorithms to handle additional constraints (multi-modal, streaming, adaptive)
4. **Cross-platform Validation**: Demonstrate effectiveness across hardware (GPUs, TPUs, specialized accelerators)

### Long-term (4+ years)

1. **Learning-based Hybrids**: Combine algorithmic foundations with learned components (e.g., learned eviction policies)
2. **Automated Algorithm Synthesis**: Use program synthesis or AutoML techniques to generate optimal algorithms for specific workload distributions
3. **Formal Verification**: Develop tools to verify algorithm correctness and performance guarantees
4. **Standardization**: Establish industry standards for algorithm design and evaluation in LLM serving

## Significance and Impact

This position paper serves a crucial role: articulating a gap between engineering excellence and algorithmic rigor in a critical infrastructure component. As LLMs become pervasive, the efficiency of serving systems directly impacts cost, availability, and carbon footprint. While the author doesn't provide solutions, the framing is sufficiently clear and compelling to guide an entire research agenda.

The paper's real strength lies in its clarity about **what needs to change** and **why it matters**, potentially catalyzing the research community to invest in principled algorithmic approaches to LLM serving. Whether measured in latency improvements, throughput gains, or cost reductions, the potential impact is substantial—and the research community is now looking for the next generation of serving systems to deliver.
