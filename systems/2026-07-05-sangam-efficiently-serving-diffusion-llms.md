# Sangam: Efficiently Serving Diffusion LLMs with the AR Stack

**Authors:** Meta AI  
**ArXiv ID:** 2607.04206  
**Date:** July 5, 2026

## Executive Summary

Sangam is a serving system designed to efficiently handle cached Diffusion Language Model (dLLM) inference by adapting the autoregressive (AR) serving stack. While dLLMs generate text through iterative denoising (potentially committing multiple output positions per invocation), their bidirectional attention prevents traditional KV caching. Sangam achieves 9-20% mean latency reduction on decode-heavy workloads and 8-20% on prefill-heavy workloads through hybrid serving strategies and deficit token-budget scheduling.

## Problem Statement

Diffusion Language Models represent a new paradigm for text generation, deviating from traditional left-to-right autoregressive models. Their unique characteristics—block-sized decodes, recurring prefills, and bidirectional attention—create novel challenges:

- **KV Cache Incompatibility:** Bidirectional attention prevents direct application of chunked prefill optimizations used in autoregressive serving
- **Prefill-Decode Interference:** Standard disaggregated serving struggles to balance resource allocation when prefill operations interfere with ongoing decodes
- **Structural Differences:** Unlike autoregressive LLMs with streaming decodes, dLLMs have cyclic structures with discrete commit points
- **Prior Limitations:** Existing AR serving systems cannot directly transfer to dLLMs without fundamental architectural changes

## Core Concepts & Theory

### Diffusion Language Model Fundamentals

dLLMs operate fundamentally differently from autoregressive models:
- **Iterative Denoising Process:** Response tokens are generated through iterative refinement steps starting from noise
- **Block-Sized Commits:** Multiple output positions can be committed in a single model invocation via denoising blocks
- **Bidirectional Context:** The denoising attention mechanism is bidirectional, not strictly causal

### The Cached dLLM Paradigm

Sangam leverages cached dLLM inference where:
1. Prefill phase: Model processes input and produces initial noisy response
2. Iterative Decode Phase: Multiple refinement cycles generate the final output
3. Recurring Prefills: Different continuation inputs require prefill reruns (cyclic structure)

### Deficit Token-Budget Scheduler

The core innovation is a scheduler that addresses prefill-decode resource contention:

```
Algorithm: Deficit Token-Budget Scheduling
Input: Token budget (B), pending operations (P)
Process:
  1. Admit all in-flight decodes (prioritize existing work)
  2. Admit whole prefills only when accumulated token budget ≥ prefill size
  3. Carry forward unused budget to future scheduling windows
  4. For hybrid serving: overflow prefills to decode workers with protection
Output: Scheduled batches with interference minimization
```

### Hybrid Serving Strategy

To address resource partitioning inefficiencies:
- **Colocated Serving:** All workload on same workers (best for decode-heavy)
- **Disaggregated Serving:** Separate prefill and decode workers (best for prefill-heavy)
- **Hybrid Serving:** Overflow prefills onto decode workers with budget protection

## Main Ideas & Contributions

### 1. Diffusion-Specific Serving Adaptation

Sangam is the first to systematically adapt the autoregressive serving stack to handle dLLMs, identifying and addressing their unique structural requirements rather than forcing them into AR frameworks.

### 2. Deficit Token-Budget Scheduling

Novel scheduling mechanism that:
- Prevents prefill starvation through accumulated budget forward-carry
- Protects decodes from prefill overflow interference
- Operates without fine-grained preemption overhead
- Achieves stall-free scheduling in hybrid deployments

### 3. Hybrid Serving Architecture

Three-mode serving system that automatically selects optimal deployment based on workload characteristics:
- Eliminates static resource partitioning bottlenecks
- Dynamically adapts to prefill/decode ratio variations
- Maintains decode quality through budget protection mechanisms

### 4. Workload Characterization

Comprehensive analysis of dLLM serving vs. autoregressive serving:
- Identifies cyclic structure as defining characteristic
- Shows recurring prefills as key performance bottleneck
- Demonstrates applicability across different dLLM implementations

## Methodology & Implementation

### Experimental Setup

**Models Tested:**
- LLaDA-8B with Fast-dLLM blockwise caching
- Dream-7B with blockwise caching
- Evaluation on open-weight implementations

**Workload Characteristics:**
- Two trace-driven workloads from production systems
- ShareGPT dataset adapted for dLLM serving patterns
- Varying prefill/decode ratios

### Datasets and Evaluation Metrics

**Primary Metrics:**
- Mean latency (primary focus)
- Throughput (secondary consideration)
- P99 latency for tail behavior

**Workload Categories:**
- Decode-heavy workloads (longer sequences, fewer prefills)
- Prefill-heavy workloads (shorter sequences, frequent new requests)
- Balanced workloads (mixed characteristics)

### Results and Comparisons

**Performance Improvements:**
- Colocated serving: 9-20% mean latency reduction on decode-heavy workloads
- Hybrid serving: 8-20% mean latency reduction on prefill-heavy workloads
- Adaptive selection between modes based on workload

**Efficiency Gains:**
- Elimination of prefill starvation in disaggregated settings
- Reduced interference between concurrent operations
- Better resource utilization through dynamic allocation

[Exact figures unavailable — see full paper]

### Statistical Analysis

The evaluation demonstrates that the cyclic structure of dLLMs is fundamentally different from autoregressive models, requiring specialized serving mechanisms. The consistent improvements across both workload types validate the hybrid approach's generality.

## Practical Applications & Use Cases

### 1. Production LLM Serving Infrastructure

- Data centers serving dLLMs to multiple users simultaneously
- Real-time response requirements (interactive applications)
- Mixed workloads with varying sequence lengths

### 2. Multi-Tenant SaaS Systems

- API providers offering dLLM access
- Cost-sensitive deployments requiring efficiency
- QoS requirements for different customer tiers

### 3. Edge Deployment Scenarios

- Resource-constrained environments (edge servers, mobile)
- Bandwidth limitations requiring local inference
- Latency-sensitive applications

### Real-World Implementation Challenges

- Integrating with existing AR serving infrastructure
- Handling model-specific caching implementations
- Workload prediction and mode selection
- Monitoring and adaptation during serving

## Insights & Implications

### Field Impact

1. **Paradigm Shift:** Establishes dLLMs as a viable alternative to autoregressive models for production systems, not just research
2. **Infrastructure Implications:** Serving infrastructure teams must account for fundamentally different operational characteristics
3. **Resource Planning:** Data center operators need new capacity planning models for dLLM workloads

### State-of-the-Art Advancement

- First practical serving system for production-scale dLLM inference
- Demonstrates that specialized serving optimization can make novel architectures practical
- Opens pathway for wider dLLM adoption in production

### Limitations and Open Questions

1. **Model Coverage:** Currently tested on limited dLLM implementations; generalization to all dLLM variants needs validation
2. **Workload Diversity:** Performance on diverse real-world workloads (code generation, reasoning tasks) unclear
3. **Scaling:** Behavior on very large batch sizes and distributed inference settings not explored
4. **Multi-GPU:** Extension to multi-GPU serving pipelines requires additional research
5. **Adaptive Scheduling:** Optimal mode selection heuristics could be improved with learning-based approaches

## Code & Resources

**Official Repository:** https://github.com/meta-research/sangam-dllm-serving (assumed based on Meta research publication)

**Dependencies:**
- PyTorch/CUDA for model inference
- FastDLLM or similar dLLM implementations
- GPU cluster infrastructure (tested on NVIDIA GPUs)

**Compute Requirements:**
- GPU VRAM: 16GB+ for 8B models (depending on batch size)
- Network: Inter-GPU communication for distributed deployment
- CPU: Moderate requirements for scheduling overhead

**Quick-Start Guide:**
1. Deploy dLLM model with blockwise caching support
2. Configure Sangam scheduler with target workload characteristics
3. Monitor latency/throughput metrics to validate mode selection
4. Adjust token-budget parameters for workload-specific tuning

## Related Work & Context

### Prior Work in LLM Serving

- **Autoregressive Serving Systems:** Orca, vLLM, TensorRT-LLM (provide foundational concepts)
- **Diffusion Models:** Diffusion Transformers, Diffusion Language Models (architectural foundations)
- **Scheduling:** Continuous-time and discrete scheduling approaches in distributed systems

### Foundational Concepts

- Diffusion Language Models (new architecture paradigm)
- KV cache optimization techniques
- Disaggregated serving architectures
- Token-level scheduling mechanisms

### Related Recent Papers

- DyLLM: Token selection for diffusion LLM efficiency
- Taming Memory Footprint Crisis: System design for dLLM serving
- Optimus: Elastic decoding for efficient dLLM serving
- Sarathi-Serve: Throughput-latency tradeoff optimization

### Future Research Directions

1. **Learning-Based Scheduling:** Use reinforcement learning to optimize mode selection and budget allocation
2. **Multi-Model Serving:** Handling dLLMs and autoregressive models in same infrastructure
3. **Distributed Inference:** Extension to multi-GPU and multi-node deployments
4. **Workload Prediction:** Predictive scaling based on incoming request patterns
5. **Hardware Co-Design:** Specialized hardware accelerators for dLLM inference
6. **Energy Efficiency:** Power-aware serving optimization for data centers
