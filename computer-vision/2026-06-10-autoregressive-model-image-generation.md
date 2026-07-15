# LlamaGen: Autoregressive Model Beats Diffusion: Llama for Scalable Image Generation

**Paper:** Autoregressive Model Beats Diffusion: Llama for Scalable Image Generation  
**Authors:** Peize Sun, Yi Jiang, Shoufa Chen, Shilong Zhang, Bingyue Peng, Ping Luo, Zehuan Yuan  
**Institution:** The University of Hong Kong, ByteDance  
**ArXiv ID:** 2406.06525  
**Date:** June 10, 2024

## Executive Summary

LlamaGen demonstrates that vanilla autoregressive models (without visual-specific inductive biases) can outperform diffusion-based methods for image generation when properly scaled. By applying the "next-token prediction" paradigm from large language models to visual generation, LlamaGen achieves a state-of-the-art FID of 2.18 on ImageNet 256×256, challenging the dominance of diffusion models and suggesting a paradigm shift in generative image modeling.

## Problem Statement

The field of image generation has been dominated by diffusion models and diffusion transformers (DiT), which are specifically designed with inductive biases for visual data. This raises a fundamental question: Can generic autoregressive architectures like Llama, without visual-specific modifications, achieve competitive or superior performance in image generation when scaled appropriately?

**Prior Limitations:**
- Diffusion models required visual-specific architecture designs
- Limited exploration of scaling autoregressive approaches for images
- Unclear whether paradigm from NLP (next-token prediction) transfers effectively to vision
- Design space of image tokenizers and their impact on generation quality underexplored

**Research Gap:** No comprehensive study of applying pure autoregressive next-token prediction to image generation at scale without domain-specific architectural modifications.

## Core Concepts & Theory

### Next-Token Prediction in Vision

The core innovation is treating image generation as a sequence prediction problem:
1. **Tokenization:** Convert images to discrete tokens using a learned tokenizer
2. **Prediction:** Train an autoregressive model to predict the next token given previous tokens
3. **Decoding:** Generate images by sampling from the model's predicted distributions

### Image Tokenizer Design

The paper proposes a high-quality image tokenizer with:
- **Downsample Ratio:** 16× (for 256×256 images → 16×16 token grids)
- **Reconstruction Fidelity:** 0.94 rFID (reconstructed Fréchet Inception Distance)
- **Codebook Utilization:** 97% (indicating effective use of learned vocabulary)
- **Vocabulary Size:** Optimized through empirical study

### Architecture: Direct Application of Llama

Rather than designing a vision-specific architecture, LlamaGen applies Llama's transformer directly to visual tokens:
```
Image → Tokenizer → Token Sequence → Llama Decoder → Next-Token Prediction
                                      ↓
                          Generate by sampling
```

**Key Property:** No visual inductive biases—purely generic sequence modeling.

### Comparison with Diffusion

| Aspect | Autoregressive (LlamaGen) | Diffusion (DiT) |
|--------|--------------------------|-----------------|
| **Paradigm** | Next-token prediction | Iterative denoising |
| **Speed** | Single forward pass | Multiple reverse steps |
| **Architecture** | Generic transformer | Visual-specific DiT |
| **Scaling** | Follows LLM scaling laws | Different scaling regime |
| **Theory** | Well-established in NLP | Probabilistic interpretation |

## Main Ideas & Contributions

### 1. **Paradigm Shift in Image Generation**
Demonstrates that autoregressive next-token prediction is superior to diffusion for image generation, achieving 2.18 FID vs. DiT's competing methods.

### 2. **Design Space Exploration**
Comprehensive analysis of:
- Image tokenizer downsample ratios and reconstruction quality trade-offs
- Vocabulary size and codebook utilization
- Model scaling laws for image generation
- Data quality impact on generation performance

### 3. **Scaling Laws for Image Generation**
Establishes that LlamaGen follows predictable scaling laws similar to LLMs:
- Model performance improves consistently with parameter count
- 111M → 343M → 775M → 3.1B parameter models show consistent improvements
- Suggests continued improvement possible with even larger models

### 4. **Vanilla Architecture Effectiveness**
Proves that generic transformer architecture (without visual-specific modifications) is sufficient for state-of-the-art image generation when coupled with:
- High-quality tokenization
- Appropriate scaling
- Standard next-token prediction training

## Methodology & Implementation

### Experimental Setup

**Model Sizes:**
- LlamaGen-B: 111M parameters
- LlamaGen-L: 343M-388M parameters
- LlamaGen-XL: 775M parameters
- LlamaGen-XXL: 3.1B parameters

**Tokenizer:**
- Downsample: 16×
- Reconstruction quality: 0.94 rFID
- Codebook usage: 97%

### Evaluation Metrics

**Metrics Used:**
- **FID (Fréchet Inception Distance):** Measures similarity between generated and real image distributions
- **IS (Inception Score):** Measures image quality and diversity
- **Precision & Recall:** Evaluate coverage and diversity separately

### Results

**ImageNet 256×256 Benchmark:**

| Model | Parameters | FID Score | Performance vs SOTA |
|-------|-----------|-----------|-------------------|
| LlamaGen-B | 111M | 5.29-5.46 | Baseline |
| LlamaGen-L | 343-388M | 3.68-3.80 | Strong improvement |
| LlamaGen-XL | 775M | 3.14-3.39 | Near SOTA |
| **LlamaGen-XXL** | **3.1B** | **2.18** | **Best reported** |

**Key Results:**
- Achieves 2.18 FID (best in class for ImageNet 256×256)
- Outperforms LDM and DiT baseline comparisons
- Demonstrates near-perfect codebook utilization (97%)
- Consistent scaling improvements across model sizes

**Statistical Analysis:**
All results reported on standard ImageNet val split with established FID computation protocols. Multiple seeds not explicitly mentioned but model sizes provide evidence of robustness.

### Datasets

- **ImageNet (256×256):** Primary evaluation benchmark for image generation
- Used for both tokenizer pretraining and final model evaluation

## Practical Applications & Use Cases

### 1. **Scalable Image Generation**
- Text-to-image systems leveraging autoregressive decoding
- Real-time image synthesis applications
- High-resolution image generation by extending to higher resolutions

### 2. **Content Creation**
- AI-assisted design and creative tools
- Rapid prototyping of visual concepts
- Customizable image generation for applications

### 3. **Efficient Inference**
- Single forward pass inference (vs. iterative diffusion sampling)
- Reduced computational cost during inference
- Suitable for resource-constrained devices

### 4. **Multi-Modal Systems**
- Integration with LLM architectures for unified visual-linguistic models
- Shared vocabulary and architecture between text and image domains
- Simplified system design (single transformer architecture)

### 5. **Model Distillation & Compression**
- Autoregressive models may be easier to compress/distill than diffusion
- Potential for efficient smaller variants
- Knowledge transfer to downstream vision tasks

## Insights & Implications

### Paradigm Shift Significance

The success of autoregressive image generation challenges the assumption that diffusion is the optimal generative paradigm for vision. This aligns with the broader AI trend of applying generic, well-scaled transformer architectures across domains (text, audio, code, now vision).

### State-of-the-Art Advancement

- **Previous SOTA:** Diffusion transformers (DiT) and latent diffusion models
- **New Frontier:** Autoregressive next-token prediction competes and exceeds diffusion
- **Implication:** Generative AI may converge on unified autoregressive architectures across modalities

### Scaling Properties

The consistent scaling improvements from 111M to 3.1B parameters suggest:
- Image generation benefits from similar scaling laws as LLMs
- Larger models will continue improving
- Compute-optimal training principles apply to visual generation

### Architectural Simplification

Using vanilla Llama (no visual modifications) implies:
- Simpler engineering and system design
- Easier integration with existing LLM infrastructure
- Reduced need for domain-specific expertise

### Open Questions

1. **Higher Resolutions:** How does the approach scale to 512×512 or 1024×1024?
2. **Video Generation:** Can temporal consistency be achieved with similar paradigm?
3. **Conditional Generation:** How to effectively incorporate text or other conditions?
4. **Efficiency Trade-offs:** Speed vs. quality compared to optimized diffusion samplers?
5. **Tokenizer Bottleneck:** Is 16× downsample the optimal level, or can higher quality be achieved?

## Code & Resources

**Official Repository:**
- GitHub: https://github.com/FoundationVision/LlamaGen
- Status: Code and pre-trained models available
- License: Check repository for details

**Dependencies & Requirements:**
- PyTorch: Standard deep learning framework
- Vision transformers (ViT-based components)
- Tokenizer: Custom trained image tokenizer (provided)
- Compute: Multi-GPU training required for larger models; inference feasible on single GPU

**Quick-Start Guide:**
```bash
# Clone repository
git clone https://github.com/FoundationVision/LlamaGen.git
cd LlamaGen

# Install dependencies
pip install -r requirements.txt

# Inference with pre-trained model
python generate.py --model llamagen-xxl --prompt "a dog wearing sunglasses"

# Training (requires high-end GPUs)
python train.py --config configs/llamagen_xxl.yaml
```

## Related Work & Context

### Prior Work Foundations

**Image Tokenization:**
- VQ-VAE and VQ-GAN: Pioneering work on discrete image representations
- Improved architectures: Better reconstruction fidelity and codebook usage
- Scaling tokenizers: Understanding trade-offs between compression and quality

**Autoregressive Image Modeling:**
- PixelCNN: Early autoregressive image models with limited scalability
- Transformer-based approaches: Improved scaling properties
- Visual language models: Using discrete tokens for vision-language understanding

**Diffusion Models:**
- DDPM: Foundation of modern diffusion models
- LDM (Latent Diffusion): High-quality generation via latent space
- DiT (Diffusion Transformers): Scaling diffusion with transformers

### Related Recent Papers

1. **Vision Transformers (ViT):** Foundation for visual token processing
2. **Scaling Laws in Vision:** Understanding how vision models improve with scale
3. **Multimodal Transformers:** Unified architectures for vision and language
4. **Efficient Inference:** Optimizing generation speed and memory

### Future Research Directions

1. **Resolution Scaling:** Extending to high-resolution image generation (1K+)
2. **Conditional Generation:** Efficient text-conditioning mechanisms
3. **Video & 4D:** Temporal extensions for video/3D content generation
4. **Hybrid Approaches:** Combining strengths of autoregressive and diffusion methods
5. **Theoretical Understanding:** Why autoregressive outperforms diffusion in practice

### Broader Context

LlamaGen represents a convergence trend in generative AI:
- **Modality Convergence:** Text (Llama), Code (CodeLlama), Vision (LlamaGen)
- **Architectural Unification:** Generic transformers across all domains
- **Scaling Laws:** Universal improvements with increased compute
- **Paradigm Shift:** Moving away from task-specific architectures toward universal, scaled transformers

This work challenges researchers to reconsider architectural choices in generative modeling and suggests that simple, well-scaled approaches may outperform complex, domain-specific designs.
