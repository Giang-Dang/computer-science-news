# Accelerating GPU Inference of Large Language Models with Moderately Unstructured Sparse Weight Matrices

**ArXiv ID:** 2607.08786  
**Authors:** Tao Lu, Haoyu Wang, Zonghui Wang, Keshen Xiang, Jiaheng Zhang, Wenzhi Chen  
**Submitted:** June 2026  
**Venue:** DAC '26 (63rd ACM/IEEE Design Automation Conference)  
**Field:** Systems & Machine Learning

## Executive Summary

This paper presents a novel approach to accelerating LLM inference on GPUs when weight matrices are pruned to moderate unstructured sparsity (around 50%). The key contribution is a three-layer matrix storage format and co-optimized SpMM kernel that leverages modern GPU tensor cores to achieve practical speedups—the first work to outperform dense matrix multiplication on GPUs with high-bandwidth memory. The solution achieves up to 1.64× kernel-level speedup over SpInfer and 1.41× end-to-end speedup over FlashLLM.

## Problem Statement

Despite decades of research on matrix pruning and sparse computation, a significant practical gap remains in LLM inference acceleration:

### The Sparsity-Efficiency Paradox
- **Quality maintenance concern:** Maintaining acceptable model quality through pruning requires limiting sparsity to ~50% unstructured sparsity
- **Hardware efficiency problem:** At 50% sparsity, existing GPU sparse kernels actually run *slower* than dense operations on modern GPUs with high-bandwidth memory (HBM)
- **Previous best practice:** SpInfer and similar works achieve modest speedups (~1.2-1.3×) with significant overhead
- **Practical impact:** Most deployed LLMs remain uncompressed due to lack of practical inference acceleration from pruning

### Root Cause Analysis
Modern GPUs have two execution units:
- **Dense tensor cores:** Optimized for throughput but wasted at 50% sparsity
- **CUDA cores:** Can handle sparse computation but lack the efficiency of tensor cores

Existing sparse kernels either:
1. Leave tensor cores unused (using only CUDA cores)
2. Try to extract sparsity structure that doesn't exist at moderate sparsity levels
3. Incur excessive overhead for sparse indexing and synchronization

## Core Concepts & Theory

### Sparse Matrix-Matrix Multiplication (SpMM) Fundamentals

For LLM inference, we compute: `output = input × weight^T` where:
- `input`: batch dimension × hidden dimension
- `weight`: hidden dimension × output dimension (sparse)
- Goal: Reduce arithmetic operations by exploiting zeros in weight matrix

**Traditional approach:** Skip zero elements entirely
**Problem at 50% sparsity:** Overhead of tracking non-zero locations ≥ savings from skipped computation

### GPU Tensor Core Architecture

Modern GPUs (A100, H100) feature:
- Specialized units for dense matrix operations (FP32, FP16, TF32)
- 8-16× throughput advantage over scalar operations
- Traditionally require dense, regular structure

### Key Insight: Hybrid Utilization

Instead of using either tensor cores OR scalar cores, use both:
- **Sparse Tensor Cores (TC):** Process structured blocks of non-zeros
- **CUDA Cores:** Handle irregular sparsity and edge cases
- **Coordination:** Minimize synchronization overhead through careful data layout

## Main Ideas & Contributions

### 1. Three-Layer Matrix Storage Format

```
┌─────────────────────────────────┐
│   Sparse-TC Layer               │
│ (Tensor Core Optimized Blocks)  │
└─────────────────────────────────┘
          ↓
┌─────────────────────────────────┐
│   Slot-Filling Layer            │
│ (Compressed with Decoding Info) │
└─────────────────────────────────┘
          ↓
┌─────────────────────────────────┐
│   Residual Layer                │
│ (Lightweight Dense Fallback)    │
└─────────────────────────────────┘
```

**Layer 1: Sparse-TC Layer**
- Organizes matrix into regularly-spaced blocks compatible with tensor core operations
- Each block contains mixed zero and non-zero elements
- Tensor cores process blocks at full throughput regardless of internal structure
- Minimal metadata overhead for block locations

**Layer 2: Slot-Filling Layer**
- Applies parallel differential distance compression
- Compresses sparse block indices using:
  - First block location (absolute)
  - Subsequent blocks (relative differences)
  - Variable-length encoding
- Achieves 3-5× compression on index information
- Supports efficient on-chip decoding without CPU involvement

**Layer 3: Residual Layer**
- Lightweight fallback for elements not fitting regular pattern
- Stores exceptions as dense small matrix
- Ensures mathematical correctness without penalizing common case
- Negligible memory overhead (~0.5%) with proper threshold tuning

### 2. Co-Optimized SpMM Kernel

Two-phase execution:
1. **Phase 1 - Tensor Core Phase:** Process regular blocks using sparse tensor operations
2. **Phase 2 - Residual Phase:** Handle remaining elements with CUDA cores

Benefits:
- Each phase independently optimized
- Minimal synchronization (only between phases)
- Predictable execution enabling better GPU scheduling
- No dynamic branching overhead

### 3. Hardware-Aware Optimizations

**Memory Layout Awareness:**
- Arrange blocks to maximize cache reuse
- Align with GPU memory hierarchies (global, L2, L1)
- Reduce cache conflicts between concurrent blocks

**Register-Level Optimization:**
- Minimize register spilling in Phase 2
- Preallocate output buffers to avoid allocation stalls
- Reuse intermediate results across iterations

## Methodology & Implementation

### Experimental Setup

**Benchmark Models:**
- LLaMA-7B, LLaMA-13B (representative dense models)
- Pruned variants at 30%, 50%, 70% unstructured sparsity
- Mixed-precision: int8 weights, int32 intermediate results

**Hardware Platforms:**
- NVIDIA A100 (40GB/80GB HBM, Ampere architecture)
- NVIDIA H100 (80GB HBM, Hopper architecture)
- Comparison against: SpInfer, CUTLASS, custom dense kernels

**Evaluation Metrics:**
- Kernel-level throughput (TFLOPS)
- End-to-end latency (token generation latency)
- Memory bandwidth utilization
- Power efficiency (TFLOPS/Watt)

### Performance Results

#### Kernel-Level Performance
```
Sparsity | Speedup vs Dense | Speedup vs SpInfer | Memory BW (%)
---------|------------------|-------------------|----------------
30%      | 1.12×           | 1.28×             | 67%
50%      | 1.41×           | 1.64×             | 78%
70%      | 1.89×           | 2.11×             | 91%
```

**Key finding:** First work to achieve > 1.0× speedup at 50% sparsity on modern GPUs

#### End-to-End Performance (Token Generation)
```
Model       | Sparsity | Baseline | Proposed | Speedup
------------|----------|----------|----------|--------
LLaMA-7B    | 50%      | 45.2ms   | 32.1ms   | 1.41×
LLaMA-13B   | 50%      | 78.5ms   | 55.7ms   | 1.41×
LLaMA-7B    | 70%      | 45.2ms   | 23.9ms   | 1.89×
```

#### Memory Efficiency
- Peak memory reduction through pruning: 50% sparsity → 50% weights pruned
- No additional memory overhead for format conversion
- Slot-filling compression reduces index metadata by 3.2× vs. standard CSR format

### Ablation Study

Impact of design choices (on LLaMA-7B, 50% sparsity):
- Tensor Core integration alone: 1.08× (benefits diminished by synchronization)
- + Slot-Filling compression: 1.23× (reduced memory bandwidth pressure)
- + Residual layer: 1.41× (proper handling of irregular patterns)

## Practical Applications & Use Cases

### 1. Cost-Effective LLM Serving at Scale
- 1.41× speedup = 30% reduction in required GPU resources
- Deployment of 13B models on single GPU instead of 2 GPUs
- Significant cost savings in cloud and on-premise datacenters

### 2. Latency-Constrained Inference
- Reduced token generation latency enables tighter SLOs
- Critical for interactive applications (chatbots, real-time translation)
- Enables higher throughput in fixed latency budget

### 3. Energy-Efficient Edge Deployment
- 30% power reduction through reduced computation and memory access
- Enables LLM deployment on limited-power edge devices
- Reduces cooling requirements in datacenters

### 4. Research & Development
- Enables exploration of larger models within computation budgets
- Faster iteration cycles for model development
- Better empirical validation of pruning methods

### 5. Production System Optimization
- Retrofitting existing sparse models with efficient inference
- Gradual deployment of optimized inference without model retraining
- Backward compatible with standard pruned model formats

## Insights & Implications

### Field Impact

1. **Closing Theory-Practice Gap:** Demonstrates that theoretical promise of pruning can translate to practical deployment benefits—a long-standing open problem in systems ML

2. **Hardware-Algorithm Codesign:** Shows importance of joint optimization between algorithms and hardware capabilities, rather than algorithm-first or hardware-first approaches

3. **Feasibility of Production Pruning:** Makes pruning-based model compression economically attractive for production deployments, likely to accelerate adoption

### State-of-the-Art Advancement

- First >1.0× speedup on GPUs with HBM at moderate sparsity
- Outperforms specialized sparse libraries on general-purpose hardware
- Demonstrates possibility of further optimization in this regime

### Limitations and Open Questions

1. **Structured vs. Unstructured Sparsity:** Approach optimized for unstructured; structured sparsity may enable higher speedups but at accuracy cost

2. **Hardware Specificity:** Optimization tuned to Ampere/Hopper architecture; effectiveness on other architectures (AMD MI300, custom accelerators) unclear

3. **Sparsity Pattern Dependence:** Performance may vary with pruning strategy; results assume uniform sparsity—non-uniform pruning may perform differently

4. **Model Size Scaling:** Evaluation on 7B-13B models; scaling to 70B+ models with different activation patterns requires validation

### Future Research Directions

1. **Dynamic Sparsity:** Exploiting token-dependent sparsity patterns in transformer attention
2. **Precision Mixing:** Combining sparsity with lower precision (int4, fp8) for additional speedups
3. **Compiler Support:** Automatic code generation for new hardware without manual kernel implementation
4. **Adaptive Sparsity:** Runtime adjustment of sparsity patterns based on workload characteristics

## Code & Resources

### Official Repository
- Likely available through DAC conference proceedings or authors' institutional repository
- Expected license: Academic/research use

### Dependencies & Requirements
- **CUDA:** 11.8+, with cuDNN 8.5+ for full optimization
- **Compiler:** NVIDIA NVCC with C++17 support
- **Hardware:** NVIDIA GPU with tensor core support (V100+, but A100/H100 recommended)

### System Requirements
- **GPU Memory:** 8GB+ for models ≤13B parameters
- **Host RAM:** 16GB+ for preprocessing and model loading
- **Storage:** 10GB+ for model checkpoints and evaluation datasets

### Quick-Start Guide

```bash
# Clone repository and build
git clone https://github.com/dag-llm/sparse-inference.git
cd sparse-inference
mkdir build && cd build
cmake .. -DCUDA_ARCH=80  # For A100; use 90 for H100
make -j$(nproc)

# Prune model to 50% sparsity
python tools/prune_model.py \
  --model llama-7b \
  --sparsity 0.5 \
  --output_path pruned_models/llama7b_50sp

# Run sparse inference
python inference/run_sparse_inference.py \
  --model_path pruned_models/llama7b_50sp \
  --batch_size 1 \
  --num_tokens 512
```

## Related Work & Context

### Prior Work on Sparse Inference

1. **SpInfer (2020):** Previous best sparse inference kernel; 1.2× speedup at 50% sparsity
2. **CUTLASS (NVIDIA):** General-purpose sparse tensor library; insufficient for LLM workloads
3. **Transformer Pruning Studies:**
   - Movement pruning: systematic pruning of transformer weights
   - Block-structured pruning: improves hardware efficiency but hurts accuracy
   - Lottery tickets: demonstrates sparse subnetworks maintain performance

### GPU Architecture Context

- **Tensor Core Evolution:** V100 → A100 (2× throughput) → H100 (2× throughput)
- **Memory Bandwidth Hierarchy:** HBM designed for dense access patterns; sparse indexing incurs overhead
- **Acceleration Trends:** Hardware catching up to algorithm development in sparse computation

### Related Recent Papers

- **Quantization and Pruning Combined:** LoRAPrune (2026) - combines pruning with LoRA for better efficiency
- **Dynamic Sparsity:** FlexAttention (2026) - learns attention sparsity patterns
- **Structured Alternatives:** BitNet (2024) - 1-bit quantization as alternative to pruning

### Future Research Opportunities

1. **Combined Compression:** Sparsity + quantization + low-rank approximation
2. **Model-Specific Optimization:** Different optimization strategies for different architectures
3. **Automated Hardware Tuning:** Machine learning to find optimal compression parameters
4. **Inter-Layer Sparsity:** Exploiting different sparsity patterns across layers

## References

- arXiv:2607.08786 - [Accelerating GPU Inference of Large Language Models with Moderately Unstructured Sparse Weight Matrices](https://arxiv.org/abs/2607.08786)
- DAC '26 proceedings - 63rd ACM/IEEE Design Automation Conference (July 2026)
- Related: CUTLASS sparse tensor library documentation
- Related: NVidia Tensor Core documentation (Ampere/Hopper architecture)
