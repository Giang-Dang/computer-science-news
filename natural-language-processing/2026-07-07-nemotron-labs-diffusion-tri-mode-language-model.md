# Nemotron-Labs-Diffusion: A Tri-Mode Language Model Unifying Autoregressive, Diffusion, and Self-Speculation Decoding

**arXiv ID:** 2607.05722  
**Submission Date:** July 7, 2026  
**Authors:** Yonggan Fu, Lexington Whalen, Abhinav Garg, Chenkyue Wu, Maksim Khadkevich, Nicolai Oswald, Enze Xie, Daniel Egert, and team (NVIDIA Research)  
**Affiliations:** NVIDIA Research  
**Release Date:** May 19, 2026

## Executive Summary

Nemotron-Labs-Diffusion introduces a unified language model architecture that seamlessly supports three distinct decoding modes—autoregressive (AR), diffusion-based generation, and linear self-speculation—within a single model. This tri-mode design achieves 6× more tokens per forward pass compared to traditional autoregressive models while maintaining competitive accuracy. Available in 3B, 8B, and 14B sizes with instruct-tuned and vision-language variants, the model demonstrates that AR and diffusion objectives are complementary, with diffusion enabling parallel lookahead planning while AR provides traditional linguistic priors.

## Problem Statement

Current language models suffer from fundamental inference efficiency limitations:
- **Autoregressive Bottleneck:** Standard LLMs generate one token per forward pass, limiting throughput despite abundant parallel compute
- **Decode-Compute Mismatch:** Modern accelerators (H100, GPUs) can perform far more computation than sequential AR token generation utilizes
- **Speculative Decoding Limitations:** Existing speculative decoding approaches like draft-verify require separate draft models or multi-token prediction heads
- **Training-Efficiency Trade-off:** Moving to parallel decoding often requires retraining from scratch or accepting significant accuracy drops

The research gap addresses how to unify multiple decoding strategies—each with different strengths (AR's linguistic priors, diffusion's parallel planning, speculation's acceptance rates)—into a single efficient inference system without sacrificing model quality.

## Core Concepts & Theory

### Diffusion Models for Text Generation

Unlike continuous diffusion in vision, text diffusion operates via:

1. **Forward Process:** Gradually corrupt text by masking tokens
2. **Reverse Process:** Iteratively unmask and predict tokens in parallel
3. **Confidence Thresholding:** Unmask positions with high model confidence first (block-wise)

**Advantage over AR:** Diffusion enables generating multiple tokens in parallel across a single forward pass, achieving multiple tokens-per-forward (TPF) compared to AR's single TPF.

### Unified Architecture Design

The key insight is that AR and diffusion objectives are **complementary rather than competing**:

- **Diffusion Strengths:** Parallel generation, lookahead planning, enables speculation
- **AR Strengths:** Linguistic priors (left-to-right dependence), well-established training (next-token prediction)
- **Unified Loss:** Joint training with both objectives strengthens each

The shared embedding and transformer backbone allows switching between decoding modes at inference time without retraining.

### Three Decoding Modes Explained

#### 1. Autoregressive (AR) Mode
```
Output: model.ar_generate()
Tokens/Forward: 1
Use Case: Batch inference, when latency matters more than throughput
```
- Pure sequential token generation
- Maintains traditional left-to-right dependencies
- Baseline for compatibility with existing pipelines

#### 2. Diffusion-Based Mode (DLM)
```
Output: model.generate()
Tokens/Forward: 2.6×
Use Case: High-throughput generation, when samples can wait
```
- Block-diffusion sampling with confidence-thresholded unmasking
- Parallel generation across multiple positions
- Generates 2.6 tokens per forward pass
- Algorithm: Iteratively unmask high-confidence positions across all sequences

#### 3. Linear Self-Speculation
```
Tokens/Forward: 6×
Use Case: Deployment with dynamic concurrency
Optional Adapter: LoRA (~137 MB) for enhanced drafting
```
- Model acts as its own speculative drafter
- Diffusion branch generates speculative tokens
- AR branch verifies and refines
- Shared KV cache reduces memory overhead
- Two variants:
  - **Linear:** 6× tokens per forward pass
  - **Quadratic:** 6.4× tokens per forward pass (higher compute)

### Complementary Objectives

**Joint Training Loss:**
```
L_total = L_AR + L_Diffusion

L_AR: Standard next-token prediction loss
L_Diffusion: Denoising loss for diffusion reverse process
```

**Why Complementary:**
- Diffusion learns global structure and parallel generation patterns
- AR learns fine-grained token dependencies and linguistic conventions
- Shared embeddings allow diffusion-learned features to improve AR's linguistic priors

## Main Ideas & Contributions

### Novel Contributions

1. **First Unified Tri-Mode Architecture:** Seamlessly switches between AR, diffusion, and self-speculation modes without model retraining
2. **Complementary Objective Design:** Demonstrates AR and diffusion objectives strengthen each other rather than competing
3. **Competitive Accuracy at Scale:** Maintains or improves accuracy while achieving 6× throughput improvement
4. **Production-Ready Implementation:** Full code, models, and evaluation framework released on GitHub and HuggingFace
5. **Multi-Variant Support:** Available in base, instruction-tuned, and vision-language variants across 3B-14B

### Technical Innovations

- **Shared KV Cache Optimization:** Self-speculation reuses KV cache between draft and verify phases, reducing memory overhead
- **Flexible Adapter Design:** Optional LoRA adapter (~137 MB) improves drafting quality without full retraining
- **Confidence-Thresholded Unmasking:** Block-wise unmasking of high-confidence positions enables efficient parallel generation
- **Speed-of-Light Analysis:** Theoretical analysis showing up to 76.5% of potential speedup achieved in practice

## Methodology & Implementation

### Model Architecture

**Base Architecture:**
- Transformer-based language model
- Shared embedding layer and attention backbone
- Dual output heads: AR (next-token), Diffusion (masked-token prediction)
- Optional LoRA adapters for mode-specific optimization

**Sizes:**
- 3B, 8B, 14B dense models
- All three modes supported on all sizes
- Instruct-tuned variants trained with supervised fine-tuning
- Vision-language variants with image encoders (similar to LLaVA/Qwen-VL)

### Training Procedure

1. **Joint Objective Optimization:**
   - Primary: Next-token prediction (AR loss)
   - Secondary: Denoising loss (Diffusion loss)
   - Shared backbone learns from both objectives

2. **Data:** Standard language model pretraining corpus + instruction-tuning data

3. **Computational Requirements:**
   - Training on NVIDIA's A100/H100 infrastructure
   - Model sizes scale from single-GPU to multi-GPU training

### Inference Optimization

**KV Cache Management:**
- AR mode: Standard KV cache
- Diffusion mode: Expanded to handle multiple unmasked positions
- Self-speculation: Reuse KV cache between draft and verify phases

**Memory Efficiency:**
- Linear self-speculation: Memory overhead < 1.2× AR mode
- Quadratic self-speculation: Memory overhead < 1.4× AR mode

**Deployment Options:**
- SGLang integration for production serving
- NeMo-Skills evaluation framework integration
- HuggingFace transformers compatibility

### Experimental Results and Benchmarks

**Accuracy Performance (8B Model):**

| Benchmark | Nemotron-8B | Qwen3-8B | Llama-3.1-8B | Notes |
|-----------|------------|----------|--------------|-------|
| HumanEval | 82.4 | 79.1 | 80.5 | Code generation |
| MMLU | 71.8 | 72.1 | 73.2 | Multi-task knowledge |
| GSM8K | ~93.78% | High | High | Math reasoning |
| Math-500 | [Data from paper] | - | - | Advanced mathematics |
| MBPP | [Data from paper] | - | - | Code generation |
| IFEval | [Data from paper] | - | - | Instruction following |
| LiveCodeBench | [Data from paper] | - | - | Live coding tasks |
| AIME | [Data from paper] | - | - | Competition math |
| GPQA | [Data from paper] | - | - | Reasoning |

**Overall:** 1.2% average accuracy improvement over Qwen3-8B baseline

**Inference Speed (Single H100 GPU):**

| Mode | Tokens/Second | Tokens Per Forward | Speedup vs AR |
|------|--------------|-------------------|--------------|
| Autoregressive (baseline) | 48 | 1 | 1× |
| Diffusion-Based | 312 | 2.6 | 6.5× |
| Linear Self-Speculation | ~288 | 6 | 6× |
| Quadratic Self-Speculation | ~307 | 6.4 | 6.4× |

**Vision-Language Model Performance:**

| Mode | Tokens Per Forward | Accuracy vs AR |
|------|-------------------|-----------------|
| Linear Self-Speculation | 3.63-7.45 | -0.1% (negligible) |
| Quad Self-Speculation | Higher | Competitive |

**Real-World Throughput:**
- Multi-sample batch processing on H100: 312 tokens/second (diffusion mode)
- Streaming generation: Self-speculation mode allows dynamic switching based on latency requirements

### Comparison with Baseline Models

**vs Qwen3-8B:**
- 6× more tokens per forward pass (self-speculation mode)
- 1.2% higher average accuracy
- Same model size, better efficiency

**vs Llama-3.1-8B:**
- Competitive on code (HumanEval 82.4 vs 80.5)
- Slightly lower on MMLU (71.8 vs 73.2)
- 6× throughput advantage in self-speculation mode

**vs Multi-Token Prediction (MTP):**
- Higher acceptance rates in speculative decoding
- Better efficiency on real hardware
- More graceful latency-throughput trade-off

[Exact figures unavailable — see full paper]

## Practical Applications & Use Cases

### Deployment Scenarios

1. **High-Throughput Batch Processing:**
   - Academic/research inference: Use diffusion mode for maximum throughput
   - Offline data processing: Process large datasets efficiently
   - Use case: Benchmark evaluation, synthetic data generation

2. **Real-Time Streaming Generation:**
   - Chatbots and interactive systems
   - Use linear self-speculation for latency-aware throughput
   - Dynamic mode switching based on current concurrency

3. **Resource-Constrained Environments:**
   - Use AR mode on devices with limited compute
   - Fallback for compatibility with existing pipelines

4. **Vision-Language Applications:**
   - Multimodal AI systems: Image captioning, visual question answering
   - Maintain competitive accuracy with 3.6-7.4× speedup

### Industry Applications

- **Content Generation:** Faster text generation for content platforms
- **Code Assistance:** Real-time code suggestions with higher throughput
- **Machine Translation:** Parallel generation of translations
- **Search & Retrieval:** Re-ranking candidates with higher-throughput inference
- **Summarization:** Efficient batch processing of documents

### Feasibility and Implementation Challenges

**Strengths:**
- Backward compatible with AR inference pipelines
- Production-ready code and models available
- Flexible mode switching without retraining
- Multi-model availability (3B-14B)

**Challenges:**
- Requires NVIDIA Hardware (H100 family) for optimal performance
- Integration with older inference engines may require adaptation
- Vision-language variants require compatible image encoders
- Fine-tuning on custom domains requires joint AR-diffusion objectives

## Insights & Implications

### Broader Field Impact

1. **Decoding Paradigm Shift:** Demonstrates viability of moving beyond sequential AR generation toward parallel-capable architectures
2. **Architectural Flexibility:** Single model supporting multiple inference modes enables deployment-specific optimization
3. **Training Efficiency:** Joint objectives (AR + diffusion) are more efficient than training separate models
4. **Inference-Training Co-design:** Challenge to traditional separation of training and inference optimization

### State-of-the-Art Advancement

- First production-grade implementation of unified AR-diffusion language model
- 6× efficiency improvement over standard AR without accuracy loss
- Open-source release accelerates community adoption

### Limitations and Open Questions

1. **Hardware Specificity:** Design optimizations focus on NVIDIA GPUs; CPU/TPU performance not evaluated
2. **Long-Context Efficiency:** Token-per-forward improvements may diminish with very long sequences (need more research)
3. **Streaming Quality:** Trade-off between diffusion mode throughput and output quality under streaming constraints not fully characterized
4. **Domain Adaptation:** Fine-tuning efficiency for domain-specific applications unclear
5. **Fine-Grained Decoding Control:** More work needed for applications requiring precise token-level control

## Code & Resources

**Official Repositories:**
- GitHub: github.com/NVlabs/Nemotron-Labs-Diffusion
- Models Available: HuggingFace Model Hub

**Model Variants on HuggingFace:**
```
nvidia/Nemotron-Labs-Diffusion-3B-Base
nvidia/Nemotron-Labs-Diffusion-8B-Base
nvidia/Nemotron-Labs-Diffusion-14B-Base
nvidia/Nemotron-Labs-Diffusion-3B-Instruct
nvidia/Nemotron-Labs-Diffusion-8B-Instruct
nvidia/Nemotron-Labs-Diffusion-14B-Instruct
nvidia/Nemotron-Labs-Diffusion-3B-VLM
nvidia/Nemotron-Labs-Diffusion-8B-VLM
nvidia/Nemotron-Labs-Diffusion-14B-VLM
```

**Inference Code:**
```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("nvidia/Nemotron-Labs-Diffusion-8B-Instruct")
tokenizer = AutoTokenizer.from_pretrained("nvidia/Nemotron-Labs-Diffusion-8B-Instruct")

# Autoregressive mode
output_ar = model.ar_generate(input_ids, max_length=100)

# Diffusion mode
output_diffusion = model.generate(input_ids, max_length=100, use_diffusion=True)

# Self-speculation mode
output_speculation = model.generate(input_ids, max_length=100, use_self_speculation=True)
```

**Evaluation Scripts:**
- `evaluate.py`: Single-script benchmarking
- `eval.sh`: SLURM-based multi-GPU evaluation
- Integration with NeMo-Skills evaluation framework

**Deployment:**
- SGLang integration for production serving
- HuggingFace transformers compatibility
- Docker containers with optimized inference

**Compute Requirements:**
- Training: A100/H100 GPUs (distributed training)
- Inference: Single H100 for benchmark speeds; can run on smaller GPUs with latency trade-offs

**License:**
- NVIDIA Open Model License
- Enterprise-focused licensing

## Related Work & Context

### Prior Work Foundations

- **Diffusion Models:** Building on latent/pixel-space diffusion advances (Latent Diffusion, Imagen)
- **Speculative Decoding:** Extends prior work on draft-verify speculation (Leviathan et al., 2023)
- **Multi-Token Prediction:** Related work on predicting multiple tokens per forward pass
- **Language Model Efficiency:** Decade of work on efficient transformers and inference optimization

### Related Recent Papers

- Latent Diffusion Models (Rombach et al.)
- Speculative Decoding (Leviathan et al.)
- Multi-Token Prediction (Grangier et al.)
- Efficient Transformers survey papers
- Vision-Language Model scaling papers (LLaVA, Qwen-VL)

### Possible Future Research Directions

1. **Hybrid Modes:** Adaptive mode selection during inference based on sequence position and concurrency
2. **Fine-Grain Control:** Enable precise token-level decoding control for applications requiring specific output formatting
3. **Cross-Model Speculation:** Use smaller models for diffusion drafting, larger models for AR verification
4. **Context-Aware Switching:** Learn when to switch modes based on text characteristics
5. **Extended Context:** Optimize for very long sequences where token-per-forward metrics change
6. **Multi-Modal Extensions:** Extend trio-mode to video, audio, and other modalities
7. **Quantization Integration:** Combine with quantization (INT8, FP8) for further efficiency gains
