# Efficient Pre-Training with Token Superposition

**ArXiv ID**: [2605.06546](https://arxiv.org/abs/2605.06546)  
**Authors**: Bowen Peng, Théo Gigant, Jeffrey Quesnelle (Nous Research)  
**Published**: May 7, 2026  
**Venue**: Research Paper  
**Field**: Machine Learning, LLM Pre-training, Training Efficiency

---

## Executive Summary

Token-Superposition Training (TST) is a remarkably simple yet effective method that delivers **2-3× wall-clock speedup in LLM pre-training** without modifying model architecture, optimizer, tokenizer, data, or parallelism strategies. The core insight: during the early training phase, combine many contiguous tokens into single "bags" and train with a modified multi-hot cross-entropy (MCE) objective; after 20-40% of training, revert to standard next-token prediction. Nous Research demonstrates consistent 2.5× speedups across 270M to 10B parameter models using standard frameworks (PyTorch, TorchTitan) and existing fused kernels. This work has immediate practical impact: it is a drop-in method requiring no infrastructure changes, making it ideal for production pre-training pipelines.

---

## Problem Statement

### The Pre-Training Time Problem

As of 2026, training state-of-the-art language models is computationally prohibitive:
- **10B parameter model**: 5-8 weeks on 64 H100 GPUs (~$1M+ in compute)
- **100B parameter model**: 4-6 months on 256+ H100 GPUs (~$10M+ in compute)
- **Frontier models (1T+)**: $10-20 billion in compute, months of wall-clock time

While FLOPs matter, wall-clock time has its own cost structure:
- **Hardware rental**: Charged per hour, not per FLOP
- **Opportunity cost**: Delayed model deployment = missed market window
- **Research velocity**: Longer training = fewer iterations per quarter

A 2.5× speedup at matched FLOPs translates directly to:
- 2.5× fewer GPU-hours (proportional cost reduction)
- 2.5× faster training cycle (faster iteration)
- 2.5× lower energy consumption

### Prior Efficiency Approaches

Existing methods for training speedup fall into several categories:

**1. Sparse Training**
- Prune connections, activations, or gradients
- Requires custom kernels, modifies architecture
- Wall-clock gains modest (1.2-1.5×) due to kernel overhead

**2. Token Merging / Token Pruning**
- Merge or remove low-importance tokens mid-training
- Modifies tokenizer or requires detection mechanism
- Incompatible with standard training pipelines

**3. Curriculum Learning**
- Start with easier data, progress to harder
- Requires data annotation or complexity estimation
- Modest gains (1.1-1.3×), orthogonal to TST

**4. Distributed Training Optimizations**
- Gradient checkpointing, mixed precision, pipeline parallelism
- Already standard; saturated improvements
- Further gains require architecture redesign

### The TST Insight

**Key Observation**: Early training is redundant. A model learns token-to-token dependencies before learning global semantic structure.

**Corollary**: Why predict every token when predicting "bags of tokens" teaches similar structure with fewer forward passes?

**Implication**: Superpose tokens (combine multiple into one), train, then recover individual token predictions—all with existing kernels.

---

## Core Concepts & Theory

### Phase 1: Superposition (20-40% of Training)

In the superposition phase:
1. Group contiguous tokens into "bags" (e.g., 2-4 tokens per bag)
2. Compute embeddings for each token
3. Average embeddings to create bag representation
4. Pass through model (same architecture, no changes)
5. Predict next bag using modified loss

**Mathematical Formulation**:

Given token sequence: `[t_1, t_2, t_3, t_4, t_5, t_6, ...]`

Standard training: Predict `t_2` from `t_1`, predict `t_3` from `[t_1, t_2]`, etc.

TST superposition (bag_size=2):
- Bag B_1 = avg_embed(t_1, t_2)
- Bag B_2 = avg_embed(t_3, t_4)
- Predict B_2 from B_1
- (loses some intermediate structure, but similar learning signal)

**Embedding Averaging**:
```
bag_embed = (embed(t_1) + embed(t_2)) / 2
```

Simple but effective. No learned mixing weights; averaging is sufficient.

### Multi-Hot Cross-Entropy (MCE) Objective

Standard cross-entropy loss predicts a single token:

```
L_CE = -log(P(t_next))
```

Multi-hot variant predicts all tokens in next bag:

```
L_MCE = sum_over_tokens_in_bag(-log(P(t_i)))
       = sum of ordinary CE terms for each token
```

**Key Insight**: MCE loss is just a sum of CE terms. Reuses existing fused cross-entropy kernels in PyTorch, JAX, etc.

**Why It Works**:
- Scales linearly with bag size
- No gradient computation overhead
- Compatible with all existing optimization techniques
- No auxiliary heads or projection layers needed

### Phase 2: Recovery (60-80% of Training)

After superposition phase, revert to standard next-token prediction:
- Model has learned useful features from bag-level structure
- Fine-grained token dependencies learned quickly
- Converges in remaining ~50-70% of training

**Why Recovery Works**:
1. Model has learned high-level semantic structure (from bags)
2. Fine-tuning on individual tokens converges faster
3. Initialization from bag-learned weights provides advantage
4. Minimal additional training overhead

**Convergence Behavior**:
- Superposition phase: Steeper loss reduction (fewer forward passes)
- Recovery phase: Standard convergence curve
- Final loss matches or exceeds standard training

---

## Main Ideas & Contributions

### 1. Drop-In Method with Zero Infrastructure Changes

**Key Contribution**: TST works with existing frameworks and kernels.

No modifications required:
- ✅ Same model architecture (RoPE, MLP, Attention all unchanged)
- ✅ Same optimizer (AdamW, SGD, etc.)
- ✅ Same data pipeline (no special preprocessing)
- ✅ Same parallelism (FSDP, Megatron, tensor parallel)
- ✅ Same tokenizer (inherit vocabulary, no retraining)

Why This Matters:
- Organizations can adopt immediately
- No retraining of existing infrastructure
- Reduces deployment risk and complexity
- Works with proprietary or in-house training systems

### 2. Consistent 2.5× Wall-Clock Speedup Across Model Scales

**Empirical Results** (validated across four scales):

| Model | Baseline Time | TST Time | Speedup |
|-------|-----------------|----------|---------|
| 270M | ~2 weeks | ~0.8 weeks | 2.5× |
| 600M | ~3 weeks | ~1.2 weeks | 2.5× |
| 3B | ~4 weeks | ~1.6 weeks | 2.5× |
| 10B A1B (MoE) | ~6 weeks | ~2.4 weeks | 2.5× |

**Scaling Consistency**: Unlike many methods that work for small models but not large, TST maintains 2.5× speedup across two orders of magnitude in model size.

### 3. No Quality Degradation at Matched Loss

When comparing models at the same final loss (not wall-clock time):
- TST and baseline achieve near-identical downstream performance
- Quality gap < 1% on standard benchmarks

**Implication**: Speed is free; no accuracy tradeoff.

### 4. Matched FLOPs, Dramatic Wall-Clock Difference

**Critical Distinction**:
- FLOPs: Total computational work (similar between TST and baseline)
- Wall-Clock: Actual time to completion (2-3× faster with TST)

How is this possible?

**Explanation**: Wall-clock time depends on:
1. **FLOPs** (theoretical work)
2. **Kernel efficiency** (how well GPU utilizes available parallelism)
3. **Memory bandwidth** (loading weights, activations from memory)
4. **Communication** (synchronization between GPUs in distributed training)

TST reduces kernel overhead by running fewer forward passes, even though total FLOPs remain similar. This is a practical systems insight: FLOPs ≠ Time.

### 5. Compatibility with All Modern Training Techniques

TST composes with:
- **Mixed Precision** (FP16, BF16): MCE compatible with reduced precision
- **Gradient Checkpointing**: Reduces memory, orthogonal to TST
- **Distributed Training**: Works with FSDP, Megatron, data parallelism
- **Curriculum Learning**: TST can be combined with data-driven curricula
- **Data Augmentation**: No data pipeline changes needed

---

## Methodology & Implementation

### Experimental Setup

**Models Trained**:
1. **270M Dense**: Modified SmolLM2 shape, untied embeddings
   - Training: ~2 weeks on 8-16 GPUs
   - Tokenizer: Llama3-8B vocabulary
   
2. **600M Dense**: Modified SmolLM2 shape
   - Training: ~3 weeks on 16-24 GPUs
   - Tokenizer: Llama3-8B vocabulary

3. **3B Dense**: SmolLM3 shape
   - Training: ~4 weeks on 32-48 GPUs
   - Tokenizer: Llama3-8B vocabulary

4. **10B A1B (MoE)**: Qwen3 family mixture-of-experts
   - Training: ~6 weeks on 64 GPUs
   - Tokenizer: Qwen vocabulary (modified for TST)

### Training Configuration

**Data**:
- **Dense models**: DCLM (Diverse Common Crawl Large) corpus
- **MoE model**: 50% DCLM + 50% FineWeb-Edu
- **Rationale**: Mix ensures diverse tokens for bag formation

**Hyperparameters**:
- **Optimizer**: AdamW (β₁=0.9, β₂=0.95, ε=1e-8)
- **Schedule**: Warmup-Stable-Decay (WSD)
  - Warmup: 2,000 steps
  - Stable: 80% of training
  - Decay: 18% of training (cosine decay to 10% peak LR)
  
- **Learning Rates**:
  - 270M: 1.0e-3 (swept)
  - 600M: 9.0e-4 (swept)
  - 3B: 6.0e-4 (family recommendation)
  - 10B: 4.0e-4 (family recommendation)

**Hardware**:
- Framework: TorchTitan (PyTorch distributed)
- Parallelism: FSDP (Fully Sharded Data Parallel)
- GPUs: Up to 64 H200 or B200 equivalents
- Precision: BF16 (PyTorch autocast)

### TST-Specific Configuration

**Superposition Phase**:
- **Bag Size**: 2-4 tokens per bag (sweep performed)
- **Duration**: 20-40% of total training steps
- **Embedding Averaging**: Simple arithmetic mean (no learned weights)
- **Loss**: MCE = sum of per-token CE losses

**Recovery Phase**:
- **Duration**: 60-80% of training
- **Objective**: Standard next-token prediction
- **Warmup**: None (initialize from superposition-learned weights)

### Evaluation Methodology

**Downstream Benchmarks**:
- **Reasoning**: MMLU, MATH, ARC-Challenge
- **Coding**: HumanEval, MBPP
- **Knowledge**: TriviaQA, MMLU-Pro
- **Language**: HellaSwag, PIQA, SIQA

**Metrics**:
- Exact match (EM) for closed-ended tasks
- Pass@1 for code generation
- Accuracy for multiple choice

**Comparison**:
- TST model at matched final loss vs. baseline at same loss
- E.g., TST 10B at 2.0 loss vs. baseline 10B at 2.0 loss
- Not comparing TST at earlier time steps (would be unfair)

### Results

**Wall-Clock Speedup**:
- Mean: 2.5×
- Range: 2.3× (270M) to 2.7× (10B MoE)
- Std. Dev: ±0.15× (highly consistent)

**Quality at Matched Loss**:
- MMLU: -0.2% to +0.3% (no statistically significant difference)
- MATH: -0.1% to +0.2%
- HumanEval: -1% to +1% (within variance)
- TriviaQA: -0.3% to +0.4%

**GPU Utilization**:
- Superposition phase: 92-96% (fewer forward passes, but high arithmetic intensity)
- Recovery phase: 88-94% (standard performance)
- Baseline: 85-90% (token-level prediction has more kernel overhead)

---

## Practical Applications & Use Cases

### 1. Open-Source Model Training

**Use Case**: Academic teams training open-source models (LLaMA, Mistral, etc.) with limited budget.

**Benefit**: 2.5× speedup = 60% cost reduction on GPU rental. Enables training on smaller clusters.

**Example**: 
- Standard: 64 H100 GPUs × 6 weeks = $500K+
- With TST: 64 H100 GPUs × 2.4 weeks = $200K
- Savings: $300K, same model quality

### 2. Rapid Iteration for Research

**Use Case**: Hyperparameter sweeps, architecture experiments requiring multiple training runs.

**Benefit**: Each iteration 2.5× faster. More experiments per timeline.

**Example**:
- Budget: 10 GPU-weeks per quarter
- Standard: Can run ~1.6 full training runs
- With TST: Can run ~4 full training runs
- Research velocity: 2.5× improvement

### 3. Fine-Tuning Efficiency

While TST focuses on pre-training, similar principles apply to domain-specific fine-tuning:
- Superpose tokens early during fine-tuning
- Switch to standard training for task-specific learning
- Reduces fine-tuning time by ~2×

### 4. Domain-Specific Language Models

**Use Case**: Companies training domain-specific models (legal, medical, financial) from foundation models.

**Benefit**: Reduced time-to-deployment, lower cost, faster iteration on prompt engineering.

**Example**: Healthcare provider training proprietary model on patient records.
- Time: 4 weeks → 1.6 weeks (3× speedup)
- Cost: $100K → $40K (60% savings)
- Deployment: Can iterate based on real-world performance

### 5. Production Training Infrastructure

**Use Case**: Cloud providers (AWS, GCP, Azure) optimizing training infrastructure.

**Benefit**: Same GPU capacity trains 2.5× more customers per year.

**Implication**: More revenue per hardware; competitive advantage for efficiency.

---

## Insights & Implications

### 1. Simplicity Is Powerful

TST achieves 2.5× speedup with minimal complexity:
- No new architecture components
- No custom kernels
- No data preprocessing changes
- No optimizer modifications

This is a systems-level efficiency gain, not a modeling innovation. It suggests that early-stage training is structured differently and can be exploited with simple methods.

### 2. Wall-Clock Time > Theoretical FLOPs

The distinction between FLOPs and wall-clock time is crucial:
- FLOPs count total operations
- Wall-clock time also includes kernel efficiency, memory bandwidth, communication

TST demonstrates that improving practical time requires systems thinking, not just algorithmic innovation.

### 3. Training Dynamics Are Non-Uniform

The fact that superposition works for 20-40% of training suggests:
- **Early phase** (superposition): Token dependencies are local, structure is learned at coarse granularity
- **Late phase** (recovery): Fine-grained dependencies matter, high-level structure is established

This has implications for understanding emergent capabilities and phase transitions in training.

### 4. Adoption Barriers Are Minimal

Unlike many efficiency techniques requiring infrastructure changes, TST:
- ✅ Uses existing frameworks (PyTorch, JAX)
- ✅ Uses existing kernels (fused CE)
- ✅ Compatible with all training strategies
- ✅ Zero breaking changes

Implication: Expect rapid adoption across industry.

### 5. Cost Implications for Frontier Training

If frontier AI training reaches $20B by 2030 (per Matsuoka's analysis), TST saves:
- **$5B per training run** (2.5× speedup = 60% cost reduction)
- **$5B across entire training lifecycle** (architecture + variants)

This is not marginal savings; it fundamentally changes economics of frontier model development.

### 6. Composability with Other Methods

TST is orthogonal to:
- Quantization (use BF16 or INT8)
- Sparsity (combine with pruning)
- Parallelism (works with FSDP, Megatron)
- Curriculum learning (works with progressive data schedules)

Potential for combining TST with other methods for >3× speedups.

---

## Code & Resources

### Official Resources
- **Paper**: arXiv [2605.06546](https://arxiv.org/abs/2605.06546)
- **Blog Post**: Nous Research [Token Superposition](https://nousresearch.com/token-superposition)
- **HuggingFace**: [Paper page](https://huggingface.co/papers/2605.06546)
- **MarkTechPost Article**: [Comprehensive summary](https://www.marktechpost.com/2026/05/13/nous-research-releases-token-superposition-training-to-speed-up-llm-pre-training-by-up-to-2-5x-across-270m-to-10b-parameter-models/)

### Implementation Guide

**PyTorch Implementation (Minimal Example)**:

```python
import torch
import torch.nn as nn

class TokenSuperpositionTraining(nn.Module):
    def __init__(self, model, bag_size=2):
        super().__init__()
        self.model = model
        self.bag_size = bag_size
        self.is_superposition = True
    
    def superpose_tokens(self, embeddings):
        # embeddings: (batch, seq_len, hidden_dim)
        batch, seq_len, hidden_dim = embeddings.shape
        
        # Group tokens into bags
        num_bags = seq_len // self.bag_size
        embeddings = embeddings[:, :num_bags * self.bag_size, :]
        
        # Reshape and average
        embeddings = embeddings.view(batch, num_bags, self.bag_size, hidden_dim)
        bag_embeddings = embeddings.mean(dim=2)  # Average across bag
        
        return bag_embeddings
    
    def forward(self, input_ids, labels=None):
        embeddings = self.model.embed_tokens(input_ids)
        
        if self.is_superposition:
            embeddings = self.superpose_tokens(embeddings)
            logits = self.model.decoder(embeddings)
            # Expand labels to match bag structure for MCE loss
            labels_expanded = labels.repeat_interleave(self.bag_size // 2, dim=1)
            loss_fn = nn.CrossEntropyLoss()
            loss = loss_fn(logits.view(-1, logits.shape[-1]), 
                          labels_expanded.view(-1))
        else:
            logits = self.model(embeddings)
            loss_fn = nn.CrossEntropyLoss()
            loss = loss_fn(logits.view(-1, logits.shape[-1]), 
                          labels.view(-1))
        
        return loss
    
    def switch_to_recovery(self):
        self.is_superposition = False
```

### Quick-Start Training Script

```bash
# Standard PyTorch training with TST
# Requires: transformers, accelerate, datasets

python train.py \
    --model_name_or_path gpt2-medium \
    --dataset_name wikitext --dataset_config wikitext-103-v1 \
    --per_device_train_batch_size 32 \
    --per_device_eval_batch_size 32 \
    --learning_rate 5e-5 \
    --num_train_epochs 3 \
    --output_dir ./gpt2-tst \
    --use_token_superposition \
    --bag_size 2 \
    --superposition_fraction 0.3  # 30% of training
```

### Dependency Requirements
- **PyTorch**: >= 2.0 (with fused CE kernels)
- **JAX**: >= 0.4 (alternative backend)
- **Transformers**: >= 4.35
- **Accelerate**: >= 0.24 (for distributed training)
- **TorchTitan**: Optional, recommended for large-scale training

### Reproducibility Resources

- **Seed Management**: Set `seed=42` for reproducibility
- **Hyperparameter Details**: In paper Table 3 (learning rates per scale)
- **Hardware**: Training validated on H100, B200 (substitute compatible GPUs)
- **Software Versions**: PyTorch 2.1.0, CUDA 12.1, transformers 4.35.0

---

## Related Work & Context

### Related Efficiency Methods

1. **Token Merging (ToMe)**: Reduces sequence length by merging similar tokens
   - Requires bipartite soft matching algorithm
   - Modifies attention computation
   - Wall-clock speedup: 1.3-1.5× (less than TST)

2. **Flash Attention**: Reduces memory via IO-aware kernels
   - Improves inference and training speed
   - Orthogonal to TST (composable)
   - Speedup: 2-3× memory, ~1.2× wall-clock

3. **Layer Dropping / Skipping**: Skip layers early in training
   - Requires architectural changes
   - Modest speedup (1.1-1.2×)
   - Quality impact at matched step count

4. **Distributed Training Optimizations**: Gradient accumulation, checkpointing
   - Standard practice (already deployed)
   - Saturation on speedup gains
   - TST is additive

### Complementary Techniques

TST combines well with:
- **Quantization**: Use INT8 or BF16 (already in use)
- **Sparsity**: Combine with learned sparsity patterns
- **Curriculum Learning**: Progressive data difficulty + TST
- **Data Augmentation**: Standard techniques remain effective

### Foundational Theory

1. **Training Dynamics**: Work on phase transitions, grokking (Nanda et al., Alford et al.)
2. **Lottery Ticket Hypothesis**: Suggests networks learn efficiently, supporting TST hypothesis
3. **Double Descent**: Understanding generalization across training curves
4. **Scaling Laws**: Chinchilla, Compute Optimal training (Hoffmann et al.)

### Future Directions

1. **Adaptive Bag Sizing**: Learn optimal bag size per layer/training stage
2. **Bag Structure Optimization**: Instead of averaging, learned aggregation
3. **Non-Contiguous Bags**: Bag distant tokens rather than contiguous
4. **Interleaved Recovery**: Earlier switching to fine-grained prediction
5. **Domain-Specific Variants**: Healthcare, code, chemistry-specific superposition

### Broader Implications

TST represents a class of solutions combining:
- Simple methodology (averaging, standard loss)
- Practical deployment (existing frameworks)
- Significant impact (2.5× speedup)
- Theoretical grounding (training dynamics understanding)

As AI infrastructure matures, expect more such techniques maximizing practical efficiency without requiring infrastructure overhaul.

