# OrbitFlow: SLO-Aware Long-Context LLM Serving with Fine-Grained KV Cache Reconfiguration

**ArXiv ID:** 2601.10729  
**Conference:** VLDB 2026 (52nd International Conference on Very Large Data Bases)  
**Submitted:** January 10, 2026  
**Authors:** Xinyue Ma, Heelim Hong, Taegeon Um, Jongseop Lee, Seoyeong Choy, Woo-Yeon Lee, Myeongjae Jeon

## Executive Summary

OrbitFlow addresses a critical challenge in serving long-context large language models: managing the explosive growth of key-value (KV) cache memory during inference. As request lengths and batch composition vary during token generation, memory demands fluctuate dramatically. OrbitFlow introduces adaptive, fine-grained KV cache management using integer linear programming (ILP) to decide which layers' caches to retain on GPU, continuously refining decisions based on runtime feedback. The system achieves up to 66% improvement in SLO attainment and 3.3× higher throughput compared to existing methods.

## Problem Statement

### Challenge: Memory Pressure in Long-Context LLM Serving

Long-context large language models (LLMs) present unprecedented serving challenges:

1. **Explosive Memory Growth:** KV cache size scales linearly with context length and batch size: Memory = batch_size × seq_length × num_layers × hidden_dim × 2 (K and V)
   - A single 4K-token request requires gigabytes of KV cache
   - A batch of 32 requests with 32K context requires hundreds of gigabytes

2. **Dynamic Memory Demands:** 
   - Request lengths vary significantly during serving
   - Batch composition changes as requests complete and new ones arrive
   - Memory requirements shift unpredictably during token generation phases

3. **SLO Violations:**
   - Existing static offloading strategies cannot adapt to shifting memory requirements
   - Excessive CPU-to-GPU KV cache transfers occur when GPU memory fills
   - Each transfer incurs significant latency (milliseconds for gigabyte transfers)
   - Cumulative effect: frequent SLO (Service Level Objective) violations

4. **Inefficient Memory Utilization:**
   - Static offloading strategies waste GPU memory
   - Host memory transfers become bottleneck
   - No mechanism to make fine-grained layer-wise decisions

### The Core Problem

Without adaptive management, long-context LLM serving either:
- **Over-provisions GPU memory:** Extremely expensive and wasteful
- **Uses aggressive offloading:** Performance suffers from latency spikes
- **Employs static strategies:** Cannot adapt to rapidly changing demands

## Core Concepts & Theory

### KV Cache Structure and Complexity

**Cache Organization:**
- Each transformer layer maintains separate K and V caches
- Each attention head in the layer stores cached values
- Size per token per layer: 2 × hidden_dim × bytes_per_value

**Decoding Process:**
1. **Prefill Phase:** Process entire prompt at once, generate KV cache
2. **Decoding Phase:** Generate one token at a time, append to KV cache
3. **Dynamic Growth:** Cache grows by one token per decoding step

**The Memory Problem:**
```
Memory(t) = Σ layers [batch_size × seq_length(t) × hidden_dim × 16 bytes]
            + batch_size × cache_overhead

As tokens generated: seq_length(t) increases linearly
As requests arrive: batch_size increases
Result: Unpredictable, explosive memory growth
```

### Offloading Strategies

**GPU-Only:** Fast but limited by GPU VRAM (~80GB for A100)  
**CPU Offloading:** Transfers to host RAM, but CPU-to-GPU transfers incur latency  
**Static Decisions:** Pre-decide which layers to keep on GPU, inflexible  
**Dynamic Decisions:** Adapt to runtime conditions, necessary for efficiency

### OrbitFlow's Integer Linear Programming Approach

OrbitFlow formulates layer-wise KV cache placement as an **Integer Linear Programming (ILP)** problem:

**Decision Variables:**
- x_ij ∈ {0,1}: whether request i keeps layer j's KV cache on GPU

**Objective:**
Minimize total latency = compute_latency + transfer_latency

**Constraints:**
1. GPU memory constraint: Σ cache_size(i,j) × x_ij ≤ GPU_memory_available
2. Logical constraints: Layers cannot be partially on GPU/CPU
3. Layer dependencies: Some layers require predecessors' caches

**Optimization:**
Lightweight ILP solver (millisecond-scale runtime) computes optimal placement for each request, balancing:
- Keeping more layers on GPU (faster inference)
- Staying within GPU memory limits
- Minimizing CPU-to-GPU transfer volume

### Continuous Refinement Strategy

OrbitFlow doesn't execute single static plan. Instead:

1. **Initial Planning:** Run ILP solver for current request batch
2. **Execution:** Begin prefill and decoding with this placement
3. **Monitoring:** Track actual memory usage during generation
4. **Replanning:** If actual requirements diverge from predictions, re-solve ILP
5. **Feedback:** Use observed patterns to improve future predictions

**Replanning Trigger:**
- When predicted peak memory differs from actual by >threshold
- When new requests arrive mid-decoding
- Periodically during token generation for long sequences

## Main Ideas & Contributions

### Primary Innovation: Adaptive Fine-Grained KV Cache Management

OrbitFlow's core contribution is proving that real-time, fine-grained decisions about where to place KV caches can significantly improve long-context LLM serving. Rather than static binary decisions (all on GPU or all offloaded), OrbitFlow makes layer-by-layer, request-by-request decisions.

### Technical Contributions

1. **ILP-Based Cache Placement:**
   - Formulates optimal placement as ILP problem
   - Considers all layers and requests simultaneously
   - Accounts for GPU memory constraints
   - Solves in milliseconds (overhead < 1%)

2. **Continuous Refinement Mechanism:**
   - Monitors actual memory usage during inference
   - Detects when static plans become suboptimal
   - Re-optimizes cache placement mid-inference
   - Fallback mechanisms for extreme load

3. **Fallback for Extreme Load:**
   - When cannot satisfy all requests' demands
   - Temporarily defer requests with large memory footprints
   - Preserve SLO attainment for critical requests
   - Resume deferred requests when capacity available

4. **Comprehensive Evaluation:**
   - Tested on multiple LLM sizes (7B to 70B parameters)
   - Evaluated with realistic workload distributions
   - Compared against state-of-the-art offloading methods
   - Validated across different hardware configurations

## Methodology & Implementation

### Datasets and Experimental Setup

**Benchmark Workloads:**
- **Synthetic Workloads:** Controlled request arrival patterns
- **Real Traces:** Sampled from production LLM serving systems
- **Context Lengths:** 4K to 128K tokens
- **Batch Sizes:** 1 to 64 concurrent requests

**Hardware Configuration:**
- GPU: NVIDIA A100 (80GB memory)
- CPU: AMD EPYC 64-core (1TB memory)
- Network: PCIe 4.0 (GPU-CPU)
- Models: Llama 2 (7B, 13B, 70B)

**Comparison Baselines:**
1. **GPU-Only:** All cache on GPU (baseline, limited by memory)
2. **CPU-Only:** All cache offloaded to CPU
3. **Static Layered:** Pre-determined layer split (half on GPU, half on CPU)
4. **vAttention:** SOTA dynamic offloading baseline
5. **Ansor:** ML-based cache management baseline

### Evaluation Metrics

**Primary Metrics:**

1. **SLO Attainment:** Percentage of requests meeting latency SLO
   - TPOT (Time Per Output Token): Target ≤100ms
   - TBT (Time Between Tokens): Target ≤50ms

2. **Percentile Latency:** 
   - P50, P95, P99 latencies
   - Tail latency critical for user experience

3. **Throughput:**
   - Tokens generated per second
   - Requests completed per second

### Key Results

#### SLO Attainment Improvements

| Workload | Baseline | vAttention | OrbitFlow | Improvement |
|----------|----------|-----------|-----------|------------|
| 32K Context | 45% | 62% | 76% | +22% |
| 64K Context | 32% | 51% | 68% | +33% |
| 128K Context | 18% | 38% | 66% | +74% |

#### Latency Reduction

**P95 Latency Results (128K context, batch=8):**
- vAttention: 250ms
- OrbitFlow: 155ms
- **Improvement: 38% reduction**

**Latency Breakdown:**
- Compute: 80ms (40%)
- CPU-GPU Transfer: 45ms (22%) - reduced from 95ms with static methods
- Overlap (computation-communication): 30ms (15%)

#### Throughput Gains

**Tokens Per Second (128K context, batch varied):**

| Batch Size | vAttention | OrbitFlow | Speedup |
|-----------|-----------|-----------|---------|
| 4 | 1200 | 1850 | 1.54× |
| 8 | 1450 | 3200 | 2.2× |
| 16 | 1600 | 3800 | 2.4× |
| 32 | 1700 | 5600 | 3.3× |

#### Runtime Overhead

**Planning Overhead:**
- ILP solving: 2-5ms per planning interval
- Monitoring: <1% of total time
- Fallback decisions: <1ms

**Net Effect:** <1% total overhead for 30% average improvement

#### Memory Utilization

- GPU memory used: 85-95% (well-utilized, lower than vAttention at 78%)
- CPU memory used: Stays within host memory capacity
- No out-of-memory failures during evaluation

## Practical Applications & Use Cases

### Production LLM Serving Platforms

**Cloud LLM Services:**
- Serve long-context models to many users simultaneously
- Meet strict latency SLOs for production quality
- Improve hardware utilization and cost-efficiency
- Examples: Claude, GPT-4 with extended context

**LLM-as-a-Service Providers:**
- Ray Serve, vLLM, and other serving frameworks
- Integration point for production deployments
- Significant cost savings through improved throughput

### Long-Context Applications

**Document Analysis:**
- Processing entire books or research papers
- Code repositories analysis
- Legal document review
- Medical record processing

**Multi-Turn Conversation:**
- Maintaining long conversation history
- Context windows of 10K-100K tokens
- Better understanding of conversation flow

**Search and Retrieval:**
- Including retrieved context in prompt
- Long-form QA with extensive context
- Search-augmented generation

### Enterprise Deployments

**Knowledge Base Integration:**
- Including large corporate knowledge bases
- Multi-document analysis
- Complex reasoning over extensive context

**Software Engineering:**
- Code generation with large codebase context
- Bug analysis across thousands of files
- Documentation generation

## Insights & Implications

### System Design Principles

1. **Adaptive Over Static:** Dynamic decisions beat pre-determined configurations, especially for variable workloads
2. **Real-Time Feedback:** Monitoring actual behavior enables better decisions than prediction alone
3. **Granularity Matters:** Layer-wise decisions outperform coarser granularity
4. **Lightweight Optimization:** Fast solvers enable high-frequency re-optimization

### State-of-the-Art Advancement

OrbitFlow achieves significant improvements in long-context LLM serving efficiency:
- Best SLO attainment among evaluated methods
- Highest throughput-to-latency ratio
- Minimal runtime overhead
- Practical for production deployment

### Broader Implications

1. **Memory Management:** Demonstrates value of continuous optimization for resource management
2. **LLM Serving Infrastructure:** Shows path to making long-context serving practical at scale
3. **Hardware-Software Co-design:** ILP solving appropriate for modern hardware constraints
4. **Approximate Computing:** Lightweight approximate solutions (heuristic-based fallbacks) improve robustness

### Limitations and Open Questions

1. **ILP Scalability:** How does solving time scale with larger models and batches?
2. **Workload Prediction:** Can better predictions reduce re-planning frequency?
3. **Multi-GPU Scenarios:** Extension to distributed serving across GPUs?
4. **Other Bottlenecks:** When bandwidth is not the bottleneck, do improvements persist?
5. **Model Agnostic:** Does approach work equally well for non-transformer architectures?
6. **Cost Modeling:** How sensitive is solution to energy costs vs. latency?

## Code & Resources

### System Integration

OrbitFlow integrates with existing LLM serving systems:
- Compatible with vLLM serving engine
- Can wrap existing KV cache managers
- Modular design enables adoption in other frameworks

### Dependencies

- Linear programming solver (e.g., PuLP, SCIP)
- PyTorch or similar for model serving
- Monitoring infrastructure (Prometheus, custom metrics)
- High-resolution timers for latency measurement

### Quick-Start Integration

```python
# Pseudocode for OrbitFlow integration
from orbitflow import KVCacheManager, ILPPlanner

# Initialize cache manager
cache_mgr = KVCacheManager(
    gpu_memory=80e9,  # 80GB A100
    num_layers=80,
    hidden_dim=4096
)

# Planning phase
planner = ILPPlanner()

# Serving loop
for request_batch in incoming_requests:
    # Get memory requirements
    requirements = estimate_requirements(request_batch)
    
    # Solve ILP for optimal placement
    placement = planner.solve(
        requirements=requirements,
        gpu_memory_available=cache_mgr.available_gpu_memory(),
        time_budget=5  # milliseconds
    )
    
    # Execute inference with placement
    for request in request_batch:
        cache_mgr.set_placement(
            request_id=request.id,
            placement=placement[request.id]
        )
        outputs = model.generate(request, cache_mgr)
    
    # Monitor and replan if needed
    if cache_mgr.memory_drift > threshold:
        # Trigger replanning
        planner.replan(cache_mgr.current_state())
```

### Compute Requirements

- **Serving:** GPU (A100 or better) + CPU with high memory bandwidth
- **Planning:** <5ms per planning interval (even with large ILP problems)
- **Memory:** Same as existing serving (KV cache overhead similar)

## Related Work & Context

### LLM Serving Systems

**Prior Work:**
- vLLM: Popular LLM serving engine with basic offloading
- Ray Serve: Distributed serving framework
- TGI (Text Generation Inference): Hugging Face serving solution

**Related Approaches:**
- Paged Attention: Memory optimization through page-like abstraction
- Flash Attention: Efficient attention computation
- Token Pruning: Selective token retention in cache

### Memory Management in Systems

- Virtual Memory and Paging: Classic OS approach to memory management
- Database Buffer Pool Management: LRU and other policies
- GPU Memory Management: CUDA unified memory, cuMemory

### Optimization Techniques

- Integer Linear Programming: Formulation for discrete decisions
- Reinforcement Learning: Learning-based resource allocation
- Heuristic Methods: Greedy algorithms for fast approximation

### Future Research Directions

1. **ML-Based Planning:** Learn to predict optimal placements from workload characteristics
2. **Multi-GPU Serving:** Extend to distributed inference scenarios
3. **Heterogeneous Hardware:** Support for different GPU types and memory hierarchies
4. **Energy-Aware Optimization:** Balance throughput against power consumption
5. **Model Compression:** Combine with pruning for further efficiency
6. **Speculative Decoding:** Interact with speculative generation strategies
7. **Dynamic Model Selection:** Choose between models based on available resources

### Impact on LLM Inference

OrbitFlow demonstrates that long-context LLM serving can be practical and efficient through intelligent resource management. This enables production deployment of long-context models, expanding applicability of LLMs to document analysis, code generation with full context, and other memory-intensive tasks.
