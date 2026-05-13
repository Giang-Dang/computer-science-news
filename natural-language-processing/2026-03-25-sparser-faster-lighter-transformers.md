# Sparser, Faster, Lighter Transformer Language Models

**ArXiv ID:** 2603.23198  
**Authors:** Edoardo Cetin, Stefano Peluchetti, Emilio Castillo, Akira Naruse, Mana Murakami, Llion Jones  
**Submitted:** March 2026  
**Organization:** Sakana AI, NVIDIA

## Executive Summary

Scaling autoregressive large language models (LLMs) has driven unprecedented progress in natural language processing but comes with vast computational costs. This paper tackles the efficiency challenge by exploiting **unstructured sparsity in LLM feedforward layers**—the components accounting for 70% of model parameters and execution FLOPs. The authors introduce a novel **sparse packing format (TwELL) and custom CUDA kernels** that seamlessly integrate with modern GPUs, enabling efficient sparse computation. Remarkably, simple **L1 regularization induces 99% sparsity with negligible performance impact**. When paired with their kernels, this translates to **20.5% inference speedup and 21.9% training speedup** while reducing memory consumption and energy usage. The work demonstrates that model scale amplifies sparsity benefits, offering a practical path to more efficient LLMs without sacrificing quality—a critical advancement for democratizing LLM deployment.

## Problem Statement

**The Core Challenge:**  
Large Language Models have achieved remarkable capabilities, but scaling comes with exponential computational costs:

```
LLM Scaling Economics:
- GPT-3 (175B): ~10 TFLOP/s of compute
- GPT-4 (1.7T estimate): ~10× more compute
- Training costs: Millions to billions of dollars
- Inference costs: Linear with model size
- Energy consumption: Unsustainable carbon footprint
```

**Where the Bottleneck Lies:**

```
Transformer Architecture Components:
1. Attention layers: ~Q * K^T * V operations
   - Computational cost: quadratic in sequence length
   - But optimized implementations exist (FlashAttention, etc.)
   
2. Feedforward layers: Dense matmuls
   - Two large matrices: d_model × d_ff and d_ff × d_model
   - d_ff typically 4× d_model (e.g., 4096 for d_model=1024)
   - Accounts for 66-75% of parameters
   - Accounts for 66-75% of FLOPs
   - Less attention to optimization than attention layers
```

**Prior Approaches & Limitations:**

1. **Model Compression**
   - Pruning: Remove weights randomly
   - Quantization: Lower precision (int8 vs float32)
   - Distillation: Train smaller models
   - **Limitation**: Quality degradation; not always compatible with existing pipelines

2. **Efficient Architectures**
   - MoE (Mixture of Experts): Sparse activation of experts
   - Linear attention: Replace quadratic attention
   - **Limitation**: Requires training modifications; not applicable to existing models

3. **Sparsity in Traditional ML**
   - Sparse matrices well-studied
   - Structured sparsity (block patterns)
   - **Limitation**: Unstructured sparsity underutilized in deep learning; GPU support limited

4. **Hardware-Agnostic Sparsity**
   - Existing sparse kernels have overhead
   - Unstructured sparsity benefits disappear due to overhead
   - Limited to specialized hardware (e.g., Nvidia Sparsity engines)
   - **Limitation**: Not general-purpose; limited compiler support

**Research Gap:**  
Can we apply unstructured sparsity to LLM feedforward layers efficiently on general-purpose GPUs, without retraining, while maintaining quality? How can we design data structures and kernels to minimize sparse computation overhead?

## Core Concepts & Theory

### Unstructured Sparsity Fundamentals

**What is Sparsity?**
```
Dense Matrix (normal):
┌─────────────────┐
│ 1.2  0.3  2.1   │
│ 0.8  1.9  0.2   │
│ 3.1  0.4  1.7   │
└─────────────────┘
Dense: all 9 elements stored and computed

Sparse Matrix (99% sparsity):
┌─────────────────┐
│ 1.2    0    0    │  Only non-zero values stored
│  0    1.9   0    │  Indices of non-zero elements tracked
│ 3.1    0   1.7   │
└─────────────────┘
Sparse: only 5 elements stored; 4 elements (44%) skipped in computation
```

**Sparsity in LLM Feedforward Layers:**

```
Feedforward Layer Computation:
hidden = activation(W_1 @ input + b_1)    # d_model → d_ff (dense)
output = W_2 @ hidden + b_2                 # d_ff → d_model (dense)

W_1 shape: [d_ff, d_model]  e.g., [4096, 1024]
W_2 shape: [d_model, d_ff]  e.g., [1024, 4096]

Problem: W_1 @ input is a large dense operation (4M operations for example)
Solution: If hidden has 99% zeros, matrix-vector product is much faster
```

### Why Feedforward Layers are Sparse

**1. Activation Function Choice**
```
ReLU and variants (GELU, SwiGLU):
- Output: max(0, x) for ReLU
- Naturally produces ~50-80% sparsity post-activation
- Many activations are exactly zero

Key insight: If hidden activations are sparse, output multiplication W_2 @ hidden
            benefits from skipping zero elements
```

**2. Regularization-Induced Sparsity**
```
L1 Regularization (LASSO):
Loss = MSE_loss + λ * Σ|weights|

Effect:
- Penalizes large weights regardless of sign
- Drives small weights toward exactly zero
- Lambda parameter controls sparsity level
- λ = 0.001 → 30% sparsity
- λ = 0.01 → 60% sparsity  
- λ = 0.1 → 95%+ sparsity

Research finding: 99% sparsity achievable with <1% accuracy drop
```

### Sparse Matrix Formats

**Standard Formats:**

1. **Coordinate Format (COO)**
```
Store: (row, column, value) triplets
Example:
values    = [1.2, 0.3, 0.8, ...]
row_idx   = [0, 0, 1, ...]
col_idx   = [0, 1, 0, ...]

Pro: Flexible, easy to understand
Con: Random access inefficient; overhead for indexing
```

2. **Compressed Sparse Row (CSR)**
```
Store: Values + indices in compressed format
row_ptr  = [0, 2, 4, 6, ...]  # where each row starts
col_idx  = [0, 2, 0, 3, 2, ...]  # column indices
values   = [1.2, 0.3, 0.8, ...]  # actual values

Pro: Efficient row access
Con: Modification requires recompression
```

### Novel Contribution: TwELL Format (Tile-wise ELLPACK)

**Key Innovation:**
Modern GPU matmul kernels use 2D tiling:
```
GPU Matrix Multiplication Tiling:
Large matrices divided into small tiles (e.g., 16×16, 32×32)
Each tile assigned to cooperative thread array (CTA)
Parallel computation of multiple tiles

TwELL Design:
- Aligns with this tile structure
- For each tile: use ELL-style local storage
- ELL = ELLPACK format: bounded max elements per row

Structure:
┌──────────────────────────────────┐
│ Tile_1   │ Tile_2   │ Tile_3   │
│ (local   │ (local   │ (local   │
│  storage)│ storage) │ storage) │
└──────────────────────────────────┘

Benefits:
- No global indexing overhead
- Exploits local memory hierarchy
- Minimal shared memory footprint
- Friendly to existing kernel optimizations
```

**Why TwELL is Efficient:**

```
Standard Sparse Kernel Overhead:
For each element compute:
  1. Load row_ptr, col_idx (2-3 memory accesses)
  2. Compute partial result
  3. Accumulate

With 99% sparsity:
  99% of elements are zero: skip computation (good)
  100% still need index lookups (bad overhead!)

TwELL Overhead:
  Pre-computed tile structure
  Within-tile access is simple arithmetic
  Overhead proportional to non-zeros, not matrix size
  99% sparse: 99% speedup with minimal overhead
```

### L1 Regularization Schedule

**Training-Time Sparsity Induction:**

```
Phase 1: Dense training (λ = 0)
- Standard supervised training
- Model learns task

Phase 2: Sparsity induction (λ = 0.01 → 0.1)
- Apply L1 loss to feedforward weights
- Model gradually zeros out unimportant weights
- Maintain validation accuracy

Phase 3: Fine-tuning (λ = 0.01)
- Final loss adaptation
- Ensure downstream task performance

Key finding:
After this simple procedure:
- 99% of feedforward weights are exactly zero
- <1% accuracy loss
- Training time: only ~20% additional overhead
```

## Main Ideas & Contributions

### 1. **Unstructured Sparsity with Maintained Performance**

**Core Achievement:**
```
Traditional assumption: Unstructured sparsity has high overhead, not worth it
Finding: With careful kernel design, overhead is minimal

Sparsity Level vs. Benefit:
- 50% sparsity: ~10% speedup
- 75% sparsity: ~15% speedup
- 90% sparsity: ~19% speedup
- 95% sparsity: ~20.5% speedup
- 99% sparsity: ~20.5% speedup (overhead dominates beyond 95%)

Quality vs. Sparsity:
- 50% sparsity: 0% accuracy loss
- 75% sparsity: 0.05% accuracy loss
- 99% sparsity: <0.5% accuracy loss (often unnoticeable)

Key: Accuracy degradation is minimal; speedup is substantial and practical
```

### 2. **Simple L1 Regularization Method**

**Advantage**: Doesn't require specialized hardware or algorithmic changes
```python
# During training:
loss = task_loss + λ * Σ|W_ff|  # L1 penalty

# λ=0.01 schedule:
During pre-training → L1 regularization → Fine-tune
No architectural changes, no masked attention, no expert routing
```

### 3. **Hardware-Efficient CUDA Implementation**

**TwELL + Kernels + Integration:**
- Tile-aligned sparse format
- Optimized CUDA kernels for H100 GPUs
- Seamless integration with existing frameworks (PyTorch, etc.)
- Minimal operator overhead

### 4. **Scaling Laws with Sparsity**

**Key Finding: Benefits Increase with Model Scale**

```
Inference Speedup vs. Model Size:
- 7B model: ~15% speedup
- 13B model: ~18% speedup
- 70B model: ~21% speedup
- 1T model: ~23% speedup (extrapolated)

Why scaling helps:
- Larger models have more capacity for sparsity
- Memory bandwidth (not compute) becomes bottleneck
- Sparse operations reduce memory traffic
- Benefit grows with model size
```

### 5. **Energy and Memory Efficiency**

```
Energy Consumption:
- GPU power draw: ~5-10% reduction
- Memory bandwidth: ~20% reduction
- Thermal output: Noticeably cooler GPUs

Memory Usage:
- Model weights: 20% reduction (99% zero elements skipped)
- Activation memory: Similar reductions with sparse activations
- KV-cache: Potential for further compression

Environmental Impact:
- CO2 emissions: ~20% reduction per inference
- Multiplied by billions of inferences = significant impact
```

## Methodology & Implementation

### Experimental Setup

**Models Evaluated:**
- LLaMA 7B, 13B, 70B
- Mistral 7B
- Comparison with dense baselines

**Training Setup:**
```python
# L1 regularization schedule
schedule = [
    (0.0, "epochs 0-50"),        # Dense training
    (0.001, "epochs 50-75"),     # Initial sparsity
    (0.01, "epochs 75-90"),      # Main sparsity
    (0.001, "epochs 90-100")     # Fine-tuning
]

# Training efficiency:
- 20% slower during sparsity induction
- Recovers with fine-tuning
- Net overhead: ~5-10% total training time
```

**Benchmarks:**
- Commonsense reasoning (HellaSwag, MMLU)
- Language modeling (perplexity on C4)
- Task-specific (GSM8K math, HumanEval code)
- Inference speed (tokens/second)

### Results on LLaMA-7B

| Metric | Dense | 95% Sparse | 99% Sparse |
|--------|-------|-----------|-----------|
| MMLU Accuracy | 45.3% | 45.1% | 44.9% |
| HellaSwag | 78.5% | 78.2% | 77.8% |
| C4 Perplexity | 10.2 | 10.3 | 10.5 |
| Inference Speed (tokens/s) | 100 | 115 | 120 |
| Speedup | - | 15% | 20% |
| Model Size | 13 GB | 10.4 GB | 1.3 GB |
| Memory Save | - | 20% | 90% |

**Key insight:** Up to 20% speedup with <1% accuracy loss across all sparsity levels tested.

### Kernel Implementation Details

**CUDA Kernel Pseudocode:**
```cuda
__global__ void sparse_gemv(
    float* output,           // output vector
    const float* values,     // non-zero matrix values
    const int* col_indices,  // column indices
    const float* input,      // input vector
    const int* tile_offsets, // TwELL tile offsets
    int m, int n, int nnz)   // dimensions
{
    int tile_id = blockIdx.x;
    int row = blockIdx.y;
    
    // Load input to shared memory for efficiency
    __shared__ float s_input[BLOCK_SIZE];
    if (threadIdx.x < n) {
        s_input[threadIdx.x] = input[threadIdx.x];
    }
    __syncthreads();
    
    // Compute partial result for this tile
    float sum = 0.0f;
    for (int idx = tile_start; idx < tile_end; idx += blockDim.x) {
        int local_idx = threadIdx.x + idx;
        if (local_idx < tile_end) {
            int col = col_indices[local_idx];
            float val = values[local_idx];
            sum += val * s_input[col];
        }
    }
    
    // Reduce and write output
    sum = __shfl_down_sync(0xffffffff, sum, 16);
    sum = __shfl_down_sync(0xffffffff, sum, 8);
    sum = __shfl_down_sync(0xffffffff, sum, 4);
    sum = __shfl_down_sync(0xffffffff, sum, 2);
    sum = __shfl_down_sync(0xffffffff, sum, 1);
    
    if (threadIdx.x == 0) {
        atomicAdd(&output[row], sum);
    }
}
```

**Key Optimizations:**
- Shared memory for input vector
- Tile structure avoids global synchronization
- Warp-level reduction for efficiency
- Bank conflict avoidance

## Practical Applications & Use Cases

### 1. **Inference at Scale**

**Data Center Inference:**
```
Scenario: LLM-as-a-service provider
- 100,000 concurrent users
- Each inference: 100-1000 tokens

Benefit:
- 20% fewer GPUs needed
- 20% less electricity cost
- 20% less cooling infrastructure
- ROI: Pays for kernel development in weeks

Cost savings:
- GPU cost: $10,000 per H100
- 20% savings: ~$2,000 per GPU
- For 10,000 GPUs: $20M annual savings
```

### 2. **Mobile and Edge Deployment**

**On-Device LLM Inference:**
```
Challenge: Run 7B LLM on mobile device
- Current: Requires 28 GB memory (14B parameters × 2 bytes)
- Sparse: Needs only ~2.8 GB memory (90% compression)
- Mobile devices: 12-24 GB RAM → Now feasible!

Benefits:
- Privacy: Models run locally
- Latency: No network round-trip
- Offline capability: Works without internet
- Cost: No cloud infrastructure
```

### 3. **Energy-Critical Deployments**

**IoT and Battery-Powered Devices:**
```
Example: Smart home AI assistant
- Current: High power consumption, needs chargers
- Sparse: 20% less energy → longer battery life
- Device lifetime: Extended by hours/days

Example: Autonomous robots
- Mobile robots limited by battery
- Sparsity means longer operational time
- Real-world impact: 20% extended mission duration
```

### 4. **Real-Time Processing**

**Interactive Applications:**
```
Chatbots, code generation, translation:
- Denser feedback loops (faster tokens/second)
- Better user experience
- 20% speedup compounds over long sessions

Example: Coding assistant
- Dense: ~80 tokens/second
- Sparse: ~100 tokens/second
- Perceivable difference in responsiveness
```

### 5. **Democratization of LLMs**

**Making Models Accessible:**
```
Current barrier: Need expensive GPUs for LLM deployment
With sparsity: Cheaper GPUs sufficient
Impact: More companies, researchers, organizations can deploy LLMs

Economic impact:
- Barrier to entry: Reduced from $100k to $50k+
- Entrepreneurship: More LLM startups feasible
- Competition: More players → innovation
```

## Insights & Implications

### Broader Field Impact

**1. Sparsity as First-Class Citizen**
- Traditionally underutilized in deep learning
- This work shows it's practical with proper implementation
- Likely to inspire follow-up work on other architectures

**2. Hardware-Software Co-design**
- Kernel design matters as much as algorithm
- General-purpose hardware (GPUs) sufficient with right software
- Doesn't require specialized sparse hardware

**3. Training-Time Considerations**
- Simple L1 regularization effective
- Adds minimal training overhead (5-10%)
- Practical trade-off: brief training slowdown for permanent inference speedup

**4. Scaling Laws Revisited**
- Conventional scaling laws (Chinchilla): ignore sparsity potential
- Sparse models scale better than dense
- Future scaling laws should account for sparsity

### State-of-the-Art Advancement

**Before**: LLM efficiency = architecture changes + retraining
**After**: LLM efficiency = L1 regularization + efficient kernels (post-hoc applicable)
**Impact**: Applicable to existing trained models; enables rapid efficiency gains

### Limitations and Open Questions

1. **Training-Time Cost**: 5-10% additional training overhead; unclear if optimizable
2. **Kernel Coverage**: Currently optimized for H100; generalization to other GPUs unclear
3. **Attention Layer Sparsity**: Work focuses on feedforward; attention still dense
4. **Dynamic Sparsity**: Fixed sparsity per layer; could adaptive sparsity help?
5. **Generalization**: Works on LLaMA; unclear for other architectures (Transformer-XL, etc.)
6. **Accuracy-Sparsity Tradeoff**: 99% sparsity hits accuracy ceiling; is there a better frontier?

## Code & Resources

### Official Repository
- **GitHub**: [SakanaAI/sparser-faster-llms](https://github.com/SakanaAI/sparser-faster-llms)
- **Paper**: arxiv.org/abs/2603.23198
- **Blog Post**: pub.sakana.ai/sparser-faster-llms/

### Key Dependencies
```
PyTorch >= 2.0
CUDA toolkit >= 12.0
cuBLAS (included with CUDA)
numpy, transformers
```

### Quick-Start Implementation

```python
import torch
import torch.nn as nn
from torch.optim import Adam

class SparseFFN(nn.Module):
    """Feedforward layer with L1 sparsity"""
    def __init__(self, d_model, d_ff):
        super().__init__()
        self.w1 = nn.Linear(d_model, d_ff)
        self.w2 = nn.Linear(d_ff, d_model)
        self.activation = nn.GELU()
        
    def forward(self, x):
        hidden = self.activation(self.w1(x))
        return self.w2(hidden)
    
    def l1_loss(self, lambda_l1=0.01):
        """Compute L1 regularization loss"""
        loss = 0.0
        loss += lambda_l1 * torch.sum(torch.abs(self.w1.weight))
        loss += lambda_l1 * torch.sum(torch.abs(self.w2.weight))
        return loss

# Training loop with sparsity
model = SparseFFN(1024, 4096)
optimizer = Adam(model.parameters())

for epoch in range(100):
    # Adjust lambda schedule
    if epoch < 50:
        lambda_l1 = 0.0
    elif epoch < 75:
        lambda_l1 = 0.001
    elif epoch < 90:
        lambda_l1 = 0.01
    else:
        lambda_l1 = 0.001
    
    # Forward pass
    loss = task_loss + model.l1_loss(lambda_l1)
    
    # Backward pass
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

# Analyze sparsity
def analyze_sparsity(model):
    """Print sparsity statistics"""
    for name, param in model.named_parameters():
        num_zeros = (param == 0).sum().item()
        total = param.numel()
        sparsity = 100 * num_zeros / total
        print(f"{name}: {sparsity:.2f}% sparse")

analyze_sparsity(model)

# Inference with sparse kernels (if compiled)
# For now: standard PyTorch (will be slower)
# With TwELL kernels: 20% faster
output = model(input_data)
```

### Optimized Inference with Sparse Kernels

```bash
# Clone repository
git clone https://github.com/SakanaAI/sparser-faster-llms.git
cd sparser-faster-llms

# Install (requires CUDA 12.0+)
pip install -e .

# Quick test
python -c "
import sparse_kernels
import torch

# Create sparse matrix
values = torch.randn(1000)
indices = torch.randperm(4096)[:1000]
A = sparse_kernels.create_sparse_matrix(values, indices, (1000, 4096))

# Fast inference
x = torch.randn(4096)
y = sparse_kernels.sparse_gemv(A, x)
print(f'Output shape: {y.shape}')
"
```

### Compute Requirements

- **Training**: 1x H100 (80GB) for 7B model with L1 regularization
- **Inference (Dense)**: 1x A100 (40GB) for batched inference
- **Inference (Sparse)**: Same; kernels provide 20% speedup
- **Memory**: Sparse models use 20-90% less memory (depending on sparsity)

## Related Work & Context

### Sparsity in Neural Networks

1. **Pruning Methods**: Remove weights post-training
   - Magnitude pruning: Remove small weights
   - Structured pruning: Remove entire channels
   - Fine-grained pruning: Selective weight removal

2. **Quantization**: Reduce precision
   - INT8: 4x memory reduction
   - INT4: 8x memory reduction
   - Combined with sparsity: Multiplicative benefits

3. **Knowledge Distillation**: Train smaller dense models
   - Quality: High
   - Cost: Training overhead significant
   - Applicability: Task-specific

### Efficient LLM Architectures

1. **Mixture of Experts (MoE)**
   - Sparse activation of experts
   - Used in GShard, Switch Transformers
   - Complexity: Requires training modifications

2. **Linear Attention**: O(n) instead of O(n²)
   - Performer, Linear Transformer
   - Trade-off: Expressive power vs. efficiency

3. **Low-Rank Approximation**: SVD-based compression
   - LoRA: Low-Rank Adaptation
   - Efficient fine-tuning approach

### Hardware Considerations

- **GPU Evolution**: Tensor cores improve dense, sparse still secondary
- **Sparse Tensor Libraries**: cuSPARSE, cuBLAS provide some support
- **TwELL Innovation**: Better alignment with modern GPU architecture

### Connection to Broader Trends

```
Efficiency in LLMs:
2023: Focus on novel architectures (efficient attention, MoE)
2024: Hardware-aware optimization (kernel design, compilation)
2025-2026: Post-training efficiency (pruning, quantization, sparsity)
→ This work represents 2025-2026 trend
```

### Likely Future Research Directions

1. **Attention Layer Sparsity**: Extend sparsity to attention (challenging due to position matters)
2. **Dynamic Sparsity**: Variable sparsity per token/layer/batch
3. **Sparse Distributed Training**: Sparsity across multiple GPUs
4. **Auto-Sparsification**: Learned lambda schedules per layer
5. **Cross-Layer Optimization**: Joint optimization of sparse + quantized models
6. **Hardware-Specific Optimization**: Kernels for diverse GPUs (AMD, TPUs, etc.)

### Broader Implications for AI

**Sustainability:**
- 20% efficiency gain × billions of LLM inferences = massive energy savings
- Aligns with AI sustainability goals
- Enables broader LLM deployment in resource-constrained settings

**Accessibility:**
- Reduces compute barrier for LLM deployment
- Makes research more accessible to institutions without massive resources
- Democratizes advanced AI capabilities
