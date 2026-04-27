# Efficient Inference for Large Vision-Language Models: Bottlenecks, Techniques, and Prospects

**ArXiv ID:** [2604.05546](https://arxiv.org/abs/2604.05546)  
**Authors:** Researchers from Zhejiang University  
**Submitted:** April 7, 2026; revised April 14, 2026  
**Field:** Computer Vision / Multimodal AI / Systems  

---

## Executive Summary

Large Vision-Language Models (LVLMs) have achieved remarkable capabilities in image and video understanding, but their inference is crippled by **visual token dominance** — the massive overhead caused by encoding high-resolution images into hundreds or thousands of tokens that must pass through quadratic-complexity attention layers. This survey provides the first systematic end-to-end taxonomy of LVLM inference efficiency, revealing how upstream encoding decisions create cascading downstream bottlenecks, and charts the path forward for practical deployment.

---

## Problem Statement

When an LVLM processes an image alongside text, the visual encoder generates a large number of tokens (often 256–4096 per image at high resolution). These visual tokens dominate the context and create three compounding bottlenecks:

1. **Compute-bound visual encoding:** High-resolution feature extraction is computationally expensive in the vision encoder (ViT variants).
2. **Quadratic attention scaling during prefilling:** Attention complexity scales as O(n²) with sequence length; hundreds of visual tokens dramatically increase prefill cost.
3. **Memory bandwidth bottleneck ("visual memory wall") during decoding:** Each decoding step must load the full KV-cache (including all visual keys and values) from GPU memory, creating bandwidth-bound execution.

Prior work on LLM efficiency largely ignores the vision modality, making existing techniques insufficient for LVLMs.

---

## Core Concepts & Theory

### The Three-Phase Inference Lifecycle

```
Phase 1: Encoding
  Visual encoder (ViT) → patch tokens
  Text tokenizer → text tokens
  Multimodal projector (MLP/cross-attention) → unified embedding
        ↓
Phase 2: Prefilling
  Full-sequence attention over all visual + text tokens
  KV-cache construction
        ↓
Phase 3: Decoding
  Autoregressive token generation
  Per-step KV-cache lookup (memory bandwidth bottleneck)
```

### Visual Token Dominance

A 448×448 image with patch size 14 produces (448/14)² = 1,024 visual tokens. For video (e.g., 8 frames), this becomes 8,192 visual tokens — 8–16× the typical text prompt length. The attention complexity for prefilling is:

$$\text{Cost}_{\text{prefill}} \propto (N_{\text{visual}} + N_{\text{text}})^2$$

Even a 50% reduction in visual tokens yields a 4× speedup in prefill for vision-heavy inputs.

### Taxonomy of Efficiency Techniques

The paper organizes techniques into three axes corresponding to the lifecycle:

| Phase | Bottleneck | Technique Classes |
|-------|-----------|-------------------|
| Encoding | Compute cost | Lower-res encoding, encoder pruning, efficient ViT variants |
| Prefilling | Quadratic attention | Visual token pruning, merging (e.g., Medusa, FastV), sparse attention |
| Decoding | Memory bandwidth | KV-cache compression, early exit, speculative decoding |

---

## Main Ideas & Key Contributions

1. **End-to-End Bottleneck Analysis:** First work to show that the three phases are interdependent — reducing visual tokens in encoding creates downstream effects on prefill and decoding that must be co-optimized.

2. **Systematic Taxonomy:** Covers 50+ efficiency techniques across encoding, prefilling, and decoding, with analysis of their compatibility and trade-offs.

3. **"Visual Memory Wall" Concept:** Coins the term for the memory bandwidth bottleneck specific to LVLM decoding, distinguishing it from the compute bottleneck of encoding.

4. **Prospects and Open Problems:** Identifies the most promising near-term directions, including **dynamic resolution adaptation** and **visual KV-cache compression**.

---

## Methodology & Implementation

### Survey Scope

- Covers major LVLM families: LLaVA, InternVL, Qwen-VL, GPT-4V class models, video LLMs.
- Evaluates efficiency techniques on standard benchmarks: MMBench, MMMU, VideoMME.

### Key Findings from Comparative Analysis

**Token pruning in prefilling (e.g., FastV, LLaVA-PruMerge):**
- Reducing visual tokens by 50% typically recovers 85–92% of baseline accuracy.
- Aggressive pruning (75%+) causes significant degradation on spatial reasoning tasks.

**KV-cache compression (e.g., visual streaming decoding):**
- Evicting visual KV entries after prefill (with careful key preservation) reduces peak memory by 40–60% with <2% accuracy drop.

**Dynamic resolution:**
- Adapting input resolution to query complexity (simple queries use lower res) saves 30–50% compute with minimal quality loss.

---

## Practical Applications & Real-World Use Cases

1. **Mobile deployment:** Reducing LVLM memory footprint to run on smartphones (8–16 GB RAM) for local image captioning, accessibility tools, and AR overlays.
2. **Cloud cost reduction:** Lowering GPU hours for vision API services (image question-answering, medical image analysis).
3. **Video understanding at scale:** Efficient video LLMs for content moderation, surveillance, and automated video summarization.
4. **Edge AI:** Deploying LVLMs on autonomous vehicles, drones, and industrial robots with limited compute budgets.

**Implementation challenges:** Most efficiency techniques require model-level changes (fine-tuning or architectural modifications); they cannot be applied post-hoc to closed-source APIs.

---

## Insights & Implications

- **Key insight:** The field has over-indexed on encoder-side optimizations; the most impactful near-term gains lie in **prefill-phase visual token reduction** and **decoding-phase KV compression**.
- **Advancing SOTA:** Provides a reference framework that future work can benchmark against, accelerating systematic progress.
- **Limitations:** Survey reflects literature up to early 2026; rapidly evolving field may already have superseded some recommendations.
- **Open questions:**
  - Can visual tokens be learned to be inherently more efficient (e.g., via tokenizer training)?
  - How does dynamic resolution interact with spatial reasoning tasks that require fine-grained visual detail?

---

## Code & Resources

- **Paper PDF:** https://arxiv.org/pdf/2604.05546  
- **Related toolkits:** Hugging Face `transformers` (LLaVA, InternVL), vLLM (for LLM serving with KV-cache management), SGLang.
- **Key libraries for experimentation:** `accelerate`, `bitsandbytes` (quantization), `flash-attention-2` (efficient attention).

---

## Related Work & Context

- **FastV (Chen et al., 2024):** Pioneer work on visual token pruning during prefilling; this survey contextualizes FastV within the broader efficiency landscape.
- **LLaVA-PruMerge:** Combines token pruning and merging for LVLM efficiency.
- **Efficient Inference of Large Vision Language Models (arXiv:2603.27960):** A contemporaneous survey; this paper provides a more structured lifecycle-based taxonomy.
- **vLLM, TensorRT-LLM:** Production serving frameworks that this survey's recommendations can be implemented within.
- **Next directions:** Hardware-software co-design for vision-specific KV-cache management, and learned visual compressors that adapt to query semantics.
