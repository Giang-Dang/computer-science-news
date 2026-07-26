# Lumos-1: On Autoregressive Video Generation with Discrete Diffusion from a Unified Model Perspective

## Executive Summary

Lumos-1 presents a purely LLM-based unified architecture for autoregressive video generation that combines discrete diffusion with novel techniques for efficient training and inference. Introducing MM-RoPE (Multimodal Rotary Position Embedding) for proper spatiotemporal modeling and AR-DF (Autoregressive Discrete Diffusion Forcing) for frame-wise loss balancing, the model achieves competitive performance comparable to state-of-the-art systems like EMU3, COSMOS, and OpenSoraPlan while training on only 48 GPUs. This work establishes an efficient pathway for scaling unified autoregressive video generation without massive computational infrastructure.

## Problem Statement

Video generation has rapidly advanced but faces significant challenges:

1. **Computational scaling**: Existing text-to-video models (EMU3, COSMOS, OpenSoraPlan) require massive GPU clusters (hundreds to thousands of GPUs)
2. **Architecture heterogeneity**: Most systems combine components from different paradigms (RNNs for sequential modeling, CNNs for spatial processing, attention for reasoning)
3. **Positional encoding limitations**: Standard RoPE (1D) is poorly suited for spatiotemporal video data; naive 3D extensions create frequency imbalance
4. **Training instability**: Autoregressive generation suffers from frame-wise information redundancy causing training imbalance
5. **Unified modeling gap**: Lack of principled unified architectures that treat text-to-video as a coherent language modeling problem

Prior work fails to elegantly handle the distinct challenges of spatiotemporal correlation modeling while maintaining training efficiency.

## Core Concepts & Theory

### Autoregressive Discrete Diffusion

Unlike continuous diffusion models that gradually denoise from pure noise, discrete diffusion models work in discrete token spaces:

```
Input: Video frames tokenized into discrete tokens
      ↓
Corruption: Gradually increase mask/noise in tokens
      ↓
Denoising: Train model to predict missing tokens
      ↓
Generation: Iterative refinement during inference
```

The key advantage is native compatibility with language models that already work on discrete tokens, enabling unified LLM-based architectures.

### MM-RoPE: Multimodal Rotary Position Embedding

**Problem with standard RoPE**: Designed for 1D sequences (text), it has equal frequency coverage across all dimensions, which is suboptimal for spatiotemporal data.

**Problem with naive 3D extension**: Naive attempts to extend RoPE to 3D create:
- Imbalanced frequency spectra across spatial and temporal dimensions
- Poor modeling of intra-frame dependencies vs. inter-frame dependencies

**MM-RoPE Solution**:
```
Text RoPE (preserved):         1D frequency spectrum optimized for sequences
Video RoPE (novel):            3D frequency spectrum with:
                               - Comprehensive frequency coverage
                               - Scaled 3D position encoding
                               - Balanced spatial and temporal modeling
```

MM-RoPE seamlessly accommodates both text and video modalities within a unified LLM architecture, achieving:
- Better dependency modeling between frames
- Improved spatial coherence within frames
- Natural handling of variable-length sequences

### Autoregressive Discrete Diffusion Forcing (AR-DF)

**Problem**: Frame-wise training loss imbalance due to spatial information redundancy. Early frames in a video contain most visual information; later frames are predictable, causing training instability.

**AR-DF Solution**: Temporal tube masking during training
```
Frame 1: [X X X X]  (mask pattern: every pixel from random map)
Frame 2: [X X X X]  (same mask pattern repeated)
Frame 3: [X X X X]  (temporal continuity in masking)
        ↓
Encourages consistent reasoning across frames
```

**Key innovation**: During inference, uses a compatible masking policy to avoid quality degradation:
- Training masking: Temporal tube masking with frame-level consistency
- Inference masking: Progressive refinement following training scheme

**Benefits**:
- Balanced gradients across frames
- Temporal consistency naturally encouraged
- Stable training without tricks or careful tuning

## Main Ideas & Contributions

### 1. Unified LLM Architecture for Video Generation

**Contribution**: Pure LLM-based design where video generation is treated as language modeling in discrete token space.

**Innovation**: Demonstrates that language models designed for text are powerful enough for multimodal tasks when given proper positional encoding.

**Advantage**: Single unified architecture reduces engineering complexity and enables knowledge transfer between text and video modalities.

### 2. MM-RoPE for Spatiotemporal Correlation

**Contribution**: First principled positional encoding for video in LLM context.

**Technical details**:
- Preserves original 1D RoPE for text, ensuring no degradation on text tasks
- Introduces multimodal frequency allocation for video
- Scaled 3D positions to handle variable frame counts

**Benchmark results**:
- GenEval score: 0.591
- VBench-OC: 0.249
- VBench-IQ: 0.559
- Outperforms VideoRoPE and HoPE variants

### 3. AR-DF: Training-Friendly Discrete Diffusion

**Contribution**: Solves frame-wise loss imbalance in autoregressive video generation.

**Technical approach**:
- Temporal tube masking: Repeat frame-level random mask across time
- Intra-frame bidirectionality: Allow dependencies within frames
- Inter-frame temporal causality: Respect temporal order

**Result**: Stable training without quality degradation during inference.

### 4. Memory-Efficient Scaling

**Contribution**: Achieves competitive performance with minimal computational resources.

**Performance**:
- 48 GPUs only (vs. hundreds/thousands for competitors)
- Pre-trained on 60 million images and 10 million videos
- Comparable to EMU3 on GenEval
- Comparable to COSMOS-Video2World on VBench-I2V
- Comparable to OpenSoraPlan on VBench-T2V

## Methodology & Implementation

### Datasets and Experimental Setup

**Pre-training Data**:
- 60 million images with captions
- 10 million videos with descriptions
- Mixed sources (LAION-like datasets, video datasets)

**Tokenization**:
- Image/video frames tokenized via pre-trained VQ-VAE or similar
- Text tokenized via standard BPE tokenizer
- Discrete token sequences fed to unified LLM

**Training Configuration**:
- Model size: [Specific architecture details available in paper]
- Batch size: Optimized for 48 GPUs
- Training duration: [Specific timeline in paper]
- Optimization: Stage-wise training with memory-efficient techniques

### Evaluation Metrics and Benchmarks

| Benchmark | Metric | Lumos-1 | EMU3 | COSMOS | OpenSoraPlan |
|-----------|--------|---------|------|--------|--------------|
| GenEval | Score | 0.591 | Comparable | - | - |
| VBench-OC | Score | 0.249 | - | - | - |
| VBench-IQ | Score | 0.559 | - | - | - |
| VBench-I2V | Score | Comparable | - | Comparable | - |
| VBench-T2V | Score | Comparable | - | - | Comparable |

[Exact figures for comparative baselines unavailable — see full paper]

### Training and Inference Algorithm

**Training Phase**:
```
Input: Text prompt, target video frames (tokenized)
      ↓
1. Sample corruption level t
2. Apply temporal tube masking to create corrupted frames
3. Forward pass through LLM with MM-RoPE
4. Predict tokens for masked positions
5. Compute loss with frame-wise balancing
6. Backprop and update
```

**Inference Phase**:
```
Input: Text prompt
      ↓
1. Initialize with all tokens masked
2. For t = T down to 1:
   - Run LLM to predict token probabilities
   - Sample new tokens based on probabilities
   - Update mask according to schedule
3. Decode discrete tokens back to video frames
```

## Practical Applications & Use Cases

### 1. Content Creation and Media

- Text-to-video generation with high quality and efficiency
- Real-time or near-real-time video synthesis
- Cost-effective video production pipeline
- Accessible video generation for smaller studios

### 2. Advertising and Marketing

- Rapid generation of multiple video variations
- Personalized video content at scale
- Efficient A/B testing of video concepts
- Cost reduction compared to traditional video production

### 3. Research and Development

- Foundation model for other vision-language tasks
- Efficient baseline for video generation research
- Accessible platform for academic research
- Standardized benchmark for video generation

### 4. Interactive Applications

- Real-time interactive video manipulation
- Video editing assistance
- Streaming applications requiring efficient generation
- Mobile or edge device deployment

## Insights & Implications

### Broader Field Impact

1. **Efficiency matters**: Demonstrates that massive computational resources aren't strictly necessary for competitive performance—proper architecture design enables efficiency

2. **Unified design**: Pure LLM architecture validates the power of language modeling as a universal paradigm across modalities

3. **Positional encoding is crucial**: MM-RoPE contribution suggests that existing architectures may be suboptimal; small changes yield significant improvements

4. **Discrete vs. continuous**: Discrete diffusion in token space provides training advantages over continuous diffusion in pixel/latent space

### State-of-the-Art Advancement

- Establishes new efficiency frontier for video generation
- Provides practical pathway for broader deployment
- Enables smaller organizations to participate in video generation research
- Competitive quality at 20-50× lower computational cost than prior work

### Limitations and Open Questions

1. **Generalization**: How well does MM-RoPE transfer to other multimodal tasks?

2. **Scaling laws**: What are the optimal allocation of parameters between spatial and temporal dimensions?

3. **Quality ceiling**: Is there a fundamental limit to discrete diffusion quality, or can it match continuous methods with more compute?

4. **Inference speed**: Current inference still requires iterative refinement; can single-step or few-step methods work with this architecture?

5. **Fine-grained control**: Limited controllability over specific video regions compared to some concurrent approaches

## Code & Resources

### Official Resources
- **ArXiv Paper**: https://arxiv.org/abs/2507.08801
- **Full Paper PDF**: https://arxiv.org/pdf/2507.08801
- **Venue**: ICLR 2026 (Camera Ready)

### Dependencies and Compute Requirements
- **Framework**: PyTorch
- **Training**: 48 A100 GPUs (8-16 hours per phase)
- **Inference**: Single GPU inference possible
- **Memory**: Moderate VRAM requirements due to memory-efficient techniques

### Implementation Highlights
- Efficient attention mechanisms
- Gradient checkpointing
- Model parallelism for 48-GPU training
- Stage-wise training to manage memory

## Related Work & Context

### Prior Work Foundations

1. **Discrete Diffusion Models**: VQGAN, VQ-VAE-2, Latent Diffusion
2. **Language Models**: GPT series, LLaMA, establishing transformer dominance
3. **Multimodal Models**: Vision-language models combining text and images
4. **Video Generation**: EMU3, COSMOS, OpenSora series

### Related Recent Papers

- "Flex-Forcing": Unified autoregressive and bidirectional video diffusion
- "Uniform Discrete Diffusion with Metric Path": Alternative discrete approaches
- "Reward Forcing": Efficient streaming video generation
- "VRoPE": Video-specific rotary position embeddings

### Possible Future Research Directions

1. **Inference acceleration**: Single-step or few-step generation methods
2. **Fine-grained control**: Region-based or token-level control over generation
3. **Longer video synthesis**: Extending beyond standard 4-16 second videos
4. **Multimodal integration**: Audio, music, or scene descriptions alongside text
5. **Efficient deployment**: Distillation and quantization for edge devices
6. **Hybrid approaches**: Combining discrete and continuous diffusion benefits

## References

- **Full Paper**: [2507.08801] Lumos-1: On Autoregressive Video Generation with Discrete Diffusion from a Unified Model Perspective (ICLR 2026)
- **Conference**: International Conference on Learning Representations (ICLR) 2026
- **Status**: Camera Ready Version
