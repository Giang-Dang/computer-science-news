# Federation of Experts: Communication Efficient Distributed Inference for Large Language Models

**ArXiv ID:** 2605.06206  
**Submission Date:** May 7, 2026  
**Authors:** Muhammad Shahir Abdurrahman, Chun Deng, Azalia Mirhoseini, Philip Levis

## Executive Summary

This paper addresses a critical bottleneck in scaling Mixture of Experts (MoE) LLMs to distributed systems: communication overhead between expert clusters. The Federation of Experts (FoE) architecture achieves communication reduction through partitioning expert blocks into isolated clusters with expert parallelism applied only within clusters. By confining all-to-all communication to intra-node fabric instead of inter-node networks, FoE achieves up to **5.2× reduction in end-to-end forward-pass latency** while maintaining comparable generation quality. This work makes distributed MoE inference practical at scale, enabling deployment of massive models across multi-node infrastructure.

## Problem Statement

Modern LLMs increasingly use Mixture of Experts (MoE) architectures for computational efficiency, where token routing directs each token to a small subset of expert modules. However, distributed inference of MoE models faces a **critical communication bottleneck**:

- **All-to-all communication overhead**: Standard MoE dispatch requires communicating token embeddings between all experts, creating massive communication traffic
- **Network bandwidth saturation**: Inter-node network links become the primary bottleneck, not computation
- **Scaling degradation**: Communication overhead scales worse than computation, making single-node assumptions invalid
- **Latency amplification**: Network round-trip latencies dominate end-to-end inference time
- **Resource contention**: Communication congestion reduces GPU utilization and increases queueing delays

**Prior Research Gaps:** Existing distributed MoE approaches assume dense expert utilization or rely on expensive hierarchical routing. No prior work effectively eliminated inter-node all-to-all communication while maintaining quality and minimal overhead. Standard expert parallelism (replicate experts across nodes) wastes memory; token parallelism (shard tokens) requires all-to-all sync.

## Core Concepts & Theory

### Mixture of Experts Background

**Standard MoE Architecture**
- Each token routed through sparse expert subset (e.g., top-2 or top-k)
- Learned routing function: `Expert = Top-k(token · expert_weights)`
- Feed-forward sublayer replaced with expert mixture
- Dramatically reduces computation vs. dense networks

**Distributed MoE Challenge**
- Simple replication: Each node has all experts → memory inefficient
- Expert parallelism: Experts sharded across nodes → all-to-all communication
- Token parallelism: Tokens sharded across nodes → synchronization barrier
- **Core Problem**: No approach cleanly separates communication and computation

### Federation of Experts Architecture

#### Key Innovation: KV-Head Partitioning

**Traditional Attention**
```
Input → Linear Projection → Q, K, V (full dim)
      ↓
Multi-Head Attention (all heads attend to full K, V)
      ↓
Head 1  Head 2  Head 3  ...  Head N (each head gets full K, V)
```

**FoE Architecture**
```
Input → Linear Projection → Q, K, V (full dim)
      ↓
KV Head Partition: Each attention head gets dedicated KV-head
      ↓
Cluster 1      Cluster 2      Cluster 3      ...  Cluster N
(Head 1 KV +   (Head 2 KV +   (Head 3 KV +
 Experts 1-8)   Experts 9-16)  Experts 17-24)
```

**Key Principle**: Each key-value attention head gets its own cluster containing:
1. The dedicated KV-head computation
2. A subset of experts (partitioned experts)
3. Residual connections from other clusters

#### Distributed Execution

```
┌─────────────────────────────────────────────────────────────┐
│                    Multi-Node System                        │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Node 1              Node 2              Node 3              │
│  ┌──────────┐       ┌──────────┐       ┌──────────┐         │
│  │Cluster 1 │       │Cluster 2 │       │Cluster 3 │         │
│  │────────  │       │────────  │       │────────  │         │
│  │Head 1 KV │       │Head 2 KV │       │Head 3 KV │         │
│  │Experts   │       │Experts   │       │Experts   │         │
│  │1-8       │       │9-16      │       │17-24     │         │
│  └──────────┘       └──────────┘       └──────────┘         │
│       ↓ (intra-node all-to-all)              ↓              │
│       │ (residual sync: post-attention)      │              │
│       ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ←               │
│          (inter-node only residuals)                        │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

#### Execution Flow

1. **Input Distributed**: Full input token sequence sent to all clusters (broadcast cost justified by elimination of token routing communication)

2. **Intra-Cluster Processing**
   - KV-head computation and storage (cluster-local)
   - Token routing to cluster's expert subset (local all-to-all)
   - Expert feed-forward computation
   - Head output generation (local reduction)

3. **Inter-Cluster Communication**
   - Residual outputs from each head/cluster sent to attention module
   - Reduced data volume (per-head residuals instead of token embeddings)
   - Synchronization at residual addition points
   - No token-to-expert routing communication across nodes

4. **Output Generation**: Final attention layer combines all head outputs; generation proceeds normally

### Theoretical Foundations

**Communication Complexity Analysis**

Let:
- `T` = sequence length (tokens)
- `d` = embedding dimension
- `H` = number of attention heads
- `E` = total number of experts
- `k` = expert fan-out (tokens per expert)
- `N` = number of nodes

**Standard Distributed MoE**
- Per-token expert routing: `O(T · E · d)` inter-node communication
- Cumulative for batch: `O(B · T · E · d)` (B = batch size)

**FoE Architecture**
- Per-head residuals: `O(T · d)` per cluster
- Total inter-node: `O(H · T · d)` (H << E in most cases)
- **Reduction ratio**: `E/H` (typical: 64-128x)

**Load Balancing Analysis**
- Expert selection per cluster is load-balanced within cluster
- Cross-cluster load imbalance acceptable due to async residual communication
- Allows heterogeneous expert utilization across clusters

## Main Ideas & Contributions

### Primary Innovation: Clustering Strategy

**Motivation**: Transform the all-to-all expert communication problem into a per-head residual synchronization problem through architectural redesign.

**Key Insight**: Attention heads naturally decompose MoE: each attention head can own its experts and communicate only via residual connections (which must be synchronized anyway).

**Benefits**:
1. **Communication Reduction**: Inter-node communication reduced to residual synchronization
2. **Flexibility**: Clusters can have different expert counts based on load
3. **Fault Tolerance**: Cluster failure affects only that head, not entire forward pass
4. **Incremental Deployment**: Clusters can be added incrementally without retraining

### Secondary Innovations

#### 1. **Residual-Based Synchronization**
- Rather than routing tokens to experts, synchronize residual outputs
- Residuals are typically smaller than token embeddings in distributed setting
- Overlaps with computation naturally through async communication

#### 2. **Hierarchical Expert Selection**
- Within-cluster routing optimized for low-latency all-to-all (same GPU memory space)
- Between-cluster routing implicit in attention
- Enables expert capacity tuning per cluster

#### 3. **Adaptive Load Balancing**
- Per-cluster load balancing with local expert load tracking
- Cross-cluster imbalance accepted as communication cost of heterogeneous distribution
- Load statistics inform cluster resizing

### Technical Contributions

1. **Architectural Pattern**: First clean separation of cluster-local and inter-node communication in MoE
2. **Communication Efficiency Analysis**: Quantifies communication reduction and conditions
3. **Practical Implementation**: End-to-end system supporting long-sequence inference
4. **Empirical Validation**: Measured 5.2× latency improvement on realistic workloads

## Methodology & Implementation

### Experimental Design

**Test Configuration**
- **Model**: Large MoE-based LLM with varying sizes
- **Hardware**: Multi-node GPU clusters (2-8 nodes)
- **Baselines**:
  - Standard distributed MoE (all-to-all expert dispatch)
  - Token parallelism approach
  - Tensor parallelism (dense network baseline)
- **Workload**: LongBench dataset (long-context inference scenarios)

### Performance Metrics

**Latency Measurements**

| Metric | Abbreviation | Definition |
|--------|-------------|-----------|
| Time to First Token | TTFT | Latency until first output token generated |
| Time Between Tokens | TBT | Per-token latency during generation |
| End-to-End Latency | E2E | Total latency for full sequence inference |
| Throughput | N/A | Tokens processed per second |

**Key Results**

| Metric | FoE | Standard MoE | Improvement |
|--------|-----|-------------|-------------|
| Forward-Pass Latency | 1.0× | 5.2× | **5.2× faster** |
| TTFT | 1.0× | 3.62× | **3.62× faster** |
| TBT | 1.0× | 1.95× | **1.95× faster** |
| Memory per Node | +5-8% | baseline | Minimal overhead |

### Datasets and Benchmarks

- **LongBench**: Long-context evaluation benchmark
- **Sequence Lengths**: 512 to 4096 tokens evaluated
- **Model Sizes**: 70B to 300B parameter models
- **Communication**: Profiling on NVIDIA NCCL stack

### Implementation Details

**System Stack**
- **Framework**: PyTorch with custom CUDA kernels
- **Communication**: NVIDIA NCCL for collective operations
- **Routing**: Standard top-k expert selection (modified for cluster awareness)
- **Hardware**: NVIDIA A100/H100 GPUs with NVLink and NVSwitch

**Key Implementation Challenges**

1. **Routing Token Awareness**
   - Router must know cluster assignments
   - Dispatch uses cluster-aware routing mask
   - Enables efficient local expert selection

2. **Residual Synchronization**
   - Post-MoE residuals must be synchronized across clusters
   - All-reduce operation on per-head outputs
   - Can be overlapped with next layer computation

3. **Memory Layout**
   - Expert sharding across nodes with cluster locality
   - KV-head localization within cluster
   - Efficient gather/scatter for token distribution

## Practical Applications & Use Cases

### Direct Applications

#### 1. **Large Model Serving at Scale**
**Use Case**: Deploy 100B+ parameter MoE models across multiple GPUs
- FoE enables practical multi-node inference
- Reduces P99 latency enabling real-time serving
- **Impact**: Makes frontier models deployable in production

#### 2. **Long-Context Inference**
**Use Case**: Process documents, code, or conversations with thousands of tokens
- Latency reduction critical for interactive applications
- FoE maintains quality while reducing latency
- **Impact**: Enables efficient long-document processing

#### 3. **Cost-Efficient Model Serving**
**Use Case**: Run inference across heterogeneous hardware
- Communication-limited design works across different network topologies
- Can utilize cheaper, older GPUs with slower interconnect
- **Impact**: Reduces infrastructure costs for MoE serving

#### 4. **Real-Time AI Applications**
**Use Case**: Chatbots, code completion, search ranking with LLMs
- Latency reduction enables real-time applications
- TTFT improvements critical for user experience
- **Impact**: Makes LLM serving viable for latency-sensitive services

### Industry Examples

**Example 1: Distributed Inference Service**
```
Configuration: 8-node cluster, 70B model
Without FoE: 850ms TTFT, 150ms/token
With FoE:    235ms TTFT, 77ms/token
Cost Benefit: ~3.6× speedup enables serving 3.6× more users per cluster
```

**Example 2: Long-Document Processing**
```
Configuration: Document QA over 4096 token context
Without FoE: Memory bottleneck, unable to process efficiently
With FoE:    Completes in <2s, enabling interactive applications
```

## Insights & Implications

### Broader Field Impact

1. **Architectural Insights**
   - Attention structure naturally decomposes MoE communication requirements
   - Per-head residual synchronization viable for large-scale systems
   - Suggests MoE architectures should be co-designed with distribution strategy

2. **Practical Systems Impact**
   - Makes distributed MoE inference production-ready
   - Enables cost-effective serving of frontier models
   - Reduces infrastructure requirements for LLM deployment

3. **Performance Analysis**
   - Communication no longer dominant bottleneck for FoE
   - Computation becomes new optimization target
   - Opens opportunity for compute-side optimizations

4. **Design Pattern Influence**
   - Per-head expert partitioning may inspire other cluster-aware architectures
   - Residual-based communication could apply to other dense-sparse hybrids

### State-of-the-Art Advances

- **Fastest MoE Inference**: FoE represents best-in-class latency for distributed MoE
- **Communication Efficiency**: 5.2× improvement is largest reported for full-scale models
- **Practical Deployment**: First system practical for production long-context inference
- **Scalability**: Linear scaling with model size, sublinear with node count

### Limitations and Open Questions

1. **Architectural Constraints**
   - Design tied to attention-based architectures
   - May not generalize to other sparse mixture paradigms
   - Cluster count limited by attention head count
   - Head count growth needed for very large clusters

2. **Load Balancing Questions**
   - Expert load imbalance across clusters not addressed
   - Dynamic load balancing during inference not explored
   - Optimal cluster sizing strategy unclear
   - Cross-cluster expert rebalancing mechanisms needed

3. **Fault Tolerance Gaps**
   - Cluster failure recovery not detailed
   - Trade-off between isolation and redundancy unexplored
   - Implications for multi-tenant serving unclear

4. **Generalization Questions**
   - Effectiveness with different MoE variants (sparse, expert choice, etc.)
   - Scaling to 1000+ GPU clusters unclear
   - Interaction with speculative decoding not studied
   - Cross-modal MoE (vision-language) applicability unexplored

## Code & Resources

### Primary Source
- **Paper Abstract**: https://arxiv.org/abs/2605.06206
- **PDF**: https://arxiv.org/pdf/2605.06206
- **HTML v1**: https://arxiv.org/html/2605.06206v1

### Related Implementation Resources

**MoE Frameworks and Libraries**
- **DeepSeek-MoE**: Large-scale MoE implementation reference
  - https://github.com/deepseek-ai/MoE-Infra
  
- **VLLM**: LLM serving system with MoE support
  - https://github.com/vllm-project/vllm
  - Recent versions support FoE-like optimizations
  
- **MegaBlocks**: Efficient MoE training and inference
  - https://github.com/stanford-futuredata/megablocks
  - Token-aware compression strategies

**Distribution Communication Libraries**
- **NCCL**: GPU communication library
  - https://github.com/NVIDIA/nccl
  - Essential for implementing FoE communication patterns

- **PyTorch Distributed**: Built-in PyTorch distributed training
  - All-reduce, broadcast operations needed for FoE

### Quick Start Guide

**Step 1: Architecture Understanding**
```python
# FoE key insight: Per-head expert clusters
# Each attention head gets dedicated experts
num_attention_heads = 32  # e.g., H = 32
total_experts = 256      # e.g., E = 256
experts_per_cluster = total_experts // num_attention_heads  # 8 experts/head
```

**Step 2: Cluster Assignment**
```python
# Map expert to cluster (head)
expert_to_cluster = expert_id // experts_per_cluster
token_routes_to = selected_experts  # Already cluster-aware

# Router output includes cluster information
cluster_ids = expert_to_cluster[selected_experts]
```

**Step 3: Communication Pattern**
```python
# Intra-cluster: local all-to-all (within GPU)
cluster_outputs = all_to_all_within_cluster(tokens, cluster_id)

# Inter-cluster: residual synchronization
residuals = [cluster_output for cluster in clusters]
synchronized_residuals = all_reduce(residuals)  # NCCL all-reduce
```

**Step 4: Integration with Inference Framework**
- Modify router to output cluster IDs alongside expert IDs
- Update dispatch logic to route per-cluster
- Replace expert communication with residual sync
- Profile communication vs. computation tradeoffs

### Compute Requirements

- **Development**: Single multi-GPU machine (8 GPUs minimum for development)
- **Full Evaluation**: 8+ node cluster with high-bandwidth interconnect
- **Deployment**: Depends on model and latency requirements:
  - 70B model: 2 nodes (16 GPUs)
  - 300B model: 8 nodes (64 GPUs)
  - Very large: Requires custom optimization

- **Network**: High-bandwidth interconnect critical (NVLink, InfiniBand)

## Related Work & Context

### Builds On
- Mixture of Experts Architecture (Lepikhin et al., 2021)
- Distributed Training Fundamentals (Dean & Ghemawat, 2008)
- Transformer Inference Optimization (Tighter, 2022; Dettmers et al., 2022)
- Expert Parallelism (Lepikhin et al., 2021; Shazeer et al., 2018)

### Related Research Areas

**MoE Optimization**
- LatentMoE: latent-space expert routing
- Piper: Pipeline-parallel MoE training
- Cross-Platform Fused MoE: GPU memory optimization

**Distributed Inference Systems**
- Ray Serve: General distributed inference framework
- vLLM: Efficient LLM serving with various parallelism strategies
- Speculative decoding: Complementary latency reduction approach

**Communication Optimization**
- NCCL: Efficient GPU collective communication
- Gradient Compression: Reducing communication in distributed training
- Communication-Computation Overlap: Pipelining techniques

### Future Research Directions

1. **Hierarchical Clustering**
   - Multi-level clusters for very large deployments
   - Adaptive cluster sizing based on workload
   - Dynamic cluster reorganization during inference

2. **Cross-Architecture Optimization**
   - FoE principles applied to other sparse-mixture paradigms
   - Integration with speculative decoding
   - Combination with other inference optimizations

3. **Hardware Co-Design**
   - Custom hardware for FoE communication patterns
   - Network-aware expert partitioning
   - Hardware support for cluster-aware routing

4. **Robustness and Reliability**
   - Fault tolerance in FoE clusters
   - Multi-tenant isolation
   - Load balancing under heterogeneous workloads

5. **Multi-Modal and Cross-Modal Applications**
   - Application to vision-language MoE models
   - Cross-modal token routing
   - Hybrid expert specialization

## Citation

```
@article{abdurrahman2026federation,
  title={Federation of Experts: Communication Efficient Distributed Inference for Large Language Models},
  authors={Abdurrahman, Muhammad Shahir and Deng, Chun and Mirhoseini, Azalia and Levis, Philip},
  journal={arXiv preprint arXiv:2605.06206},
  year={2026}
}
```
