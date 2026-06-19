# End-to-End Context Compression at Scale

**Paper**: [2606.09659] End-to-End Context Compression at Scale

**Authors**: Ang Li, Sean McLeish, Haozhe Chen, Nimit Kalra, Zaiqian Chen, Artem Gazizov, Venkata Anoop Suhas Kumar Morisetty, Bhavya Kailkhura, Harshitha Menon, Zhuang Liu, Brian R. Bartoldson, Tom Goldstein, Sanae Lotfi, Micah Goldblum, Pavel Izmailov

**Submitted**: June 9, 2026

**ArXiv Link**: https://arxiv.org/abs/2606.09659

## Executive Summary

Long-context language model inference is fundamentally constrained by the exponential growth of the key-value (KV) cache, which scales linearly with sequence length and quickly exhausts GPU memory. This paper revisits encoder-decoder context compression—a promising but previously underexplored approach that maps long token sequences to compact latent representations—and demonstrates how to close the accuracy-efficiency frontier through principled architecture search and training methodology. The resulting Latent Context Language Models (LCLMs) achieve 8.8× faster inference on long-context benchmarks while maintaining model quality, offering a practical path to trillion-token-scale inference.

## Problem Statement

### The KV Cache Memory Bottleneck

In transformer-based language models, attention computation requires storing keys and values for all previous tokens:

- **Memory Growth**: For a 70B parameter model, processing 64K tokens requires ~2TB of KV cache (assuming 16-bit precision)
- **Inference Bottleneck**: Time-to-first-token (TTFT) and overall throughput are dominated by memory bandwidth requirements
- **Deployment Constraint**: Practical deployments are limited to 4K-16K context windows despite architectural support for longer contexts

### Existing Compression Approaches and Their Limitations

1. **Token Pruning** (SnapKV, KVzip):
   - Achieves reasonable compression but typically requires significant inference-time computation to identify important tokens
   - Maintains O(T) space complexity—still linear in sequence length
   - Often degrades model quality noticeably at high compression ratios

2. **Prompt Caching**:
   - Only applicable to static prefixes, unsuitable for dynamic or mixed contexts
   - Requires context to fit within model's native window before caching

3. **Quantization**:
   - Reduces precision but doesn't eliminate quadratic attention over full sequence length
   - Quality degradation at extreme compression ratios

4. **KV Cache Recomputation**:
   - Trades memory for computation (typically unfavorable)
   - Increases latency and energy consumption

### The Encoder-Decoder Compression Opportunity

Encoder-decoder compression, where a separate encoder compresses long sequences into latent embeddings consumed by the original decoder, presents an attractive alternative:

- **Potential Advantages**: Could achieve sub-linear space complexity and production compatibility
- **Prior Limitations**: Existing approaches failed to match pruning-based methods on accuracy-efficiency frontier
- **Unexplored Territory**: No systematic approach to designing these compressors had been attempted at scale

## Core Concepts & Theory

### Latent Context Language Model (LCLM) Framework

The architecture consists of two main components:

**Encoder**: Compresses long input context C into latent representations Z
```
Z = Encoder(C)  // Z ∈ ℝ^{m×d} where m << |C|
```

**Decoder**: Original language model that processes both latent context and current tokens
```
P(x_t | x_{<t}, Z) = LM_decoder(x_{<t}, Z)
```

Key insight: The decoder only sees latent representations, not original tokens—forcing the encoder to preserve all information necessary for downstream prediction.

### Architecture Search for Optimal Compression

Rather than handcrafting encoder designs, the paper employs neural architecture search (NAS) to explore the design space:

1. **Search Variables**:
   - Encoder depth (number of transformer layers)
   - Attention pattern (local, strided, or full)
   - Compression ratio (target latent sequence length)
   - Fusion mechanism (how encoder outputs integrate with decoder)

2. **Search Strategy**: Evolutionary algorithms or reinforcement learning-based architecture search to identify top-performing configurations

3. **Training from Scratch**: Each candidate architecture is trained from initialization to ensure fair comparison

### Compression Mechanisms

**Token-to-Latent Mapping**:
```
Latent Embedding = LinearProjection(EncoderOutput)
Decoder input = [LatentEmbeddings; CurrentTokenEmbeddings]
```

The latent representations act as context summaries that the decoder learns to interpret during pre-training.

## Main Ideas & Contributions

### 1. Principled Architecture Search

The paper performs the first large-scale, systematic exploration of encoder-decoder compression designs:
- Evaluated hundreds of architectural variants
- Trained from scratch to elimination training bias
- Identified configuration principles for optimal compression-accuracy trade-offs

### 2. Specialized Decoder Integration

Rather than using the original decoder unmodified, the paper demonstrates that decoders trained jointly with compressing encoders achieve superior results:
- Adapts internal representations for latent input interpretation
- Learns to optimally utilize compression artifacts
- Maintains compatibility with existing inference engines (via prefix prepending)

### 3. Production-Compatible Inference

Unlike many compression schemes, LCLMs:
- Work with arbitrary-length contexts (encoder handles any length)
- Integrate with existing inference infrastructure (latent context acts as prefix)
- Support streaming and incremental decoding
- Compatible with modern inference engines (vLLM, SGLang, TensorRT-LLM)

### 4. Scaling Law Analysis

Comprehensive study of how compression effectiveness scales:
- Parameter count of both encoder and decoder
- Compression ratio impact on model capability
- Context length scaling properties

## Methodology & Implementation

### Architecture Search and Training

1. **Pre-training Setup**:
   - Base decoder: Qwen3-4B-Instruct-2507 (4 billion parameter model)
   - Encoders: 125M to 1B parameters
   - Datasets: Common crawl subset + synthetic long-context data

2. **Baseline Configurations**:
   - Pure attention encoders with varying depth
   - Linear attention variants
   - Sparse attention patterns (strided, local windows)

3. **Search Space**:
   - Encoder layers: [2, 4, 6, 12, 24]
   - Compression ratios: [4×, 8×, 16×, 32×]
   - Attention patterns: [full, local-64, strided-4, linear]

### Experimental Datasets and Benchmarks

#### RULER Benchmark (4K Context)
- **Task**: Long-context understanding over 4,000 tokens
- **Evaluation**: Accuracy vs. TTFT (time-to-first-token) trade-off
- **Results**: LCLM achieves 8.8× faster inference while maintaining accuracy

#### LongBench Benchmark (64K Context)
- **Task**: Diverse long-context understanding tasks (summarization, QA, retrieval)
- **Baseline Tasks**: Book summarization, code understanding, question answering
- **Results**: LCLM achieves 5.2× faster inference with minimal quality loss

#### Model Configuration
- **Decoder Base**: Qwen3-4B-Instruct-2507
- **Encoder Variants**: Multiple configurations from 125M to 1B parameters
- **Compression Ratios**: 4×, 8×, 16×, 32×

### Metrics and Evaluation Protocol

**Inference Speed Metrics**:
- Time-to-First-Token (TTFT): Latency until first output token
- Throughput: Tokens-per-second during generation
- Memory Usage: GPU memory consumption (GB)

**Quality Metrics**:
- Task Accuracy: Percentage of correctly answered questions/summaries
- Perplexity: Language modeling perplexity on held-out sets
- Human Evaluation: [Exact figures unavailable — see full paper]

**Compression Trade-off Analysis**:
- Accuracy-efficiency frontier: Quality vs. TTFT curve
- Pareto optimal points: Identifying non-dominated configurations

### Inference Optimization

1. **Batch Processing**: Compress entire context batch before decoding
2. **Speculative Decoding**: Use cheap compression for early draft generation
3. **Multi-GPU Scaling**: Distribute encoder and decoder across devices

## Practical Applications & Use Cases

### 1. Long-Document Processing
- **Legal/Compliance**: Processing contracts and regulatory documents (50K-100K tokens)
- **Scientific Research**: Analyzing full papers and technical reports with context preservation
- **Medical Records**: Analyzing complete patient histories and clinical notes

### 2. Agentic Systems
- **Research Agents**: Maintaining context over hundreds of paper reads
- **Code Analysis**: Reasoning over entire repository codebases (repository-scale code)
- **Multi-Turn Dialogue**: Persistent memory systems with arbitrarily long conversation history

### 3. Real-Time Applications
- **Live Transcription**: Maintaining context during streaming video/audio
- **News Aggregation**: Processing multiple documents simultaneously
- **Customer Service**: Full conversation history analysis without token limits

### 4. Cost-Efficient Inference
- **Cloud Services**: Reducing inference costs on long-context workloads (pay-per-token savings)
- **Edge Deployment**: Enabling long-context capabilities on resource-constrained devices
- **Batch Processing**: Efficient handling of document processing pipelines

## Insights & Implications

### Key Findings

1. **Encoder Design Matters**: Architecture choices in the compressor have dramatic impact on final performance—handcrafted designs consistently underperformed NAS results

2. **Depth is Critical**: Deeper encoders (12-24 layers) consistently outperformed shallow alternatives, suggesting rich compression requires meaningful computation

3. **Attention Pattern Trade-offs**:
   - Full attention: Best accuracy but slowest
   - Strided attention: Good balance of speed and quality
   - Linear attention: Fastest but notable quality loss at high compression

4. **Scaling Principle**: LCLM quality improves predictably with encoder size, following power-law scaling similar to standard language models

### Implications for the Field

- **Practical Long-Context**: Makes 64K-256K context window inference economically viable
- **Alternative to Scaling**: Compression complementary to model scaling for capability increase
- **Future Direction**: Suggests encoder-decoder paradigm more promising than pure architectural modifications

### Limitations and Open Questions

1. **Generalization**: Unclear how encoders trained on one task generalize to others
2. **Adaptive Compression**: Fixed compression ratios may be suboptimal—could benefit from input-dependent compression levels
3. **Theoretical Understanding**: Lacks formal analysis of what information is preserved in latent representations
4. **Domain Adaptation**: May require fine-tuning encoders for specialized domains

## Code & Resources

### Implementation Approach

Based on the paper description, implementation would likely involve:

- **Base Architecture**: PyTorch or JAX with transformer-based encoder-decoder
- **Training Framework**: Hugging Face Transformers compatible
- **Inference Engine**: Integration with vLLM or similar serving framework

### Key Components

1. **Encoder Module**:
   - Configurable transformer encoder
   - Supports various attention patterns
   - Output projection to decoder embedding dimension

2. **Decoder Integration**:
   - Latent context prepending mechanism
   - Compatibility with existing chat/instruction templates
   - Streaming generation support

3. **Inference Optimization**:
   - Batch compression before generation
   - KV cache management for latent representations
   - Multi-GPU distribution strategies

### Quick-Start Guide

1. Start with RULER (4K) benchmark for easier validation
2. Use Qwen3-4B-Instruct as baseline decoder
3. Train simple 2-4 layer encoder with local attention pattern
4. Evaluate TTFT and accuracy trade-off
5. Scale to deeper encoder and test generalization

## Related Work & Context

### Prior Compression Approaches

1. **Token Selection Methods**:
   - SnapKV: Attention-pattern-based selection
   - KVzip: Clustering-based compression
   - Limitation: All maintain O(T) complexity

2. **State Compression**:
   - Gisting: Separate dense summarization
   - Context distillation approaches
   - Often separate from main training pipeline

3. **Architectural Modifications**:
   - Linear attention variants
   - State space models
   - Trade-off between quality and efficiency

### Future Research Directions

1. **Adaptive Compression**: Input-dependent compression ratios based on content complexity

2. **Multi-Modal Extension**: Extending encoder-decoder compression to images, audio, and video

3. **Hybrid Approaches**: Combining encoder-decoder compression with token pruning or quantization

4. **Theoretical Foundation**: Formalizing information preservation guarantees in latent representations

5. **Domain-Specific Optimization**: Specialized encoders for legal, scientific, or code domains with unique long-range structure

6. **Streaming Compression**: Online compression algorithms for continuous context streams

## Impact and Significance

This work represents a paradigm shift in long-context inference, moving from purely architectural innovations to pragmatic compression-based approaches. By demonstrating that well-designed compressors can achieve 8×-10× inference speedup without proportional quality loss, the paper makes long-context reasoning economically viable at scale, potentially enabling new applications in agentic AI, knowledge synthesis, and persistent memory systems.
