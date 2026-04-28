# Counting Circuits: Mechanistic Interpretability of Visual Reasoning in Large Vision-Language Models

**ArXiv ID:** [2603.18523](https://arxiv.org/abs/2603.18523)  
**Authors:** (See paper for full author list)  
**Submission Date:** March 19, 2026  
**Subfield:** Mechanistic Interpretability — Vision-Language Models, Circuit Analysis

---

## Executive Summary

This paper applies mechanistic interpretability to **Large Vision-Language Models (LVLMs)** by studying the internal circuits responsible for **visual counting** — the ability to determine how many objects appear in an image. Introducing two novel techniques, **Visual Activation Patching** and **HeadLens**, the authors uncover a structured "counting circuit" with four distinct functional categories of attention heads, largely shared across diverse visual reasoning tasks. The discovery enables a lightweight fine-tuning intervention that improves out-of-distribution counting robustness and generalizes to complex visual reasoning benchmarks.

---

## Problem Statement

### Why Counting?

Visual counting is a deceptively simple task that requires a model to:
1. **Localize** individual objects (visual grounding)
2. **Abstract** those localizations into numerical concepts (cross-modal routing)
3. **Aggregate** counts across the image (counting aggregation)
4. **Reason** about difficulty and object existence (awareness)

This multi-step process makes counting an ideal **probe for mechanistic interpretability**: it is simple enough to analyze fully, yet rich enough to reveal modular processing within multimodal transformers.

### The Problem with VLMs

Large Vision-Language Models (e.g., LLaVA, InstructBLIP, Idefics) achieve impressive performance on visual question answering benchmarks, but they exhibit systematic failures on counting tasks, especially for:
- Larger numerosities (>6 objects) — noisy estimation analogous to human subitizing limits
- Out-of-distribution object arrangements
- Complex scenes with occlusions and overlapping objects

These failures are not explainable by benchmark artifacts alone: they reflect genuine computational limitations in *how* VLMs implement counting. Without understanding the underlying mechanism, targeted improvements are impossible.

### Gap in Existing Interpretability Work

Prior interpretability work on VLMs focused on:
- **Attention visualization** — which image regions the model "attends to" (correlational, not causal)
- **Probing classifiers** — testing whether representations encode specific features (doesn't explain routing)
- **Behavioral benchmarks** — measuring *what* models can do, not *how* they do it

No prior work had applied **causal circuit analysis** to the internal mechanisms of multimodal transformers.

---

## Core Concepts & Theory

### The Multi-Head Self-Attention Decomposition

In a transformer with H attention heads, the multi-head self-attention (MHSA) output can be written as a **linear sum** of individual head contributions:

```
MHSA(x) = Σ_{h=1}^{H} Head_h(x) · W_O^h
```

This **linear additivity** property is the foundation for HeadLens: it means each head's contribution to the residual stream can be isolated and decoded independently.

### Visual Activation Patching

**Visual Activation Patching (VAP)** is an adaptation of activation patching for multimodal settings:

**Standard activation patching** (from LLM mechanistic interpretability):
```
effect(component_i) = f(patch_{i}(clean_run, corrupt_run)) - f(corrupt_run)
```

**VAP for VLMs** distinguishes between text and image token streams:
- **Clean run:** LVLM processes an image with N objects + counting question
- **Corrupted run:** Same question, but image replaced with a version having N±k objects
- **Patching target:** Specific attention head activations, isolated to either image or text token positions

This allows attribution of counting behavior to specific heads that process *visual* information versus *textual* reasoning.

### HeadLens: Token-Level Semantic Decoding

**HeadLens** is a novel technique that decodes the semantic content being processed by individual attention heads:

**Key insight:** The output of each head is projected into the vocabulary space through the model's output embedding matrix:
```
decoded_tokens(h, pos) = top-k( W_U · W_O^h · head_h(x)[pos] )
```

Where:
- `W_U` is the unembedding matrix (vocabulary projection)
- `W_O^h` is the output projection for head h
- `head_h(x)[pos]` is head h's output at position pos

By inspecting the top-k decoded tokens, we can semantically label what each head "is thinking about" at each position. A head whose top decoded tokens at the `[CLS]` position are `{three, 3, trio, triad}` is clearly performing counting aggregation.

### The Counting Circuit

The complete counting circuit spans the full depth of the LVLM and consists of four functional stages:

```
Input: [Image tokens] [Text tokens: "How many apples?"]
         ↓
[Early Layers: Visual Grounding Heads]
→ Extract color, shape, size features from image tokens
→ Create object-specific representations

[Middle Layers: Cross-Modal Routing Heads]
→ Bridge visual object representations to numerical vocabulary
→ Translate "round red patch × N" → "N"

[Late Layers: Counting Aggregation Heads]
→ Attend heavily to text prompt
→ Top HeadLens tokens: {"one", "two", "three", ...}
→ Converge on a single count prediction

[Late Layers: Awareness Heads]
→ Encode object existence (binary: "are there any?")
→ Encode task difficulty ("is this a hard counting scene?")
         ↓
Output: Count prediction
```

---

## Main Ideas & Key Contributions

### 1. First Mechanistic Analysis of Counting in VLMs

The paper provides the **first causal, mechanistic account** of how a major vision-language capability (counting) is implemented internally in large multimodal models. This opens a research program analogous to the circuit-finding work done for LLMs (indirect object identification, factual recall, etc.) but extended to multimodal reasoning.

### 2. Visual Activation Patching

VAP adapts the standard activation patching methodology to the multimodal setting, enabling **causal attribution** of counting behavior to specific model components. Key innovations:
- Separates attribution for image vs. text token positions
- Handles the visual encoder / language model interface
- Works with any LVLM that uses a transformer language backbone

### 3. HeadLens

HeadLens is a **lightweight, architecture-agnostic** interpretability technique that exploits MHSA's linear additivity to decode the semantic content of individual heads without modifying the model. Unlike probing classifiers (which require training), HeadLens is:
- **Training-free:** Direct projection through existing embedding matrices
- **Token-resolved:** Provides per-token semantic labels, not just head-level summaries
- **Compositional:** Can be applied to any subset of heads in combination

### 4. Human-Like Subitizing in VLMs

The paper demonstrates that LVLMs exhibit a **subitizing-like pattern** analogous to human perception:
- **Small numerosities (1-4):** High accuracy, precise counts
- **Large numerosities (5+):** Noisy estimation, systematic undercount

This behavioral finding motivates the mechanistic analysis: the counting circuit operates precisely for small counts (all four stages function well) but degrades for larger counts (aggregation heads lose precision).

### 5. Cross-Task Generalization of the Counting Circuit

The same counting circuit, identified through counting tasks, is **largely shared across visual reasoning tasks** including:
- Spatial relationship reasoning ("is the cat to the left of the dog?")
- Existence queries ("is there a bird in this image?")
- Comparison tasks ("which group has more objects?")

This suggests the circuit is not task-specific but represents a **core visual reasoning module** in LVLMs.

### 6. Lightweight Intervention for Improved Counting

Using the circuit analysis, the authors develop a fine-tuning intervention:
- **Target:** Fine-tune only the attention heads in the counting aggregation stage
- **Data:** Simple, synthetic counting images (abundant and cheap to generate)
- **Effect:** Significant improvement in out-of-distribution counting robustness AND general visual reasoning benchmarks

This demonstrates the practical utility of mechanistic interpretability: understanding *why* a model fails enables targeted, efficient fixes.

---

## Methodology & Implementation

### Models Analyzed

| Model | Architecture | Scale | Modality |
|-------|-------------|-------|----------|
| LLaVA-1.5 | LLaMA + CLIP | 7B / 13B | Image + Text |
| InstructBLIP | Vicuna + BLIP-2 | 7B | Image + Text |
| Idefics2 | Mistral + SigLIP | 8B | Image + Text |

### Datasets

**Controlled Benchmarks:**
- **SugarCrepe:** Compositional visual reasoning with controlled difficulty
- **CLEVR-Count:** Synthetic counting with exact ground truth, variable numerosity 1-10
- **Visual Counting Benchmark (VCB):** Real-world images, labeled by human annotators

**Out-of-Distribution Evaluation:**
- **CountBench:** Holds out specific object categories during fine-tuning
- **GQA (counting split):** General visual question answering, counting questions

### Evaluation Metrics

| Metric | Description |
|--------|-------------|
| Counting Accuracy | Exact match between predicted and true count |
| Mean Absolute Error (MAE) | Average deviation from true count |
| HeadLens Correlation | Pearson correlation between decoded token scores and final prediction |
| Circuit Faithfulness | % of model logit variance explained by circuit alone |
| Cross-Task Transfer | Accuracy improvement on non-counting tasks after counting-focused fine-tuning |

### Key Results

**Counting accuracy by numerosity (LLaVA-1.5):**

| Numerosity | Baseline | After Intervention |
|-----------|---------|-------------------|
| 1-4 | 87.3% | 91.2% |
| 5-8 | 61.4% | 78.9% |
| 9-12 | 38.7% | 61.3% |
| 13+ | 21.2% | 44.8% |

**Cross-task generalization:** Counting-focused fine-tuning improves GQA accuracy by +3.1% overall, demonstrating that the counting circuit overlaps with general visual reasoning.

**Circuit faithfulness:** The 4-category circuit explains >85% of logit variance for counting predictions with only ~8% of total model parameters.

### Limitations

1. **Architecture-specific circuits:** The counting circuit was studied in attention-based LVLMs; diffusion-based or CNN-based vision models may implement counting differently
2. **Synthetic training bias:** The intervention uses synthetic images that may differ from real-world distributions in ways that limit transfer
3. **Scale dependency:** Circuit structure may change significantly in larger models (70B+)
4. **Temporal counting:** The paper focuses on static image counting; video-based counting involves additional temporal reasoning circuits not analyzed here

---

## Practical Applications & Real-World Use Cases

### 1. Quality Control in Manufacturing

Industrial vision systems often need to count items on assembly lines. Understanding the counting circuit enables:
- **Failure mode diagnosis:** If the system miscounts, which circuit stage is failing?
- **Targeted fine-tuning:** Adapt only the aggregation heads to the specific factory setting
- **Confidence calibration:** Use Awareness Heads' "difficulty" signal as a confidence proxy

### 2. Medical Image Analysis

Counting cells, lesions, or anatomical structures in medical scans:
- Pathologists need to count cancer cells in histology slides
- Radiologists count nodules in CT scans
- HeadLens can validate that the model grounds counts in genuine anatomical features, not imaging artifacts

### 3. Retail and Inventory Management

Visual inventory systems (retail shelves, warehouse management) rely on counting. The intervention strategy enables rapid adaptation to new product categories with minimal labeled data.

### 4. Educational AI and Assessment

AI tutoring systems that need to reason about quantities (how many objects in a math problem image?). Understanding the counting circuit enables reliable quantitative reasoning in educational contexts.

### 5. Regulatory Compliance

For high-stakes VLM deployments (EU AI Act high-risk category), the counting circuit provides an auditable, mechanism-level explanation of quantitative reasoning, supporting transparency requirements.

---

## Insights & Implications

### VLMs Implement Modular Visual Reasoning

The discovery of a structured, 4-stage counting circuit suggests that **visual reasoning in LVLMs is more modular than previously assumed**. This has implications for:
- Model surgery (targeted component replacement)
- Continual learning (preserving specific circuits while learning new tasks)
- Interpretability-by-design (architectures that make circuits more explicit)

### Bridging Behavioral and Mechanistic Analysis

The paper demonstrates that **behavioral observations** (human-like subitizing) can be *explained mechanistically* (aggregation head degradation at high numerosities). This bridges the behavioral and mechanistic traditions in AI interpretability research.

### From Interpretability to Action

The paper exemplifies a complete interpretability pipeline:
```
Behavior → Mechanism → Intervention → Verification
```
This "close the loop" approach is a model for future xAI research: interpretability findings should directly inform model improvements.

### Open Questions

1. **Are counting circuits shared across modalities?** Do audio-language models have analogous circuits for rhythmic counting?
2. **Circuit dynamics during training:** How does the counting circuit emerge during LVLM pretraining?
3. **Superposition in counting heads:** Do counting aggregation heads multiplex multiple numerical concepts, and if so, how are they separated?
4. **Scaling laws for circuits:** Do larger LVLMs develop more refined counting circuits, or just larger versions of the same structure?

---

## Code & Resources

- **ArXiv Paper:** [arxiv.org/abs/2603.18523](https://arxiv.org/abs/2603.18523)
- **HeadLens Implementation:** See paper's official repository (check ArXiv for GitHub link)
- **Visual Activation Patching:** Built on top of [TransformerLens](https://github.com/TransformerLensOrg/TransformerLens) patching infrastructure

### Dependencies

```
transformers >= 4.40.0
torch >= 2.1.0
transformer_lens >= 1.14.0
datasets (HuggingFace)
numpy, scipy, matplotlib
```

### Quick Start (HeadLens)

```python
from head_lens import HeadLens
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("llava-hf/llava-1.5-7b-hf")
hl = HeadLens(model)

# Decode what head 12 at the CLS position is processing
decoded = hl.decode_head(
    layer=8,
    head=12,
    position="cls_token",
    top_k=10
)
print(decoded)  # e.g., ['three', '3', 'trio', 'thrice', ...]
```

---

## Related Work & Context

### Direct Predecessors

- **Automated Circuit Discovery (ACDC, Conmy et al., 2023):** The core algorithm Vi-CD adapts for vision; Counting Circuits extends to multimodal
- **Attention Head Analysis in LLMs (Wang et al., 2022):** Indirect object identification circuits — the LLM analog of this paper's vision work
- **Can VLMs Count? (2511.17722):** Behavioral analysis that motivates the mechanistic investigation here

### Concurrent Work

- **Seeing Through Circuits (2604.14477):** Develops Vi-CD for ViT circuit discovery; Counting Circuits focuses on multimodal models and introduces HeadLens
- **Circuit Tracing in VLMs (2602.20330):** Parallel work on multimodal mechanistic interpretability from a different angle

### Broader Context

This paper is part of an emerging wave of **multimodal mechanistic interpretability**, extending the circuit-finding tradition from pure LLMs to vision-language models. The field is rapidly maturing, with methods that can now handle the additional complexity of cross-modal information routing.

The connection to the **cognitive science of counting** (subitizing, numerosity estimation) is notable: mechanistic interpretability is not just engineering, it can illuminate connections between neural network implementations and human cognitive mechanisms.
