# Tuna-2: Pixel Embeddings Beat Vision Encoders for Multimodal Understanding and Generation

**Paper**: [arXiv:2604.24763](https://arxiv.org/abs/2604.24763)  
**Authors**: Zhiheng Liu, Weiming Ren, Xiaoke Huang, Shoufa Chen, Tianhong Li, Mengzhao Chen, Yatai Ji, Sen He, Jonas Schult, Belinda Zeng, Tao Xiang, Wenhu Chen, Ping Luo, Luke Zettlemoyer, Yuren Cong  
**Institution**: Meta AI (FAIR) and collaborating institutions  
**Submitted**: April 27, 2026  
**Field**: Computer Vision / Multimodal Learning  

---

## Executive Summary

Tuna-2 is a unified multimodal model from Meta AI that challenges the dominant paradigm of using pretrained vision encoders (such as CLIP or DINO) and VAE-based latent spaces for multimodal understanding and generation. By replacing these modules with simple patch embedding layers that operate directly on raw pixel values, Tuna-2 demonstrates that **encoder-free, end-to-end pixel-space modeling can achieve state-of-the-art performance** on both multimodal understanding and high-fidelity image generation benchmarks. This work has significant architectural implications: it suggests the entrenched modular design of vision-language models may be unnecessary, pointing toward simpler and more jointly optimizable architectures.

---

## Problem Statement

### The Encoder Lock-In Problem in Multimodal Models

Modern multimodal large language models (MLLMs) follow a well-established pattern:

1. A **vision encoder** (e.g., CLIP ViT, SigLIP) extracts visual features from images.
2. A **connector** (e.g., Q-Former, MLP projector) maps visual features into the LLM's token embedding space.
3. An **LLM backbone** performs reasoning over both visual and text tokens.
4. For generation tasks, a separate **VAE (Variational Autoencoder)** or diffusion-based decoder generates images from latent codes.

This modular pipeline has two fundamental problems:

**Misalignment between understanding and generation**: The visual representations used for understanding (e.g., CLIP features optimized for semantic similarity) differ from those used for generation (e.g., VAE latents optimized for pixel reconstruction). This forces the model to maintain dual visual representations — one semantic, one reconstructive — creating an internal inconsistency that limits unified optimization.

**Blocked end-to-end gradient flow**: Because the vision encoder is typically a frozen pretrained model, the system cannot back-propagate gradients from the final task objectives all the way through the image processing pipeline. The model cannot learn to extract task-relevant features that differ from what the frozen encoder provides.

### Limitations of Prior Work

- **BLIP-2, LLaVA, InstructBLIP**: All rely on frozen or lightly fine-tuned vision encoders, creating the misalignment described above.
- **Chameleon, Emu3**: Discretize images into tokens using a VQ-VAE, losing continuous pixel information and introducing quantization artifacts.
- **Unified-IO, Gemini**: Use separate processing pipelines for visual understanding versus generation.
- **The original Tuna (v1)**: Still relied on a representation encoder for visual understanding, separating it from the generation pathway.

The open question prior to Tuna-2 was: *Can a model be built that processes raw pixels end-to-end without any specialized visual encoders or latent-space intermediaries — and can it actually compete with encoder-based approaches?*

---

## Core Concepts & Theory

### Pixel Embeddings vs. Vision Encoders

A **vision encoder** is a deep neural network (typically a ViT or CNN) pretrained on a large visual dataset, designed to compress an image into a compact, semantically rich representation. It carries two burdens:
- It was trained with its own objective (contrastive learning, masked autoencoding, etc.), which may not perfectly align with the downstream multimodal task.
- Its weights are typically fixed or only lightly updated, preserving its original feature distribution even if that distribution is suboptimal for the current task.

A **patch embedding layer** (used in Tuna-2) is a single linear projection — literally a learned matrix multiplication — that maps a flattened image patch of pixels to a vector of the desired dimensionality. No pretraining, no complex architecture, no frozen weights. It is conceptually identical to how text tokens are embedded: a lookup table or linear layer maps a raw discrete token ID to a continuous vector. Tuna-2 applies the same philosophy to vision: map raw pixel patches to embedding vectors via a learned linear transformation.

**Mathematical formulation**:

Given an image $I \in \mathbb{R}^{H \times W \times 3}$, it is divided into $N = \frac{HW}{P^2}$ patches of size $P \times P$. Each patch $p_i \in \mathbb{R}^{P^2 \times 3}$ is flattened to a vector $\hat{p}_i \in \mathbb{R}^{3P^2}$ and projected:

$$e_i = W_{\text{patch}} \cdot \hat{p}_i + b_{\text{patch}}$$

where $W_{\text{patch}} \in \mathbb{R}^{d \times 3P^2}$ and $d$ is the LLM embedding dimension. The resulting sequence $\{e_1, \ldots, e_N\}$ is passed directly to the LLM backbone, just like text token embeddings.

**The critical difference**: Unlike a vision encoder (which performs many non-linear transformations through dozens or hundreds of layers), the patch embedding is a *single* linear layer. The LLM backbone itself must learn to process and interpret raw pixel-level information.

### Why This Can Work: The Role of Scale and Pretraining

At first glance, a single linear projection seems far too weak to capture the rich visual structure that a pretrained ViT provides. The key insight from Tuna-2 is:

- **At sufficient scale and with sufficient pretraining compute**, the LLM backbone — which is itself a massive transformer — can learn to extract the necessary visual abstractions from pixel patches.
- The LLM has vastly more capacity than a standalone vision encoder, and when trained end-to-end with the generation objective, it learns visual representations that are inherently aligned with both understanding and generation.
- Encoder-based models converge faster initially (because the encoder provides ready-made semantic features), but plateau sooner. Pixel-embedding models converge slower but ultimately achieve *higher* performance.

### Unified Pixel-Space Modeling

Tuna-2's key architectural claim: **a single model trained on raw pixels can simultaneously learn to understand images (VQA, captioning, reasoning) and generate images (text-to-image, editing), without the modular boundary that separates these in prior work**.

For generation, Tuna-2 predicts pixel patches autoregressively (or through diffusion), using the same LLM backbone as for understanding. The model never needs to map between semantic space and pixel space — it operates in pixel space throughout.

---

## Main Ideas & Key Contributions

### Contribution 1: Eliminating the Vision Encoder Entirely

Tuna-2 removes both:
- The **representation encoder** (e.g., CLIP ViT) used for visual understanding
- The **VAE/tokenizer** (e.g., VQGAN, SDVAE) used for image generation

Both are replaced by a single patch embedding layer. This is a radical architectural simplification — reducing the number of distinct pretrained components from 3+ to 1 (the LLM backbone itself).

### Contribution 2: Empirical Proof That Pixel Embeddings Scale

The paper provides systematic ablation studies showing that:
- At small scale, encoder-based models (Tuna-R, the encoder-based variant) outperform Tuna-2
- At larger compute budgets and with more pretraining, Tuna-2 catches up and surpasses encoder-based models
- The crossover point occurs at a compute scale that is practical for modern training runs

This is analogous to the finding in NLP that simpler architectures (e.g., transformer vs. LSTM) outperform more complex ones at scale — the same phenomenon appears to hold for visual processing.

### Contribution 3: State-of-the-Art on Multimodal Benchmarks

Tuna-2 achieves SOTA on a diverse suite of multimodal benchmarks, particularly excelling on:
- **Fine-grained visual perception tasks** that require detailed pixel-level understanding
- **High-fidelity image generation** metrics comparable to diffusion-based approaches
- **Image editing** tasks, where the unified representation allows coherent modifications

### Contribution 4: Theoretical and Practical Case Against Modular Design

Beyond the empirical results, Tuna-2 makes a principled argument that the modular design (encoder + connector + LLM + decoder) was a historical artifact of how the field developed — not an architectural necessity. The paper argues that end-to-end training from pixels is the right long-term direction.

---

## Methodology & Implementation

### Training Pipeline

Tuna-2's training follows a multi-stage curriculum designed to gradually build up pixel-level visual understanding:

**Stage 1 — Visual Pretraining (Pixel-level)**:
- Train the patch embedding + LLM backbone on large-scale image-text pairs
- The model learns to associate raw pixel patches with language tokens
- Key challenge: the model must bootstrap visual understanding from scratch (no pretrained encoder initialization)
- This stage requires significantly more compute than encoder-based approaches at equivalent model sizes

**Stage 2 — Unified Understanding + Generation Training**:
- Jointly train on multimodal understanding tasks (VQA, captioning) and generation tasks (text-to-image, image editing)
- The shared pixel-space representation ensures consistent gradients across both objectives
- Loss = understanding loss + generation loss (weighted sum)

**Stage 3 — Instruction Fine-Tuning**:
- Fine-tune on curated instruction-following data for chat-style interactions
- Standard RLHF/DPO alignment procedures

### Key Architectural Choices

| Component | Traditional MLLM | Tuna-2 |
|---|---|---|
| Visual input processing | Pretrained ViT encoder (frozen/fine-tuned) | Single linear patch embedding (trained from scratch) |
| Image generation | Separate VAE + diffusion decoder | Autoregressive pixel patch prediction via LLM |
| Visual feature space | Frozen semantic embedding space | Dynamically learned pixel-aligned space |
| Parameter efficiency | Encoder parameters not updated during LLM training | All parameters updated end-to-end |
| Training complexity | Lower (encoder pre-done) | Higher (more pretraining needed) |
| Final performance (at scale) | Good | Better |

### Datasets

- **Pretraining**: Large-scale image-text pairs (comparable scale to existing MLLM pretraining datasets)
- **Generation**: Text-to-image training data (similar to those used for diffusion models)
- **Instruction fine-tuning**: Mix of multimodal instruction datasets (LLaVA-type data, ShareGPT4V, etc.)

### Evaluation

Benchmarks evaluated include:
- **VQA benchmarks**: VQAv2, GQA, OK-VQA
- **Multimodal reasoning**: MMBench, MMMU, ScienceQA
- **Fine-grained perception**: TextVQA, DocVQA, ChartQA
- **Image generation**: FID, CLIP score on MS-COCO and GenAI-Bench
- **Image editing**: EditBench, MAGICBRUSH

### Results

- Tuna-2 (encoder-free) outperforms Tuna-R (encoder-based) on multimodal understanding at scale, especially on fine-grained, perception-heavy benchmarks.
- Tuna-2 achieves high-fidelity image generation quality comparable to dedicated diffusion models.
- Performance gains are most pronounced on benchmarks requiring detailed pixel-level reasoning, where the encoder's compressed semantic features are less helpful.

---

## Practical Applications & Real-World Use Cases

### 1. Unified Multimodal Assistants

The primary application is building AI assistants that can:
- Understand and reason about images with fine-grained detail
- Generate new images from text descriptions
- Edit existing images based on natural language instructions

With a single unified architecture, the system avoids the awkward handoff between understanding and generation modules that plagues current assistants.

### 2. Medical Imaging

Medical images (histopathology slides, radiology scans) often require pixel-level precision that semantic encoders may smooth over. An encoder-free model trained end-to-end on medical image data could potentially extract more diagnostically relevant features.

### 3. Satellite and Remote Sensing

High-resolution satellite imagery analysis requires detecting fine-grained spatial details. Pixel-level embeddings allow the model to preserve and reason about subtle spatial patterns that CLIP-style encoders might discard.

### 4. Document Understanding

OCR-heavy tasks (PDF parsing, chart analysis, table extraction) benefit from pixel-level feature extraction that can capture exact character shapes, font properties, and layout structure without the information loss of semantic encoders.

### 5. Simplifying Production Deployment

From a systems perspective, replacing 3+ model components with a single LLM backbone dramatically simplifies deployment. No need to maintain separate encoder services, VAE decoders, or cross-component version compatibility.

### Implementation Challenges

- **Higher pretraining compute**: The model needs substantially more training compute to bootstrap visual understanding without a pretrained encoder.
- **Longer convergence time**: The crossover point where Tuna-2 beats encoder-based models requires patience during training.
- **Memory efficiency**: Processing raw pixel patches (rather than compressed encoder features) requires more memory per image token.

---

## Insights & Implications

### Broader Implications for the Field

Tuna-2 challenges a foundational assumption of the multimodal learning field: that pretrained vision encoders are necessary for efficient visual understanding. If the results hold at larger scales and across more domains, it suggests:

1. **The field may be over-relying on transfer learning from vision encoders** — a practice inherited from data-scarce regimes that may no longer be necessary.
2. **End-to-end optimization is more important than initialization** — at sufficient scale, random initialization + enough data can match or beat carefully curated pretrained initializations.
3. **Architectural simplicity is a virtue** — the patch embedding approach is easier to understand, debug, and extend than complex modular pipelines.

### How This Advances State-of-the-Art

- Sets a new paradigm for unified multimodal model design
- Proves empirically that SOTA performance does not require specialized visual encoders
- Provides a cleaner theoretical framework: multimodal models as *unified* systems, not modular assemblies

### Limitations

- **Higher pretraining cost**: Models trained with pixel embeddings need more compute before they become competitive, creating a barrier for researchers with limited resources.
- **Domain-specific encoders may still win**: For narrow domains (e.g., medical imaging with DICOM-specific encoders), specialized pretrained encoders trained on domain data might still provide an advantage.
- **Tokenization efficiency**: Pixel patches are verbose representations — a 224×224 image at patch size 16 yields 196 tokens, all carrying raw pixel information. Efficient compression remains an open challenge.

### Open Questions

- Does the crossover point (where pixel embeddings beat encoders) shift with model scale?
- Can pixel embedding approaches work with video, where the token count explodes?
- How does this interact with quantization and efficient inference techniques?

---

## Code & Resources

- **Official GitHub**: [https://github.com/facebookresearch/tuna-2](https://github.com/facebookresearch/tuna-2)
- **Project Page**: [https://tuna-ai.org/tuna-2/](https://tuna-ai.org/tuna-2/)
- **ArXiv Paper**: [https://arxiv.org/abs/2604.24763](https://arxiv.org/abs/2604.24763)
- **HuggingFace Paper Page**: [https://huggingface.co/papers/2604.24763](https://huggingface.co/papers/2604.24763)

### Dependencies and Compute Requirements

- PyTorch (latest stable)
- Substantial GPU compute for pretraining (the paper uses infrastructure comparable to training large LLMs)
- Inference can be done on consumer hardware for smaller model variants

---

## Related Work & Context

### Builds Upon

- **Tuna (v1)**: The predecessor model that explored unification of understanding and generation, but still used a representation encoder for visual understanding.
- **Chameleon** (Meta, 2024): Used VQ-VAE tokenization for both visual understanding and generation, establishing that unified image-text models are feasible. Tuna-2 pushes further by removing even the VQ-VAE.
- **Emu3** (BAAI, 2024): Similar tokenization-based unified model; Tuna-2 surpasses this approach by working in continuous pixel space.
- **Vision Transformers (ViT)**: The core architecture insight that images can be processed as sequences of patches carries through to Tuna-2, though Tuna-2 removes the transformer-based encoder and replaces it with a simple linear projection.

### Related Contemporary Work

- **LLaDA2-Uni** (April 2026, already in this repo): Explores unified multimodal understanding and generation via diffusion language models — a complementary approach that also seeks to unify the understanding/generation dichotomy.
- **Image Generators as Generalist Vision Learners** (April 2026, already in this repo): Investigates whether generative models can serve as general-purpose visual feature extractors — conceptually related to Tuna-2's claim that generation and understanding can be unified.

### Where This Research Leads

- **Scaling laws for pixel-based models**: Establishing compute-optimal training strategies for encoder-free multimodal models.
- **Video understanding**: Extending pixel embedding approaches to temporal sequences.
- **3D multimodal models**: Processing raw 3D point clouds or voxels without specialized 3D encoders.
- **Efficient pixel tokenization**: Developing better methods for compressing pixel information before feeding it to the LLM.
