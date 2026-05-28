# From Pixels to Words: Towards Native One-Vision Models at Scale

**ArXiv ID:** 2605.28820  
**Authors:** Haiwen Diao, Jinglong Du, Long Li, Ye Ma, Pan Zhang, Xujie Pan, Geyang Qi, Yuhang Zang, Xiaohuan Zhou, Anyi Jiang, Tong Wu, Yuzhen Wei, Xiaoyi Dong, Meina Song, Pan Pan  
**Submitted:** May 27, 2026  
**Field:** Computer Vision, Vision-Language Models

## Executive Summary

This paper challenges the dominant modular architecture paradigm in vision-language models by proposing NEO-ov, a native foundation model that learns pixel-word correspondence end-to-end without external encoders or adapters. By unifying the vision and language pathways within a single architecture, the model achieves competitive performance with modular systems while enabling fine-grained spatiotemporal understanding at scale. This represents a fundamental shift in how vision-language models should be designed.

## Problem Statement

### Current Limitations of Modular Vision-Language Models

Current vision-language models (VLMs) employ a modular architecture that stitches together:
- Separate, pre-trained image encoders (e.g., CLIP, DINOv2)
- Language decoders (e.g., LLaMA, GPT-style)
- Multi-stage alignment mechanisms (e.g., linear projections, adapters)

This modular approach introduces several fundamental problems:

1. **Pixel-Level Signal Fragmentation:** Image encoders process images independently, creating fixed representations before language interaction occurs, fragmenting early pixel-word interactions
2. **Loss of Spatiotemporal Information:** Multi-frame video inputs are encoded separately, scattering frame-level information across the architecture
3. **Inefficient Parameter Allocation:** Frozen or partially trainable encoders limit the model's ability to jointly optimize visual and linguistic understanding
4. **Architectural Constraints:** Module boundaries prevent the model from learning optimal pixel-level representations for language tasks

### Research Gap

Prior work assumed that modular vision-language architectures were necessary for scaling and performance. No prior work had successfully demonstrated that native, unified vision-language models could achieve comparable performance to modular approaches while offering architectural simplicity and end-to-end optimization.

## Core Concepts & Theory

### Unified Native Architecture

The key innovation is designing a single foundation model that:
- Processes pixels directly as input (no pre-trained vision encoder)
- Maintains unified token representations throughout (vision and language tokens in the same space)
- Enables cross-frame and cross-modal attention natively
- Learns optimal pixel-level representations end-to-end

### Architectural Components

**Input Representation:**
- Pixels are converted to initial embeddings using learned projections
- Unlike CLIP-based approaches, these embeddings are not pre-trained
- Cross-frame information is represented natively in the sequence

**Native Attention Mechanism:**
- Self-attention operates over both visual and language tokens uniformly
- Cross-frame attention emerges naturally as the model learns to relate information across frames
- Early layers develop pixel-level understanding while later layers develop semantic understanding

**Spatiotemporal Modeling:**
- Video is processed as a continuous sequence: [frame1_pixels, frame2_pixels, ..., frameN_pixels, text_tokens]
- The model learns implicit temporal relationships without explicit temporal encoding
- Fine-grained spatial relationships are preserved throughout the network

### Comparison with Modular Approaches

| Aspect | Modular (CLIP-based) | NEO-ov (Native) |
|--------|----------------------|-----------------|
| **Vision Processing** | Pre-trained encoder | Learned end-to-end |
| **Cross-Modal Interaction** | Post-encoding via adapters | Native from input |
| **Spatiotemporal Understanding** | Fixed encoder representations | Emergent through attention |
| **Parameter Efficiency** | Multiple component optimization | Single unified optimization |
| **Fine-Grained Perception** | Limited by encoder bottleneck | Direct pixel access |

## Main Ideas & Contributions

### Primary Innovation: End-to-End Pixel-to-Word Learning

NEO-ov eliminates module boundaries entirely, allowing the model to:
1. Learn pixel representations optimized for language understanding
2. Develop cross-frame relationships natively
3. Allocate parameters dynamically between vision and language tasks

### Technical Contributions

1. **Architecture Design:** First successful demonstration of a native vision-language foundation model at scale
2. **Training Methodology:** Effective pre-training strategy for unified vision-language models without pre-trained vision encoders
3. **Scalability:** Proof that native models can scale to billions of parameters while maintaining competitive performance

### Intuition Behind Design Choices

**Why eliminate encoders?**
- Pre-trained vision encoders optimize for generic vision tasks (classification, detection)
- Language-specific visual understanding requires different feature hierarchies
- End-to-end learning allows automatic discovery of optimal representations

**Why native attention?**
- Modular fusion via adapters acts as a bottleneck
- Native attention allows early layers to develop pixel-level understanding
- This mirrors how biological vision systems process information

## Methodology & Implementation

### Training Setup

**Model Architecture:**
- Transformer-based decoder with unified attention
- No separate vision encoder or language decoder
- Supports variable-length video inputs seamlessly

**Dataset:**
- Large-scale vision-language dataset with video and text pairs
- Multi-modal training corpus combining images and text

**Training Objectives:**
- Causal language modeling on text tokens
- Contrastive learning between visual and linguistic representations
- Multi-task training on vision-language tasks

### Experimental Evaluation

**Benchmarks Tested:**
- Image captioning (MSCOCO, Flickr30K, Conceptual Captions)
- Visual question answering (GQA, OK-VQA, TextVQA)
- Video understanding (VideoChatGPT, LVQA)
- Fine-grained visual reasoning (MMSTAR)
- Text-in-image understanding and OCR tasks

**Key Results:**
- Competitive or superior performance compared to modular counterparts on image understanding
- Significant improvements on fine-grained visual perception tasks
- Strong performance on video understanding without explicit temporal modeling
- Efficient inference compared to models with separate encoders

**Specific Metrics:**
- Image captioning: Competitive BLEU, METEOR scores
- VQA: Comparable accuracy to CLIP-based VLMs
- Video tasks: [Exact figures unavailable — see full paper]
- Fine-grained tasks: Notable improvements on MMSTAR and similar benchmarks

### Ablation Studies

[Details on architectural ablations and design choices — see full paper]

## Practical Applications & Use Cases

### Industry Applications

1. **Autonomous Vehicles:**
   - Real-time video understanding from multiple camera feeds
   - Native video processing enables efficient multi-frame reasoning

2. **Content Creation & Analysis:**
   - Video captioning and summarization
   - Automated content understanding and recommendation
   - Fine-grained visual search in video libraries

3. **Medical Imaging:**
   - Fine-grained spatial understanding crucial for diagnosis
   - Multi-frame analysis (CT scans, ultrasound sequences)
   - Direct pixel-level information preservation

4. **Robotics & Embodied AI:**
   - Real-time visual understanding for robotic control
   - Fine-grained object perception and manipulation
   - Efficient inference on edge devices

### Real-World Examples

- **Video Search:** Find specific events or objects in hours of video footage
- **Accessibility:** Describe images and videos with precise spatial and temporal details
- **Scientific Analysis:** Interpret microscopy, satellite imagery, and medical scans
- **Security & Surveillance:** Efficient real-time video understanding

### Implementation Considerations

**Advantages:**
- Simpler deployment (single model instead of encoder+decoder)
- More efficient inference (no encoder overhead)
- Better fine-grained understanding for specialized domains
- Easier end-to-end optimization for specific tasks

**Challenges:**
- Requires larger training datasets (no pre-trained vision encoder)
- Longer training times compared to adapter-based approaches
- Needs careful initialization strategies for effective training
- May require task-specific fine-tuning for specialized domains

## Insights & Implications

### Broader Field Impact

1. **Paradigm Shift:** Challenges the assumption that modular vision-language architecture is optimal
2. **Unification Movement:** Contributes to trend of unified foundation models across modalities
3. **Architectural Innovation:** Opens new research directions in multi-modal architecture design
4. **Scaling Laws:** Demonstrates that native models can scale without sacrificing performance

### Limitations & Open Questions

1. **Data Requirements:** Native models may require more diverse training data
2. **Compute Efficiency:** Training efficiency compared to modular approaches remains unclear
3. **Generalization:** How well do native models transfer to specialized visual domains?
4. **Temporal Understanding:** Whether implicit temporal modeling matches explicit temporal encodings
5. **Comparison Fairness:** How models compare when matched for total parameter count

### Future Research Directions

1. **Efficient Training:** Developing more efficient training strategies for native models
2. **Knowledge Distillation:** Transferring knowledge from large modular models to native models
3. **Specialized Variants:** Domain-specific native models (medical, robotics, etc.)
4. **Hybrid Approaches:** Combining benefits of modular and native architectures
5. **Multi-Modal Extension:** Extending native architecture to incorporate audio and other modalities

## State-of-the-Art Advancement

- **First successful native foundation model** at scale for vision-language understanding
- **Competitive performance** with established modular approaches (CLIP-based VLMs)
- **Superior fine-grained perception** on specialized visual reasoning tasks
- **Unified architecture** enabling simpler deployment and optimization

## Code & Resources

### Official Resources
- **Paper:** https://arxiv.org/abs/2605.28820
- **ArXiv ID:** 2605.28820

### Dependencies & Requirements
- PyTorch or similar deep learning framework
- CUDA-capable GPU (minimum 40GB VRAM for training)
- Large-scale vision-language dataset for pre-training

### Quick-Start Guide
[Code and implementation details expected to be released — check paper for repository links]

## Related Work & Context

### Related Papers
1. **CLIP (Contrastive Language-Image Pre-training):** Foundation for modular vision-language models
2. **GPT-4V and LLaVA:** Architectural variants using modular approaches
3. **Vision Transformers (ViT):** Foundation for modern vision encoders
4. **Unified Multi-Modal Models:** Related work in unified architecture design

### Prior Work Foundations
- Image-text contrastive learning (Radford et al., 2021)
- Vision Transformers (Dosovitskiy et al., 2021)
- Multi-modal fusion techniques
- Foundation model scaling principles

### Possible Future Research Directions
1. **Adaptive Compute:** Dynamic allocation of computation between vision and language
2. **Cross-Modal Retrieval:** Native models for efficient image-text retrieval
3. **Video Generation:** Leveraging native architecture for generative video tasks
4. **Few-Shot Learning:** How native models perform in low-data regimes
5. **Robustness & Adversarial:** Adversarial robustness of native vs. modular architectures
