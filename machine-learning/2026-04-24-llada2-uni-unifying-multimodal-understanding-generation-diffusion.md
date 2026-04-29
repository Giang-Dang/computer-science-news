# LLaDA2.0-Uni: Unifying Multimodal Understanding and Generation with Diffusion Large Language Model

**ArXiv ID:** [2604.20796](https://arxiv.org/abs/2604.20796)  
**Authors:** Tiwei Bie, Haoxing Chen, Tieyuan Chen, Zhenglin Cheng, Long Cui, Kai Gan, Zhicheng Huang, Zhenzhong Lan, Haoquan Li, Jianguo Li, Tao Lin, Qi Qin, Hongjun Wang, Xiaomei Wang, Haoyuan Wu, Yi Xin, Junbo Zhao (Inclusion AI, Ant Group)  
**Official Code:** [https://github.com/inclusionAI/LLaDA2.0-Uni](https://github.com/inclusionAI/LLaDA2.0-Uni)  
**Model Weights:** [https://huggingface.co/inclusionAI/LLaDA2.0-Uni](https://huggingface.co/inclusionAI/LLaDA2.0-Uni)  
**Submitted:** April 24, 2026  
**Field:** Machine Learning / Multimodal Models / Diffusion Language Models

---

## Executive Summary

LLaDA2.0-Uni presents a fundamental paradigm shift in unified multimodal AI: instead of bolting vision capabilities onto an autoregressive LLM backbone, it builds a **natively unified discrete diffusion large language model** that treats text and image tokens symmetrically under the same masked diffusion framework. By combining a semantic visual discretizer (SigLIP-VQ), a Mixture-of-Experts diffusion backbone, and a high-fidelity diffusion decoder, the model matches specialized vision-language models on multimodal understanding benchmarks while achieving competitive image generation and editing — all in a single model. This establishes discrete diffusion as a promising, scalable alternative to the autoregressive paradigm for building the next generation of unified foundation models.

---

## Problem Statement

### The Unification Challenge

The field has long pursued a "one model for everything" vision: a system that can understand images, generate images, answer visual questions, and follow complex instructions involving both modalities. However, current unified models face a structural tension:

**Autoregressive approaches (GPT-4o, Gemini, LLaVA-style):**
- Excellent at multimodal understanding (visual question answering, captioning, reasoning)
- Image generation requires separate discrete tokenization or a bolt-on diffusion decoder
- The autoregressive token-by-token generation is fundamentally mismatched with 2D spatial image structure
- Bidirectional reasoning about image content is limited by unidirectional attention

**Pure diffusion approaches (DALL-E 3, Stable Diffusion, FLUX):**
- State-of-the-art image generation quality
- Cannot do instruction following or text reasoning
- No natural interface for multimodal understanding tasks

**Hybrid approaches (MLLM + diffusion decoder, e.g., Show-o, Chameleon):**
- Bolts an autoregressive LLM and a diffusion generator together
- Two separate model families with different training objectives
- The interface between them is a learned adapter, not a principled unification

### The Masked Diffusion Opportunity

The LLaDA line of work (LLaDA v1, LLaDA2.0 at 100B scale) has demonstrated that **masked discrete diffusion language models** can match or exceed autoregressive LLMs on text-only benchmarks while offering unique advantages:
- Bidirectional context for all tokens (no causal mask)
- Parallel decoding (faster inference at quality parity)
- Natural handling of "fill-in-the-middle" tasks without tricks

LLaDA2.0-Uni extends this framework to images, asking: *what if we discretize images into tokens and apply masked diffusion to text and image tokens jointly?*

---

## Core Concepts & Theory

### Discrete Diffusion for Language

In a masked discrete diffusion model, the forward process corrupts text by randomly masking tokens:

$$q(\mathbf{x}_t \mid \mathbf{x}_0) = \prod_i q(x_t^i \mid x_0^i)$$

where each token is independently masked with probability $t/T$ (linear noise schedule) or replaced with a `[MASK]` token:

$$q(x_t^i \mid x_0^i) = (1 - \sigma(t)) \cdot \delta_{x_0^i} + \sigma(t) \cdot \delta_{[\text{MASK}]}$$

The reverse process (denoising) uses a bidirectional transformer to predict the unmasked token distribution:

$$p_\theta(\mathbf{x}_0 \mid \mathbf{x}_t) = \prod_i p_\theta(x_0^i \mid \mathbf{x}_t)$$

Training objective (masked token prediction):
$$\mathcal{L}_\text{dLLM} = \mathbb{E}_{t, \mathbf{x}_0, \mathbf{x}_t}\left[\sum_{i: x_t^i = [\text{MASK}]} -\log p_\theta(x_0^i \mid \mathbf{x}_t)\right]$$

This is equivalent to BERT's masked language modeling loss but with a continuous-time noise level.

### Visual Discretization via SigLIP-VQ

For images to participate in masked diffusion, continuous pixel values must be converted to discrete tokens. LLaDA2.0-Uni uses **SigLIP-VQ**, a vision encoder fine-tuned with vector quantization:

1. **SigLIP encoder** maps image patches to continuous embeddings $\mathbf{e}_\text{vis} \in \mathbb{R}^{H \times W \times d}$
2. **Vector quantization** maps each embedding to the nearest codebook entry: $\hat{e}_i = \arg\min_{c \in \mathcal{C}} \|e_i - c\|_2$
3. The discrete visual token sequence $\mathbf{v} \in \{0, \ldots, |\mathcal{C}|-1\}^{H \times W}$ is appended to the text token sequence

Key design choices:
- **Semantic codebook:** SigLIP's visual-semantic pretraining ensures the codebook captures semantically meaningful visual concepts rather than low-level texture patterns
- **High codebook utilization:** 8,192-entry codebook with >95% utilization, preventing codebook collapse
- **Spatial structure preservation:** 2D positional embeddings for visual tokens preserve spatial relationships

### Block-Level Masked Diffusion

In a naive extension, we would apply token-level masking uniformly to text + image tokens. LLaDA2.0-Uni instead uses **block-level masking**, where text and image tokens are masked independently with potentially different noise levels $\sigma_\text{text}(t)$ and $\sigma_\text{img}(t)$.

This allows the model to:
- Generate text conditioned on fully revealed images (understanding mode)
- Generate images conditioned on fully revealed text (generation mode)
- Generate both modalities jointly with partial conditioning (interleaved generation)

### MoE-Based dLLM Backbone

The backbone is a **Mixture-of-Experts (MoE) discrete diffusion LLM** — combining the parameter efficiency of MoE with the bidirectional reasoning of diffusion. With $N$ total experts and top-$k$ routing:
- Each token routes to the top-$k$ expert FFN layers based on a learned router
- Total parameters: ~7× more than an equivalent dense model
- Active parameters per token: same as a dense model of the base size

For the dLLM, the MoE backbone is adapted with:
- **Modality-conditioned routing:** Separate routing logits for text vs. image tokens
- **Cross-modal attention:** Full bidirectional attention across text and image tokens (no separation of modality-specific attention heads)

### Diffusion Decoder

The VQ-encoded visual tokens lose some fine-grained pixel detail. To reconstruct high-fidelity images, LLaDA2.0-Uni uses a **continuous diffusion decoder** that takes discrete visual tokens as conditioning:

$$p_\phi(\mathbf{x}_\text{image} \mid \mathbf{v}) \approx \text{DDPM}_\phi(\mathbf{v})$$

The decoder is a standard DiT conditioned on the discrete token sequence, fine-tuned to reconstruct pixel-level detail. This two-stage design (discrete backbone → continuous decoder) enables:
- Fast joint inference in the discrete space
- High-quality final image output via the pixel-space decoder

---

## Main Ideas & Key Contributions

### 1. Symmetric Multimodal Diffusion

Unlike all prior unified models that treat text as "primary" and images as "auxiliary" (or vice versa), LLaDA2.0-Uni treats both modalities as **first-class citizens** in the same masked diffusion framework. This means:
- Understanding and generation use the same model, not two models bridged by adapters
- Cross-modal reasoning is natural (bidirectional attention sees both text and image tokens)
- The model can condition generation on partial observations of both modalities simultaneously

### 2. Semantic Visual Tokenization

The SigLIP-VQ tokenizer is the first to demonstrate that **semantically pre-trained vision encoders produce better VQ codebooks** for unified multimodal diffusion. Compared to vanilla VQ-VAE tokenizers:
- +4.2 points on VQA-v2
- +1.1 FID on class-conditional generation
- Better robustness to image quality variation

### 3. Interleaved Generation and Reasoning

Because text and image tokens are handled symmetrically, LLaDA2.0-Uni natively supports:
- Generating an image, then reasoning about it, then generating more text
- Partially completing an image (image inpainting as a special case of masked diffusion)
- Editing images via text instructions (mask the parts to change, condition on the instruction)

### 4. Competitive Performance Across Both Tasks

Previously, models that were good at generation (diffusion models) were bad at understanding (VQA), and vice versa. LLaDA2.0-Uni achieves:
- **Understanding:** Competitive with LLaVA-1.6-34B on MMBench, SeedBench, MMMU
- **Generation:** FID competitive with DALL-E 2 on MS-COCO
- **Editing:** Strong performance on image editing benchmarks (IEVE, EditBench)

---

## Methodology & Implementation

### Architecture Details

| Component | Design | Parameters |
|-----------|--------|-----------|
| Visual Tokenizer | SigLIP-VQ (16×16 patches, 8192-entry codebook) | 400M |
| dLLM Backbone | MoE Transformer, 16 experts, top-2 routing, 24 layers | 7B active / 50B total |
| Diffusion Decoder | DiT-XL/2 conditioned on discrete tokens | 600M |
| Total | — | ~51B total, ~8B active |

### Training Pipeline (4 Stages)

**Stage 1 — Visual Tokenizer Pre-training:**
- Train SigLIP-VQ on image-only data
- Objective: reconstruction + semantic alignment (SigLIP contrastive loss)
- Data: 1B image-text pairs

**Stage 2 — Text-Only dLLM Pre-training:**
- Initialize backbone with LLaDA2.0 weights (pre-trained on 3T text tokens)
- Freeze tokenizer; train backbone on masked text prediction
- This leverages the strong text capabilities of the LLaDA2.0 series

**Stage 3 — Multimodal Joint Training:**
- Unfreeze all components
- Train on interleaved image-text data
- Objective: masked diffusion loss over both text and image tokens
- Data: 500B text + image tokens

**Stage 4 — Instruction Fine-tuning:**
- SFT on visual instruction-following data (LLaVA-Instruct-style)
- RLHF-style preference optimization for generation quality
- Data: 50M instruction-following pairs

### Evaluation Benchmarks

**Understanding benchmarks:**
- MMBench, SeedBench, MMMU, VQA-v2, TextVQA, GQA, DocVQA

**Generation benchmarks:**
- FID on MS-COCO 30K (CLIP-filtered prompts)
- Human preference scores (ELO rating vs. DALL-E 2, FLUX-schnell)

**Editing benchmarks:**
- IEVE (Instruction-guided Visual Editing), EditBench

### Key Results

| Task | LLaDA2.0-Uni | Reference Model | Gap |
|------|-------------|-----------------|-----|
| MMBench | 77.3% | LLaVA-1.6-34B: 79.4% | -2.1pp |
| MMMU | 52.1% | Qwen-VL-72B: 56.8% | -4.7pp |
| FID (COCO) | 14.2 | DALL-E 2: 10.4 | +3.8 |
| EditBench | 72.1% | InstructPix2Pix: 69.3% | +2.8pp |

The understanding gap vs. specialized models is small and expected to close with scale; generation quality is already competitive with dedicated generators.

---

## Practical Applications & Real-World Use Cases

### 1. Unified Creative Assistant

A single LLaDA2.0-Uni deployment can handle:
- "Describe this image" (understanding)
- "Create an image of [prompt]" (generation)
- "Edit this image to make the sky purple" (editing)
- "Generate a story with an illustration for each paragraph" (interleaved)

Eliminating the need for 3–4 separate models reduces deployment complexity and inference infrastructure cost.

### 2. Document Intelligence with Generation

Enterprise document workflows often require both understanding documents and generating new content. LLaDA2.0-Uni enables:
- Extract data from charts/tables (understanding) → generate updated visualizations (generation)
- Analyze product images (understanding) → generate ad copy + hero image (generation)

### 3. Visual Reasoning with Iterative Refinement

The model's masked diffusion framework enables a unique interaction pattern: partially generate an image, reason about it, then continue generation — a form of visual chain-of-thought that autoregressive models cannot naturally support.

### 4. Medical Imaging Report Generation

Analyze radiology images and generate structured reports. The bidirectional attention allows the model to condition the text report generation on the full image context simultaneously rather than sequentially.

### Implementation Considerations

- **Memory:** 8B active parameters; requires ~16GB VRAM for BF16 inference
- **Speed:** ~2–5 seconds per image on A100 (20 diffusion steps)
- **API:** Hugging Face `transformers` compatible interface via `inclusionAI/LLaDA2.0-Uni`

---

## Insights & Implications

### Discrete Diffusion as Unified Foundation

LLaDA2.0-Uni's most important implication is that **autoregressive generation is not the only scalable path to unified multimodal models**. Discrete diffusion provides bidirectionality and parallel decoding that may become decisive advantages at scale, particularly for tasks requiring global reasoning over both modalities.

### MoE + Diffusion Synergy

The MoE backbone enables different experts to specialize in different modalities or different types of visual content without the performance degradation that comes from fine-tuning a dense model on diverse multimodal data. This specialization without interference is a key scalability advantage.

### The Semantic Tokenizer Hypothesis

The strong performance of SigLIP-VQ (vs. pixel-space VQ-VAE tokenizers) suggests that **the quality of visual discretization is a bottleneck for unified multimodal diffusion** — not just the backbone architecture. Future work should invest heavily in better visual tokenizers.

### Limitations

1. **Generation quality gap:** Still lags behind state-of-the-art dedicated generators (FLUX, SD3.5) by a meaningful margin
2. **Video:** Not extended to video; 3D temporal extension is nontrivial
3. **Training cost:** 4-stage training pipeline is complex and expensive; smaller teams cannot easily reproduce
4. **Evaluation breadth:** Interleaved generation quality is not yet systematically benchmarked

### Open Questions

- Can discrete diffusion scale to match GPT-4o-level multimodal understanding?
- Does the bidirectional attention advantage lead to better compositional reasoning?
- Can the framework be extended to audio, code, and other modalities uniformly?

---

## Code & Resources

- **GitHub:** [https://github.com/inclusionAI/LLaDA2.0-Uni](https://github.com/inclusionAI/LLaDA2.0-Uni)
- **Model on HuggingFace:** [https://huggingface.co/inclusionAI/LLaDA2.0-Uni](https://huggingface.co/inclusionAI/LLaDA2.0-Uni)
- **ArXiv:** [https://arxiv.org/abs/2604.20796](https://arxiv.org/abs/2604.20796)
- **Predecessor:** [LLaDA2.0 (2512.15745)](https://arxiv.org/abs/2512.15745)

### Quick Start

```python
from transformers import AutoProcessor, AutoModel
import torch

model = AutoModel.from_pretrained("inclusionAI/LLaDA2.0-Uni", torch_dtype=torch.bfloat16)
processor = AutoProcessor.from_pretrained("inclusionAI/LLaDA2.0-Uni")

# Visual understanding
inputs = processor(
    text="What is in this image?",
    images=image,
    return_tensors="pt"
)
output = model.generate(**inputs, task="understanding")

# Image generation
inputs = processor(text="A sunset over the ocean with dramatic clouds", return_tensors="pt")
image = model.generate(**inputs, task="generation", num_steps=20)
```

### Dependencies

```bash
pip install transformers>=4.45 torch>=2.3 diffusers>=0.30
# For optimal speed:
pip install flash-attn xformers
```

---

## Related Work & Context

### Lineage

- **LLaDA v1 (2502.09992):** First masked diffusion LLM, showed competitiveness with GPT-2 scale ARs
- **LLaDA2.0 (2512.15745):** Scaled to 100B parameters, competitive with LLaMA-3-70B
- **LLaDA2.0-Uni (this work):** Extends LLaDA2.0 to multimodal understanding + generation

### Comparison with Other Unified Models

| Model | Architecture | Understanding | Generation | Unified? |
|-------|-------------|---------------|------------|---------|
| GPT-4o | AR + VQVAE | ✓✓✓ | ✓✓ | Partial |
| Show-o | AR + Diffusion hybrid | ✓✓ | ✓✓ | Partial |
| Chameleon | AR discrete tokens | ✓✓ | ✓ | Yes |
| **LLaDA2.0-Uni** | Masked diffusion | ✓✓ | ✓✓ | **Yes** |
| FLUX + LLaVA | Separate models | ✓✓✓ | ✓✓✓ | No |

### Where This Leads

1. **Scaling:** LLaDA3.0-Uni with 200B+ total parameters
2. **Video unification:** Extend masked diffusion to temporal sequences
3. **Multi-task instruction tuning:** RLHF/DPO for joint multimodal alignment
4. **Real-time applications:** Distillation to smaller unified models for edge deployment
